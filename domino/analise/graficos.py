# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import seaborn as sns
# import warnings
# warnings.filterwarnings("ignore")

# sns.set_theme(style="whitegrid")

# CORES = {
#     "Aleatório":      "#A8C5DA",
#     "Aleatorio":      "#A8C5DA",
#     "Defensivo":      "#F4A261",
#     "Ofensivo":       "#E63946",
#     "Probabilístico": "#2A9D8F",
#     "Probabilistico": "#2A9D8F",
# }

# NOMES_DUPLA = {
#     "Ofensivo_vs_Defensivo":      ("Ofensivo",       "Defensivo"),
#     "Ofensivo_vs_Probabilistico": ("Ofensivo",       "Probabilístico"),
#     "Ofensivo_vs_Aleatorio":      ("Ofensivo",       "Aleatório"),
#     "Defensivo_vs_Probabilistico":("Defensivo",      "Probabilístico"),
#     "Defensivo_vs_Aleatorio":     ("Defensivo",      "Aleatório"),
#     "Probabilistico_vs_Aleatorio":("Probabilístico", "Aleatório"),
# }

# ROTULOS = {
#     "Ofensivo_vs_Defensivo":      "Ofensivo  vs  Defensivo",
#     "Ofensivo_vs_Probabilistico": "Ofensivo  vs  Probabilístico",
#     "Ofensivo_vs_Aleatorio":      "Ofensivo  vs  Aleatório",
#     "Defensivo_vs_Probabilistico":"Defensivo  vs  Probabilístico",
#     "Defensivo_vs_Aleatorio":     "Defensivo  vs  Aleatório",
#     "Probabilistico_vs_Aleatorio":"Probabilístico  vs  Aleatório",
# }

# def _cor(nome):
#     return CORES.get(nome, "#999999")

# def _lum(hex_cor):
#     r = int(hex_cor[1:3], 16) / 255
#     g = int(hex_cor[3:5], 16) / 255
#     b = int(hex_cor[5:7], 16) / 255
#     return 0.299 * r + 0.587 * g + 0.114 * b


# # ══════════════════════════════════════════════════════════════════════════════
# # Gráfico 1 — Barras horizontais empilhadas 100%
# # ══════════════════════════════════════════════════════════════════════════════
# def gerar_grafico_vitorias(arquivos_resultados, output_dir):
#     confrontos = []
#     for arq in arquivos_resultados:
#         nome = (os.path.basename(arq)
#                 .replace("confronto_", "")
#                 .replace("_resultados.csv", ""))
#         confrontos.append((nome, arq))

#     fig, ax = plt.subplots(figsize=(13, 7))
#     fig.patch.set_facecolor("white")
#     ax.set_facecolor("#F8F8F8")

#     rotulos_y = []
#     BAR_H = 0.52

#     for i, (nome, arq) in enumerate(confrontos):
#         if not os.path.exists(arq):
#             print(f"⚠️  Arquivo não encontrado: {arq}")
#             rotulos_y.append(nome)
#             continue

#         df    = pd.read_csv(arq)
#         da, db = NOMES_DUPLA.get(nome, ("Dupla A", "Dupla B"))
#         rotulos_y.append(ROTULOS.get(nome, nome))

#         total = len(df)
#         venc  = df["dupla_vencedora"].value_counts()

#         chaves_a = [k for k in venc.index if da[:3].lower() in k.lower()]
#         chaves_b = [k for k in venc.index if db[:3].lower() in k.lower()]
#         pct_a = venc.get(chaves_a[0], 0) / total * 100 if chaves_a else 0
#         pct_b = venc.get(chaves_b[0], 0) / total * 100 if chaves_b else 0

#         ca, cb = _cor(da), _cor(db)
#         ax.barh(i, pct_a, height=BAR_H, color=ca, zorder=3)
#         ax.barh(i, pct_b, height=BAR_H, left=pct_a, color=cb, zorder=3)

#         for pct, left, cor in [(pct_a, 0, ca), (pct_b, pct_a, cb)]:
#             if pct > 6:
#                 txt_c = "white" if _lum(cor) < 0.55 else "#333333"
#                 ax.text(left + pct / 2, i, f"{pct:.0f}%",
#                         ha="center", va="center", fontsize=13,
#                         fontweight="bold", color=txt_c, zorder=5)

