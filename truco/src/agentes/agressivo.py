from truco.src.agentes.base import AgenteBase
from truco.src.constantes import RespostasTruco
import random

class AgenteAgressivo(AgenteBase):

    def __init__(self, nome, limiar=4, chance_blefe=0.4):
        super().__init__(nome)
        self.limiar = limiar
        self.chance_blefe = chance_blefe

    def escolher_carta(self, mao):
        carta = max(mao.cartas, key=lambda carta: carta.get_forca())
        return mao.jogar_carta(carta)

    def decidir_truco(self, mao):
        forca_mao = mao.avaliar_forca()
        return forca_mao["media"] >= self.limiar or random.random() < self.chance_blefe
    
    def responder_truco(self, mao, valor_atual):
        forca_mao = mao.avaliar_forca()
        if forca_mao["media"] >= self.limiar:
            return RespostasTruco.AUMENTAR if valor_atual < 12 else RespostasTruco.ACEITAR
        return RespostasTruco.CORRER
    
    def foi_blefe(self, mao):
        forca = mao.avaliar_forca()["media"]
        return forca < self.limiar and self.chance_blefe > 0