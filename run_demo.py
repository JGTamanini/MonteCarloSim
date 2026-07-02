import sys
import os
import logging
import streamlit as st

# Garante que o diretório raiz está no PYTHONPATH
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from truco.src.core.constantes import AcoesJogador, RespostasTruco, get_valor_manilha
from truco.src.core.carta import Carta
from truco.src.core.ambiente import AmbienteJogo
from truco.src.events.event_bus import EventBus
from truco.src.events import events
from truco.src.agents.base_agent import AgenteBase
from truco.src.core.state_machine import (
    SetupState,
    DealState,
    RevealViraState,
    PlayerTurnState,
    TrucoDecisionState,
    MatchEndState,
)

# Configuração básica de log para a aplicação
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TrucoDemo")


# Exceções customizadas para pausar a máquina de estados e aguardar input humano
class AguardandoJogadaHumana(Exception):
    pass


class AguardandoRespostaHumana(Exception):
    pass


def obter_html_carta(carta, css_class=""):
    simbolos = {"copas": "♥️", "ouros": "♦️", "paus": "♣️", "espadas": "♠️"}
    cores = {
        "copas": "#ef4444",
        "ouros": "#ef4444",
        "paus": "#3b82f6",
        "espadas": "#3b82f6",
    }
    simbolo = simbolos.get(carta.naipe.lower(), "")
    cor = cores.get(carta.naipe.lower(), "#ffffff")

    return f"""
    <div class="truco-card {css_class}" style="border: 2px solid {cor};">
        <div class="card-corner-top">{carta.valor}</div>
        <div class="card-center-suit" style="color: {cor};">{simbolo}</div>
        <div class="card-corner-bottom">{carta.valor}</div>
    </div>
    """


# Agente que representa o Humano e lê inputs da interface Streamlit
class AgenteHumano(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, None)

    def decidir_acao(self, percepcao, pode_pedir_truco):
        # Verifica se o jogador selecionou uma jogada no Streamlit
        if (
            "jogada_humana" in st.session_state
            and st.session_state.jogada_humana is not None
        ):
            jogada = st.session_state.jogada_humana
            st.session_state.jogada_humana = None
            return jogada
        raise AguardandoJogadaHumana()

    def responder_truco_proposto(self, percepcao, valor_proposto):
        # Verifica se o jogador escolheu uma resposta para o truco
        if (
            "resposta_humana" in st.session_state
            and st.session_state.resposta_humana is not None
        ):
            resposta = st.session_state.resposta_humana
            st.session_state.resposta_humana = None
            return resposta
        raise AguardandoRespostaHumana()


# Inicialização do estado do Streamlit
if "partida_logs" not in st.session_state:
    st.session_state.partida_logs = []
if "quedas_historico_mao" not in st.session_state:
    st.session_state.quedas_historico_mao = []
if "maos_finalizadas_historico" not in st.session_state:
    st.session_state.maos_finalizadas_historico = []
if "logs_mao_atual" not in st.session_state:
    st.session_state.logs_mao_atual = []
if "ultima_explicacao_ia" not in st.session_state:
    st.session_state.ultima_explicacao_ia = None
if "placar_geral" not in st.session_state:
    st.session_state.placar_geral = {"Humano": 0, "IA": 0}
if "jogada_humana" not in st.session_state:
    st.session_state.jogada_humana = None
if "resposta_humana" not in st.session_state:
    st.session_state.resposta_humana = None
if "confirmou_proxima_queda" not in st.session_state:
    st.session_state.confirmou_proxima_queda = False
if "oponente_instancia" not in st.session_state:
    st.session_state.oponente_instancia = None
if "ambiente" not in st.session_state:
    st.session_state.ambiente = None
if "estrategia_anterior" not in st.session_state:
    st.session_state.estrategia_anterior = None

