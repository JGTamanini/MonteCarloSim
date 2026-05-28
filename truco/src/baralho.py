from truco.src.carta import Carta
from truco.src.constantes import HIERARQUIA, NAIPES
import random

class Baralho:
    def __init__(self):
        self.cartas = [Carta(valor, naipe) for valor in HIERARQUIA.keys() for naipe in NAIPES.keys()]
    
    def embaralhar(self):
        random.shuffle(self.cartas)
    
    def distribuir(self, num_jogadores, cartas_por_jogador):
        self.embaralhar()
        if num_jogadores * cartas_por_jogador > len(self.cartas):
            raise ValueError("Não há cartas suficientes para distribuir")
        
        distribuicao = []
        for i in range(num_jogadores):
            mao = self.cartas[i*cartas_por_jogador:(i+1)*cartas_por_jogador]
            distribuicao.append(mao)
        
        return distribuicao