import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from domino.src.partida import Partida, Dupla


def rodar_simulacao(n_partidas, dupla_a, dupla_b, nome_confronto=None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data", "domino")

    resultados = []
    historico_completo = []

    for i in range(n_partidas):
        da = Dupla(dupla_a[0], dupla_a[1])
        db = Dupla(dupla_b[0], dupla_b[1])
        partida = Partida(da, db)
        partida.jogar()

        resultados.append({
            "partida": i + 1,
            "dupla_vencedora": partida.vencedor.nome,
            "pontos_dupla_a": da.pontos,
            "pontos_dupla_b": db.pontos,
        })

        for j, rodada in enumerate(partida.historico):
            historico_completo.append({
                "partida": i + 1,
                "rodada": j + 1,
                "dupla_vencedora": rodada["dupla_vencedora"],
                "motivo": rodada["motivo"],
                "pontos_ganhos": rodada["pontos_ganhos"],
                "forca_dupla_a": rodada["forca_dupla_a"],
                "forca_dupla_b": rodada["forca_dupla_b"],
            })

    if nome_confronto is None:
        nome_confronto = f"{dupla_a[0].nome}+{dupla_a[1].nome}_vs_{dupla_b[0].nome}+{dupla_b[1].nome}"

    df          = pd.DataFrame(resultados)
    df_historico = pd.DataFrame(historico_completo)
    df.to_csv(os.path.join(DATA_DIR, f"confronto_{nome_confronto}_resultados.csv"), index=False)
    df_historico.to_csv(os.path.join(DATA_DIR, f"confronto_{nome_confronto}_historico.csv"), index=False)

    return resultados, historico_completo


if __name__ == "__main__":
    from domino.src.agentes.aleatorio import AgenteAleatorio
    from domino.src.agentes.defensivo import AgenteDefensivo
    from domino.src.agentes.ofensivo import AgenteOfensivo
    from domino.src.agentes.probabilistico import AgenteProbabilistico

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

    for dupla_a, dupla_b, nome in confrontos:
        print(f"\nSimulando: {nome}")
        rodar_simulacao(1000, dupla_a, dupla_b, nome_confronto=nome)
        print("Concluído!")