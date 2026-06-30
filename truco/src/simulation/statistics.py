import logging
from typing import Dict, List, Any
from truco.src.events import events
from truco.src.events.event_bus import EventBus
from truco.src.core.carta import Carta

logger = logging.getLogger("StatisticsTracker")


class StatisticsTracker:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

        # Métricas gerais
        self.partidas_total = 0
        self.vitorias: Dict[str, int] = {}
        self.historico_placar: List[Dict[str, int]] = []

        # Métricas de tomada de decisão (XAI)
        self.tempos_decisao: Dict[str, List[float]] = {}      # {nome_agente: [tempos_ms]}
        self.contagem_decisoes: Dict[str, Dict[str, int]] = {} # {nome_agente: {decisao_str: count}}
        self.forcas_maos: Dict[str, List[float]] = {}          # {nome_agente: [forcas]}

        # Comportamento de Truco
        self.trucos_pedidos: Dict[str, int] = {}
        self.trucos_aceitos: Dict[str, int] = {}
        self.trucos_corridos: Dict[str, int] = {}
        self.trucos_aumentados: Dict[str, int] = {}

        # Frequência de blefes
        # Consideramos blefe quando o jogador pede truco com força de mão < 5.5
        self.blefes_tentados: Dict[str, int] = {}
        self.blefes_sucedidos: Dict[str, int] = {}

        # Frequência de cartas mais jogadas
        self.cartas_jogadas: Dict[str, Dict[str, int]] = {} # {nome_agente: {carta_str: count}}

        # Inscreve-se nos eventos para coletar métricas de forma transparente
        self._inscrever_eventos()

    def _inscrever_eventos(self):
        self.event_bus.subscribe(events.MatchFinishedEvent, self._on_match_finished)
        self.event_bus.subscribe(events.CardPlayedEvent, self._on_card_played)
        self.event_bus.subscribe(events.TrucoRequestedEvent, self._on_truco_requested)
        self.event_bus.subscribe(events.TrucoAcceptedEvent, self._on_truco_accepted)
        self.event_bus.subscribe(events.TrucoRejectedEvent, self._on_truco_rejected)
        self.event_bus.subscribe(events.TrucoRaisedEvent, self._on_truco_raised)
        self.event_bus.subscribe(events.DecisionMadeEvent, self._on_decision_made)

    def _on_decision_made(self, event: events.DecisionMadeEvent):
        agente_nome = event.jogador
        if agente_nome not in self.tempos_decisao:
            self.tempos_decisao[agente_nome] = []
        if agente_nome not in self.forcas_maos:
            self.forcas_maos[agente_nome] = []
        if agente_nome not in self.contagem_decisoes:
            self.contagem_decisoes[agente_nome] = {}

        self.tempos_decisao[agente_nome].append(event.tempo_ms)
        self.forcas_maos[agente_nome].append(event.forca_mao)

        decisao = event.decisao
        self.contagem_decisoes[agente_nome][decisao] = self.contagem_decisoes[agente_nome].get(decisao, 0) + 1

        # Avalia se foi uma tentativa de blefe (Truco pedido/aumentado com força de mão < 5.5)
        if decisao in ["PEDIR_TRUCO", "AUMENTAR_TRUCO"]:
            if agente_nome not in self.blefes_tentados:
                self.blefes_tentados[agente_nome] = 0
            if event.forca_mao < 5.5:
                self.blefes_tentados[agente_nome] += 1
                # Armazena quem é o blefador ativo na rodada para verificar se terá sucesso
                self._ultimo_blefador = agente_nome

    def _on_truco_rejected(self, event: events.TrucoRejectedEvent):
        self.trucos_corridos[event.jogador] = self.trucos_corridos.get(event.jogador, 0) + 1
        # Se houve corrida, quem provocou a decisão (o último blefador) obteve sucesso no blefe
        if hasattr(self, "_ultimo_blefador") and self._ultimo_blefador:
            blefador = self._ultimo_blefador
            if blefador != event.jogador:
                if blefador not in self.blefes_sucedidos:
                    self.blefes_sucedidos[blefador] = 0
                self.blefes_sucedidos[blefador] += 1
            self._ultimo_blefador = None

    def _on_match_finished(self, event: events.MatchFinishedEvent):
        self.partidas_total += 1
        self.vitorias[event.vencedor] = self.vitorias.get(event.vencedor, 0) + 1
        self.historico_placar.append(event.placar)

    def _on_card_played(self, event: events.CardPlayedEvent):
        agente = event.jogador
        carta_str = str(event.carta)

        if agente not in self.cartas_jogadas:
            self.cartas_jogadas[agente] = {}
        self.cartas_jogadas[agente][carta_str] = self.cartas_jogadas[agente].get(carta_str, 0) + 1

    def _on_truco_requested(self, event: events.TrucoRequestedEvent):
        self.trucos_pedidos[event.jogador] = self.trucos_pedidos.get(event.jogador, 0) + 1

    def _on_truco_accepted(self, event: events.TrucoAcceptedEvent):
        self.trucos_aceitos[event.jogador] = self.trucos_aceitos.get(event.jogador, 0) + 1

    def _on_truco_raised(self, event: events.TrucoRaisedEvent):
        self.trucos_aumentados[event.jogador] = self.trucos_aumentados.get(event.jogador, 0) + 1

    def obter_resumo(self) -> Dict[str, Any]:
        """Gera um dicionário consolidado com as estatísticas coletadas."""
        agentes = list(self.tempos_decisao.keys())
        resumo = {
            "partidas_total": self.partidas_total,
            "vitorias": dict(self.vitorias),
            "agentes": {}
        }

        for ag in agentes:
            tempos = self.tempos_decisao.get(ag, [0.0])
            forcas = self.forcas_maos.get(ag, [0.0])
            resumo["agentes"][ag] = {
                "tempo_medio_ms": sum(tempos) / len(tempos) if tempos else 0.0,
                "forca_media_mao": sum(forcas) / len(forcas) if forcas else 0.0,
                "total_decisoes": sum(self.contagem_decisoes.get(ag, {}).values()),
                "decisoes": dict(self.contagem_decisoes.get(ag, {})),
                "trucos_pedidos": self.trucos_pedidos.get(ag, 0),
                "trucos_aceitos": self.trucos_aceitos.get(ag, 0),
                "trucos_corridos": self.trucos_corridos.get(ag, 0),
                "trucos_aumentados": self.trucos_aumentados.get(ag, 0),
                "blefes_tentados": self.blefes_tentados.get(ag, 0),
                "blefes_sucedidos": self.blefes_sucedidos.get(ag, 0),
                "taxa_sucesso_blefe": (
                    self.blefes_sucedidos.get(ag, 0) / self.blefes_tentados.get(ag, 1) 
                    if self.blefes_tentados.get(ag, 0) > 0 else 0.0
                ),
                "cartas_mais_jogadas": sorted(
                    self.cartas_jogadas.get(ag, {}).items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
            }

        return resumo
