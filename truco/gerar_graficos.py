import os
import sys

# Garante que o diretório raiz esteja no path para corretos imports do módulo truco
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from truco.src.simulation.tournament import TournamentManager
from truco.src.analysis.plots import (
    gerar_heatmap_confrontos,
    gerar_grafico_ranking,
    gerar_grafico_tempo_resposta,
    gerar_grafico_blefes,
)
from truco.src.analysis.reports import gerar_relatorio_markdown

# Configuração de caminhos de saída
DATA_DIR = os.path.join(BASE_DIR, "data", "truco")
GRAFICOS_DIR = os.path.join(DATA_DIR, "graficos")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

os.makedirs(GRAFICOS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def main():
    print("======================================================================")
    print("      SIMULADOR MULTIAGENTES — CAMPEONATO DE TRUCO PAULISTA           ")
    print("======================================================================\n")

    # Quantidade de partidas por confronto (100 a 500 partidas para robustez estatística rápida)
    n_partidas = 200
    print(f"-> Executando campeonato round-robin ({n_partidas} partidas por confronto)...")

    manager = TournamentManager()
    resumo = manager.rodar_campeonato(n_partidas_confronto=n_partidas)

    print("\n================ Tabela de Classificação Final ================")
    for idx, (nome, pontos) in enumerate(resumo["ranking"]):
        print(f" {idx + 1}º | {nome:<16} | {pontos} pontos")
    print("===============================================================\n")

    print("-> Gerando gráficos analíticos...")
    gerar_heatmap_confrontos(resumo["matriz_confrontos"], GRAFICOS_DIR)
    gerar_grafico_ranking(resumo["ranking"], GRAFICOS_DIR)
    gerar_grafico_tempo_resposta(resumo["estatisticas_finais"], GRAFICOS_DIR)
    gerar_grafico_blefes(resumo["estatisticas_finais"], GRAFICOS_DIR)

    print("\n-> Compilando relatório em formato Markdown...")
    gerar_relatorio_markdown(resumo, n_partidas, REPORTS_DIR)

    print("\n[Sucesso] Processo concluido com sucesso!")
    print(f"[Info] Graficos salvos na pasta: {os.path.abspath(GRAFICOS_DIR)}")
    print(f"[Info] Relatorio gerado em: {os.path.abspath(os.path.join(REPORTS_DIR, 'torneio_report.md'))}")


if __name__ == "__main__":
    main()