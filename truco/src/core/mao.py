from typing import List
from truco.src.core.carta import Carta


class Mao:
    def __init__(self, cartas: List[Carta], vira: Carta = None):
        self.cartas = list(cartas)
        self.vira = vira

    def jogar_carta(self, carta: Carta) -> Carta:
        for c in self.cartas:
            if c.valor == carta.valor and c.naipe == carta.naipe:
                self.cartas.remove(c)
                return c
        raise ValueError(f"Carta {carta} não está na mão do jogador.")

    def __len__(self):
        return len(self.cartas)

    def __str__(self):
        return ", ".join(str(c) for c in self.cartas)

    def __repr__(self):
        return f"Mao({self.cartas}, vira={self.vira})"