# Interface - Configuração da Página
st.set_page_config(
    page_title="MAS Truco Paulista — Demonstração",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilização CSS personalizada para um design dark e premium
st.markdown(
    """
<style>
    .main {
        background-color: #0f1116;
        color: #e2e8f0;
    }
    .truco-board {
        background-color: #16171b;
        border: 1px solid #2e2f37;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
    }
    .card-back {
        border: 1px solid #3f3f46;
        background-color: #212228;
        border-radius: 8px;
        height: 85px;
        width: 60px;
        display: inline-block;
        position: relative;
    }
    .card-back::after {
        content: "";
        width: 14px;
        height: 14px;
        border: 2px solid #52525b;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .truco-card {
        border: 2px solid #3f3f46;
        background-color: #212228;
        border-radius: 8px;
        height: 105px;
        width: 75px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
        position: relative;
        user-select: none;
        margin: 0 auto;
        transition: all 0.2s ease-in-out;
    }
    .truco-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .card-corner-top {
        font-size: 0.95rem;
        font-weight: bold;
        text-align: left;
        color: white;
        line-height: 1;
    }
    .card-center-suit {
        font-size: 2.2rem;
        line-height: 1;
        text-align: center;
        align-self: center;
    }
    .card-corner-bottom {
        font-size: 0.95rem;
        font-weight: bold;
        text-align: right;
        color: white;
        line-height: 1;
        transform: rotate(180deg);
    }
    .mesa-card {
        margin: 0 auto;
    }
    .mesa-card-cpu {
        animation: throw-cpu-kf 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
    }
    .mesa-card-hum {
        animation: throw-hum-kf 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
    }
    @keyframes throw-cpu-kf {
        from {
            transform: translateY(-80px) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        to {
            transform: translateY(0) rotate(-6deg) scale(1.0);
            opacity: 1;
        }
    }
    @keyframes throw-hum-kf {
        from {
            transform: translateY(80px) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        to {
            transform: translateY(0) rotate(6deg) scale(1.0);
            opacity: 1;
        }
    }
    .mesa-card-empty {
        border: 2px dashed #27272a;
        border-radius: 8px;
        height: 105px;
        width: 75px;
        margin: 0 auto;
        background-color: transparent;
    }
    .minha-mao-container div[data-testid="column"] button {
        background-color: #17181c !important;
        border: 1px solid #3f3f46 !important;
        border-radius: 6px !important;
        height: 36px !important;
        color: #d1d5db !important;
        font-weight: bold !important;
        transition: all 0.2s ease-in-out !important;
        display: block !important;
        margin-top: 8px !important;
    }
    .minha-mao-container div[data-testid="column"] button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
        border-color: #3b82f6 !important;
        transform: translateY(-2px) !important;
    }
    .score-card {
        background-color: #16171b;
        border: 1px solid #2e2f37;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .score-card-title {
        font-size: 0.9rem;
        color: #71717a;
        font-weight: bold;
    }
    .score-card-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
        margin-top: 5px;
    }
    .botoes-acao button {
        height: 48px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    /* Estilo do botão primário (Pedir Truco / Aceitar) */
    .botoes-acao div[data-testid="column"]:nth-of-type(1) button {
        background-color: #450a0a !important; /* vermelho escuro */
        border: 1px solid #b91c1c !important;
        color: #ef4444 !important;
    }
    .botoes-acao div[data-testid="column"]:nth-of-type(1) button:hover {
        background-color: #b91c1c !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    /* Estilo do botão de Correr / Desistir */
    .botoes-acao div[data-testid="column"]:nth-of-type(2) button {
        background-color: #16171b !important;
        border: 1px solid #3f3f46 !important;
        color: #d1d5db !important;
    }
    .botoes-acao div[data-testid="column"]:nth-of-type(2) button:hover {
        background-color: #3f3f46 !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    /* Estilo do botão de Log / Aumentar */
    .botoes-acao div[data-testid="column"]:nth-of-type(3) button {
        background-color: #16171b !important;
        border: 1px solid #3f3f46 !important;
        color: #d1d5db !important;
    }
    .botoes-acao div[data-testid="column"]:nth-of-type(3) button:hover {
        background-color: #3f3f46 !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    .log-container {
        max-height: 250px;
        overflow-y: auto;
        background-color: #090d16;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px;
        font-family: monospace;
        font-size: 0.85rem;
        line-height: 1.4;
</style>
""",
    unsafe_allow_html=True,
)

# Barra Lateral - Configuração do Agente Oponente
st.sidebar.title("🤖 Configuração do Oponente")

estrategia_selecionada = st.sidebar.selectbox(
    "Estratégia da IA:",
    [
        "Híbrido",
        "Adaptativo",
        "Bayesiano",
        "Probabilístico",
        "Conservador",
        "Agressivo",
        "Blefador",
        "RiscoEvitador",
        "RiscoBuscador",
        "Aleatório",
    ],
)

# Verifica se o oponente mudou para resetar a instância e reter a memória a longo prazo
if (
    st.session_state.estrategia_anterior != estrategia_selecionada
    or st.session_state.oponente_instancia is None
):
    st.session_state.estrategia_anterior = estrategia_selecionada
    from truco.src.agents.concrete_agents import (
        AgenteAleatorio,
        AgenteConservador,
        AgenteAgressivo,
        AgenteProbabilistico,
        AgenteAdaptativo,
        AgenteBlefador,
        AgenteBayesiano,
        AgenteRiscoEvitador,
        AgenteRiscoBuscador,
        AgenteHibrido,
    )

    mapeamento = {
        "Aleatório": AgenteAleatorio,
        "Conservador": AgenteConservador,
        "Agressivo": AgenteAgressivo,
        "Probabilístico": AgenteProbabilistico,
        "Adaptativo": AgenteAdaptativo,
        "Blefador": AgenteBlefador,
        "Bayesiano": AgenteBayesiano,
        "RiscoEvitador": AgenteRiscoEvitador,
        "RiscoBuscador": AgenteRiscoBuscador,
        "Híbrido": AgenteHibrido,
    }
    classe_agente = mapeamento.get(estrategia_selecionada, AgenteAleatorio)
    st.session_state.oponente_instancia = classe_agente("IA_Oponente")
    st.session_state.ambiente = None  # Força recriação do ambiente
    st.session_state.partida_logs = ["Agente oponente configurado com sucesso!"]

# Placar Global
st.sidebar.write("---")
st.sidebar.subheader("🏆 Placar Geral de Partidas")
col_p1, col_p2 = st.sidebar.columns(2)
col_p1.metric("Humano", st.session_state.placar_geral["Humano"])
col_p2.metric(f"IA ({estrategia_selecionada})", st.session_state.placar_geral["IA"])

if st.sidebar.button("Zerar Placar Global"):
    st.session_state.placar_geral = {"Humano": 0, "IA": 0}
    st.rerun()

# Botão de reinicialização da partida atual
if st.sidebar.button("Iniciar Nova Partida / Reiniciar", type="primary"):
    st.session_state.ambiente = None
    st.session_state.partida_logs = ["Partida reiniciada pelo usuário."]
    st.session_state.quedas_historico_mao = []
    st.session_state.maos_finalizadas_historico = []
    st.session_state.logs_mao_atual = []
    st.session_state.confirmou_proxima_queda = False
    st.session_state.ultima_explicacao_ia = None
    st.rerun()


# Definições de callbacks globais executadas a cada rodada (para manter contexto do Streamlit atualizado)
def registrar_log(event):
    msg = ""
    if isinstance(event, events.MatchStartedEvent):
        msg = "🎮 A PARTIDA COMEÇOU!"
        st.session_state.partida_logs.append(msg)
        st.session_state.maos_finalizadas_historico = []

    elif isinstance(event, events.RoundStartedEvent):
        manilha_val = get_valor_manilha(event.vira.valor)
        msg = f"🆕 **Mão {event.numero_mao} Iniciada!** Vira: **{event.vira}** | Manilha: **{manilha_val}**"
        st.session_state.partida_logs.append(msg)
        st.session_state.quedas_historico_mao = []
        st.session_state.logs_mao_atual = [msg]

    elif isinstance(event, events.CardPlayedEvent):
        msg = f"🃏 **{event.jogador}** jogou a carta **{event.carta}**"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

    elif isinstance(event, events.TrucoRequestedEvent):
        msg = f"⚡ **{event.jogador}** pediu **TRUCO** (Aposta vale {event.valor_proposto} pontos!)"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

    elif isinstance(event, events.TrucoAcceptedEvent):
        msg = (
            f"✅ **{event.jogador}** ACEITOU o Truco! Partida vale {event.novo_valor}."
        )
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

    elif isinstance(event, events.TrucoRejectedEvent):
        msg = f"🏃 **{event.jogador}** CORREU do Truco!"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

    elif isinstance(event, events.TrucoRaisedEvent):
        msg = f"🔥 **{event.jogador}** AUMENTOU o Truco de {event.valor_atual} para {event.valor_proposto}!"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

    elif isinstance(event, events.QuedaFinishedEvent):
        vencedor_traduzido = (
            "Empate" if event.vencedor_queda == "Empate" else event.vencedor_queda
        )
        msg = (
            f"🏁 **{event.numero_queda}ª Queda** vencida por: **{vencedor_traduzido}**"
        )
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)
        st.session_state.quedas_historico_mao.append(event)

    elif isinstance(event, events.RoundFinishedEvent):
        msg = f"🏁 **Fim da Mão {event.numero_mao}.** Vencedor da Mão: **{event.vencedor}** (+{event.pontos_ganhos} pts)"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)

        # Adiciona ao histórico de mãos finalizadas
        summary = f"Mão {event.numero_mao} -> Vencedora: {event.vencedor} (+{event.pontos_ganhos} pts). Placar: Humano {event.placar.get('Humano', 0)} x IA {event.placar.get('IA_Oponente', 0)}"
        st.session_state.maos_finalizadas_historico.append(summary)

    elif isinstance(event, events.MatchFinishedEvent):
        msg = f"🏆 **FIM DA PARTIDA!** Vencedor da partida: **{event.vencedor}**"
        st.session_state.partida_logs.append(msg)
        st.session_state.logs_mao_atual.append(msg)
        # Atualiza o placar global
        if event.vencedor == "Humano":
            st.session_state.placar_geral["Humano"] += 1
        else:
            st.session_state.placar_geral["IA"] += 1


