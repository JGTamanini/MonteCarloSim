import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings

warnings.filterwarnings("ignore")

CORES = {
    "Aleatório": "#A8C5DA",
    "Aleatorio": "#A8C5DA",
    "Defensivo": "#F4A261",
    "Ofensivo": "#E63946",
    "Probabilístico": "#2A9D8F",
    "Probabilistico": "#2A9D8F",
}

NOMES_DUPLA = {
    "Ofensivo_vs_Defensivo": ("Ofensivo", "Defensivo"),
    "Ofensivo_vs_Probabilistico": ("Ofensivo", "Probabilístico"),
    "Ofensivo_vs_Aleatorio": ("Ofensivo", "Aleatório"),
    "Defensivo_vs_Probabilistico": ("Defensivo", "Probabilístico"),
    "Defensivo_vs_Aleatorio": ("Defensivo", "Aleatório"),
    "Probabilistico_vs_Aleatorio": ("Probabilístico", "Aleatório"),
}

ROTULOS = {
    "Ofensivo_vs_Defensivo": "Ofensivo  vs  Defensivo",
    "Ofensivo_vs_Probabilistico": "Ofensivo  vs  Probabilístico",
    "Ofensivo_vs_Aleatorio": "Ofensivo  vs  Aleatório",
    "Defensivo_vs_Probabilistico": "Defensivo  vs  Probabilístico",
    "Defensivo_vs_Aleatorio": "Defensivo  vs  Aleatório",
    "Probabilistico_vs_Aleatorio": "Probabilístico  vs  Aleatório",
}


def _cor(nome):
    return CORES.get(nome, "#999999")


def _lum(hex_cor):
    r = int(hex_cor[1:3], 16) / 255
    g = int(hex_cor[3:5], 16) / 255
    b = int(hex_cor[5:7], 16) / 255
    return 0.299 * r + 0.587 * g + 0.114 * b


def _desenhar_barras(ax, confrontos, data_dir, n, mostrar_rotulos):
    """Desenha as barras de um painel de convergência."""
    ax.set_facecolor("#F8F8F8")
    rotulos_y = []
    BAR_H = 0.45

    for i, nome in enumerate(confrontos):
        da, db = NOMES_DUPLA.get(nome, ("Dupla A", "Dupla B"))
        rotulos_y.append(ROTULOS.get(nome, nome))

        if n == 1_000:
            arq = os.path.join(data_dir, f"confronto_{nome}_resultados.csv")
        else:
            arq = os.path.join(data_dir, f"convergencia_{nome}_{n}.csv")

        if not os.path.exists(arq):
            ax.barh(i, 50, height=BAR_H, color="#eeeeee", zorder=3)
            ax.barh(i, 50, height=BAR_H, left=50, color="#dddddd", zorder=3)
            ax.text(
                50,
                i,
                "sem dados",
                ha="center",
                va="center",
                fontsize=9,
                color="#aaaaaa",
                zorder=5,
            )
            continue

        df = pd.read_csv(arq)
        total = len(df)
        venc = df["dupla_vencedora"].value_counts()

        chaves_a = [k for k in venc.index if da[:3].lower() in k.lower()]
        chaves_b = [k for k in venc.index if db[:3].lower() in k.lower()]
        pct_a = venc.get(chaves_a[0], 0) / total * 100 if chaves_a else 0
        pct_b = venc.get(chaves_b[0], 0) / total * 100 if chaves_b else 0

        ca, cb = _cor(da), _cor(db)
        ax.barh(i, pct_a, height=BAR_H, color=ca, zorder=3)
        ax.barh(i, pct_b, height=BAR_H, left=pct_a, color=cb, zorder=3)

        for pct, left, cor in [(pct_a, 0, ca), (pct_b, pct_a, cb)]:
            if pct > 7:
                txt_c = "white" if _lum(cor) < 0.55 else "#333333"
                ax.text(
                    left + pct / 2,
                    i,
                    f"{pct:.0f}%",
                    ha="center",
                    va="center",
                    fontsize=8,
                    fontweight="bold",
                    color=txt_c,
                    zorder=5,
                )

    ax.axvline(50, color="#888888", lw=1.2, ls="--", zorder=4)
    ax.set_yticks(range(len(rotulos_y)))
    if mostrar_rotulos:
        labels = [r.replace("  vs  ", "\nvs\n") for r in rotulos_y]
        ax.set_yticklabels(
            labels, fontsize=7, linespacing=1.2, ha="right", multialignment="center"
        )
    else:
        ax.set_yticklabels([])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Taxa de vitória (%)", fontsize=8, color="#555555")
    ax.tick_params(axis="x", colors="#888888", labelsize=7)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.grid(axis="x", color="#dddddd", zorder=0)

    label_n = f"{n:,}".replace(",", ".") + " partidas"
    ax.set_title(label_n, fontsize=10, fontweight="bold", color="#333333", pad=6)


