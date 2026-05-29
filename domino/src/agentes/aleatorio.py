import random
from domino.src.agentes.base import AgenteBase


class AgenteAleatorio(AgenteBase):
    """
    Agente baseline: escolhe aleatoriamente entre as jogadas válidas.
    Ignora o parceiro e o estado da mesa — puro acaso.
    """

    def __init__(self, nome):
        super().__init__(nome)

    def escolher_peca(self, mao, mesa, parceiro=None):
        jogaveis = mesa.pecas_jogaveis(mao.pecas)
        return random.choice(jogaveis)