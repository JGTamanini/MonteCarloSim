from truco.src.rodada import Rodada
from truco.src.baralho import Baralho
from truco.src.mao import Mao

class Partida:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.baralho = Baralho()
        self.rodadas = []
        self.pontos = {j: 0 for j in jogadores}
        self.historico = []
    
    def jogar(self):
        while max(self.pontos.values()) < 12:
            self._jogar_mao()
        self.vencedor = max(self.pontos, key=lambda j: self.pontos[j])

    def _jogar_mao(self):
        distribuicao = self.baralho.distribuir(len(self.jogadores), 3)
        maos = {j: Mao(distribuicao[i]) for i, j in enumerate(self.jogadores)}

        forca_inicial = {j.nome: maos[j].avaliar_forca()["media"] for j in self.jogadores}
        
        vitorias = {j: 0 for j in self.jogadores}
        valor_mao = 1
        
        rodadas_da_mao = []
        for _ in range(3):
            rodada = Rodada(self.jogadores, maos)
            rodadas_da_mao.append(rodada)
            self.rodadas.append(rodada)
            
            for jogador in self.jogadores:
                if jogador.decidir_truco(maos[jogador]):
                    rodada.pedir_truco(jogador)
                    break

            for jogador in self.jogadores:
                carta = jogador.escolher_carta(maos[jogador])
                rodada.jogar_carta(jogador, carta)

            if rodada.vencedor:
                vitorias[rodada.vencedor] += 1
                valor_mao = rodada.valor_truco

            if max(vitorias.values()) >= 2:
                break

        vencedor_mao = max(vitorias, key=lambda j: vitorias[j])
        self.historico.append({
            "vencedor_mao": vencedor_mao.nome,
            "pontos_atuais": {j.nome: self.pontos[j] for j in self.jogadores},
            "houve_blefe": any(r.houve_blefe for r in rodadas_da_mao),
            "valor_truco": valor_mao,
            f"forca_{self.jogadores[0].nome}": forca_inicial[self.jogadores[0].nome],
            f"forca_{self.jogadores[1].nome}": forca_inicial[self.jogadores[1].nome],
        })
        self.pontos[vencedor_mao] += valor_mao