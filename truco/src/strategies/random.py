import random
from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception


class RandomStrategy:
    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        # Decisão aleatória de truco
        if pode_pedir_truco and random.random() < 0.15:
            return AcoesJogador.PEDIR_TRUCO, None, "Decisão aleatória de pedir Truco (15% de chance)."

        # Escolhe uma carta aleatória da mão
        carta = random.choice(percepcao.mao_cartas)
        return AcoesJogador.JOGAR_CARTA, carta, f"Carta {carta} escolhida aleatoriamente."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        escolha = random.choice(list(RespostasTruco))
        return escolha, f"Resposta {escolha.name} escolhida aleatoriamente."
