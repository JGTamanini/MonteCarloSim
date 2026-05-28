from abc import ABC, abstractmethod

class AgenteBase(ABC):
    def __init__(self, nome):
        self.nome = nome

    @abstractmethod
    def escolher_carta(self, mao):
        pass

    @abstractmethod
    def decidir_truco(self, mao):
        pass

    @abstractmethod
    def responder_truco(self, mao, valor_atual):
        pass
    
    @abstractmethod
    def foi_blefe(self, mao):
        pass