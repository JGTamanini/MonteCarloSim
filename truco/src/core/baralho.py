import random
from typing import List, Tuple
from truco.src.core.carta import Carta
from truco.src.core.constantes import HIERARQUIA, NAIPES


class Baralho:
    def __init__(self):
        self.cartas = [
            Carta(valor, naipe)
            for valor in HIERARQUIA.keys()
            for naipe in NAIPES.keys()
        ]
        self.vira = None

    def embaralhar(self):
        random.shuffle(self.cartas)

    def distribuir(self, num_jogadores: int, cartas_por_jogador: int = 3) -> Tuple[List[List[Carta]], Carta]:
        """
        Embaralha e distribui as cartas para os jogadores.
        Define a vira como a carta imediatamente posterior ao montante distribuído.
        Retorna as mãos dos jogadores e a vira.
        """
        self.embaralhar()
        total_cartas = num_jogadores * cartas_por_jogador
        if total_cartas + 1 > len(self.cartas):
            raise ValueError("Não há cartas suficientes no baralho.")

        distribuicao = []
        for i in range(num_jogadores):
            mao = list(self.cartas[i * cartas_por_jogador:(i + 1) * cartas_por_jogador])
            distribuicao.append(mao)

        self.vira = self.cartas[total_cartas]
        return distribuicao, self.vira
