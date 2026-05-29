from domino.src.agentes.base import AgenteBase
from domino.src.peca import Peca


class AgenteProbabilistico(AgenteBase):
    """
    Estratégia probabilística com consciência de dupla.

    Lógica individual (sempre ativa):
    - Calcula peças invisíveis (não na própria mão, não na mesa).
    - Prefere jogadas que deixam a ponta nova com MENOS encaixes possíveis
      para peças invisíveis → trava os adversários.

    Lógica colaborativa (ativa quando parceiro é passado):
    - Se a ponta que vai ficar exposta após minha jogada é um valor que
      eu mesmo tenho outra peça com aquele lado → provavelmente o parceiro
      também tem, pois os valores estão concentrados na dupla.
    - Desempata escolhendo a jogada que abre uma ponta cujo valor aparece
      mais vezes na própria mão → sinaliza ao parceiro qual lado jogar.

    Em caso de empate total, desempata pelo peso (mais pesada primeiro).
    """

    def __init__(self, nome, max_valor=6):
        super().__init__(nome)
        self.max_valor = max_valor
        self._todas_pecas = frozenset(
            Peca(a, b) for a in range(max_valor + 1) for b in range(a, max_valor + 1)
        )

    def _pecas_invisiveis(self, mao, mesa):
        visiveis = set(mao.pecas) | set(mesa.sequencia)
        return self._todas_pecas - visiveis

    def _conta_encaixes(self, valor, pecas_invisiveis):
        return sum(1 for p in pecas_invisiveis if p.encaixa(valor))

    def _frequencia_valor_na_mao(self, valor, mao):
        """Quantas peças da minha mão têm o valor dado em algum lado."""
        return sum(1 for p in mao.pecas if p.encaixa(valor))

    def _nova_ponta(self, peca, lado, mesa):
        """Calcula qual valor ficará exposto na ponta após jogar a peça."""
        if mesa.esta_vazia():
            return peca.lado_b
        if lado == "direita":
            return peca.outro_lado(mesa.ponta_dir) if peca.encaixa(mesa.ponta_dir) else peca.lado_a
        else:
            return peca.outro_lado(mesa.ponta_esq) if peca.encaixa(mesa.ponta_esq) else peca.lado_b

    def escolher_peca(self, mao, mesa, parceiro=None):
        jogaveis = mesa.pecas_jogaveis(mao.pecas)
        invisiveis = self._pecas_invisiveis(mao, mesa)

        melhor = None
        menor_encaixes = float("inf")
        maior_freq_parceiro = -1
        maior_peso = -1

        for peca, lado in jogaveis:
            nova_pt = self._nova_ponta(peca, lado, mesa)
            encaixes = self._conta_encaixes(nova_pt, invisiveis)
            peso = peca.total_pontos()

            # Frequência do valor da nova ponta na própria mão
            # (proxy de quanto aquele valor está concentrado na dupla)
            freq = self._frequencia_valor_na_mao(nova_pt, mao)

            melhor_que_atual = False
            if encaixes < menor_encaixes:
                melhor_que_atual = True
            elif encaixes == menor_encaixes:
                if freq > maior_freq_parceiro:
                    melhor_que_atual = True
                elif freq == maior_freq_parceiro and peso > maior_peso:
                    melhor_que_atual = True

            if melhor_que_atual:
                menor_encaixes = encaixes
                maior_freq_parceiro = freq
                maior_peso = peso
                melhor = (peca, lado)

        return melhor