from typing import Any, Dict, List
from truco.src.core.carta import Carta
from truco.src.core.blackboard import Blackboard


class Perception:
    def __init__(
        self,
        nome_agente: str,
        mao_cartas: List[Carta],
        vira: Carta,
        cartas_jogadas_queda: Dict[str, Carta],
        placar_partida: Dict[str, int],
        quedas_vencidas: Dict[str, int],
        valor_truco_atual: int,
        mensagens: List[Dict[str, Any]],
        blackboard_compartilhado: Blackboard
    ):
        self.nome_agente = nome_agente
        self.mao_cartas = list(mao_cartas)
        self.vira = vira
        self.cartas_jogadas_queda = dict(cartas_jogadas_queda)
        self.placar_partida = dict(placar_partida)
        self.quedas_vencidas = dict(quedas_vencidas)
        self.valor_truco_atual = valor_truco_atual
        self.mensagens = list(mensagens)
        self.blackboard = blackboard_compartilhado

    def __str__(self):
        return (
            f"Percepcao(Agente: {self.nome_agente}, Mão: {self.mao_cartas}, "
            f"Vira: {self.vira}, Placar: {self.placar_partida}, Truco: {self.valor_truco_atual})"
        )


class PerceptionEngine:
    @staticmethod
    def gerar_percepcao(
        nome_agente: str,
        mao_agente: List[Carta],
        vira: Carta,
        cartas_jogadas_queda: Dict[str, Carta],
        placar_partida: Dict[str, int],
        quedas_vencidas: Dict[str, int],
        valor_truco_atual: int,
        blackboard: Blackboard
    ) -> Perception:
        """
        Gera o objeto de percepção filtrado para o agente.
        Garante que ele tenha acesso apenas às suas próprias cartas e a informações públicas.
        """
        # Filtra mensagens destinadas especificamente a este agente
        mensagens = blackboard.obter_mensagens(destinatario=nome_agente)

        return Perception(
            nome_agente=nome_agente,
            mao_cartas=mao_agente,
            vira=vira,
            cartas_jogadas_queda=cartas_jogadas_queda,
            placar_partida=placar_partida,
            quedas_vencidas=quedas_vencidas,
            valor_truco_atual=valor_truco_atual,
            mensagens=mensagens,
            blackboard_compartilhado=blackboard
        )
