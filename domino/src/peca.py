class Peca:
    """Representa uma peça de dominó com dois lados (lado_a, lado_b)."""

    def __init__(self, lado_a, lado_b):
        # Por convenção, lado_a <= lado_b para evitar duplicatas
        self.lado_a = min(lado_a, lado_b)
        self.lado_b = max(lado_a, lado_b)

    def is_dupla(self):
        return self.lado_a == self.lado_b

    def total_pontos(self):
        return self.lado_a + self.lado_b

    def encaixa(self, valor):
        """Verifica se a peça pode ser jogada em uma ponta com o valor dado."""
        return self.lado_a == valor or self.lado_b == valor

    def outro_lado(self, valor):
        """Retorna o lado oposto ao valor informado."""
        if self.lado_a == valor:
            return self.lado_b
        elif self.lado_b == valor:
            return self.lado_a
        raise ValueError(f"Valor {valor} não pertence a esta peça {self}")

    def __eq__(self, outra):
        return self.lado_a == outra.lado_a and self.lado_b == outra.lado_b

    def __hash__(self):
        return hash((self.lado_a, self.lado_b))

    def __str__(self):
        return f"[{self.lado_a}|{self.lado_b}]"

    def __repr__(self):
        return self.__str__()