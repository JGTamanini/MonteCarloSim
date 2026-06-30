import pytest
from truco.src.core.carta import Carta
from truco.src.agents.inference import InferenceEngine
from truco.src.agents.memory import AgentMemory
from truco.src.agents.beliefs import BeliefState


def test_obter_cartas_restantes():
    mao = [Carta("3", "copas"), Carta("4", "paus")]
    vira = Carta("K", "ouros")
    reveladas = [Carta("A", "espadas"), Carta("2", "copas")]

    restantes = InferenceEngine.obter_cartas_restantes(mao, vira, reveladas)
    # Total de cartas no truco = 40.
    # Conhecidas = 2 (mão) + 1 (vira) + 2 (reveladas) = 5.
    # Restantes devem ser 35.
    assert len(restantes) == 35
    for c in mao + [vira] + reveladas:
        assert c not in restantes


def test_probabilidade_manilha_oponente():
    # Se o baralho restante tem 10 cartas e 2 manilhas, e o adversário tem 2 cartas em mãos.
    restantes = [
        Carta("4", "paus"), Carta("4", "copas"),  # 2 manilhas se vira é 3
        Carta("Q", "ouros"), Carta("Q", "copas"),
        Carta("5", "ouros"), Carta("5", "copas"),
        Carta("6", "ouros"), Carta("6", "copas"),
        Carta("7", "ouros"), Carta("7", "copas"),
    ]
    vira = Carta("3", "espadas")  # vira = 3 -> manilha = 4

    prob = InferenceEngine.calcular_probabilidade_manilha_oponente(restantes, vira, cartas_restantes_oponente=2)
    # Total de combinações do adversário com 2 cartas: 10 escolhe 2 = 45.
    # Combinações sem nenhuma manilha: 8 escolhe 2 = 28.
    # Prob sem manilha = 28 / 45 = 62.2%
    # Prob com pelo menos uma manilha = 1 - 0.622 = 37.8%
    assert abs(prob - 0.37777777777777777) < 1e-5


def test_bayes_bluff_inference():
    memoria = AgentMemory("Teste")
    # Inicialmente neutro
    prob_neutral = InferenceEngine.calcular_probabilidade_posterior_blefe_bayes(memoria, oponente_pediu_truco=True)

    # Adiciona histórico de blefes confirmados do oponente para enviesar o prior
    memoria.total_trucos_pedidos_oponente = 5
    memoria.blefes_confirmados_oponente = 4  # Oponente blefa muito (80%)

    prob_high_bluff = InferenceEngine.calcular_probabilidade_posterior_blefe_bayes(memoria, oponente_pediu_truco=True)
    assert prob_high_bluff > prob_neutral
