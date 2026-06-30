import random
from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class AggressiveStrategy:
    def __init__(self, chance_blefe: float = 0.35, limiar_truco: float = 6.0, limiar_aumento: float = 8.0):
        self.chance_blefe = chance_blefe
        self.limiar_truco = limiar_truco
        self.limiar_aumento = limiar_aumento

    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria

        # Agressivo pede truco com mão média/forte ou se blefar
        blefe = random.random() < self.chance_blefe
        if pode_pedir_truco:
            if forca >= self.limiar_truco:
                return AcoesJogador.PEDIR_TRUCO, None, f"Mão agressiva (força: {forca:.2f} >= {self.limiar_truco}), pedindo truco."
            elif blefe:
                return AcoesJogador.PEDIR_TRUCO, None, f"Blefando ativamente (chance de blefe: {self.chance_blefe * 100:.1f}%)."

        # Joga a carta mais forte para pressionar
        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira), reverse=True)
        carta = cartas_ordenadas[0]
        return AcoesJogador.JOGAR_CARTA, carta, f"Jogando a carta mais forte ({carta}) para impor pressão na queda."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria

        # Se tiver mão muito forte e puder aumentar, aumenta
        if forca >= self.limiar_aumento and valor_proposto < 12:
            return RespostasTruco.AUMENTAR, f"Mão excelente (força: {forca:.2f} >= {self.limiar_aumento}), aumentando a aposta."
        # Aceita truco com mãos moderadas (força >= 5.5)
        elif forca >= 5.5:
            return RespostasTruco.ACEITAR, f"Mão razoável (força: {forca:.2f} >= 5.5), aceitando a aposta."
        return RespostasTruco.CORRER, f"Mão muito fraca (força: {forca:.2f} < 5.5), correndo da pressão."
