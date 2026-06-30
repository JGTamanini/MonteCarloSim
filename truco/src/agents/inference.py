import math
from typing import List, Set
from truco.src.core.carta import Carta
from truco.src.core.constantes import HIERARQUIA, NAIPES
from truco.src.core.rule_engine import RuleEngine
from truco.src.agents.memory import AgentMemory


class InferenceEngine:
    @staticmethod
    def obter_cartas_restantes(mao_propria: List[Carta], vira: Carta, cartas_reveladas: List[Carta]) -> List[Carta]:
        """
        Retorna as cartas restantes no baralho que não estão na mão própria,
        não são a vira e não foram jogadas publicamente ainda.
        """
        cartas_conhecidas = set()
        for c in mao_propria:
            cartas_conhecidas.add((c.valor, c.naipe))
        if vira:
            cartas_conhecidas.add((vira.valor, vira.naipe))
        for c in cartas_reveladas:
            cartas_conhecidas.add((c.valor, c.naipe))

        cartas_restantes = []
        for valor in HIERARQUIA.keys():
            for naipe in NAIPES.keys():
                if (valor, naipe) not in cartas_conhecidas:
                    cartas_restantes.append(Carta(valor, naipe))

        return cartas_restantes

    @classmethod
    def calcular_probabilidade_manilha_oponente(
        cls,
        cartas_restantes: List[Carta],
        vira: Carta,
        cartas_restantes_oponente: int
    ) -> float:
        """
        Calcula a probabilidade de o oponente possuir pelo menos uma manilha forte.
        Usa probabilidade hipergeométrica.
        """
        if not cartas_restantes or cartas_restantes_oponente <= 0:
            return 0.0

        # Conta quantas manilhas ainda restam nas cartas desconhecidas
        manilhas_restantes = sum(1 for c in cartas_restantes if RuleEngine.is_manilha(c, vira))

        total_desconhecidas = len(cartas_restantes)
        k = cartas_restantes_oponente

        if total_desconhecidas < k:
            return 0.0

        # Combinação de n escolhe r
        def comb(n, r):
            if r < 0 or r > n:
                return 0
            return math.comb(n, r)

        # Probabilidade de NÃO ter nenhuma manilha
        # comb(total_desconhecidas - manilhas_restantes, k) / comb(total_desconhecidas, k)
        comb_sem_manilha = comb(total_desconhecidas - manilhas_restantes, k)
        comb_total = comb(total_desconhecidas, k)

        if comb_total == 0:
            return 0.0

        prob_sem_manilha = comb_sem_manilha / comb_total
        return max(0.0, min(1.0, 1.0 - prob_sem_manilha))

    @staticmethod
    def calcular_probabilidade_posterior_blefe_bayes(
        memoria: AgentMemory,
        oponente_pediu_truco: bool
    ) -> float:
        """
        Aplica o Teorema de Bayes para calcular a probabilidade a posteriori
        de o oponente estar blefando ao pedir Truco.
        P(Blefe | Truco) = [ P(Truco | Blefe) * P(Blefe) ] / P(Truco)
        """
        if not oponente_pediu_truco:
            return 0.0

        # P(Blefe): Prior de blefe do oponente estimado pela memória
        prior_blefe = memoria.obter_taxa_blefe_oponente()
        prior_mao_forte = 1.0 - prior_blefe

        # Likelihoods baseadas em comportamento geral
        # P(Truco | Blefe) - Se ele está blefando, ele pede truco (alta chance)
        p_truco_dado_blefe = 0.85

        # P(Truco | Mao Forte) - Se ele tem mão forte, ele pede truco
        p_truco_dado_mao_forte = 0.65

        # P(Truco) = P(Truco | Blefe)*P(Blefe) + P(Truco | Mao Forte)*P(Mao Forte)
        p_truco = (p_truco_dado_blefe * prior_blefe) + (p_truco_dado_mao_forte * prior_mao_forte)

        if p_truco == 0:
            return 0.0

        # Teorema de Bayes
        posterior_blefe = (p_truco_dado_blefe * prior_blefe) / p_truco
        return max(0.0, min(1.0, posterior_blefe))