#     ax.axvline(50, color="#888888", lw=1.2, ls="--", zorder=4)
#     ax.set_yticks(range(len(rotulos_y)))
#     ax.set_yticklabels(rotulos_y, fontsize=12)
#     ax.set_xlim(0, 100)
#     ax.set_xlabel("Taxa de vitória (%)", fontsize=11, color="#555555")
#     ax.set_title("Quem vence mais?\nTaxa de vitória por confronto — 1 000 partidas cada",
#                  fontsize=15, fontweight="bold", pad=14, color="#222222")
#     ax.tick_params(axis="x", colors="#888888")
#     ax.spines[["top", "right", "bottom"]].set_visible(False)
#     ax.spines["left"].set_color("#cccccc")
#     ax.grid(axis="x", color="#dddddd", zorder=0)

#     patches = [mpatches.Patch(color=_cor(s), label=s)
#                for s in ["Aleatório", "Defensivo", "Ofensivo", "Probabilístico"]]
#     fig.legend(handles=patches, loc="lower center", ncol=4, fontsize=10,
#                framealpha=0.9, edgecolor="#cccccc", bbox_to_anchor=(0.5, -0.04))

#     plt.tight_layout()
#     plt.savefig(os.path.join(output_dir, "grafico_vitorias.png"), dpi=180, bbox_inches="tight")
#     plt.close()
#     print("✅ grafico_vitorias.png gerado")


# # ══════════════════════════════════════════════════════════════════════════════
# # Gráfico 2 — Donuts batida vs trancado (2 linhas de 3)
# # ══════════════════════════════════════════════════════════════════════════════
# def gerar_grafico_trancamentos(arquivos_historico, nomes_confronto, output_dir):
#     COR_BATIDA   = "#2A9D8F"
#     COR_TRANCADO = "#E63946"

#     leg = [mpatches.Patch(color=COR_BATIDA,   label="Batida (alguém esvazia a mão)"),
#            mpatches.Patch(color=COR_TRANCADO, label="Trancado (ninguém consegue jogar)")]

#     grupos = [
#         (nomes_confronto[:3], arquivos_historico[:3], "1"),
#         (nomes_confronto[3:], arquivos_historico[3:], "2"),
#     ]

#     for nomes, arquivos, sufixo in grupos:
#         fig, axes = plt.subplots(1, 3, figsize=(13, 5))
#         fig.patch.set_facecolor("white")
#         fig.suptitle("Como as rodadas terminam?\nBatida vs Trancamento por confronto",
#                      fontsize=15, fontweight="bold", color="#222222", y=1.02)

#         for ax, arq, nome in zip(axes, arquivos, nomes):
#             if not os.path.exists(arq):
#                 print(f"⚠️  Arquivo não encontrado: {arq}")
#                 ax.axis("off")
#                 continue

#             df    = pd.read_csv(arq)
#             tot   = len(df)
#             trap  = (df["motivo"] == "trancado").sum()
#             pct_t = trap / tot * 100
#             pct_b = 100 - pct_t

#             ax.pie([pct_b, pct_t],
#                    colors=[COR_BATIDA, COR_TRANCADO],
#                    startangle=90,
#                    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2))
#             ax.text(0,  0.08, f"{pct_t:.0f}%", ha="center", va="center",
#                     fontsize=20, fontweight="bold", color=COR_TRANCADO)
#             ax.text(0, -0.22, "trancado", ha="center", va="center",
#                     fontsize=10, color="#666666")

#             titulo = ROTULOS.get(nome, nome).replace("  vs  ", "\nvs\n")
#             ax.set_title(titulo, fontsize=10.5, fontweight="bold", color="#333333", pad=10)

#         fig.legend(handles=leg, loc="lower center", ncol=2, fontsize=11,
#                    framealpha=0.9, edgecolor="#cccccc", bbox_to_anchor=(0.5, -0.08))

#         plt.tight_layout()
#         plt.savefig(os.path.join(output_dir, f"grafico_trancamentos_{sufixo}.png"),
#                     dpi=180, bbox_inches="tight")
#         plt.close()
#         print(f"✅ grafico_trancamentos_{sufixo}.png gerado")


# # ══════════════════════════════════════════════════════════════════════════════
# # Gráfico 3 — Boxplot força da mão vs motivo (antigo)
# # ══════════════════════════════════════════════════════════════════════════════
# def gerar_grafico_forca_vs_motivo(arquivo_historico, nome_confronto, output_dir):
#     if not os.path.exists(arquivo_historico):
#         print(f"⚠️  Arquivo não encontrado: {arquivo_historico}")
#         return

