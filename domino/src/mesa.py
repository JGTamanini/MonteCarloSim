class Mesa:
    """
    Representa o estado da mesa de dominó.

    Mantém a sequência de peças jogadas e as duas pontas abertas
    onde novas peças podem ser encaixadas.
    """

    def __init__(self):
        self.sequencia = []   # lista de Peca na ordem de jogo
        self.ponta_esq = None  # valor na ponta esquerda
        self.ponta_dir = None  # valor na ponta direita

    def esta_vazia(self):
        return len(self.sequencia) == 0

    def primeira_peca(self, peca):
        """Coloca a primeira peça na mesa."""
        self.sequencia.append(peca)
        self.ponta_esq = peca.lado_a
        self.ponta_dir = peca.lado_b

    def jogar(self, peca, lado="direita"):
        """
        Adiciona uma peça à mesa no lado informado ('esquerda' ou 'direita').
        Retorna True se bem-sucedido, False se a peça não encaixa.
        """
        if self.esta_vazia():
            self.primeira_peca(peca)
            return True

        if lado == "direita":
            if peca.lado_a == self.ponta_dir:
                self.sequencia.append(peca)
                self.ponta_dir = peca.lado_b
            elif peca.lado_b == self.ponta_dir:
                self.sequencia.append(peca)
                self.ponta_dir = peca.lado_a
            else:
                return False
        elif lado == "esquerda":
            if peca.lado_b == self.ponta_esq:
                self.sequencia.insert(0, peca)
                self.ponta_esq = peca.lado_a
            elif peca.lado_a == self.ponta_esq:
                self.sequencia.insert(0, peca)
                self.ponta_esq = peca.lado_b
            else:
                return False
        return True

    def pecas_jogaveis(self, mao_pecas):
        """
        Retorna lista de (peca, lado) que podem ser jogadas a partir
        da mão fornecida no estado atual da mesa.
        """
        if self.esta_vazia():
            return [(p, "direita") for p in mao_pecas]

        jogaveis = []
        vistas = set()
        for peca in mao_pecas:
            opcoes = []
            if peca.encaixa(self.ponta_dir):
                opcoes.append((peca, "direita"))
            if peca.encaixa(self.ponta_esq) and self.ponta_esq != self.ponta_dir:
                opcoes.append((peca, "esquerda"))
            elif peca.encaixa(self.ponta_esq) and self.ponta_esq == self.ponta_dir and not opcoes:
                opcoes.append((peca, "esquerda"))

            for op in opcoes:
                key = (op[0].lado_a, op[0].lado_b, op[1])
                if key not in vistas:
                    vistas.add(key)
                    jogaveis.append(op)

        return jogaveis

    def __str__(self):
        if self.esta_vazia():
            return "(mesa vazia)"
        return f"[{self.ponta_esq}] ... [{self.ponta_dir}]  ({len(self.sequencia)} peças)"