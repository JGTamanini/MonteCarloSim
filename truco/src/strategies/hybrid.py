from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.strategies.conservative import ConservativeStrategy
from truco.src.strategies.aggressive import AggressiveStrategy
from truco.src.strategies.probabilistic import ProbabilisticStrategy


class HybridStrategy:
    def __init__(self):
        self._conservative = ConservativeStrategy()
        self._aggressive = AggressiveStrategy()
        self._probabilistic = ProbabilisticStrategy()

    def _obter_estrategia_por_placar(self, agente: Any, placar: dict) -> Any:
        meus_pontos = placar.get(agente.nome, 0)
        adversario_nome = [n for n in placar.keys() if n != agente.nome][0]
        pontos_adv = placar.get(adversario_nome, 0)

        # Se estamos perto de ganhar (>= 9 pontos), jogamos conservador para não entregar
        if meus_pontos >= 9:
            return self._conservative, "Estamos perto da vitória (pontos >= 9). Ativando modo Conservador para segurança."

        # Se estamos prestes a perder (adversário >= 9 e nós estamos atrás), entramos em desespero agressivo
        if pontos_adv >= 9 and meus_pontos < pontos_adv:
            return self._aggressive, "Estamos prestes a perder (oponente >= 9). Ativando modo Agressivo para tentar virar."

        # Condições normais: usa análise probabilística equilibrada
        return self._probabilistic, "Partida equilibrada. Ativando modo Probabilístico padrão."

    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        est, motivo = self._obter_estrategia_por_placar(agente, percepcao.placar_partida)
        acao, detalhe, mot_detalhe = est.escolher_acao(agente, percepcao, beliefs, memory, pode_pedir_truco)
        return acao, detalhe, f"Híbrido ({motivo}) -> {mot_detalhe}"

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        est, motivo = self._obter_estrategia_por_placar(agente, percepcao.placar_partida)
        resposta, mot_detalhe = est.responder_truco(agente, percepcao, beliefs, memory, valor_proposto)
        return resposta, f"Híbrido ({motivo}) -> {mot_detalhe}"