def capturar_xai(event: events.DecisionMadeEvent):
    if event.jogador == "IA_Oponente":
        st.session_state.ultima_explicacao_ia = {
            "decisao": event.decisao,
            "forca_mao": event.forca_mao,
            "tempo_ms": event.tempo_ms,
            "motivo": event.motivo,
            "estrategia": event.estrategia,
        }


# Instanciação do Ambiente
if st.session_state.ambiente is None:
    humano = AgenteHumano("Humano")
    ia = st.session_state.oponente_instancia
    bus = EventBus()
    st.session_state.ambiente = AmbienteJogo([humano, ia], bus)

# Re-inscreve os callbacks de UI a cada rerun.
# Usa unsubscribe para evitar duplicação sem apagar handlers dos agentes.
_bus = st.session_state.ambiente.event_bus
_tipos_log = [
    events.MatchStartedEvent,
    events.RoundStartedEvent,
    events.CardPlayedEvent,
    events.TrucoRequestedEvent,
    events.TrucoAcceptedEvent,
    events.TrucoRejectedEvent,
    events.TrucoRaisedEvent,
    events.QuedaFinishedEvent,
    events.RoundFinishedEvent,
    events.MatchFinishedEvent,
]
for _t in _tipos_log:
    _bus.unsubscribe(_t, registrar_log)
    _bus.subscribe(_t, registrar_log)
