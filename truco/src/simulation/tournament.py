import logging
from typing import Any, Dict, List
from truco.src.agents import (
    AgenteAleatorio,
    AgenteConservador,
    AgenteAgressivo,
    AgenteProbabilistico,
    AgenteAdaptativo,
    AgenteBlefador,
    AgenteBayesiano,
    AgenteRiscoEvitador,
    AgenteRiscoBuscador,
    AgenteHibrido,
)
from truco.src.simulation.simulator import Simulator

logger = logging.getLogger("TournamentManager")


class TournamentManager:
    def __init__(self):
        # Mapeamento para instanciar novas cópias limpas dos agentes
        self.agent_classes = {
            "Aleatório": lambda: AgenteAleatorio("Aleatório"),
            "Conservador": lambda: AgenteConservador("Conservador"),
            "Agressivo": lambda: AgenteAgressivo("Agressivo"),
            "Probabilístico": lambda: AgenteProbabilistico("Probabilístico"),
            "Adaptativo": lambda: AgenteAdaptativo("Adaptativo"),
            "Blefador": lambda: AgenteBlefador("Blefador"),
            "Bayesiano": lambda: AgenteBayesiano("Bayesiano"),
            "RiscoEvitador": lambda: AgenteRiscoEvitador("RiscoEvitador"),
            "RiscoBuscador": lambda: AgenteRiscoBuscador("RiscoBuscador"),
            "Híbrido": lambda: AgenteHibrido("Híbrido"),
        }

    def rodar_campeonato(self, n_partidas_confronto: int = 100) -> Dict[str, Any]:
        """
        Executa um campeonato todos-contra-todos entre todos os agentes cadastrados.
        Retorna a matriz de taxas de vitória e estatísticas consolidadas.
        """
        agente_nomes = list(self.agent_classes.keys())
        confrontos_resultados = {}
        tabela_pontos = {nome: 0 for nome in agente_nomes}
        stats_agentes = {nome: [] for nome in agente_nomes}

        # Matriz de taxas de vitória: {agente_A: {agente_B: taxa_vitoria}}
        matriz_confrontos = {a: {b: 0.0 for b in agente_nomes} for a in agente_nomes}

        logger.info(f"Iniciando Campeonato Round-Robin com {len(agente_nomes)} agentes.")

        for i in range(len(agente_nomes)):
            for j in range(i + 1, len(agente_nomes)):
                a1_nome = agente_nomes[i]
                a2_nome = agente_nomes[j]

                logger.info(f"Confronto: {a1_nome} vs {a2_nome} ({n_partidas_confronto} partidas)")

                # Instancia novas cópias limpas dos agentes para evitar contaminação de memória de longo prazo
                agente1 = self.agent_classes[a1_nome]()
                agente2 = self.agent_classes[a2_nome]()

                # Roda a simulação do confronto
                sim = Simulator([agente1, agente2])
                resultado = sim.rodar(n_partidas_confronto)

                # Coleta vitórias de cada um
                vits_a1 = resultado["vitorias"].get(a1_nome, 0)
                vits_a2 = resultado["vitorias"].get(a2_nome, 0)

                taxa_a1 = (vits_a1 / n_partidas_confronto) * 100
                taxa_a2 = (vits_a2 / n_partidas_confronto) * 100

                matriz_confrontos[a1_nome][a2_nome] = taxa_a1
                matriz_confrontos[a2_nome][a1_nome] = taxa_a2

                # Registra pontuação (vencedor do confronto ganha 2 pontos, empate 1 ponto cada)
                if vits_a1 > vits_a2:
                    tabela_pontos[a1_nome] += 2
                elif vits_a2 > vits_a1:
                    tabela_pontos[a2_nome] += 2
                else:
                    tabela_pontos[a1_nome] += 1
                    tabela_pontos[a2_nome] += 1

                # Coleta estatísticas individuais de XAI dos agentes
                for nome, agente_res in resultado["agentes"].items():
                    stats_agentes[nome].append(agente_res)

        # Consolida estatísticas médias de cada agente
        estatisticas_finais = {}
        for nome in agente_nomes:
            confrontos_stats = stats_agentes[nome]
            if not confrontos_stats:
                continue

            estatisticas_finais[nome] = {
                "tempo_medio_ms": sum(c["tempo_medio_ms"] for c in confrontos_stats) / len(confrontos_stats),
                "forca_media_mao": sum(c["forca_media_mao"] for c in confrontos_stats) / len(confrontos_stats),
                "trucos_pedidos": sum(c["trucos_pedidos"] for c in confrontos_stats),
                "trucos_aceitos": sum(c["trucos_aceitos"] for c in confrontos_stats),
                "trucos_corridos": sum(c["trucos_corridos"] for c in confrontos_stats),
                "blefes_tentados": sum(c["blefes_tentados"] for c in confrontos_stats),
                "blefes_sucedidos": sum(c["blefes_sucedidos"] for c in confrontos_stats),
                "taxa_sucesso_blefe": (
                    sum(c["blefes_sucedidos"] for c in confrontos_stats) /
                    max(1, sum(c["blefes_tentados"] for c in confrontos_stats)) * 100
                )
            }

        # Ordena a tabela de classificação
        ranking = sorted(tabela_pontos.items(), key=lambda x: x[1], reverse=True)

        resumo_campeonato = {
            "matriz_confrontos": matriz_confrontos,
            "tabela_pontos": tabela_pontos,
            "ranking": ranking,
            "estatisticas_finais": estatisticas_finais
        }

        return resumo_campeonato
