import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analise.graficos import (
    gerar_grafico_vitorias,
    gerar_grafico_forca_vs_motivo,
    gerar_grafico_pontos_por_rodada,
    gerar_grafico_trancamentos,
)

DATA_DIR   = os.path.join(BASE_DIR, "data", "domino")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "domino", "graficos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

confrontos = [
    "Defensivo_vs_Aleatorio",
    "Ofensivo_vs_Aleatorio",
    "Defensivo_vs_Ofensivo",
    "Probabilistico_vs_Ofensivo",
]

arquivos_resultados  = [f"{DATA_DIR}/confronto_{c}_resultados.csv"  for c in confrontos]
arquivos_historico   = [f"{DATA_DIR}/confronto_{c}_historico.csv"   for c in confrontos]

gerar_grafico_vitorias(arquivos_resultados, OUTPUT_DIR)
gerar_grafico_trancamentos(arquivos_historico, confrontos, OUTPUT_DIR)

for confronto, hist in zip(confrontos, arquivos_historico):
    gerar_grafico_forca_vs_motivo(hist, confronto, OUTPUT_DIR)
    gerar_grafico_pontos_por_rodada(hist, confronto, OUTPUT_DIR)