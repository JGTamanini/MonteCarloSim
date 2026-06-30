from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class ProbabilisticStrategy:
    def _estimar_forca_media_restantes(self, beliefs: Any, vira: Any) -> float:
        cartas = beliefs.cartas_restantes
        if not cartas:
            return 5.0
        return sum(RuleEngine.get_forca_carta(c, vira) for c in cartas) / len(cartas)

    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria
        forca_adv = self._estimar_forca_media_restantes(beliefs, percepcao.vira)

        # Pede truco se tiver vantagem probabilística clara e oponente com pouca chance de manilha
        vantagem = forca - forca_adv
        if pode_pedir_truco and vantagem >= 1.5 and beliefs.probabilidade_manilha_oponente < 0.5:
            return AcoesJogador.PEDIR_TRUCO, None, (
                f"Probabilidades favoráveis: Vantagem de {vantagem:.2f} pts sobre força média estimada, "
                f"com chance de manilha adversária baixa ({beliefs.probabilidade_manilha_oponente * 100:.1f}%)."
            )

        # Joga a carta mediana (nem desperdiça a melhor nem entrega de graça)
        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira))
        carta = cartas_ordenadas[len(cartas_ordenadas) // 2]
        return AcoesJogador.JOGAR_CARTA, carta, f"Jogando a carta mediana ({carta}) calculada pela distribuição probabilística."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria
        forca_adv = self._estimar_forca_media_restantes(beliefs, percepcao.vira)
        vantagem = forca - forca_adv

        # Aumenta se a vantagem for excelente
        if vantagem >= 2.5 and valor_proposto < 12:
            return RespostasTruco.AUMENTAR, f"Vantagem probabilística excelente ({vantagem:.2f} > 2.5), aumentando aposta."
        # Aceita se tiver qualquer vantagem positiva
        elif vantagem >= 0.0:
            return RespostasTruco.ACEITAR, f"Mão matematicamente superior ({vantagem:.2f} >= 0.0), aceitando truco."
        return RespostasTruco.CORRER, f"Expectativa matemática negativa (desvantagem de {vantagem:.2f} pts), correndo."
