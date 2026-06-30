# from truco.src.carta import Carta

# class Mao:
#     def __init__(self, cartas):
#         self.cartas = cartas
    
#     def avaliar_forca(self):
#         soma_forca = 0
#         media_forca = 0
#         mais_forte = float('-inf')
#         for carta in self.cartas:
#             forca = carta.get_forca()
#             soma_forca += forca
#             if forca > mais_forte:
#                 mais_forte = forca
#         media_forca = soma_forca / len(self.cartas) if self.cartas else 0
#         return {"soma": soma_forca, "media": media_forca, "mais_forte": mais_forte}
    
#     def jogar_carta(self, carta):
#         if carta in self.cartas:
#             self.cartas.remove(carta)
#             return carta
#         else:
#             raise ValueError("Carta não está na mão")


from truco.src.carta import Carta


class Mao:
    def __init__(self, cartas, vira):
        self.cartas = list(cartas)
        self.vira = vira

    def avaliar_forca(self):
        if not self.cartas:
            return {"soma": 0, "media": 0, "mais_forte": 0}
        soma = sum(c.get_forca(self.vira) for c in self.cartas)
        mais_forte = max(c.get_forca(self.vira) for c in self.cartas)
        return {
            "soma": soma,
            "media": soma / len(self.cartas),
            "mais_forte": mais_forte,
        }

    def jogar_carta(self, carta):
        if carta in self.cartas:
            self.cartas.remove(carta)
            return carta
        raise ValueError(f"Carta {carta} não está na mão.")

    def __len__(self):
        return len(self.cartas)