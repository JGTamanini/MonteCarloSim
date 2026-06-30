# from truco.src.agentes.base import AgenteBase
# from truco.src.constantes import RespostasTruco

# class AgenteConservador(AgenteBase):

#     def __init__(self, nome, limiar=8):
#         super().__init__(nome)
#         self.limiar = limiar

#     def escolher_carta(self, mao):
#         carta = min(mao.cartas, key=lambda carta: carta.get_forca())
#         return mao.jogar_carta(carta)

#     def decidir_truco(self, mao):
#         forca_mao = mao.avaliar_forca()
#         if forca_mao["media"] >= self.limiar:
#             return True
#         return False
    
#     def responder_truco(self, mao, valor_atual):
#         forca_mao = mao.avaliar_forca()
#         if forca_mao["media"] >= self.limiar:
#             return RespostasTruco.ACEITAR
#         return RespostasTruco.CORRER

#     def foi_blefe(self, mao):
#         return mao.avaliar_forca()["media"] < self.limiar







from truco.src.agentes.base import AgenteBase
from truco.src.constantes import RespostasTruco


class AgenteConservador(AgenteBase):
    def __init__(self, nome, limiar=8):
        super().__init__(nome)
        self.limiar = limiar

    def escolher_carta(self, mao):
        # Joga a carta mais fraca (preserva as boas para rodadas decisivas)
        carta = min(mao.cartas, key=lambda c: c.get_forca(mao.vira))
        return mao.jogar_carta(carta)

    def decidir_truco(self, mao):
        return mao.avaliar_forca()["media"] >= self.limiar

    def responder_truco(self, mao, valor_atual):
        if mao.avaliar_forca()["media"] >= self.limiar:
            return RespostasTruco.ACEITAR
        return RespostasTruco.CORRER

    def foi_blefe(self, mao):
        return mao.avaliar_forca()["media"] < self.limiar