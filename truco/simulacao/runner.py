import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
from truco.src.partida import Partida

def rodar_simulacao(n_partidas, jogadores, nome_confronto=None):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data", "truco")

    resultados = []
    historico_completo = []
    
    for i in range(n_partidas):
        partida = Partida(jogadores)
        partida.jogar()
        
        resultados.append({
            "partida": i + 1,
            "vencedor": partida.vencedor.nome,
            "pontos": {j.nome: p for j, p in partida.pontos.items()}
        })
        
        for j, mao in enumerate(partida.historico):
            historico_completo.append({
                "partida": i + 1,
                "mao": j + 1,
                "vencedor_mao": mao["vencedor_mao"],
                "pontos_atuais": mao["pontos_atuais"],
                "houve_blefe": mao["houve_blefe"],
                "valor_truco": mao["valor_truco"],
                f"forca_{jogadores[0].nome}": mao.get(f"forca_{jogadores[0].nome}"),
                f"forca_{jogadores[1].nome}": mao.get(f"forca_{jogadores[1].nome}"),
            })
    
    if nome_confronto is None:
        nome_confronto = f"{jogadores[0].nome}_vs_{jogadores[1].nome}"
    
    df = pd.DataFrame(resultados)
    df_historico = pd.DataFrame(historico_completo)
    df.to_csv(os.path.join(DATA_DIR, f"confronto_{nome_confronto}_resultados.csv"), index=False)
    df_historico.to_csv(os.path.join(DATA_DIR, f"confronto_{nome_confronto}_historico.csv"), index=False)
    return resultados, historico_completo

if __name__ == "__main__":
    from truco.src.baralho import Baralho
    from truco.src.agentes.aleatorio import AgenteAleatorio
    from truco.src.agentes.conservador import AgenteConservador
    from truco.src.agentes.agressivo import AgenteAgressivo
    from truco.src.agentes.probabilistico import AgenteProbabilistico

    baralho = Baralho()

    confrontos = [
        [AgenteConservador("Conservador"), AgenteAleatorio("Aleatório")],
        [AgenteAgressivo("Agressivo"), AgenteAleatorio("Aleatório")],
        [AgenteConservador("Conservador"), AgenteAgressivo("Agressivo")],
        [AgenteProbabilistico("Probabilístico", baralho), AgenteAgressivo("Agressivo")],
        [AgenteProbabilistico("Probabilístico", baralho), AgenteConservador("Conservador")],
        [AgenteProbabilistico("Probabilístico", baralho), AgenteAleatorio("Aleatório")],
    ]

    for confronto in confrontos:
        nome = f"{confronto[0].nome}_vs_{confronto[1].nome}"
        print(f"\nSimulando: {nome}")
        rodar_simulacao(1000, confronto, nome_confronto=nome)
        print("Concluído!")