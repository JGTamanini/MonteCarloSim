# from truco.src.carta import Carta
# from truco.src.constantes import HIERARQUIA, NAIPES
# import random

# class Baralho:
#     def __init__(self):
#         self.cartas = [Carta(valor, naipe) for valor in HIERARQUIA.keys() for naipe in NAIPES.keys()]
    
#     def embaralhar(self):
#         random.shuffle(self.cartas)
    
#     def distribuir(self, num_jogadores, cartas_por_jogador):
#         self.embaralhar()
#         if num_jogadores * cartas_por_jogador > len(self.cartas):
#             raise ValueError("Não há cartas suficientes para distribuir")
        
#         distribuicao = []
#         for i in range(num_jogadores):
#             mao = self.cartas[i*cartas_por_jogador:(i+1)*cartas_por_jogador]
#             distribuicao.append(mao)
        
#         return distribuicao


import random
from truco.src.carta import Carta
from truco.src.constantes import HIERARQUIA, NAIPES


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

    def distribuir(self, num_jogadores, cartas_por_jogador=3):
        """
        Embaralha, define a vira (primeira carta após a distribuição)
        e distribui as mãos. A vira NÃO entra na mão de ninguém.
        """
        self.embaralhar()

        total_cartas = num_jogadores * cartas_por_jogador
        if total_cartas + 1 > len(self.cartas):
            raise ValueError("Não há cartas suficientes para distribuir + vira.")

        distribuicao = []
        for i in range(num_jogadores):
            mao = list(self.cartas[i * cartas_por_jogador:(i + 1) * cartas_por_jogador])
            distribuicao.append(mao)

        # A vira é a carta imediatamente após as distribuídas
        self.vira = self.cartas[total_cartas]

        return distribuicao