def gerar_grafico_convergencia(
    data_dir, output_dir, n_simulacoes=[1_000, 10_000, 100_000]
):
    confrontos = list(ROTULOS.keys())

    # divide em 2 grupos de 3
    grupo1 = confrontos[:3]
    grupo2 = confrontos[3:]

    # descobre quais tamanhos têm dados
    ns_disponiveis = []
    for n in n_simulacoes:
        arq1k = os.path.join(data_dir, f"confronto_{confrontos[0]}_resultados.csv")
        arq_nk = os.path.join(data_dir, f"convergencia_{confrontos[0]}_{n}.csv")
        if (n == 1_000 and os.path.exists(arq1k)) or os.path.exists(arq_nk):
            ns_disponiveis.append(n)

    if not ns_disponiveis:
        print("⚠️  Nenhum arquivo encontrado.")
        return

    n_cols = len(ns_disponiveis)

    titulos_grupos = [
        "A taxa de vitória muda com mais simulações?\nGrupo 1: Ofensivo vs Defensivo · Ofensivo vs Probabilístico · Ofensivo vs Aleatório",
        "A taxa de vitória muda com mais simulações?\nGrupo 2: Defensivo vs Probabilístico · Defensivo vs Aleatório · Probabilístico vs Aleatório",
    ]

    for grupo_idx, (grupo, sufixo) in enumerate([(grupo1, "1"), (grupo2, "2")]):
        fig, axes = plt.subplots(1, n_cols, figsize=(3.5 * n_cols, 3.5))
        if n_cols == 1:
            axes = [axes]
        fig.patch.set_facecolor("white")

        # título dentro da figura, com espaço reservado no topo
        fig.text(
            0.5,
            0.97,
            titulos_grupos[grupo_idx],
            ha="center",
            va="top",
            fontsize=11,
            fontweight="bold",
            color="#222222",
        )

        for col_idx, (ax, n) in enumerate(zip(axes, ns_disponiveis)):
            _desenhar_barras(ax, grupo, data_dir, n, mostrar_rotulos=(col_idx == 0))

        # legenda dentro da figura, com espaço reservado no rodapé
        patches = [
            mpatches.Patch(color=_cor(s), label=s)
            for s in ["Aleatório", "Defensivo", "Ofensivo", "Probabilístico"]
        ]
        fig.legend(
            handles=patches,
            loc="lower center",
            ncol=4,
            fontsize=8,
            framealpha=0.9,
            edgecolor="#cccccc",
            bbox_to_anchor=(0.5, 0.01),
        )

        # reserva espaço: topo para título, rodapé para legenda
        plt.tight_layout(rect=[0, 0.1, 1, 0.88])
        path = os.path.join(output_dir, f"grafico_convergencia_{sufixo}.png")
        plt.savefig(path, dpi=180, bbox_inches="tight", pad_inches=1.5)
        plt.close()
        print(f"✅ grafico_convergencia_{sufixo}.png gerado")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    DATA_DIR = os.path.join(BASE_DIR, "data", "domino")
    OUTPUT_DIR = os.path.join(BASE_DIR, "data", "domino", "graficos")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    gerar_grafico_convergencia(DATA_DIR, OUTPUT_DIR)