_bus.unsubscribe(events.DecisionMadeEvent, capturar_xai)
_bus.subscribe(events.DecisionMadeEvent, capturar_xai)

# Título Principal do App
st.title("🃏 Truco Paulista Multiagentes — Humano vs IA")
st.write(
    "Jogue contra diferentes estratégias de agentes cognitivos providos de BeliefState, Inferência Bayesiana e XAI."
)


# Função para executar a Máquina de Estados passo a passo
def processar_passo_jogo():
    amb = st.session_state.ambiente
    if amb._estado_atual is None:
        amb.definir_estado(SetupState())

    try:
        while not isinstance(amb._estado_atual, MatchEndState):
            # Intercepta ANTES de avaliar o fim da queda para permitir que o usuário veja as duas cartas na mesa
            if len(amb.cartas_jogadas_queda) == 2 and not st.session_state.get(
                "confirmou_proxima_queda", False
            ):
                return "proxima_queda"

            # Se confirmou, reinicia a flag
            if st.session_state.get("confirmou_proxima_queda", False):
                st.session_state.confirmou_proxima_queda = False

            amb._estado_atual.processar(amb)
        # Executa o estado final se necessário
        amb._estado_atual.processar(amb)
    except Exception as e:
        class_name = type(e).__name__
        if class_name == "AguardandoJogadaHumana":
            # Pausa a execução para aguardar input do usuário
            return "jogar"
        elif class_name == "AguardandoRespostaHumana":
            # Pausa a execução para aguardar resposta do usuário sobre truco
            return "responder"
        else:
            raise e

    return "fim"


