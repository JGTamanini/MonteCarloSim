from truco.src.carta import Carta

class Mao:
    def __init__(self, cartas):
        self.cartas = cartas
    
    def avaliar_forca(self):
        soma_forca = 0
        media_forca = 0
        mais_forte = float('-inf')
        for carta in self.cartas:
            forca = carta.get_forca()
            soma_forca += forca
            if forca > mais_forte:
                mais_forte = forca
        media_forca = soma_forca / len(self.cartas) if self.cartas else 0
        return {"soma": soma_forca, "media": media_forca, "mais_forte": mais_forte}
    
    def jogar_carta(self, carta):
        if carta in self.cartas:
            self.cartas.remove(carta)
            return carta
        else:
            raise ValueError("Carta não está na mão")