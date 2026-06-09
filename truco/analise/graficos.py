import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

CORES_AGENTES = {
    "Aleatório":     "#1565C0",
    "Conservador":   "#2E7D32",
    "Agressivo":     "#C62828",
    "Probabilístico":"#00695C",
}

# =============================================
# Gráfico 1 — Barras horizontais empilhadas
# =============================================
def gerar_grafico_vitorias(arquivos_resultados, output_dir):
    dados = []
    for arquivo in arquivos_resultados:
        df = pd.read_csv(arquivo)
        confronto = os.path.basename(arquivo).replace("confronto_", "").replace("_resultados.csv", "")
        label = confronto.replace("_vs_", " vs ")
        total = len(df)
        vitorias = df['vencedor'].value_counts()
        for agente, contagem in vitorias.items():
            dados.append({
                "confronto": label,
                "agente": agente,
                "taxa": contagem / total * 100
            })

    df_plot = pd.DataFrame(dados)
    confrontos = df_plot["confronto"].unique()

    fig, ax = plt.subplots(figsize=(12, 7))

    for i, confronto in enumerate(confrontos):
        subset = df_plot[df_plot["confronto"] == confronto].sort_values("taxa", ascending=False)
        left = 0
        for _, row in subset.iterrows():
            cor = CORES_AGENTES.get(row["agente"], "#CCCCCC")
            ax.barh(i, row["taxa"], left=left, color=cor, edgecolor="white", linewidth=0.8, height=0.6)
            if row["taxa"] >= 8:
                ax.text(left + row["taxa"] / 2, i, f"{row['taxa']:.0f}%",
                        ha="center", va="center", fontsize=11, fontweight="bold", color="white")
            left += row["taxa"]

    ax.axvline(50, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_yticks(list(range(len(confrontos))))
    ax.set_yticklabels(confrontos, fontsize=11)
    ax.set_xlabel("Taxa de vitória (%)", fontsize=11)
    ax.set_xlim(0, 100)
    ax.set_title("Quem vence mais?\nTaxa de vitória por confronto — 1.000 partidas cada",
                 fontsize=13, fontweight="bold")

    legendas = [mpatches.Patch(color=cor, label=agente)
                for agente, cor in CORES_AGENTES.items()]
    ax.legend(handles=legendas, loc="upper center", bbox_to_anchor=(0.5, -0.08),
          ncol=4, fontsize=10, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_vitorias.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("✅ grafico_vitorias.png gerado")


# =============================================
# Gráfico 2 — Distribuição de duração
# =============================================
def gerar_grafico_duracao(arquivos_historico, output_dir):
    dados = []
    for arquivo in arquivos_historico:
        df = pd.read_csv(arquivo)
        confronto = os.path.basename(arquivo).replace("confronto_", "").replace("_historico.csv", "")
        duracao = df.groupby("partida")["mao"].max().reset_index()
        duracao.columns = ["partida", "num_maos"]
        duracao["confronto"] = confronto.replace("_vs_", " vs ")
        dados.append(duracao)

    df_all = pd.concat(dados, ignore_index=True)
    confrontos = df_all["confronto"].unique()
    n = len(confrontos)
    cols = 3
    rows = (n + cols - 1) // cols

    cores = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]
    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4.5))
    axes = axes.flatten()

    for idx, (confronto, cor) in enumerate(zip(confrontos, cores)):
        ax = axes[idx]
        subset = df_all[df_all["confronto"] == confronto]["num_maos"]
        media = subset.mean()
        mediana = subset.median()

        ax.hist(subset, bins=range(int(subset.min()), int(subset.max()) + 2),
                color=cor, alpha=0.7, edgecolor="white", linewidth=0.5)
        ax.axvline(media, color="black", linestyle="--", linewidth=1.5,
                   label=f"Média: {media:.1f}")
        ax.axvline(mediana, color="gray", linestyle=":", linewidth=1.5,
                   label=f"Mediana: {mediana:.1f}")

        ax.set_title(confronto, fontsize=11, fontweight="bold")
        ax.set_xlabel("Número de Mãos por Partida", fontsize=10)
        ax.set_ylabel("Frequência", fontsize=10)
        ax.legend(fontsize=9)

    for idx in range(len(confrontos), len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle("Distribuição de Duração das Partidas\nMenos mãos = estratégia mais eficiente",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_duracao_partidas.png"), dpi=150)
    plt.close()
    print("✅ grafico_duracao_partidas.png gerado")


# =============================================
# Gráfico 3 — Força da mão vs blefe (boxplot)
# =============================================
def gerar_grafico_blefe_vs_forca(arquivo_historico, nome_confronto, output_dir):
    df = pd.read_csv(arquivo_historico)
    colunas_forca = [c for c in df.columns if c.startswith("forca_")]
    if not colunas_forca:
        print(f"⚠️ Nenhuma coluna de força encontrada em {arquivo_historico}")
        return

    for coluna in colunas_forca[:2]:
        nome_agente = coluna.replace("forca_", "")

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.boxplot(data=df, x="houve_blefe", y=coluna, ax=ax,
                    palette=["#4CAF50", "#F44336"])
        ax.set_title(f"{nome_agente} — Força da Mão vs Blefe\n{nome_confronto}", fontsize=12)
        ax.set_xlabel("Houve Blefe?")
        ax.set_ylabel("Força Média da Mão")
        ax.set_xticklabels(["Não", "Sim"])

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"grafico_blefe_forca_{nome_confronto}_{nome_agente}.png"), dpi=150)
        plt.close()
        print(f"✅ grafico_blefe_forca_{nome_confronto}_{nome_agente}.png gerado")

# =============================================
# Gráfico 4 — Taxa de vitória com blefe vs sem blefe
# =============================================
def gerar_grafico_vitoria_com_blefe(arquivo_historico, nome_confronto, output_dir):
    df = pd.read_csv(arquivo_historico)
    agentes = df['vencedor_mao'].unique()
    dados = []

    for agente in agentes:
        for houve_blefe in [True, False]:
            subset = df[df['houve_blefe'] == houve_blefe]
            if len(subset) == 0:
                continue
            taxa = (subset['vencedor_mao'] == agente).sum() / len(subset) * 100
            dados.append({
                "agente": agente,
                "houve_blefe": "Com Blefe" if houve_blefe else "Sem Blefe",
                "taxa_vitoria": taxa
            })

    df_plot = pd.DataFrame(dados)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_plot, x="agente", y="taxa_vitoria", hue="houve_blefe", ax=ax,
                palette=["#F44336", "#2196F3"])

    ax.set_title(f"Taxa de Vitória — Com Blefe vs Sem Blefe\n{nome_confronto}",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Agente")
    ax.set_ylabel("Taxa de Vitória nas Mãos (%)")
    ax.axhline(50, color="gray", linestyle="--", linewidth=0.8)
    ax.legend(title="Situação")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"grafico_vitoria_blefe_{nome_confronto}.png"), dpi=150)
    plt.close()
    print(f"✅ grafico_vitoria_blefe_{nome_confronto}.png gerado")