from typing import Dict, List, Optional
from truco.src.core.carta import Carta
from truco.src.core.constantes import HIERARQUIA, NAIPES, get_valor_manilha


class RuleEngine:
    @staticmethod
    def is_manilha(carta: Carta, vira: Carta) -> bool:
        """Verifica se a carta é uma manilha com base na vira."""
        if vira is None:
            return False
        return carta.valor == get_valor_manilha(vira.valor)

    @classmethod
    def get_forca_carta(cls, carta: Carta, vira: Carta) -> int:
        """
        Retorna a força numérica de uma carta considerando a vira.
        Manilhas: 11 (ouros) a 14 (paus).
        Cartas normais: 1 (4) a 10 (3).
        """
        if cls.is_manilha(carta, vira):
            return 10 + NAIPES[carta.naipe]
        return HIERARQUIA[carta.valor]

    @classmethod
    def comparar_cartas(cls, carta1: Carta, carta2: Carta, vira: Carta) -> int:
        """
        Compara duas cartas. Retorna:
         1 se carta1 > carta2
        -1 se carta1 < carta2
         0 se empatarem
        """
        f1 = cls.get_forca_carta(carta1, vira)
        f2 = cls.get_forca_carta(carta2, vira)
        if f1 > f2:
            return 1
        elif f1 < f2:
            return -1
        return 0

    @classmethod
    def determinar_vencedor_queda(cls, jogadas: Dict[str, Carta], vira: Carta) -> List[str]:
        """
        Determina quem venceu a queda (trick).
        Retorna uma lista com os nomes dos jogadores vencedores.
        Se houver empate (cangará), retorna a lista com múltiplos jogadores (empate).
        """
        if not jogadas:
            return []

        maior_forca = -1
        vencedores = []

        for jogador, carta in jogadas.items():
            forca = cls.get_forca_carta(carta, vira)
            if forca > maior_forca:
                maior_forca = forca
                vencedores = [jogador]
            elif forca == maior_forca:
                vencedores.append(jogador)

        return vencedores

    @staticmethod
    def calcular_pontos_truco(valor_atual: int) -> int:
        """Retorna o próximo valor de aposta após um pedido de Truco."""
        if valor_atual == 1:
            return 3
        elif valor_atual == 3:
            return 6
        elif valor_atual == 6:
            return 9
        elif valor_atual == 9:
            return 12
        return 12

    @classmethod
    def avaliar_forca_mao(cls, mao: List[Carta], vira: Carta) -> Dict[str, float]:
        """Calcula soma, média e maior força das cartas de uma mão."""
        if not mao:
            return {"soma": 0.0, "media": 0.0, "mais_forte": 0.0}
        forcas = [cls.get_forca_carta(c, vira) for c in mao]
        soma = sum(forcas)
        return {
            "soma": float(soma),
            "media": float(soma / len(mao)),
            "mais_forte": float(max(forcas))
        }
