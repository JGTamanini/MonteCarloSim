from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class RiskStrategy:
    def __init__(self, perfil: str = "avoid"):
        # "avoid" (evita risco / avesso) ou "seek" (busca risco / propenso)
        self.perfil = perfil

    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria

        if self.perfil == "avoid":
            # Avesso ao risco: pede truco somente com mãos perfeitas
            if pode_pedir_truco and forca >= 9.0:
                return AcoesJogador.PEDIR_TRUCO, None, "Avesso ao Risco: Mão perfeita (força >= 9.0). Pedindo truco de forma extremamente segura."
            # Joga conservador (carta mais baixa)
            cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira))
            carta = cartas_ordenadas[0]
            return AcoesJogador.JOGAR_CARTA, carta, f"Avesso ao Risco: Jogando carta mais baixa ({carta}) para mitigar variância."

        else:
            # Propenso ao risco: arrisca truco com qualquer mão razoável
            if pode_pedir_truco and forca >= 5.0:
                return AcoesJogador.PEDIR_TRUCO, None, "Propenso ao Risco: Mão regular (força >= 5.0). Pedindo truco agressivamente."
            # Joga ofensivo (carta mais alta)
            cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira), reverse=True)
            carta = cartas_ordenadas[0]
            return AcoesJogador.JOGAR_CARTA, carta, f"Propenso ao Risco: Jogando carta mais alta ({carta}) para tentar levar a queda de imediato."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria

        if self.perfil == "avoid":
            # Avesso: só aceita com mão muito sólida
            if forca >= 8.0:
                return RespostasTruco.ACEITAR, f"Avesso ao Risco: Mão sólida ({forca:.2f} >= 8.0). Aceitando proposta de truco."
            return RespostasTruco.CORRER, f"Avesso ao Risco: Fugindo do confronto para preservar pontos (força: {forca:.2f} < 8.0)."
        else:
            # Propenso: aceita com quase tudo e aumenta se tiver mão boa
            if forca >= 7.0 and valor_proposto < 12:
                return RespostasTruco.AUMENTAR, f"Propenso ao Risco: Mão boa ({forca:.2f} >= 7.0). Dobrando a aposta!"
            elif forca >= 4.0:
                return RespostasTruco.ACEITAR, f"Propenso ao Risco: Mão regular ({forca:.2f} >= 4.0). Aceitando o desafio."
            return RespostasTruco.CORRER, f"Propenso ao Risco: Mão ruim demais mesmo para arriscar (força: {forca:.2f} < 4.0)."
        class_name = "RiskStrategy"
