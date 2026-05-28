from enum import Enum

class RespostasTruco(Enum):
    ACEITAR = "aceitar"
    AUMENTAR = "aumentar"
    CORRER = "correr"

HIERARQUIA = {
    "4": 1, "5": 2, "6": 3, "7": 4,
    "J": 5, "Q": 6, "K": 7,
    "A": 8, "2": 9, "3": 10
}

MANILHAS = {
    ("7", "espadas"): 11,
    ("A", "espadas"): 12,
    ("7", "copas"):   13,
    ("4", "paus"):    14
}

NAIPES = {
    "paus":    1,
    "ouros":   2,
    "copas":   3,
    "espadas": 4
}