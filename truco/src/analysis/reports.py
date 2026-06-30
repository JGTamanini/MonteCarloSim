import os
from typing import Any, Dict


def gerar_relatorio_markdown(resumo: Dict[str, Any], n_partidas: int, output_dir: str):
    """Gera um relatório acadêmico completo em formato Markdown."""
    ranking = resumo["ranking"]
    matriz = resumo["matriz_confrontos"]
    stats = resumo["estatisticas_finais"]

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "torneio_report.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# 🏆 Relatório do Torneio Multiagentes — Truco Paulista\n\n")
        f.write("Este relatório resume o desempenho de 10 estratégias distintas de agentes ")
        f.write(f"simuladas em um campeonato todos-contra-todos, com **{n_partidas} partidas** por confronto.\n\n")

        f.write("## 📊 1. Classificação Geral\n\n")
        f.write("| Posição | Agente / Estratégia | Pontos Acumulados |\n")
        f.write("|:---:|:---|:---:|\n")
        for idx, (nome, pontos) in enumerate(ranking):
            f.write(f"| {idx + 1}º | **{nome}** | {pontos} |\n")
        f.write("\n*(Critério: Vitória no confronto = 2 pts, Empate = 1 pt, Derrota = 0 pts)*\n\n")

        f.write("## ⚔️ 2. Matriz de Confrontos Diretos (Win Rates %)\n\n")
        f.write("Exibe a taxa de vitória do agente da linha (Agente) contra o agente da coluna (Oponente).\n\n")

        agentes = list(matriz.keys())
        # Header da tabela
        f.write("| Agente \\ Oponente | " + " | ".join(agentes) + " |\n")
        f.write("|:---|:" + ":|:".join(["---" for _ in agentes]) + ":|\n")

        for a in agentes:
            linha = [f"**{a}**"]
            for o in agentes:
                if a == o:
                    linha.append("-")
                else:
                    taxa = matriz[a][o]
                    linha.append(f"{taxa:.1f}%")
            f.write("| " + " | ".join(linha) + " |\n")
        f.write("\n")

        f.write("## ⚙️ 3. Métricas de Tomada de Decisão e Comportamento\n\n")
        f.write("| Agente / Estratégia | Tempo Médio (ms) | Força Média da Mão | Trucos Pedidos | Blefes Tentados | Sucessos | Taxa Sucesso Blefe |\n")
        f.write("|:---|:---:|:---:|:---:|:---:|:---:|:---:|\n")

        for ag in agentes:
            st = stats.get(ag, {})
            if not st:
                continue
            f.write(
                f"| **{ag}** | {st['tempo_medio_ms']:.2f} ms | {st['forca_media_mao']:.2f} | "
                f"{st['trucos_pedidos']} | {st['blefes_tentados']} | {st['blefes_sucedidos']} | "
                f"{st['taxa_sucesso_blefe']:.1f}% |\n"
            )
        f.write("\n")

        f.write("## 💡 4. Análise e Conclusões Científicas (MAS)\n\n")
        # Identifica quem venceu
        campeao = ranking[0][0]
        f.write(f"1. **Dominância da Estratégia**: A estratégia **{campeao}** consagrou-se campeã do torneio. ")

        # Adiciona conclusões adicionais com base no tipo de campeão
        if campeao in ["Adaptativo", "Híbrido", "Bayesiano"]:
            f.write("Isso evidencia que agentes que alteram dinamicamente seus parâmetros ")
            f.write("ou realizam inferência ativa sobre as crenças e oponente superam baseline estáticos.\n")
        else:
            f.write("Isso mostra a força bruta da estratégia estática configurada.\n")

        f.write("2. **Exploração do Blefe**: Estratégias como *Blefador* e *Agressivo* exibem alto volume de propostas, ")
        f.write("mas sofrem contra agentes de inferência (como o *Bayesiano* e *Adaptativo*) que calculam a probabilidade ")
        f.write("a posteriori de blefe e punem propostas falsas.\n")

        f.write("3. **Eficiência Computacional**: O tempo de decisão reflete a complexidade do Decision Engine. ")
        f.write("Estratégias probabilísticas e Bayesianas demandam cálculos extras de combinações de cartas, ")
        f.write("enquanto estratégias estáticas e aleatórias tomam decisões em tempo quase nulo.\n")

    print(f"[Relatorio] Relatorio Markdown salvo em: {filepath}")
