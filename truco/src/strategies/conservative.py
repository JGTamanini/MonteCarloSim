from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class ConservativeStrategy:
    def __init__(self, limiar_truco: float = 8.5, limiar_aceitar: float = 8.0):
        self.limiar_truco = limiar_truco
        self.limiar_aceitar = limiar_aceitar

    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria

        # Conservador só pede truco se tiver mão extremamente forte
        if pode_pedir_truco and forca >= self.limiar_truco:
            return AcoesJogador.PEDIR_TRUCO, None, f"Mão forte (força: {forca:.2f} >= limiar: {self.limiar_truco}), pedindo truco."

        # Joga a carta mais fraca para economizar as melhores
        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira))
        carta = cartas_ordenadas[0]
        return AcoesJogador.JOGAR_CARTA, carta, f"Jogando a carta mais fraca ({carta}) para economizar força."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria

        # Conservador aceita se a mão for forte, caso contrário corre
        if forca >= self.limiar_aceitar:
            return RespostasTruco.ACEITAR, f"Mão forte (força: {forca:.2f} >= limiar: {self.limiar_aceitar}), aceitando truco."
        return RespostasTruco.CORRER, f"Mão fraca/mediana (força: {forca:.2f} < limiar: {self.limiar_aceitar}), correndo por segurança."
