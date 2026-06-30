import pytest
from truco.src.agents import AgenteAdaptativo, AgenteBayesiano
from truco.src.simulation.simulator import Simulator


def test_simulation_run():
    # Instancia dois agentes inteligentes diferentes
    agente1 = AgenteAdaptativo("IA_Adaptativa")
    agente2 = AgenteBayesiano("IA_Bayesiana")

    sim = Simulator([agente1, agente2])
    # Executa 3 partidas para verificar se a máquina de estados e o simulador correm sem erros
    resumo = sim.rodar(n_partidas=3)

    assert resumo["partidas_total"] == 3
    assert len(resumo["vitorias"]) > 0
    assert "IA_Adaptativa" in resumo["agentes"]
    assert "IA_Bayesiana" in resumo["agentes"]
