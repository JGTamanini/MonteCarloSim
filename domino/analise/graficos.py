import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


# =============================================
# Gráfico 1 — Taxa de vitória por confronto
# =============================================
def gerar_grafico_vitorias(arquivos_resultados, output_dir):
    dados = []
    for arquivo in arquivos_resultados:
        if not os.path.exists(arquivo):
            print(f"⚠️  Arquivo não encontrado: {arquivo}")
            continue
        df = pd.read_csv(arquivo)
        confronto = os.path.basename(arquivo).replace("confronto_", "").replace("_resultados.csv", "")
        total = len(df)
        for dupla, contagem in df["dupla_vencedora"].value_counts().items():
            dados.append({
                "confronto": confronto,
                "dupla": dupla,
                "taxa_vitoria": contagem / total * 100,
            })

    if not dados:
        print("⚠️  Nenhum dado disponível para gráfico de vitórias.")
        return

    df_plot = pd.DataFrame(dados)
    fig, ax = plt.subplots(figsize=(13, 6))
    sns.barplot(data=df_plot, x="confronto", y="taxa_vitoria", hue="dupla", ax=ax)
    ax.set_title("Taxa de Vitória por Confronto — Dominó em Duplas", fontsize=14, fontweight="bold")
    ax.set_xlabel("Confronto")
    ax.set_ylabel("Taxa de Vitória (%)")
    ax.tick_params(axis="x", rotation=15)
    ax.axhline(50, color="gray", linestyle="--", linewidth=0.8)
    ax.legend(title="Dupla", bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_vitorias.png"), dpi=150)
    plt.close()
    print("✅ grafico_vitorias.png gerado")


# =============================================
# Gráfico 2 — Força média da dupla vs motivo
# =============================================
def gerar_grafico_forca_vs_motivo(arquivo_historico, nome_confronto, output_dir):
    if not os.path.exists(arquivo_historico):
        print(f"⚠️  Arquivo não encontrado: {arquivo_historico}")
        return

    df = pd.read_csv(arquivo_historico)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, col, titulo in zip(
        axes,
        ["forca_dupla_a", "forca_dupla_b"],
        ["Dupla A", "Dupla B"],
    ):
        sns.boxplot(
            data=df, x="motivo", y=col, ax=ax,
            hue="motivo",
            palette={"batida": "#4CAF50", "trancado": "#F44336"},
            legend=False,
        )
        ax.set_title(f"{titulo} — Força da Mão vs Motivo", fontsize=12)
        ax.set_xlabel("Motivo de Encerramento")
        ax.set_ylabel("Força Média da Mão Inicial")

    fig.suptitle(f"Força da Mão × Motivo de Encerramento\n{nome_confronto}",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(output_dir, f"grafico_forca_motivo_{nome_confronto}.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"✅ grafico_forca_motivo_{nome_confronto}.png gerado")


# =============================================
# Gráfico 3 — Distribuição de pontos por rodada
# =============================================
def gerar_grafico_pontos_por_rodada(arquivo_historico, nome_confronto, output_dir):
    if not os.path.exists(arquivo_historico):
        print(f"⚠️  Arquivo não encontrado: {arquivo_historico}")
        return

    df = pd.read_csv(arquivo_historico)
    df = df[df["dupla_vencedora"] != "empate"]

    fig, ax = plt.subplots(figsize=(10, 6))
    for dupla in df["dupla_vencedora"].unique():
        subset = df[df["dupla_vencedora"] == dupla]["pontos_ganhos"]
        sns.histplot(subset, label=dupla, ax=ax, kde=True, bins=20, alpha=0.6)

    ax.set_title(f"Distribuição de Pontos Ganhos por Rodada\n{nome_confronto}",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Pontos Ganhos na Rodada")
    ax.set_ylabel("Frequência")
    ax.legend(title="Dupla Vencedora")
    plt.tight_layout()
    path = os.path.join(output_dir, f"grafico_pontos_rodada_{nome_confronto}.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"✅ grafico_pontos_rodada_{nome_confronto}.png gerado")


# =============================================
# Gráfico 4 — Taxa de trancamento por confronto
# =============================================
def gerar_grafico_trancamentos(arquivos_historico, nomes_confronto, output_dir):
    dados = []
    for arquivo, nome in zip(arquivos_historico, nomes_confronto):
        if not os.path.exists(arquivo):
            continue
        df = pd.read_csv(arquivo)
        total = len(df)
        trancados = (df["motivo"] == "trancado").sum()
        dados.append({
            "confronto": nome,
            "taxa_trancamento": trancados / total * 100,
        })

    if not dados:
        return

    df_plot = pd.DataFrame(dados)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_plot, x="confronto", y="taxa_trancamento", ax=ax,
                palette="Reds_d", hue="confronto", legend=False)
    ax.set_title("Taxa de Trancamento por Confronto", fontsize=14, fontweight="bold")
    ax.set_xlabel("Confronto")
    ax.set_ylabel("% de Rodadas Trancadas")
    ax.tick_params(axis="x", rotation=15)
    plt.tight_layout()
    path = os.path.join(output_dir, "grafico_trancamentos.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print("✅ grafico_trancamentos.png gerado")