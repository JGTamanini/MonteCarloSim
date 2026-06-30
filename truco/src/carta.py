# from truco.src.constantes import HIERARQUIA, MANILHAS, NAIPES

# class Carta:
#     def __init__(self, valor, naipe):
#         self.valor = valor
#         self.naipe = naipe
    
#     def __eq__(self, outra):
#         return self.valor == outra.valor and self.naipe == outra.naipe
    
#     def is_manilha(self):
#         return (self.valor, self.naipe) in MANILHAS
    
#     def get_forca(self):
#         if self.is_manilha():
#             return MANILHAS[(self.valor, self.naipe)]
#         return HIERARQUIA[self.valor]
        
#     def power_compare(self, outra_carta):
#         card1 = self.is_manilha()
#         card2 = outra_carta.is_manilha()
#         forca_self = MANILHAS.get((self.valor, self.naipe))
#         forca_outra = MANILHAS.get((outra_carta.valor, outra_carta.naipe))
#         if card1 and card2:
#             return (forca_self > forca_outra) - (forca_self < forca_outra)
#         elif card1 and not card2:
#             return 1
#         elif not card1 and card2:
#             return -1
#         else:
#             forca_valores = (HIERARQUIA[self.valor] > HIERARQUIA[outra_carta.valor]) - \
#                             (HIERARQUIA[self.valor] < HIERARQUIA[outra_carta.valor])
            
#             if forca_valores != 0:
#                 return forca_valores
            
#             return (NAIPES[self.naipe] > NAIPES[outra_carta.naipe]) - \
#                 (NAIPES[self.naipe] < NAIPES[outra_carta.naipe])
        
#     def __str__(self):
#         return f"{self.valor} de {self.naipe}"











from truco.src.constantes import HIERARQUIA, NAIPES, get_valor_manilha


class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __eq__(self, outra):
        return self.valor == outra.valor and self.naipe == outra.naipe

    def is_manilha(self, vira):
        """Verifica se esta carta é manilha dado a vira."""
        return self.valor == get_valor_manilha(vira)

    def get_forca(self, vira):
        """
        Retorna a força da carta considerando a vira.
        Manilhas valem 11+ conforme a força do naipe (ouros=11, copas=12, espadas=13, paus=14).
        Cartas normais valem conforme HIERARQUIA.
        """
        if self.is_manilha(vira):
            return 10 + NAIPES[self.naipe]  # 11 a 14
        return HIERARQUIA[self.valor]

    def power_compare(self, outra_carta, vira):
        """Compara esta carta com outra, retornando 1, -1 ou 0."""
        return (self.get_forca(vira) > outra_carta.get_forca(vira)) - \
               (self.get_forca(vira) < outra_carta.get_forca(vira))

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

    def __repr__(self):
        return self.__str__()