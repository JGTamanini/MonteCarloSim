import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analise.graficos import (
    gerar_grafico_vitorias,
    gerar_grafico_blefe_vs_forca,
    gerar_grafico_vitoria_com_blefe
)

DATA_DIR = os.path.join(BASE_DIR, "data", "truco")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "truco", "graficos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

confrontos = [
    "Conservador_vs_Aleatório",
    "Agressivo_vs_Aleatório",
    "Conservador_vs_Agressivo",
    "Probabilístico_vs_Agressivo",
]

# Gráfico 1 — todos os confrontos juntos
arquivos_resultados = [f"{DATA_DIR}/confronto_{c}_resultados.csv" for c in confrontos]
gerar_grafico_vitorias(arquivos_resultados, OUTPUT_DIR)

# Gráficos 2 e 3 — por confronto
for confronto in confrontos:
    arquivo_historico = f"{DATA_DIR}/confronto_{confronto}_historico.csv"
    gerar_grafico_blefe_vs_forca(arquivo_historico, confronto, OUTPUT_DIR)
    gerar_grafico_vitoria_com_blefe(arquivo_historico, confronto, OUTPUT_DIR)