# Executa o jogo até travar em um input do Humano ou terminar
estado_interacao = processar_passo_jogo()

# ----------------- TELA DO JOGO -----------------
col_esq, col_dir = st.columns([1.9, 1.1])

with col_esq:
    amb = st.session_state.ambiente
    p_humano = amb.placar_partida.get("Humano", 0)
    p_ia = amb.placar_partida.get("IA_Oponente", 0)
    # Cabeçalho da Simulação com título e Badges de Mão e Manilha
    col_hdr1, col_hdr2 = st.columns([2.0, 1.5])
    with col_hdr1:
        st.markdown("### 🎴 Truco Paulista — simulação")
    with col_hdr2:
        if amb.vira:
            manilha_val = get_valor_manilha(amb.vira.valor)
            st.markdown(
                f"<div style='text-align: right; display: flex; gap: 8px; justify-content: flex-end; line-height: 40px;'>"
                f"<span style='background-color:#065f46; color:#34d399; padding: 4px 10px; border-radius: 6px; font-weight:bold; font-size:0.9rem;'>Mão {amb.numero_mao}</span>"
                f"<span style='background-color:#1e3a8a; color:#60a5fa; padding: 4px 10px; border-radius: 6px; font-weight:bold; font-size:0.9rem;'>Manilha: {manilha_val}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # TABULEIRO PRINCIPAL (truco-board)
    st.markdown('<div class="truco-board">', unsafe_allow_html=True)

    # 1. Linha do Oponente (CPU)
    col_cpu_lbl, col_cpu_cards = st.columns([1.5, 2.0])
    with col_cpu_lbl:
        if estado_interacao == "proxima_queda":
            status_cpu = "queda concluída"
        else:
            status_cpu = (
                "pensando..."
                if amb.obter_jogador_ativo().nome == "IA_Oponente"
                and estado_interacao != "fim"
                else "aguardando..."
            )
        st.markdown(
            f"<div style='display: flex; align-items: center; gap: 10px;'>"
            f"<span style='background-color:#450a0a; color:#ef4444; width:36px; height:36px; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:1.2rem;'>🤖</span>"
            f"<div>"
            f"<div style='font-weight:bold; color:white; font-size:0.95rem;'>Máquina (CPU)</div>"
            f"<div style='font-size:0.8rem; color:#71717a;'>{status_cpu}</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_cpu_cards:
        n_cards_cpu = len(amb.maos_jogadores.get("IA_Oponente", []))
        cards_html = "".join(
            '<div class="card-back" style="margin-left: 5px;"></div>'
            for _ in range(n_cards_cpu)
        )
        st.markdown(
            f"<div style='display:flex; justify-content:flex-end;'>{cards_html}</div>",
            unsafe_allow_html=True,
        )

    # Espaçamento
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # 2. Mesa Central (Cartas Jogadas na Queda)
    col_mesa_cards, col_mesa_lbl = st.columns([2.0, 1.5])
    with col_mesa_cards:
        col_m_ia, col_m_hum = st.columns(2)
        with col_m_ia:
            if "IA_Oponente" in amb.cartas_jogadas_queda:
                c = amb.cartas_jogadas_queda["IA_Oponente"]
                st.markdown(
                    obter_html_carta(c, css_class="mesa-card mesa-card-cpu"),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='mesa-card-empty'></div>", unsafe_allow_html=True
                )
        with col_m_hum:
            if "Humano" in amb.cartas_jogadas_queda:
                c = amb.cartas_jogadas_queda["Humano"]
                st.markdown(
                    obter_html_carta(c, css_class="mesa-card mesa-card-hum"),
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<div class='mesa-card-empty'></div>", unsafe_allow_html=True
                )
    with col_mesa_lbl:
        col_vr, col_lbl_txt = st.columns([1.1, 1.0])
        with col_vr:
            if amb.vira:
                st.markdown(
                    "<div style='font-size:0.75rem; font-weight:bold; color:#71717a; text-align:center; margin-bottom:2px;'>VIRA</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(obter_html_carta(amb.vira), unsafe_allow_html=True)
        with col_lbl_txt:
            st.markdown(
                "<div style='line-height:105px; color:#52525b; font-weight:bold; font-size:1.1rem; padding-left:10px;'>mesa</div>",
                unsafe_allow_html=True,
            )

    # Espaçamento
    st.markdown("<div style='margin: 25px 0;'></div>", unsafe_allow_html=True)

    # 3. Linha do Jogador (Você)
    col_hum_cards, col_hum_lbl = st.columns([2.0, 1.5])
    with col_hum_cards:
        st.markdown('<div class="minha-mao-container">', unsafe_allow_html=True)
        mao_humano = amb.maos_jogadores.get("Humano", [])
        cols_cartas = st.columns(max(len(mao_humano), 1))

        for idx, carta in enumerate(mao_humano):
            with cols_cartas[idx]:
                st.markdown(obter_html_carta(carta), unsafe_allow_html=True)
                btn_desabilitado = estado_interacao != "jogar"
                if st.button(
                    "Jogar",
                    key=f"c_{idx}",
                    disabled=btn_desabilitado,
                    use_container_width=True,
                ):
                    st.session_state.jogada_humana = (AcoesJogador.JOGAR_CARTA, carta)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_hum_lbl:
        if estado_interacao == "proxima_queda":
            status_hum = "queda concluída"
        else:
            status_hum = (
                "sua vez"
                if amb.obter_jogador_ativo().nome == "Humano"
                and estado_interacao == "jogar"
                else (
                    "respondendo truco..."
                    if estado_interacao == "responder"
                    else "aguardando..."
                )
            )
        st.markdown(
            f"<div style='display: flex; align-items: center; gap: 10px; justify-content: flex-end; text-align: right; height: 105px;'>"
            f"<div>"
            f"<div style='font-weight:bold; color:white; font-size:0.95rem;'>Você</div>"
            f"<div style='font-size:0.8rem; color:#71717a;'>{status_hum}</div>"
            f"</div>"
            f"<span style='background-color:#1e3a8a; color:#3b82f6; width:36px; height:36px; border-radius:50%; display:flex; justify-content:center; align-items:center; font-size:1.2rem;'>👤</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # Fim do truco-board

    # 4. Placar dos dois lados
    col_pl_hum, col_pl_ia = st.columns(2)
    with col_pl_hum:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-card-title'>Você</div>"
            f"<div class='score-card-value'>{p_humano}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_pl_ia:
        st.markdown(
            f"<div class='score-card'>"
            f"<div class='score-card-title'>Máquina</div>"
            f"<div class='score-card-value'>{p_ia}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # 5. Botões de Ação no Rodapé (Pedir Truco, Correr, Log/Aumentar)
    st.markdown('<div class="botoes-acao">', unsafe_allow_html=True)
    col_act1, col_act2, col_act3 = st.columns(3)

    with col_act1:
        if estado_interacao == "jogar":
            pode_pedir_truco = (
                not amb.truco_pedido_nesta_mao or amb.proponente_truco != "Humano"
            ) and amb.valor_truco_atual < 12
            if st.button(
                "🔥 Pedir truco",
                key="btn_truco_bottom",
                disabled=not pode_pedir_truco,
                use_container_width=True,
            ):
                st.session_state.jogada_humana = (AcoesJogador.PEDIR_TRUCO, None)
                st.rerun()
        elif estado_interacao == "responder":
            if st.button(
                "✅ Aceitar Truco", key="btn_aceitar_bottom", use_container_width=True
            ):
                st.session_state.resposta_humana = RespostasTruco.ACEITAR
                st.rerun()
        elif estado_interacao == "proxima_queda":
            if st.button(
                "▶️ Continuar",
                key="btn_continuar_bottom",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.confirmou_proxima_queda = True
                st.rerun()
        else:
            st.button(
                "🔥 Pedir truco",
                key="btn_truco_disabled",
                disabled=True,
                use_container_width=True,
            )

    with col_act2:
        if estado_interacao == "responder":
            if st.button("🏳️ Correr", key="btn_correr_bottom", use_container_width=True):
                st.session_state.resposta_humana = RespostasTruco.CORRER
                st.rerun()
        else:
            st.button(
                "🏳️ Correr",
                key="btn_correr_disabled",
                disabled=True,
                use_container_width=True,
            )

    with col_act3:
        if estado_interacao == "responder":
            pode_aumentar = amb.valor_truco_proposto < 12
            if st.button(
                "🔥 Aumentar",
                key="btn_aumentar_bottom",
                disabled=not pode_aumentar,
                use_container_width=True,
            ):
                st.session_state.resposta_humana = RespostasTruco.AUMENTAR
                st.rerun()
        else:
            # Botão decorativo "Log da rodada"
            st.button(
                "📋 Log da rodada", key="btn_log_decorativo", use_container_width=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

with col_dir:
    # Painel XAI da Inteligência Artificial
    st.markdown("### 🧠 Pensamento da IA")
    if st.session_state.ultima_explicacao_ia:
        xai = st.session_state.ultima_explicacao_ia
        st.markdown(f"**Estratégia Oponente:** `{xai['estrategia']}`")
        st.markdown(f"**Ação IA:** `{xai['decisao']}`")

        # Métrica Visual da Força da Mão da IA
        forca = xai["forca_mao"]
        st.markdown(f"**Força da Mão da IA (0-10):** {forca:.2f}")
        st.progress(min(forca / 10.0, 1.0))

        ia_agent = st.session_state.oponente_instancia
        if ia_agent and hasattr(ia_agent, "beliefs") and ia_agent.beliefs:
            b = ia_agent.beliefs
            p_manilha = b.probabilidade_manilha_oponente * 100
            perfil = b.perfil_oponente
            p_blefe = b.chance_blefe_oponente * 100

            st.markdown(f"- P(Humano ter Manilha): **{p_manilha:.1f}%**")
            st.markdown(f"- Perfil Mapeado do Humano: **{perfil}**")
            st.markdown(f"- P(Humano Blefando | Truco): **{p_blefe:.1f}%**")

        st.markdown("**Raciocínio Interno (Rationale):**")
        st.info(xai["motivo"])
        st.caption(f"Tempo de Decisão: {xai['tempo_ms']:.4f} ms")
    else:
        st.info("Aguardando ação da IA para exibir raciocínio.")

    st.markdown("---")

    # Histórico detalhado da Mão Corrente (Logs organizados)
    st.markdown("### 📜 Linha do Tempo da Mão")
    logs_mao_html = "<br>".join(st.session_state.logs_mao_atual[::-1])
    st.markdown(
        f'<div class="log-container" style="max-height: 200px;">{logs_mao_html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Histórico de Mãos Anteriores
    with st.expander("📝 Histórico das Mãos Anteriores"):
        if st.session_state.maos_finalizadas_historico:
            for resumo_m in st.session_state.maos_finalizadas_historico[::-1]:
                st.write(resumo_m)
        else:
            st.write("*Nenhuma mão finalizada ainda nesta partida.*")
