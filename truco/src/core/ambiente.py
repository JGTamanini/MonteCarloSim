import logging
from typing import Any, Dict, List
from truco.src.core.baralho import Baralho
from truco.src.core.blackboard import Blackboard
from truco.src.core.carta import Carta
from truco.src.core.perception import Perception, PerceptionEngine
from truco.src.core.state_machine import JogoState, MatchEndState, SetupState
from truco.src.events.event_bus import EventBus

logger = logging.getLogger("AmbienteJogo")


class AmbienteJogo:
    def __init__(self, agentes: List[Any], event_bus: EventBus):
        self.agentes = agentes
        self.event_bus = event_bus
        self.blackboard = Blackboard()
        self.baralho = Baralho()

        # Estado dinâmico do jogo controlado pela State Machine
        self.placar_partida: Dict[str, int] = {}
        self.maos_jogadores: Dict[str, List[Carta]] = {}
        self.vira: Optional[Carta] = None
        self.jogador_ativo_idx: int = 0
        self.cartas_jogadas_queda: Dict[str, Carta] = {}
        self.vencedores_quedas: List[str] = []
        self.valor_truco_atual: int = 1
        self.valor_truco_proposto: int = 1
        self.proponente_truco: Optional[str] = None
        self.truco_pedido_nesta_mao: bool = False
        self.numero_mao: int = 0
        self.numero_queda_atual: int = 1
        self.vencedor_partida: Optional[str] = None
        self.historico_rodadas: List[Dict[str, Any]] = []

        self._estado_atual: Optional[JogoState] = None

        # Conecta os agentes ao EventBus e ao Blackboard para atualizar suas memórias
        for agente in self.agentes:
            agente.conectar_ambiente(self.event_bus, self.blackboard)

    def definir_estado(self, novo_estado: JogoState):
        """Transiciona para um novo estado do jogo."""
        if self._estado_atual:
            self._estado_atual.sair(self)
        self._estado_atual = novo_estado
        self._estado_atual.entrar(self)

    def obter_jogador_ativo(self) -> Any:
        return self.agentes[self.jogador_ativo_idx]

    def obter_jogador_inativo(self) -> Any:
        # Em 1v1, o inativo é o outro
        return self.agentes[(self.jogador_ativo_idx + 1) % len(self.agentes)]

    def alternar_jogador_ativo(self):
        self.jogador_ativo_idx = (self.jogador_ativo_idx + 1) % len(self.agentes)
        logger.debug(f"Turno alternado para: {self.obter_jogador_ativo().nome}")

    def gerar_percepcao_para(self, jogador: Any) -> Perception:
        """Gera uma percepção filtrada ocultando dados privados dos outros agentes."""
        mao_agente = self.maos_jogadores.get(jogador.nome, [])

        # Calcula quedas ganhas por cada jogador
        quedas_vencidas = {j.nome: 0 for j in self.agentes}
        for vencedor in self.vencedores_quedas:
            if vencedor in quedas_vencidas:
                quedas_vencidas[vencedor] += 1

        return PerceptionEngine.gerar_percepcao(
            nome_agente=jogador.nome,
            mao_agente=mao_agente,
            vira=self.vira,
            cartas_jogadas_queda=self.cartas_jogadas_queda,
            placar_partida=self.placar_partida,
            quedas_vencidas=quedas_vencidas,
            valor_truco_atual=self.valor_truco_atual,
            blackboard=self.blackboard
        )

    def jogar_partida(self):
        """Executa a partida do início (SetupState) até o fim (MatchEndState)."""
        logger.info("Iniciando partida...")
        self.definir_estado(SetupState())
        while not isinstance(self._estado_atual, MatchEndState):
            self._estado_atual.processar(self)
        # Executa uma última vez o MatchEndState para disparar os eventos de encerramento
        self._estado_atual.processar(self)
        logger.info(f"Partida finalizada! Vencedor: {self.vencedor_partida}. Histórico: {self.historico_rodadas}")
        return self.vencedor_partida, self.historico_rodadas
