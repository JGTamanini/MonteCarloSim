# from abc import ABC, abstractmethod

# class AgenteBase(ABC):
#     def __init__(self, nome):
#         self.nome = nome

#     @abstractmethod
#     def escolher_carta(self, mao):
#         pass

#     @abstractmethod
#     def decidir_truco(self, mao):
#         pass

#     @abstractmethod
#     def responder_truco(self, mao, valor_atual):
#         pass
    
#     @abstractmethod
#     def foi_blefe(self, mao):
#         pass






from abc import ABC, abstractmethod


class AgenteBase(ABC):
    def __init__(self, nome):
        self.nome = nome

    @abstractmethod
    def escolher_carta(self, mao):
        """Escolhe e remove uma carta da mão. A vira está em mao.vira."""
        pass

    @abstractmethod
    def decidir_truco(self, mao):
        """Retorna True se o agente quer pedir truco."""
        pass

    @abstractmethod
    def responder_truco(self, mao, valor_atual):
        """Retorna RespostasTruco."""
        pass

    @abstractmethod
    def foi_blefe(self, mao):
        """Retorna True se o pedido de truco foi blefe."""
        pass