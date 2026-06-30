class Carta:
    def __init__(self, valor: str, naipe: str):
        self.valor = valor
        self.naipe = naipe

    def __eq__(self, outra):
        if not isinstance(outra, Carta):
            return False
        return self.valor == outra.valor and self.naipe == outra.naipe

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

    def __repr__(self):
        return f"Carta('{self.valor}', '{self.naipe}')"

    def to_dict(self):
        return {"valor": self.valor, "naipe": self.naipe}

    @staticmethod
    def from_dict(d):
        return Carta(d["valor"], d["naipe"])
