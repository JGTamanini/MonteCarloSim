import random
from domino.src.peca import Peca


class Conjunto:
    """Conjunto completo de peças de dominó (duplo-6: 28 peças)."""

    def __init__(self, max_valor=6):
        self.max_valor = max_valor
        self.pecas = [
            Peca(a, b)
            for a in range(max_valor + 1)
            for b in range(a, max_valor + 1)
        ]

    def embaralhar(self):
        random.shuffle(self.pecas)

    def distribuir(self, num_jogadores, pecas_por_jogador=7):
        self.embaralhar()
        total_necessario = num_jogadores * pecas_por_jogador
        if total_necessario > len(self.pecas):
            raise ValueError("Peças insuficientes para distribuição.")

        distribuicao = []
        for i in range(num_jogadores):
            mao = list(self.pecas[i * pecas_por_jogador:(i + 1) * pecas_por_jogador])
            distribuicao.append(mao)

        # Peças restantes ficam no monte (dorme)
        self.dorme = list(self.pecas[total_necessario:])

        return distribuicao

    def __len__(self):
        return len(self.pecas)