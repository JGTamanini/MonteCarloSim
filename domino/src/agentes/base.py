from abc import ABC, abstractmethod


class AgenteBase(ABC):
    """Classe base para todos os agentes de dominó."""

    def __init__(self, nome):
        self.nome = nome

    @abstractmethod
    def escolher_peca(self, mao, mesa, parceiro=None):
        """
        Decide qual peça jogar e em qual lado da mesa.

        Parâmetros:
            mao     : Mao    — mão atual do jogador
            mesa    : Mesa   — estado atual da mesa
            parceiro: Agente — referência ao parceiro de dupla (pode ser None)

        Retorna:
            (Peca, str) — peça escolhida e lado ('esquerda' ou 'direita')

        Pré-condição: mesa.pecas_jogaveis(mao.pecas) não é vazio.
        """
        pass