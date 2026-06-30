import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Any, Dict

sns.set_theme(style="whitegrid")


def gerar_heatmap_confrontos(matriz: Dict[str, Dict[str, float]], output_dir: str):
    """Gera um heatmap de correlação de taxas de vitória entre os agentes."""
    agentes = list(matriz.keys())
    df = pd.DataFrame(matriz)

    # Garante a ordem correta
    df = df.reindex(index=agentes, columns=agentes)

    # Preenche a diagonal com 50% (auto-confronto simulado)
    for i in range(len(agentes)):
        df.iloc[i, i] = 50.0

    plt.figure(figsize=(12, 10))
    # Paleta divergente (azul para perda < 50, vermelho/laranja para vitória > 50)
    sns.heatmap(
        df,
        annot=True,
        fmt=".1f",
        cmap="coolwarm",
        vmin=0,
        vmax=100,
        center=50,
        cbar_kws={'label': 'Taxa de Vitória (%)'},
        linewidths=0.5
    )

    plt.title("Matriz de Taxa de Vitória (%) entre Estratégias", fontsize=14, fontweight="bold", pad=20)
    plt.xlabel("Oponente", fontsize=12)
    plt.ylabel("Agente", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "torneio_matriz_confrontos.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"[Grafico] Heatmap salvo em: {filepath}")


def gerar_grafico_ranking(ranking: list, output_dir: str):
    """Gera um gráfico de barras horizontal com a classificação do campeonato."""
    agentes, pontos = zip(*ranking)

    plt.figure(figsize=(10, 6))
    cores = sns.color_palette("viridis", len(agentes))

    bars = plt.barh(agentes[::-1], pontos[::-1], color=cores[::-1], edgecolor="black", height=0.6)

    # Adiciona rótulos com a pontuação
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)} pts",
            ha='left',
            va='center',
            fontsize=11,
            fontweight='bold'
        )

    plt.title("Classificação Geral do Torneio (Pontos Acumulados)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Pontuação", fontsize=12)
    plt.ylabel("Agente / Estratégia", fontsize=12)
    plt.xlim(0, max(pontos) + 3)
    plt.tight_layout()

    filepath = os.path.join(output_dir, "torneio_classificacao.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"[Grafico] Grafico de ranking salvo em: {filepath}")


def gerar_grafico_tempo_resposta(stats: Dict[str, Dict[str, Any]], output_dir: str):
    """Compara o tempo médio de resposta de cada estratégia em ms."""
    agentes = list(stats.keys())
    tempos = [stats[a]["tempo_medio_ms"] for a in agentes]

    # Ordena para exibição
    agentes_ordenados, tempos_ordenados = zip(*sorted(zip(agentes, tempos), key=lambda x: x[1]))

    plt.figure(figsize=(10, 6))
    bars = plt.bar(agentes_ordenados, tempos_ordenados, color="#008080", edgecolor="black", width=0.5)

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            yval + 0.05,
            f"{yval:.2f} ms",
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )

    plt.title("Tempo Médio de Resposta por Decisão", fontsize=14, fontweight="bold", pad=15)
    plt.ylabel("Tempo (ms)", fontsize=12)
    plt.xlabel("Agente / Estratégia", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, max(tempos) * 1.15 if tempos else 10.0)
    plt.tight_layout()

    filepath = os.path.join(output_dir, "torneio_tempo_resposta.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"[Grafico] Grafico de tempos de resposta salvo em: {filepath}")


def gerar_grafico_blefes(stats: Dict[str, Dict[str, Any]], output_dir: str):
    """Compara tentativas de blefe com blefes bem-sucedidos por agente."""
    agentes = []
    tentados = []
    sucedidos = []

    for ag, val in stats.items():
        if val["blefes_tentados"] > 0:
            agentes.append(ag)
            tentados.append(val["blefes_tentados"])
            sucedidos.append(val["blefes_sucedidos"])

    if not agentes:
        print("[Aviso] Nenhum blefe registrado. Pulando grafico de blefes.")
        return

    x = np.arange(len(agentes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, tentados, width, label='Blefes Tentados', color='#F44336', edgecolor='black')
    rects2 = ax.bar(x + width/2, sucedidos, width, label='Blefes Sucedidos', color='#4CAF50', edgecolor='black')

    ax.set_ylabel('Quantidade de Blefes', fontsize=12)
    ax.set_title('Tentativas vs. Sucesso de Blefes por Estratégia', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(agentes, rotation=45, ha='right')
    ax.legend()

    # Adiciona a porcentagem de sucesso no topo de cada par de barras
    for i in range(len(agentes)):
        tent = tentados[i]
        suc = sucedidos[i]
        taxa = (suc / tent * 100) if tent > 0 else 0.0
        max_h = max(tent, suc)
        ax.text(i, max_h + 1, f"{taxa:.0f}% suc", ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    filepath = os.path.join(output_dir, "torneio_analise_blefes.png")
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"[Grafico] Grafico de blefes salvo em: {filepath}")
