import random
from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class AdaptiveStrategy:
    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria
        perfil = beliefs.perfil_oponente

        # Ajusta parâmetros dinamicamente baseado no perfil do oponente
        if perfil == "Conservador":
            chance_blefe = 0.45
            limiar_truco = 5.5
            motivo_perfil = "Oponente Conservador detectado: aumentando blefe para 45% e baixando limiar para 5.5."
        elif perfil == "Agressivo":
            chance_blefe = 0.08
            limiar_truco = 7.5
            motivo_perfil = "Oponente Agressivo detectado: reduzindo blefe para 8% e subindo limiar para 7.5 para evitar retruco."
        else:  # Probabilístico ou Desconhecido
            chance_blefe = 0.20
            limiar_truco = 6.5
            motivo_perfil = "Perfil oponente moderado: blefe em 20%, limiar de truco em 6.5."

        # Decisão de Truco
        if pode_pedir_truco:
            if forca >= limiar_truco:
                return AcoesJogador.PEDIR_TRUCO, None, f"Mão forte adaptada. {motivo_perfil}"
            elif random.random() < chance_blefe:
                return AcoesJogador.PEDIR_TRUCO, None, f"Blefe adaptado contra perfil '{perfil}'. {motivo_perfil}"

        # Joga a carta baseando-se nas rodadas ganhas
        minhas_quedas = percepcao.quedas_vencidas.get(agente.nome, 0)
        adversario_nome = [n for n in percepcao.placar_partida.keys() if n != agente.nome][0]
        quedas_adv = percepcao.quedas_vencidas.get(adversario_nome, 0)

        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira))

        if minhas_quedas > quedas_adv:
            # Estamos na frente, joga a carta mais fraca para forçar o adversário
            carta = cartas_ordenadas[0]
            motivo_carta = f"À frente nas quedas ({minhas_quedas} vs {quedas_adv}), jogando a mais fraca ({carta}) para poupar."
        else:
            # Atrás ou empatados, joga a mais forte
            carta = cartas_ordenadas[-1]
            motivo_carta = f"Atrás ou empatados nas quedas ({minhas_quedas} vs {quedas_adv}), jogando a mais forte ({carta}) para garantir."

        return AcoesJogador.JOGAR_CARTA, carta, motivo_carta

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria
        perfil = beliefs.perfil_oponente

        if perfil == "Conservador":
            # Trucos de conservadores são honestos
            limiar_aceitar = 7.5
            motivo = "Oponente Conservador pediu Truco: assumindo mão forte. Limiar de aceitação alto (7.5)."
        elif perfil == "Agressivo":
            # Trucos de agressivos costumam conter blefes
            limiar_aceitar = 4.8
            motivo = "Oponente Agressivo pediu Truco: suspeita de blefe elevada. Limiar de aceitação baixo (4.8)."
        else:
            limiar_aceitar = 6.2
            motivo = "Pedido de truco por perfil moderado/desconhecido. Limiar de aceitação padrão (6.2)."

        if forca >= limiar_aceitar:
            # Se for muito forte, podemos até aumentar
            if forca >= 9.0 and valor_proposto < 12:
                return RespostasTruco.AUMENTAR, f"Mão monstruosa ({forca:.2f} >= 9.0), aumentando o truco. {motivo}"
            return RespostasTruco.ACEITAR, f"Mão aceitável para o perfil ({forca:.2f} >= {limiar_aceitar}), aceitando. {motivo}"
        return RespostasTruco.CORRER, f"Mão fraca para o cenário ({forca:.2f} < {limiar_aceitar}), correndo. {motivo}"