#     df = pd.read_csv(arquivo_historico)

#     fig, axes = plt.subplots(1, 2, figsize=(12, 5))
#     for ax, col, titulo in zip(
#         axes,
#         ["forca_dupla_a", "forca_dupla_b"],
#         ["Dupla A", "Dupla B"],
#     ):
#         sns.boxplot(
#             data=df, x="motivo", y=col, ax=ax,
#             hue="motivo",
#             palette={"batida": "#4CAF50", "trancado": "#F44336"},
#             legend=False,
#         )
#         ax.set_title(f"{titulo} — Força da Mão vs Motivo", fontsize=12)
#         ax.set_xlabel("Motivo de Encerramento")
#         ax.set_ylabel("Força Média da Mão Inicial")

#     fig.suptitle(f"Força da Mão × Motivo de Encerramento\n"
#                  f"{ROTULOS.get(nome_confronto, nome_confronto)}",
#                  fontsize=14, fontweight="bold")
#     plt.tight_layout()
#     path = os.path.join(output_dir, f"grafico_forca_motivo_{nome_confronto}.png")
#     plt.savefig(path, dpi=150)
#     plt.close()
#     print(f"✅ grafico_forca_motivo_{nome_confronto}.png gerado")


# # ══════════════════════════════════════════════════════════════════════════════
# # Gráfico 4 — Histograma distribuição de pontos (antigo + cores fixas)
# # ══════════════════════════════════════════════════════════════════════════════
# def gerar_grafico_pontos_por_rodada(arquivo_historico, nome_confronto, output_dir):
#     if not os.path.exists(arquivo_historico):
#         print(f"⚠️  Arquivo não encontrado: {arquivo_historico}")
#         return

#     df = pd.read_csv(arquivo_historico)
#     df = df[df["dupla_vencedora"] != "empate"]

#     da, db = NOMES_DUPLA.get(nome_confronto, ("Dupla A", "Dupla B"))

#     fig, ax = plt.subplots(figsize=(10, 6))
#     for dupla in df["dupla_vencedora"].unique():
#         subset = df[df["dupla_vencedora"] == dupla]["pontos_ganhos"]
#         estrategia = da if da[:3].lower() in dupla.lower() else db
#         cor = _cor(estrategia)
#         sns.histplot(subset, label=estrategia, ax=ax, kde=True,
#                      bins=20, alpha=0.55, color=cor)

#     ax.set_title(f"Distribuição de Pontos Ganhos por Rodada\n"
#                  f"{ROTULOS.get(nome_confronto, nome_confronto)}",
#                  fontsize=14, fontweight="bold")
#     ax.set_xlabel("Pontos Ganhos na Rodada")
#     ax.set_ylabel("Frequência")
#     ax.legend(title="Estratégia vencedora")
#     plt.tight_layout()
#     path = os.path.join(output_dir, f"grafico_pontos_rodada_{nome_confronto}.png")
#     plt.savefig(path, dpi=150)
#     plt.close()
#     print(f"✅ grafico_pontos_rodada_{nome_confronto}.png gerado")


























import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

CORES = {
    "Aleatório":      "#A8C5DA",
    "Aleatorio":      "#A8C5DA",
    "Defensivo":      "#F4A261",
    "Ofensivo":       "#E63946",
    "Probabilístico": "#2A9D8F",
    "Probabilistico": "#2A9D8F",
}

NOMES_DUPLA = {
    "Ofensivo_vs_Defensivo":      ("Ofensivo",       "Defensivo"),
    "Ofensivo_vs_Probabilistico": ("Ofensivo",       "Probabilístico"),
    "Ofensivo_vs_Aleatorio":      ("Ofensivo",       "Aleatório"),
    "Defensivo_vs_Probabilistico":("Defensivo",      "Probabilístico"),
    "Defensivo_vs_Aleatorio":     ("Defensivo",      "Aleatório"),
    "Probabilistico_vs_Aleatorio":("Probabilístico", "Aleatório"),
}

ROTULOS = {
    "Ofensivo_vs_Defensivo":      "Ofensivo  vs  Defensivo",
    "Ofensivo_vs_Probabilistico": "Ofensivo  vs  Probabilístico",
    "Ofensivo_vs_Aleatorio":      "Ofensivo  vs  Aleatório",
    "Defensivo_vs_Probabilistico":"Defensivo  vs  Probabilístico",
    "Defensivo_vs_Aleatorio":     "Defensivo  vs  Aleatório",
    "Probabilistico_vs_Aleatorio":"Probabilístico  vs  Aleatório",
}

