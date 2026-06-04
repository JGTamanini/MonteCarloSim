import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from domino.src.partida import Partida, Dupla
from domino.src.agentes.aleatorio import AgenteAleatorio
from domino.src.agentes.defensivo import AgenteDefensivo
from domino.src.agentes.ofensivo import AgenteOfensivo
from domino.src.agentes.probabilistico import AgenteProbabilistico


def rodar_simulacao(n_partidas, dupla_a, dupla_b, nome_confronto):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data", "domino")

    resultados = []
    for i in range(n_partidas):
        da = Dupla(dupla_a[0], dupla_a[1])
        db = Dupla(dupla_b[0], dupla_b[1])
        partida = Partida(da, db)
        partida.jogar()
        resultados.append({"partida": i + 1, "dupla_vencedora": partida.vencedor.nome})

    df = pd.DataFrame(resultados)
    path = os.path.join(DATA_DIR, f"convergencia_{nome_confronto}_{n_partidas}.csv")
    df.to_csv(path, index=False)
    print(f"  ✅ {n_partidas:,} partidas salvas")
    return df


if __name__ == "__main__":
    confrontos = [
        ([AgenteOfensivo("Ofe1"),        AgenteOfensivo("Ofe2")],
         [AgenteDefensivo("Def1"),       AgenteDefensivo("Def2")],
         "Ofensivo_vs_Defensivo"),
        ([AgenteOfensivo("Ofe1"),        AgenteOfensivo("Ofe2")],
         [AgenteProbabilistico("Prob1"), AgenteProbabilistico("Prob2")],
         "Ofensivo_vs_Probabilistico"),
        ([AgenteOfensivo("Ofe1"),        AgenteOfensivo("Ofe2")],
         [AgenteAleatorio("Ale1"),       AgenteAleatorio("Ale2")],
         "Ofensivo_vs_Aleatorio"),
        ([AgenteDefensivo("Def1"),       AgenteDefensivo("Def2")],
         [AgenteProbabilistico("Prob1"), AgenteProbabilistico("Prob2")],
         "Defensivo_vs_Probabilistico"),
        ([AgenteDefensivo("Def1"),       AgenteDefensivo("Def2")],
         [AgenteAleatorio("Ale1"),       AgenteAleatorio("Ale2")],
         "Defensivo_vs_Aleatorio"),
        ([AgenteProbabilistico("Prob1"), AgenteProbabilistico("Prob2")],
         [AgenteAleatorio("Ale1"),       AgenteAleatorio("Ale2")],
         "Probabilistico_vs_Aleatorio"),
    ]

    for n in [10_000, 100_000]:
        print(f"\n{'='*50}")
        print(f"Rodando {n:,} partidas por confronto...")
        print(f"{'='*50}")
        for dupla_a, dupla_b, nome in confrontos:
            print(f"\n{nome}")
            rodar_simulacao(n, dupla_a, dupla_b, nome)

    print("\nConcluído!")