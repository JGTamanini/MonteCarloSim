import random
from truco.src.agentes.base import AgenteBase
from truco.src.constantes import RespostasTruco

class AgenteAleatorio(AgenteBase):
    def __init__(self, nome):
        super().__init__(nome)

    def escolher_carta(self, mao):
        carta = random.choice(mao.cartas)
        return mao.jogar_carta(carta)

    def decidir_truco(self, mao):
        return random.choice([True, False])
    
    def responder_truco(self, mao, valor_atual):
        return random.choice(list(RespostasTruco))
    
    def foi_blefe(self, mao):
        return True