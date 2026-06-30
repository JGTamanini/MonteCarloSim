from typing import Dict
from truco.src.core.carta import Carta


class JogoEvent:
    """Classe base para todos os eventos do sistema."""
    pass


class MatchStartedEvent(JogoEvent):
    def __init__(self, jogador1: str, jogador2: str):
        self.jogador1 = jogador1
        self.jogador2 = jogador2

    def __str__(self):
        return f"[MatchStartedEvent] Partida iniciada entre {self.jogador1} e {self.jogador2}."


class MatchFinishedEvent(JogoEvent):
    def __init__(self, vencedor: str, placar: Dict[str, int]):
        self.vencedor = vencedor
        self.placar = placar

    def __str__(self):
        return f"[MatchFinishedEvent] Partida finalizada! Vencedor: {self.vencedor}. Placar final: {self.placar}."


class RoundStartedEvent(JogoEvent):
    def __init__(self, numero_mao: int, vira: Carta):
        self.numero_mao = numero_mao
        self.vira = vira

    def __str__(self):
        return f"[RoundStartedEvent] Mão {self.numero_mao} iniciada. Vira: {self.vira}."


class RoundFinishedEvent(JogoEvent):
    def __init__(self, numero_mao: int, vencedor: str, pontos_ganhos: int, placar: Dict[str, int]):
        self.numero_mao = numero_mao
        self.vencedor = vencedor
        self.pontos_ganhos = pontos_ganhos
        self.placar = placar

    def __str__(self):
        return (
            f"[RoundFinishedEvent] Mão {self.numero_mao} finalizada. "
            f"Vencedor da mão: {self.vencedor} (+{self.pontos_ganhos} pts). Placar: {self.placar}."
        )


class QuedaStartedEvent(JogoEvent):
    def __init__(self, numero_queda: int):
        self.numero_queda = numero_queda

    def __str__(self):
        return f"[QuedaStartedEvent] Queda {self.numero_queda} iniciada."


class QuedaFinishedEvent(JogoEvent):
    def __init__(self, numero_queda: int, vencedor_queda: str, cartas_jogadas: Dict[str, Carta]):
        self.numero_queda = numero_queda
        self.vencedor_queda = vencedor_queda
        self.cartas_jogadas = cartas_jogadas

    def __str__(self):
        jogadas_str = ", ".join(f"{j}: {c}" for j, c in self.cartas_jogadas.items())
        return f"[QuedaFinishedEvent] Queda {self.numero_queda} vencida por: {self.vencedor_queda}. Jogadas: {jogadas_str}."


class CardPlayedEvent(JogoEvent):
    def __init__(self, jogador: str, carta: Carta):
        self.jogador = jogador
        self.carta = carta

    def __str__(self):
        return f"[CardPlayedEvent] {self.jogador} jogou a carta: {self.carta}."


class TrucoRequestedEvent(JogoEvent):
    def __init__(self, jogador: str, valor_proposto: int):
        self.jogador = jogador
        self.valor_proposto = valor_proposto

    def __str__(self):
        return f"[TrucoRequestedEvent] {self.jogador} pediu TRUCO para valer {self.valor_proposto}!"


class TrucoAcceptedEvent(JogoEvent):
    def __init__(self, jogador: str, novo_valor: int):
        self.jogador = jogador
        self.novo_valor = novo_valor

    def __str__(self):
        return f"[TrucoAcceptedEvent] {self.jogador} ACEITOU o truco. Valor atual: {self.novo_valor}."


class TrucoRejectedEvent(JogoEvent):
    def __init__(self, jogador: str):
        self.jogador = jogador

    def __str__(self):
        return f"[TrucoRejectedEvent] {self.jogador} CORREU (recusou) o truco."


class TrucoRaisedEvent(JogoEvent):
    def __init__(self, jogador: str, valor_atual: int, valor_proposto: int):
        self.jogador = jogador
        self.valor_atual = valor_atual
        self.valor_proposto = valor_proposto

    def __str__(self):
        return f"[TrucoRaisedEvent] {self.jogador} AUMENTOU de {self.valor_atual} para {self.valor_proposto}!"


class DecisionMadeEvent(JogoEvent):
    def __init__(self, jogador: str, decisao: str, forca_mao: float, tempo_ms: float, motivo: str, estrategia: str):
        self.jogador = jogador
        self.decisao = decisao
        self.forca_mao = forca_mao
        self.tempo_ms = tempo_ms
        self.motivo = motivo
        self.estrategia = estrategia

    def __str__(self):
        return f"[DecisionMadeEvent] {self.jogador} decidiu {self.decisao} ({self.tempo_ms:.1f}ms) | Motivo: {self.motivo}"

