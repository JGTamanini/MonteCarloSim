import logging
import time
from typing import Any, Dict, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine

logger = logging.getLogger("DecisionEngine")


class DecisionExplanation:
    """Classe que encapsula a explicação em linguagem natural da decisão da IA (XAI)."""

    def __init__(
        self,
        nome_agente: str,
        decisao: str,
        motivo: str,
        forca_mao: float,
        prob_manilha_oponente: float,
        chance_blefe_oponente: float,
        perfil_oponente: str,
        estrategia_ativa: str,
        tempo_gasto_ms: float
    ):
        self.nome_agente = nome_agente
        self.decisao = decisao
        self.motivo = motivo
        self.forca_mao = forca_mao
        self.prob_manilha_oponente = prob_manilha_oponente
        self.chance_blefe_oponente = chance_blefe_oponente
        self.perfil_oponente = perfil_oponente
        self.estrategia_ativa = estrategia_ativa
        self.tempo_gasto_ms = tempo_gasto_ms

    def __str__(self):
        return (
            f"\n====== EXPLICAÇÃO DA IA ({self.nome_agente}) ======\n"
            f"Decisão: {self.decisao}\n"
            f"Motivo: {self.motivo}\n"
            f"---------------- METRICAS ----------------\n"
            f"Força da Mão: {self.forca_mao:.2f}\n"
            f"Prob. Manilha Oponente: {self.prob_manilha_oponente * 100:.1f}%\n"
            f"Prob. Posterior Blefe (Bayes): {self.chance_blefe_oponente * 100:.1f}%\n"
            f"Perfil Mapeado do Oponente: {self.perfil_oponente}\n"
            f"Estratégia Ativa: {self.estrategia_ativa}\n"
            f"Tempo de Processamento: {self.tempo_gasto_ms:.2f} ms\n"
            f"==========================================\n"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agente": self.nome_agente,
            "decisao": self.decisao,
            "motivo": self.motivo,
            "forca_mao": self.forca_mao,
            "prob_manilha_oponente": self.prob_manilha_oponente,
            "chance_blefe_oponente": self.chance_blefe_oponente,
            "perfil_oponente": self.perfil_oponente,
            "estrategia_ativa": self.estrategia_ativa,
            "tempo_ms": self.tempo_gasto_ms
        }


class DecisionEngine:
    @staticmethod
    def processar_decisao_acao(
        agente: Any,
        percepcao: Perception,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, DecisionExplanation]:
        """
        Executa a tomada de decisão do turno do agente, gerando a ação e a explicação XAI.
        """
        inicio = time.perf_counter()

        # 1. Atualiza crenças com a inferência
        agente.atualizar_crencas(percepcao)

        # 2. Executa a estratégia injetada
        acao, detalhe, motivo = agente.estrategia.escolher_acao(
            agente, percepcao, agente.beliefs, agente.memory, pode_pedir_truco
        )

        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000

        expl = DecisionExplanation(
            nome_agente=agente.nome,
            decisao=acao.name if hasattr(acao, "name") else str(acao),
            motivo=motivo,
            forca_mao=agente.beliefs.forca_mao_propria,
            prob_manilha_oponente=agente.beliefs.probabilidade_manilha_oponente,
            chance_blefe_oponente=agente.beliefs.chance_blefe_oponente,
            perfil_oponente=agente.beliefs.perfil_oponente,
            estrategia_ativa=agente.estrategia.__class__.__name__,
            tempo_gasto_ms=tempo_ms
        )

        logger.debug(str(expl))
        return acao, detalhe, expl

    @staticmethod
    def processar_decisao_resposta_truco(
        agente: Any,
        percepcao: Perception,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, DecisionExplanation]:
        """
        Executa a tomada de decisão para responder a um pedido de truco, gerando a resposta e a explicação XAI.
        """
        inicio = time.perf_counter()

        # 1. Atualiza crenças com a inferência
        agente.atualizar_crencas(percepcao)

        # 2. Executa a estratégia injetada
        resposta, motivo = agente.estrategia.responder_truco(
            agente, percepcao, agente.beliefs, agente.memory, valor_proposto
        )

        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000

        expl = DecisionExplanation(
            nome_agente=agente.nome,
            decisao=resposta.name if hasattr(resposta, "name") else str(resposta),
            motivo=motivo,
            forca_mao=agente.beliefs.forca_mao_propria,
            prob_manilha_oponente=agente.beliefs.probabilidade_manilha_oponente,
            chance_blefe_oponente=agente.beliefs.chance_blefe_oponente,
            perfil_oponente=agente.beliefs.perfil_oponente,
            estrategia_ativa=agente.estrategia.__class__.__name__,
            tempo_gasto_ms=tempo_ms
        )

        logger.debug(str(expl))
        return resposta, expl
class_name = "DecisionEngine"
