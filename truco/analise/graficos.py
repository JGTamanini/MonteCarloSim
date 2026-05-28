import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo geral dos gráficos
sns.set_theme(style="whitegrid")

# =============================================
# Gráfico 1 — Taxa de vitória por confronto
# =============================================
def gerar_grafico_vitorias(arquivos_resultados, output_dir):
    """
    Recebe uma lista de caminhos para CSVs de resultados
    e gera um gráfico de barras com a taxa de vitória de cada agente.
    """
    dados = []
    for arquivo in arquivos_resultados:
        df = pd.read_csv(arquivo)
        confronto = os.path.basename(arquivo).replace("confronto_", "").replace("_resultados.csv", "")
        total = len(df)
        for agente, contagem in df['vencedor'].value_counts().items():
            dados.append({
                "confronto": confronto,
                "agente": agente,
                "taxa_vitoria": contagem / total * 100
            })

    df_plot = pd.DataFrame(dados)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_plot, x="confronto", y="taxa_vitoria", hue="agente", ax=ax)

    ax.set_title("Taxa de Vitória por Confronto", fontsize=14, fontweight="bold")
    ax.set_xlabel("Confronto")
    ax.set_ylabel("Taxa de Vitória (%)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha="right")
    ax.axhline(50, color="gray", linestyle="--", linewidth=0.8, label="50%")
    ax.legend(title="Agente")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_vitorias.png"), dpi=150)
    plt.close()
    print("✅ grafico_vitorias.png gerado")


# =============================================
# Gráfico 2 — Força da mão quando houve blefe
# =============================================
def gerar_grafico_blefe_vs_forca(arquivo_historico, nome_confronto, output_dir):
    """
    Scatter plot mostrando a força da mão do primeiro agente
    separado por se houve blefe ou não naquela mão.
    """
    df = pd.read_csv(arquivo_historico)

    # Pega a coluna de força do primeiro agente do confronto
    colunas_forca = [c for c in df.columns if c.startswith("forca_")]
    if not colunas_forca:
        print(f"⚠️ Nenhuma coluna de força encontrada em {arquivo_historico}")
        return

    agente1 = colunas_forca[0]  # ex: forca_Agressivo
    agente2 = colunas_forca[1]  # ex: forca_Conservador

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, coluna in zip(axes, [agente1, agente2]):
        nome_agente = coluna.replace("forca_", "")
        sns.boxplot(
            data=df,
            x="houve_blefe",
            y=coluna,
            ax=ax,
            palette=["#4CAF50", "#F44336"]
        )
        ax.set_title(f"{nome_agente} — Força da Mão vs Blefe", fontsize=12)
        ax.set_xlabel("Houve Blefe?")
        ax.set_ylabel("Força Média da Mão")
        ax.set_xticklabels(["Não", "Sim"])

    fig.suptitle(f"Força da Mão quando Houve Blefe\n{nome_confronto}", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"grafico_blefe_forca_{nome_confronto}.png"), dpi=150)
    plt.close()
    print(f"✅ grafico_blefe_forca_{nome_confronto}.png gerado")


# =============================================
# Gráfico 3 — Vitória com blefe vs sem blefe
# =============================================
def gerar_grafico_vitoria_com_blefe(arquivo_historico, nome_confronto, output_dir):
    """
    Barras mostrando a taxa de vitória nas mãos onde houve blefe
    versus mãos onde não houve blefe.
    """
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