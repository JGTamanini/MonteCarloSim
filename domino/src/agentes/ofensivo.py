from domino.src.agentes.base import AgenteBase


class AgenteOfensivo(AgenteBase):
    """
    Estratégia ofensiva: joga a peça mais pesada disponível,
    priorizando duplas pesadas para travar a ponta com força.

    Raciocínio em duplas: jogar pesado trava adversários e, se a dupla
    bater, maximiza os pontos ganhos (a soma adversária tende a ser maior
    quando o jogo abre rápido). Duplas são preferidas pois bloqueiam
    um valor com mais peças do total de 28.
    """

    def __init__(self, nome):
        super().__init__(nome)

    def escolher_peca(self, mao, mesa, parceiro=None):
        jogaveis = mesa.pecas_jogaveis(mao.pecas)
        duplas = [(p, l) for p, l in jogaveis if p.is_dupla()]
        if duplas:
            return max(duplas, key=lambda jogada: jogada[0].total_pontos())
        return max(jogaveis, key=lambda jogada: jogada[0].total_pontos())