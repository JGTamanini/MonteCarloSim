class Mao:
    """
    Representa a mão de um jogador no dominó.
    """

    def __init__(self, pecas):
        self.pecas = list(pecas)

    def esta_vazia(self):
        return len(self.pecas) == 0

    def total_pontos(self):
        return sum(p.total_pontos() for p in self.pecas)

    def tem_dupla(self):
        return any(p.is_dupla() for p in self.pecas)

    def maior_dupla(self):
        duplas = [p for p in self.pecas if p.is_dupla()]
        if not duplas:
            return None
        return max(duplas, key=lambda p: p.lado_a)

    def peca_mais_pesada(self):
        if not self.pecas:
            return None
        return max(self.pecas, key=lambda p: p.total_pontos())

    def peca_mais_leve(self):
        if not self.pecas:
            return None
        return min(self.pecas, key=lambda p: p.total_pontos())

    def jogar_peca(self, peca):
        if peca in self.pecas:
            self.pecas.remove(peca)
            return peca
        raise ValueError(f"Peça {peca} não está na mão.")

    def avaliar_forca(self):
        """Retorna métricas da mão para uso pelos agentes."""
        if not self.pecas:
            return {"soma": 0, "media": 0, "mais_pesada": 0, "num_duplas": 0}
        soma = self.total_pontos()
        return {
            "soma": soma,
            "media": soma / len(self.pecas),
            "mais_pesada": self.peca_mais_pesada().total_pontos(),
            "num_duplas": sum(1 for p in self.pecas if p.is_dupla()),
        }

    def __len__(self):
        return len(self.pecas)

    def __str__(self):
        return " ".join(str(p) for p in self.pecas)