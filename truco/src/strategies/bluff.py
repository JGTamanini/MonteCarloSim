import random
from typing import Any, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine


class BluffStrategy:
    def escolher_acao(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        pode_pedir_truco: bool
    ) -> Tuple[AcoesJogador, Any, str]:
        forca = beliefs.forca_mao_propria
        taxa_corrida_op = memory.obter_taxa_corrida_oponente()

        # Se o adversário costuma correr muito (>35% das vezes), blefamos agressivamente
        if pode_pedir_truco:
            if taxa_corrida_op > 0.35 and forca < 5.0 and random.random() < 0.60:
                return AcoesJogador.PEDIR_TRUCO, None, (
                    f"Explorando oponente amedrontado (taxa de corrida: {taxa_corrida_op * 100:.1f}%). "
                    f"Peticionando blefe tático com mão fraca (força: {forca:.2f})."
                )
            elif forca >= 6.5:
                return AcoesJogador.PEDIR_TRUCO, None, f"Pedindo Truco legítimo com mão forte (força: {forca:.2f})."

        # Joga a carta mais forte para simular força
        cartas_ordenadas = sorted(percepcao.mao_cartas, key=lambda c: RuleEngine.get_forca_carta(c, percepcao.vira), reverse=True)
        carta = cartas_ordenadas[0]
        return AcoesJogador.JOGAR_CARTA, carta, f"Jogando a carta mais forte ({carta}) para simular posse de manilhas."

    def responder_truco(
        self,
        agente: Any,
        percepcao: Perception,
        beliefs: Any,
        memory: Any,
        valor_proposto: int
    ) -> Tuple[RespostasTruco, str]:
        forca = beliefs.forca_mao_propria

        # Blefador sabe blefar, mas é cauteloso ao receber truco alheio
        if forca >= 7.0:
            return RespostasTruco.ACEITAR, f"Mão forte ({forca:.2f} >= 7.0). Aceita truco do oponente."
        return RespostasTruco.CORRER, f"Mão fraca/média ({forca:.2f} < 7.0). Prefere correr para não entregar pontos em blefes alheios."
