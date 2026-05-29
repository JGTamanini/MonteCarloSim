from domino.src.agentes.base import AgenteBase


class AgenteDefensivo(AgenteBase):
    """
    Estratégia defensiva: joga sempre a peça mais leve (menos pontos).

    Raciocínio: minimiza os pontos que a dupla adversária ganharia se
    trancarem o jogo, e facilita batidas ao esvaziar peças pesadas cedo.
    Em duplas, o parceiro se beneficia também — se ambos jogam leve,
    a dupla fica com pouca soma em caso de trancamento.
    """

    def __init__(self, nome):
        super().__init__(nome)

    def escolher_peca(self, mao, mesa, parceiro=None):
        jogaveis = mesa.pecas_jogaveis(mao.pecas)
        return min(jogaveis, key=lambda jogada: jogada[0].total_pontos())