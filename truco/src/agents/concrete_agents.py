from truco.src.agents.base_agent import AgenteBase
from truco.src.strategies import (
    RandomStrategy,
    ConservativeStrategy,
    AggressiveStrategy,
    ProbabilisticStrategy,
    AdaptiveStrategy,
    BluffStrategy,
    BayesianStrategy,
    RiskStrategy,
    HybridStrategy,
)


class AgenteAleatorio(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, RandomStrategy())


class AgenteConservador(AgenteBase):
    def __init__(self, nome: str, limiar_truco: float = 8.5, limiar_aceitar: float = 8.0):
        super().__init__(nome, ConservativeStrategy(limiar_truco, limiar_aceitar))


class AgenteAgressivo(AgenteBase):
    def __init__(self, nome: str, chance_blefe: float = 0.35):
        super().__init__(nome, AggressiveStrategy(chance_blefe=chance_blefe))


class AgenteProbabilistico(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, ProbabilisticStrategy())


class AgenteAdaptativo(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, AdaptiveStrategy())


class AgenteCooperativo(AgenteBase):
    def __init__(self, nome: str):
        # Um agente adaptativo cooperativo que compartilha conhecimento via Blackboard
        super().__init__(nome, AdaptiveStrategy(), cooperativo=True)


class AgenteBlefador(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, BluffStrategy())


class AgenteBayesiano(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, BayesianStrategy())


class AgenteRiscoEvitador(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, RiskStrategy(perfil="avoid"))


class AgenteRiscoBuscador(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, RiskStrategy(perfil="seek"))


class AgenteHibrido(AgenteBase):
    def __init__(self, nome: str):
        super().__init__(nome, HybridStrategy())
