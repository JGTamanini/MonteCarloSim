import logging
from typing import Dict, List
from truco.src.core.carta import Carta

logger = logging.getLogger("AgentMemory")


class AgentMemory:
    def __init__(self, nome_agente: str):
        self.nome_agente = nome_agente

        # Memória de Curto Prazo (Mão/Rodada atual)
        self.cartas_jogadas_na_mao: List[Dict[str, Any]] = []  # [{"jogador": str, "carta": Carta}]
        self.cartas_reveladas: List[Carta] = []
        self.historico_apostas_na_mao: List[Dict[str, Any]] = []

        # Estatísticas acumuladas sobre o oponente
        self.total_trucos_recebidos_oponente = 0
        self.trucos_aceitos_oponente = 0
        self.trucos_corridos_oponente = 0
        self.trucos_aumentados_oponente = 0

        self.total_trucos_pedidos_oponente = 0
        self.blefes_confirmados_oponente = 0

        self.cartas_jogadas_oponente: List[Carta] = []

        # Histórico geral de partidas contra o oponente
        self.partidas_jogadas = 0
        self.vitorias = 0
        self.derrotas = 0

    def reset_curto_prazo(self):
        """Zera a memória de curto prazo (chamada a cada nova mão)."""
        self.cartas_jogadas_na_mao.clear()
        self.cartas_reveladas.clear()
        self.historico_apostas_na_mao.clear()

    def registrar_carta_jogada(self, jogador: str, carta: Carta):
        self.cartas_jogadas_na_mao.append({"jogador": jogador, "carta": carta})
        self.cartas_reveladas.append(carta)
        if jogador != self.nome_agente:
            self.cartas_jogadas_oponente.append(carta)

    def registrar_pedido_truco(self, jogador: str, valor: int):
        self.historico_apostas_na_mao.append({"tipo": "pedido", "jogador": jogador, "valor": valor})
        if jogador != self.nome_agente:
            self.total_trucos_pedidos_oponente += 1

    def registrar_resposta_truco(self, jogador: str, resposta: str, valor_final: int):
        self.historico_apostas_na_mao.append({"tipo": "resposta", "jogador": jogador, "resposta": resposta, "valor": valor_final})
        if jogador != self.nome_agente:
            self.total_trucos_recebidos_oponente += 1
            if resposta == "aceitar":
                self.trucos_aceitos_oponente += 1
            elif resposta == "correr":
                self.trucos_corridos_oponente += 1
            elif resposta == "aumentar":
                self.trucos_aumentados_oponente += 1

    def registrar_blefe_confirmado_oponente(self):
        self.blefes_confirmados_oponente += 1

    def obter_taxa_aceitacao_oponente(self) -> float:
        """Retorna a porcentagem de vezes que o oponente aceitou propostas de Truco."""
        if self.total_trucos_recebidos_oponente == 0:
            return 0.5  # Valor padrão neutro (50%)
        return self.trucos_aceitos_oponente / self.total_trucos_recebidos_oponente

    def obter_taxa_corrida_oponente(self) -> float:
        """Retorna a porcentagem de vezes que o oponente fugiu do Truco."""
        if self.total_trucos_recebidos_oponente == 0:
            return 0.3  # Padrão
        return self.trucos_corridos_oponente / self.total_trucos_recebidos_oponente

    def obter_taxa_blefe_oponente(self) -> float:
        """Estima a taxa de blefe do oponente com base nos trucos pedidos e mãos avaliadas."""
        if self.total_trucos_pedidos_oponente == 0:
            return 0.15  # Padrão baixo
        return self.blefes_confirmados_oponente / self.total_trucos_pedidos_oponente

    def obter_perfil_estimado_oponente(self) -> str:
        """
        Classifica o perfil estratégico do oponente.
        """
        if self.total_trucos_recebidos_oponente < 2 and self.total_trucos_pedidos_oponente < 2:
            return "Desconhecido"

        taxa_corrida = self.obter_taxa_corrida_oponente()
        taxa_blefe = self.obter_taxa_blefe_oponente()

        # Oponente que corre muito (conservador/medroso)
        if taxa_corrida > 0.6:
            return "Conservador"

        # Oponente que blefa muito ou pede muito truco
        if taxa_blefe > 0.35 or (self.total_trucos_pedidos_oponente / max(1, self.partidas_jogadas * 4) > 0.5):
            return "Agressivo"

        # Padrão equilibrado
        return "Probabilístico"
