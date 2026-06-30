# from truco.src.agentes.base import AgenteBase
# from truco.src.constantes import RespostasTruco

# class AgenteProbabilistico(AgenteBase):

#     def __init__(self, nome, baralho, limiar=4, limiar_aumento=2):
#         super().__init__(nome)
#         self.limiar = limiar
#         self.baralho = baralho
#         self.limiar_aumento = limiar_aumento
    
#     def _estimar_forca_adversario(self, mao):
#         cartas_restantes = [carta for carta in self.baralho.cartas if carta not in mao.cartas]
#         return sum(carta.get_forca() for carta in cartas_restantes) / len(cartas_restantes) if cartas_restantes else 0

#     def escolher_carta(self, mao):
#         cartas_ordenadas = sorted(mao.cartas, key=lambda c: c.get_forca())
#         carta = cartas_ordenadas[len(cartas_ordenadas) // 2]
#         return mao.jogar_carta(carta)

#     def decidir_truco(self, mao):
#         forca_propria = mao.avaliar_forca()
#         forca_adversario = self._estimar_forca_adversario(mao)
#         return forca_propria["media"] >= self.limiar and forca_propria["media"] > forca_adversario
    
#     def responder_truco(self, mao, valor_atual):
#         forca_propria = mao.avaliar_forca()
#         forca_adversario = self._estimar_forca_adversario(mao)
#         vantagem = forca_propria["media"] - forca_adversario
#         if vantagem >= self.limiar_aumento and valor_atual < 12:
#             return RespostasTruco.AUMENTAR
#         elif vantagem > 0:
#             return RespostasTruco.ACEITAR
#         return RespostasTruco.CORRER
    
#     def foi_blefe(self, mao):
#         return mao.avaliar_forca()["media"] < self.limiar












from truco.src.agentes.base import AgenteBase
from truco.src.constantes import RespostasTruco


class AgenteProbabilistico(AgenteBase):
    def __init__(self, nome, baralho, limiar=4, limiar_aumento=2):
        super().__init__(nome)
        self.baralho = baralho
        self.limiar = limiar
        self.limiar_aumento = limiar_aumento

    def _estimar_forca_adversario(self, mao):
        """Estima força média do adversário pelas cartas que não estão na minha mão."""
        cartas_visiveis = set((c.valor, c.naipe) for c in mao.cartas)
        # Exclui também a vira
        cartas_visiveis.add((mao.vira.valor, mao.vira.naipe))
        cartas_restantes = [
            c for c in self.baralho.cartas
            if (c.valor, c.naipe) not in cartas_visiveis
        ]
        if not cartas_restantes:
            return 0
        return sum(c.get_forca(mao.vira) for c in cartas_restantes) / len(cartas_restantes)

    def escolher_carta(self, mao):
        # Joga a carta mediana (nem desperdiça a melhor nem entrega de graça)
        cartas_ordenadas = sorted(mao.cartas, key=lambda c: c.get_forca(mao.vira))
        carta = cartas_ordenadas[len(cartas_ordenadas) // 2]
        return mao.jogar_carta(carta)

    def decidir_truco(self, mao):
        forca_propria = mao.avaliar_forca()["media"]
        forca_adv = self._estimar_forca_adversario(mao)
        return forca_propria >= self.limiar and forca_propria > forca_adv

    def responder_truco(self, mao, valor_atual):
        forca_propria = mao.avaliar_forca()["media"]
        forca_adv = self._estimar_forca_adversario(mao)
        vantagem = forca_propria - forca_adv
        if vantagem >= self.limiar_aumento and valor_atual < 12:
            return RespostasTruco.AUMENTAR
        elif vantagem > 0:
            return RespostasTruco.ACEITAR
        return RespostasTruco.CORRER

    def foi_blefe(self, mao):
        return mao.avaliar_forca()["media"] < self.limiar