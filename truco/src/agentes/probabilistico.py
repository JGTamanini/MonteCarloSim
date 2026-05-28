from truco.src.agentes.base import AgenteBase
from truco.src.constantes import RespostasTruco

class AgenteProbabilistico(AgenteBase):

    def __init__(self, nome, baralho, limiar=4, limiar_aumento=2):
        super().__init__(nome)
        self.limiar = limiar
        self.baralho = baralho
        self.limiar_aumento = limiar_aumento
    
    def _estimar_forca_adversario(self, mao):
        cartas_restantes = [carta for carta in self.baralho.cartas if carta not in mao.cartas]
        return sum(carta.get_forca() for carta in cartas_restantes) / len(cartas_restantes) if cartas_restantes else 0

    def escolher_carta(self, mao):
        cartas_ordenadas = sorted(mao.cartas, key=lambda c: c.get_forca())
        carta = cartas_ordenadas[len(cartas_ordenadas) // 2]
        return mao.jogar_carta(carta)

    def decidir_truco(self, mao):
        forca_propria = mao.avaliar_forca()
        forca_adversario = self._estimar_forca_adversario(mao)
        return forca_propria["media"] >= self.limiar and forca_propria["media"] > forca_adversario
    
    def responder_truco(self, mao, valor_atual):
        forca_propria = mao.avaliar_forca()
        forca_adversario = self._estimar_forca_adversario(mao)
        vantagem = forca_propria["media"] - forca_adversario
        if vantagem >= self.limiar_aumento and valor_atual < 12:
            return RespostasTruco.AUMENTAR
        elif vantagem > 0:
            return RespostasTruco.ACEITAR
        return RespostasTruco.CORRER
    
    def foi_blefe(self, mao):
        return mao.avaliar_forca()["media"] < self.limiar