from domino.src.conjunto import Conjunto
from domino.src.mesa import Mesa
from domino.src.mao import Mao


class Dupla:
    """Representa uma dupla de jogadores com pontuação compartilhada."""

    def __init__(self, jogador1, jogador2):
        self.jogadores = [jogador1, jogador2]
        self.pontos = 0

    @property
    def nome(self):
        return f"{self.jogadores[0].nome}/{self.jogadores[1].nome}"

    def contem(self, jogador):
        return jogador in self.jogadores

    def parceiro_de(self, jogador):
        return [j for j in self.jogadores if j != jogador][0]


class Partida:
    """
    Gerencia uma partida completa de dominó em duplas (2x2).

    Regras implementadas:
    - 4 jogadores divididos em 2 duplas; parceiros sentam em posições opostas.
      Ordem na mesa: J0(dupla A) → J1(dupla B) → J2(dupla A) → J3(dupla B) → ...
    - Cada jogador recebe 7 peças; nenhuma fica no dorme (7×4 = 28).
    - Começa quem tem o [6|6]; se ninguém tiver, quem tem o maior duplo, e assim por diante.
    - Jogadores passam se não puderem jogar.
    - Rodada termina por batida (alguém esvazia a mão) ou trancamento
      (todos os 4 passam consecutivamente).
    - Pontuação por rodada:
        Batida normal   → soma das peças dos dois adversários
        Batida de chapa → dobro da soma adversária (parceiro também ficou sem jogar na rodada)
        Trancado        → dupla com menor soma total nas duas mãos vence e ganha essa diferença
        Empate trancado → nenhuma dupla pontua
    - Partida: melhor de N rodadas ou primeira dupla a atingir PONTOS_VITORIA.
    """

    PONTOS_VITORIA = 100

    def __init__(self, dupla_a, dupla_b):
        """
        dupla_a, dupla_b : instâncias de Dupla
        A ordem na mesa é: dupla_a.jogadores[0], dupla_b.jogadores[0],
                           dupla_a.jogadores[1], dupla_b.jogadores[1]
        """
        self.duplas = [dupla_a, dupla_b]
        self.historico = []

        # Ordem de sentar: A0, B0, A1, B1
        self.ordem_mesa = [
            dupla_a.jogadores[0],
            dupla_b.jogadores[0],
            dupla_a.jogadores[1],
            dupla_b.jogadores[1],
        ]

    def _dupla_do(self, jogador):
        for d in self.duplas:
            if d.contem(jogador):
                return d
        raise ValueError(f"Jogador {jogador.nome} não pertence a nenhuma dupla.")

    def jogar(self):
        while max(d.pontos for d in self.duplas) < self.PONTOS_VITORIA:
            self._jogar_rodada()
        self.vencedor = max(self.duplas, key=lambda d: d.pontos)

    def _jogar_rodada(self):
        conjunto = Conjunto()
        distribuicao = conjunto.distribuir(4, pecas_por_jogador=7)
        maos = {j: Mao(distribuicao[i]) for i, j in enumerate(self.ordem_mesa)}
        mesa = Mesa()

        forca_inicial = {j.nome: maos[j].avaliar_forca()["media"] for j in self.ordem_mesa}

        # Quem começa: dono do maior duplo disponível
        primeiro = self._determinar_primeiro(maos)
        ordem = self._ordem_a_partir_de(primeiro)

        passes_consecutivos = 0
        rodada_encerrada = False
        vencedor_jogador = None
        motivo = "batida"

        # Rastreia se cada jogador jogou alguma peça nesta rodada (para chapa)
        jogou_na_rodada = {j: False for j in self.ordem_mesa}

        while not rodada_encerrada:
            for jogador in ordem:
                mao = maos[jogador]
                jogaveis = mesa.pecas_jogaveis(mao.pecas)

                if not jogaveis:
                    passes_consecutivos += 1
                    if passes_consecutivos >= 4:
                        motivo = "trancado"
                        rodada_encerrada = True
                        break
                    continue

                passes_consecutivos = 0
                parceiro = self._dupla_do(jogador).parceiro_de(jogador)
                peca, lado = jogador.escolher_peca(mao, mesa, parceiro=parceiro)
                mao.jogar_peca(peca)
                mesa.jogar(peca, lado)
                jogou_na_rodada[jogador] = True

                if mao.esta_vazia():
                    vencedor_jogador = jogador
                    rodada_encerrada = True
                    break

            if rodada_encerrada:
                break

        # --- Calcula pontuação ---
        dupla_vencedora = None
        pontos_ganhos = 0

        if motivo == "batida" and vencedor_jogador is not None:
            dupla_vencedora = self._dupla_do(vencedor_jogador)
            dupla_adversaria = [d for d in self.duplas if d != dupla_vencedora][0]

            soma_adversarios = sum(maos[j].total_pontos() for j in dupla_adversaria.jogadores)

            # Chapa: o parceiro também não jogou nenhuma peça nesta rodada
            parceiro = dupla_vencedora.parceiro_de(vencedor_jogador)
            eh_chapa = not jogou_na_rodada[parceiro]

            pontos_ganhos = soma_adversarios * (2 if eh_chapa else 1)

        elif motivo == "trancado":
            soma_duplas = {d: sum(maos[j].total_pontos() for j in d.jogadores) for d in self.duplas}
            soma_a, soma_b = soma_duplas[self.duplas[0]], soma_duplas[self.duplas[1]]
            if soma_a < soma_b:
                dupla_vencedora = self.duplas[0]
                pontos_ganhos = soma_b - soma_a
            elif soma_b < soma_a:
                dupla_vencedora = self.duplas[1]
                pontos_ganhos = soma_a - soma_b
            # empate: dupla_vencedora = None, pontos_ganhos = 0

        if dupla_vencedora is not None:
            dupla_vencedora.pontos += pontos_ganhos

        self.historico.append({
            "dupla_vencedora": dupla_vencedora.nome if dupla_vencedora else "empate",
            "motivo": motivo,
            "pontos_ganhos": pontos_ganhos,
            "pontos_atuais": {d.nome: d.pontos for d in self.duplas},
            "forca_dupla_a": sum(forca_inicial[j.nome] for j in self.duplas[0].jogadores) / 2,
            "forca_dupla_b": sum(forca_inicial[j.nome] for j in self.duplas[1].jogadores) / 2,
        })

    def _determinar_primeiro(self, maos):
        """Quem tem o maior duplo ([6|6] → [5|5] → ... → [0|0]) começa."""
        for valor in range(6, -1, -1):
            for jogador in self.ordem_mesa:
                from domino.src.peca import Peca
                duplo = Peca(valor, valor)
                if duplo in maos[jogador].pecas:
                    return jogador
        # Fallback: quem tem a peça mais pesada
        return max(self.ordem_mesa, key=lambda j: maos[j].peca_mais_pesada().total_pontos())

    def _ordem_a_partir_de(self, primeiro):
        idx = self.ordem_mesa.index(primeiro)
        return self.ordem_mesa[idx:] + self.ordem_mesa[:idx]