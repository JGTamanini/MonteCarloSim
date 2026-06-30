import pytest
from truco.src.core.carta import Carta
from truco.src.core.baralho import Baralho
from truco.src.core.rule_engine import RuleEngine
from truco.src.core.blackboard import Blackboard


def test_is_manilha():
    # Se a vira é 3, a manilha é 4
    vira = Carta("3", "copas")
    manilha = Carta("4", "paus")
    normal = Carta("K", "ouros")

    assert RuleEngine.is_manilha(manilha, vira) is True
    assert RuleEngine.is_manilha(normal, vira) is False


def test_get_forca_carta():
    # Vira = 7 -> Manilha = J
    vira = Carta("7", "ouros")

    # J de paus é a manilha mais forte
    j_paus = Carta("J", "paus")
    # J de ouros é a manilha mais fraca
    j_ouros = Carta("J", "ouros")
    # 3 de copas é a carta normal mais forte
    tres_copas = Carta("3", "copas")
    # 4 de espadas é a carta normal mais fraca
    quatro_espadas = Carta("4", "espadas")

    assert RuleEngine.get_forca_carta(j_paus, vira) == 14
    assert RuleEngine.get_forca_carta(j_ouros, vira) == 11
    assert RuleEngine.get_forca_carta(tres_copas, vira) == 10
    assert RuleEngine.get_forca_carta(quatro_espadas, vira) == 1


def test_comparar_cartas():
    # Vira = K -> Manilha = A
    vira = Carta("K", "copas")
    a_ouros = Carta("A", "ouros")
    tres_copas = Carta("3", "copas")

    # Manilha vs normal
    assert RuleEngine.comparar_cartas(a_ouros, tres_copas, vira) == 1
    assert RuleEngine.comparar_cartas(tres_copas, a_ouros, vira) == -1

    # Normal vs normal
    assert RuleEngine.comparar_cartas(tres_copas, Carta("3", "ouros"), vira) == 0


def test_blackboard():
    bb = Blackboard()
    bb.registrar_fato("placar_teste", {"A": 10, "B": 8})
    assert bb.obter_fato("placar_teste")["A"] == 10

    bb.registrar_perfil_adversario("AdversarioX", {"tipo": "Agressivo"})
    assert bb.obter_perfil_adversario("AdversarioX")["tipo"] == "Agressivo"