def _cor(nome):
    return CORES.get(nome, "#999999")

def _lum(hex_cor):
    r = int(hex_cor[1:3], 16) / 255
    g = int(hex_cor[3:5], 16) / 255
    b = int(hex_cor[5:7], 16) / 255
    return 0.299 * r + 0.587 * g + 0.114 * b

PAD = 1.5  # borda externa padrão para todos os gráficos


# ══════════════════════════════════════════════════════════════════════════════
# Gráfico 1 — Barras horizontais empilhadas 100%
# ══════════════════════════════════════════════════════════════════════════════
def gerar_grafico_vitorias(arquivos_resultados, output_dir):
    confrontos = []
    for arq in arquivos_resultados:
        nome = (os.path.basename(arq)
                .replace("confronto_", "")
                .replace("_resultados.csv", ""))
        confrontos.append((nome, arq))

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8F8F8")

    rotulos_y = []
    BAR_H = 0.52

    for i, (nome, arq) in enumerate(confrontos):
        if not os.path.exists(arq):
            print(f"⚠️  Arquivo não encontrado: {arq}")
            rotulos_y.append(nome)
            continue

        df    = pd.read_csv(arq)
        da, db = NOMES_DUPLA.get(nome, ("Dupla A", "Dupla B"))
        rotulos_y.append(ROTULOS.get(nome, nome))

        total = len(df)
        venc  = df["dupla_vencedora"].value_counts()

        chaves_a = [k for k in venc.index if da[:3].lower() in k.lower()]
        chaves_b = [k for k in venc.index if db[:3].lower() in k.lower()]
        pct_a = venc.get(chaves_a[0], 0) / total * 100 if chaves_a else 0
        pct_b = venc.get(chaves_b[0], 0) / total * 100 if chaves_b else 0

        ca, cb = _cor(da), _cor(db)
        ax.barh(i, pct_a, height=BAR_H, color=ca, zorder=3)
        ax.barh(i, pct_b, height=BAR_H, left=pct_a, color=cb, zorder=3)

        for pct, left, cor in [(pct_a, 0, ca), (pct_b, pct_a, cb)]:
            if pct > 6:
                txt_c = "white" if _lum(cor) < 0.55 else "#333333"
                ax.text(left + pct / 2, i, f"{pct:.0f}%",
                        ha="center", va="center", fontsize=13,
                        fontweight="bold", color=txt_c, zorder=5)

    ax.axvline(50, color="#888888", lw=1.2, ls="--", zorder=4)
    ax.set_yticks(range(len(rotulos_y)))
    # rótulos quebrados em 3 linhas, "vs" centralizado
    labels = [r.replace("  vs  ", "\nvs\n") for r in rotulos_y]
    ax.set_yticklabels(labels, fontsize=12, linespacing=1.2, multialignment="center")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Taxa de vitória (%)", fontsize=11, color="#555555")
    ax.set_title("Quem vence mais?\nTaxa de vitória por confronto — 1 000 partidas cada",
                 fontsize=15, fontweight="bold", pad=14, color="#222222")
    ax.tick_params(axis="x", colors="#888888")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.grid(axis="x", color="#dddddd", zorder=0)

    patches = [mpatches.Patch(color=_cor(s), label=s)
               for s in ["Aleatório", "Defensivo", "Ofensivo", "Probabilístico"]]
    fig.legend(handles=patches, loc="lower center", ncol=4, fontsize=10,
               framealpha=0.9, edgecolor="#cccccc", bbox_to_anchor=(0.5, -0.04))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "grafico_vitorias.png"),
                dpi=180, bbox_inches="tight", pad_inches=PAD)
    plt.close()
    print("✅ grafico_vitorias.png gerado")


