from enum import Enum


class RespostasTruco(Enum):
    ACEITAR = "aceitar"
    AUMENTAR = "aumentar"
    CORRER = "correr"


class AcoesJogador(Enum):
    JOGAR_CARTA = "jogar_carta"
    PEDIR_TRUCO = "pedir_truco"
    ACEITAR_TRUCO = "aceitar_truco"
    CORRER_TRUCO = "correr_truco"
    AUMENTAR_TRUCO = "aumentar_truco"


# Hierarquia base dos valores (sem manilhas)
# 4 é o mais fraco, 3 é o mais forte
HIERARQUIA = {
    "4": 1, "5": 2, "6": 3, "7": 4,
    "J": 5, "Q": 6, "K": 7,
    "A": 8, "2": 9, "3": 10
}

# Ordem dos naipes para desempate entre manilhas
# paus > espadas > copas > ouros (do mais forte para o mais fraco)
NAIPES = {
    "ouros":   1,
    "copas":   2,
    "espadas": 3,
    "paus":    4,
}

# Sequência circular para determinar a manilha a partir da vira.
# A manilha é o valor imediatamente superior ao da vira.
# Exemplo: vira = "3" → manilha = "4"; vira = "7" → manilha = "J"
SEQUENCIA_VIRA = ["4", "5", "6", "7", "J", "Q", "K", "A", "2", "3"]


def get_valor_manilha(valor_vira):
    """Retorna o valor da carta que é manilha dado o valor da vira."""
    idx = SEQUENCIA_VIRA.index(valor_vira)
    return SEQUENCIA_VIRA[(idx + 1) % len(SEQUENCIA_VIRA)]
