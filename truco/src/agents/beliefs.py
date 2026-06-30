from typing import Any, Dict, List
from truco.src.core.carta import Carta
from truco.src.core.perception import Perception
from truco.src.agents.memory import AgentMemory


class BeliefState:
    """Representação subjetiva do mundo (Crenças) do agente Truco."""

    def __init__(self):
        self.cartas_restantes: List[Carta] = []          # Cartas que ainda estão ocultas para o agente
        self.probabilidade_manilha_oponente: float = 0.0  # Chance do adversário ter ao menos uma manilha forte
        self.chance_blefe_oponente: float = 0.0          # Probabilidade estimada de que o oponente esteja blefando
        self.perfil_oponente: str = "Desconhecido"       # Perfil mapeado do oponente (Agressivo, Conservador, etc.)
        self.forca_mao_propria: float = 0.0               # Força média calculada das próprias cartas
        self.placar: Dict[str, int] = {}                  # Placar atual da partida
        self.valor_aposta_atual: int = 1                  # Valor de pontos da mão ativa

    def atualizar_crencas(self, percepcao: Perception, memoria: AgentMemory):
        """Atualiza o estado de crenças com base na percepção e memória histórica."""
        self.placar = percepcao.placar_partida
        self.valor_aposta_atual = percepcao.valor_truco_atual
        self.perfil_oponente = memoria.obter_perfil_estimado_oponente()
        self.chance_blefe_oponente = memoria.obter_taxa_blefe_oponente()

    def to_dict(self) -> Dict[str, Any]:
        """Gera um dicionário representativo das crenças para logs e explicações."""
        return {
            "probabilidade_manilha_oponente": round(self.probabilidade_manilha_oponente, 3),
            "chance_blefe_oponente": round(self.chance_blefe_oponente, 3),
            "perfil_oponente": self.perfil_oponente,
            "forca_mao_propria": round(self.forca_mao_propria, 2),
            "valor_aposta_atual": self.valor_aposta_atual
        }