# ══════════════════════════════════════════════════════════════════════════════
# Gráfico 2 — Donuts batida vs trancado (2 arquivos de 3)
# ══════════════════════════════════════════════════════════════════════════════
def gerar_grafico_trancamentos(arquivos_historico, nomes_confronto, output_dir):
    COR_BATIDA   = "#2A9D8F"
    COR_TRANCADO = "#E63946"

    leg = [mpatches.Patch(color=COR_BATIDA,   label="Batida (alguém esvazia a mão)"),
           mpatches.Patch(color=COR_TRANCADO, label="Trancado (ninguém consegue jogar)")]

    grupos = [
        (nomes_confronto[:3], arquivos_historico[:3], "1"),
        (nomes_confronto[3:], arquivos_historico[3:], "2"),
    ]

    for nomes, arquivos, sufixo in grupos:
        fig, axes = plt.subplots(1, 3, figsize=(13, 5))
        fig.patch.set_facecolor("white")
        fig.suptitle("Como as rodadas terminam?\nBatida vs Trancamento por confronto",
                     fontsize=15, fontweight="bold", color="#222222", y=1.02)

        for ax, arq, nome in zip(axes, arquivos, nomes):
            if not os.path.exists(arq):
                print(f"⚠️  Arquivo não encontrado: {arq}")
                ax.axis("off")
                continue

            df    = pd.read_csv(arq)
            tot   = len(df)
            trap  = (df["motivo"] == "trancado").sum()
            pct_t = trap / tot * 100
            pct_b = 100 - pct_t

            ax.pie([pct_b, pct_t],
                   colors=[COR_BATIDA, COR_TRANCADO],
                   startangle=90,
                   wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2))
            ax.text(0,  0.08, f"{pct_t:.0f}%", ha="center", va="center",
                    fontsize=20, fontweight="bold", color=COR_TRANCADO)
            ax.text(0, -0.22, "trancado", ha="center", va="center",
                    fontsize=10, color="#666666")

            titulo = ROTULOS.get(nome, nome).replace("  vs  ", "\nvs\n")
            ax.set_title(titulo, fontsize=10.5, fontweight="bold", color="#333333", pad=10)

        fig.legend(handles=leg, loc="lower center", ncol=2, fontsize=11,
                   framealpha=0.9, edgecolor="#cccccc", bbox_to_anchor=(0.5, -0.08))

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"grafico_trancamentos_{sufixo}.png"),
                    dpi=180, bbox_inches="tight", pad_inches=PAD)
        plt.close()
        print(f"✅ grafico_trancamentos_{sufixo}.png gerado")


# ══════════════════════════════════════════════════════════════════════════════
# Gráfico 3 — Boxplot força da mão vs motivo
# ══════════════════════════════════════════════════════════════════════════════
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

    fig.suptitle(f"Força da Mão × Motivo de Encerramento\n"
                 f"{ROTULOS.get(nome_confronto, nome_confronto)}",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(output_dir, f"grafico_forca_motivo_{nome_confronto}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", pad_inches=PAD)
    plt.close()
    print(f"✅ grafico_forca_motivo_{nome_confronto}.png gerado")


# ══════════════════════════════════════════════════════════════════════════════
# Gráfico 4 — Histograma distribuição de pontos
# ══════════════════════════════════════════════════════════════════════════════
def gerar_grafico_pontos_por_rodada(arquivo_historico, nome_confronto, output_dir):
    if not os.path.exists(arquivo_historico):
        print(f"⚠️  Arquivo não encontrado: {arquivo_historico}")
        return

    df = pd.read_csv(arquivo_historico)
    df = df[df["dupla_vencedora"] != "empate"]

    da, db = NOMES_DUPLA.get(nome_confronto, ("Dupla A", "Dupla B"))

    fig, ax = plt.subplots(figsize=(10, 6))
    for dupla in df["dupla_vencedora"].unique():
        subset = df[df["dupla_vencedora"] == dupla]["pontos_ganhos"]
        estrategia = da if da[:3].lower() in dupla.lower() else db
        cor = _cor(estrategia)
        sns.histplot(subset, label=estrategia, ax=ax, kde=True,
                     bins=20, alpha=0.55, color=cor)

    ax.set_title(f"Distribuição de Pontos Ganhos por Rodada\n"
                 f"{ROTULOS.get(nome_confronto, nome_confronto)}",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Pontos Ganhos na Rodada")
    ax.set_ylabel("Frequência")
    ax.legend(title="Estratégia vencedora")
    plt.tight_layout()
    path = os.path.join(output_dir, f"grafico_pontos_rodada_{nome_confronto}.png")
    plt.savefig(path, dpi=150, bbox_inches="tight", pad_inches=PAD)
    plt.close()
    print(f"✅ grafico_pontos_rodada_{nome_confronto}.png gerado")















