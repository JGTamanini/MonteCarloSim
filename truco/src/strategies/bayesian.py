from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class BayesianStrategy:
    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria

        # Usa base probabilística para propor apostas
        if pode_pedir_truco and forca >= 7.0 and beliefs.probabilidade_manilha_oponente < 0.4:
            return AcoesJogador.PEDIR_TRUCO, None, (
                f"Proposta Bayesiana: Força própria ({forca:.2f}) é alta e chance de manilha do "
                f"oponente é baixa ({beliefs.probabilidade_manilha_oponente * 100:.1f}%)."
            )

        # Joga a carta mediana para manter flexibilidade
        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira))
        carta = cartas_ordenadas[len(cartas_ordenadas) // 2]
        return AcoesJogador.JOGAR_CARTA, carta, f"Jogando a carta mediana ({carta}) por tática probabilística."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria

        # P(Blefe | Truco) computada no BeliefState
        prob_blefe_op = beliefs.chance_blefe_oponente

        # Decisão baseada em Bayes:
        if prob_blefe_op > 0.45:
            # Alta chance de blefe, aceitamos com cartas fracas/médias
            limiar_aceitacao = 4.0
            motivo = f"Filtro Bayesiano: Oponente com alta probabilidade de blefe ({prob_blefe_op * 100:.1f}%). Aceitando com limiar baixo (4.0)."
        else:
            # Oponente é honesto, aceitamos apenas com cartas muito boas
            limiar_aceitacao = 7.0
            motivo = f"Filtro Bayesiano: Oponente com baixa probabilidade de blefe ({prob_blefe_op * 100:.1f}%). Exigindo mão forte (limiar 7.0)."

        if forca >= limiar_aceitacao:
            # Se a chance de blefe for gigantesca e tivermos mão boa, podemos contra-atacar
            if prob_blefe_op > 0.65 and forca >= 6.5 and valor_proposto < 12:
                return RespostasTruco.AUMENTAR, f"Retruco Bayesiano: Alta probabilidade de blefe detectada ({prob_blefe_op * 100:.1f}%) e mão razoável. Aumentando!"
            return RespostasTruco.ACEITAR, f"Aceitando baseado no cálculo Bayesiano. {motivo}"

        return RespostasTruco.CORRER, f"Correndo baseado no cálculo Bayesiano. {motivo}"
