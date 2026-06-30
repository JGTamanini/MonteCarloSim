# from truco.src.constantes import RespostasTruco

# class Rodada:
#     def __init__(self, jogadores, maos):
#         self.jogadores = jogadores
#         self.cartas_jogadas = {}   # {jogador: carta}
#         self.valor_truco = 1       # começa valendo 1
#         self.truco_pedido = False
#         self.vencedor = None
#         self.maos = maos  # {jogador: mao}
#         self.houve_blefe = False
#         self.quem_pediu_truco = None

#     def determinar_vencedor(self):
#         self.vencedor = max(self.cartas_jogadas, key=lambda j: self.cartas_jogadas[j].get_forca())

#     def jogar_carta(self, jogador, carta):
#         if jogador not in self.jogadores:
#             raise ValueError("Jogador não pertence à rodada.")
#         if jogador in self.cartas_jogadas:
#             raise ValueError("Jogador já jogou sua carta.")

#         self.cartas_jogadas[jogador] = carta

#         if len(self.cartas_jogadas) == len(self.jogadores):
#             self.determinar_vencedor()

#     def pedir_truco(self, jogador):
#         if self.truco_pedido:
#             raise ValueError("Truco já foi pedido nesta rodada.")
#         if jogador not in self.jogadores:
#             raise ValueError("Jogador não pertence à rodada.")

#         pedinte = jogador
#         self.quem_pediu_truco = pedinte
#         if pedinte.foi_blefe(self.maos[pedinte]):
#             self.houve_blefe = True
#         adversario = [j for j in self.jogadores if j != pedinte][0]
#         self.truco_pedido = True
#         novo_valor = self.valor_truco + 2 if self.valor_truco == 1 else self.valor_truco + 3
#         adversario_decisao = adversario.responder_truco(self.maos[adversario], novo_valor)
#         if adversario_decisao == RespostasTruco.ACEITAR:
#             self.valor_truco = novo_valor
#         elif adversario_decisao == RespostasTruco.CORRER:
#             self.vencedor = pedinte
#         elif adversario_decisao == RespostasTruco.AUMENTAR:
#             self.valor_truco = novo_valor
#             self.truco_pedido = False
#             if novo_valor < 12:
#                 self.pedir_truco(adversario)


from truco.src.constantes import RespostasTruco


class Rodada:
    def __init__(self, jogadores, maos, vira):
        self.jogadores = jogadores
        self.maos = maos
        self.vira = vira
        self.cartas_jogadas = {}  # {jogador: carta}
        self.valor_truco = 1
        self.truco_pedido = False
        self.vencedor = None
        self.houve_blefe = False
        self.quem_pediu_truco = None

    def determinar_vencedor(self):
        self.vencedor = max(
            self.cartas_jogadas,
            key=lambda j: self.cartas_jogadas[j].get_forca(self.vira),
        )

    def jogar_carta(self, jogador, carta):
        if jogador not in self.jogadores:
            raise ValueError("Jogador não pertence à rodada.")
        if jogador in self.cartas_jogadas:
            raise ValueError("Jogador já jogou sua carta.")

        self.cartas_jogadas[jogador] = carta

        if len(self.cartas_jogadas) == len(self.jogadores):
            self.determinar_vencedor()

    def pedir_truco(self, jogador):
        if self.truco_pedido:
            raise ValueError("Truco já foi pedido nesta rodada.")
        if jogador not in self.jogadores:
            raise ValueError("Jogador não pertence à rodada.")

        self.quem_pediu_truco = jogador
        if jogador.foi_blefe(self.maos[jogador]):
            self.houve_blefe = True

        adversario = [j for j in self.jogadores if j != jogador][0]
        self.truco_pedido = True
        novo_valor = (
            self.valor_truco + 2 if self.valor_truco == 1 else self.valor_truco + 3
        )

        decisao = adversario.responder_truco(self.maos[adversario], novo_valor)

        if decisao == RespostasTruco.ACEITAR:
            self.valor_truco = novo_valor
        elif decisao == RespostasTruco.CORRER:
            self.vencedor = jogador
        elif decisao == RespostasTruco.AUMENTAR:
            self.valor_truco = novo_valor
            self.truco_pedido = False
            if novo_valor < 12:
                self.pedir_truco(adversario)
