import logging
from typing import Any, Dict, Tuple
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.perception import Perception
from truco.src.core.rule_engine import RuleEngine
from truco.src.agents.beliefs import BeliefState
from truco.src.agents.decision_engine import DecisionEngine, DecisionExplanation
from truco.src.agents.inference import InferenceEngine
from truco.src.agents.memory import AgentMemory
from truco.src.events import events
from truco.src.events.event_bus import EventBus

logger = logging.getLogger("AgenteBase")


class AgenteBase:
    def __init__(self, nome: str, estrategia: Any, cooperativo: bool = False):
        self.nome = nome
        self.estrategia = estrategia
        self.cooperativo = cooperativo
        self.memory = AgentMemory(nome)
        self.beliefs = BeliefState()
        self.last_explanation: Optional[DecisionExplanation] = None
        self.blackboard = None
        self.event_bus = None

    def conectar_ambiente(self, event_bus: EventBus, blackboard: Any):
        """Conecta o agente ao barramento de eventos e ao blackboard."""
        self.event_bus = event_bus
        self.blackboard = blackboard

        # Inscreve-se nos eventos para manter sua memória atualizada
        self.event_bus.subscribe(events.CardPlayedEvent, self._on_card_played)
        self.event_bus.subscribe(events.TrucoRequestedEvent, self._on_truco_requested)
        self.event_bus.subscribe(events.TrucoAcceptedEvent, self._on_truco_accepted)
        self.event_bus.subscribe(events.TrucoRejectedEvent, self._on_truco_rejected)
        self.event_bus.subscribe(events.TrucoRaisedEvent, self._on_truco_raised)
        self.event_bus.subscribe(events.RoundStartedEvent, self._on_round_started)
        self.event_bus.subscribe(events.RoundFinishedEvent, self._on_round_finished)
        self.event_bus.subscribe(events.MatchFinishedEvent, self._on_match_finished)

        # Se for cooperativo, tenta ler perfil pré-existente do oponente no Blackboard
        # Isso simula o compartilhamento de conhecimento entre agentes de confrontos passados
        self._carregar_conhecimento_cooperativo()

    def _carregar_conhecimento_cooperativo(self):
        if self.cooperativo and self.blackboard:
            # Assumimos que o oponente é o outro agente (descobriremos o nome na primeira percepção ou no início)
            # Para carregar, buscamos perfis disponíveis no blackboard
            perfis = self.blackboard.to_dict().get("public_facts", {})
            # Procuramos por chaves de perfil de oponente
            for chave, dados in perfis.items():
                if chave.startswith("perfil_"):
                    oponente_nome = chave.replace("perfil_", "")
                    if oponente_nome != self.nome:
                        logger.info(f"[{self.nome}] Carregando perfil cooperativo de {oponente_nome} do Blackboard.")
                        self.memory.blefes_confirmados_oponente = dados.get("blefes", 0)
                        self.memory.total_trucos_pedidos_oponente = dados.get("trucos_pedidos", 0)
                        self.memory.total_trucos_recebidos_oponente = dados.get("trucos_recebidos", 0)
                        self.memory.trucos_aceitos_oponente = dados.get("trucos_aceitos", 0)
                        self.memory.trucos_corridos_oponente = dados.get("trucos_corridos", 0)
                        self.memory.trucos_aumentados_oponente = dados.get("trucos_aumentados", 0)

    def _salvar_conhecimento_cooperativo(self):
        if self.cooperativo and self.blackboard:
            # Encontra o nome do oponente nos registros de jogadas ou histórico
            # Registra no Blackboard o perfil que construímos sobre ele
            oponente_nome = None
            for jogada in self.memory.cartas_jogadas_na_mao:
                if jogada["jogador"] != self.nome:
                    oponente_nome = jogada["jogador"]
                    break

            if oponente_nome:
                logger.info(f"[{self.nome}] Salvando conhecimento cooperativo sobre {oponente_nome} no Blackboard.")
                dados_perfil = {
                    "blefes": self.memory.blefes_confirmados_oponente,
                    "trucos_pedidos": self.memory.total_trucos_pedidos_oponente,
                    "trucos_recebidos": self.memory.total_trucos_recebidos_oponente,
                    "trucos_aceitos": self.memory.trucos_aceitos_oponente,
                    "trucos_corridos": self.memory.trucos_corridos_oponente,
                    "trucos_aumentados": self.memory.trucos_aumentados_oponente,
                    "perfil_estimado": self.memory.obter_perfil_estimado_oponente()
                }
                self.blackboard.registrar_perfil_adversario(oponente_nome, dados_perfil)

    def atualizar_crencas(self, percepcao: Perception):
        """Atualiza a representação interna (Beliefs) baseada na percepção atual."""
        self.beliefs.atualizar_crencas(percepcao, self.memory)

        # 1. Calcula força da própria mão
        forca_info = RuleEngine.avaliar_forca_mao(percepcao.mao_cartas, percepcao.vira)
        self.beliefs.forca_mao_propria = forca_info["media"]

        # 2. Reconstrói as cartas restantes ocultas no baralho
        cartas_reveladas = self.memory.cartas_reveladas
        cartas_restantes = InferenceEngine.obter_cartas_restantes(
            percepcao.mao_cartas, percepcao.vira, cartas_reveladas
        )
        self.beliefs.cartas_restantes = cartas_restantes

        # 3. Calcula probabilidade do oponente ter pelo menos uma manilha
        # Conta quantas cartas o oponente tem em mãos baseado nas quedas já concluídas
        oponente_nome = [n for n in percepcao.placar_partida.keys() if n != self.nome][0]
        oponente_jogou_na_queda_atual = oponente_nome in percepcao.cartas_jogadas_queda
        quedas_concluidas = sum(percepcao.quedas_vencidas.values())
        
        cartas_oponente_em_mao = 3 - quedas_concluidas - (1 if oponente_jogou_na_queda_atual else 0)
        cartas_oponente_em_mao = max(1, cartas_oponente_em_mao)

        self.beliefs.probabilidade_manilha_oponente = InferenceEngine.calcular_probabilidade_manilha_oponente(
            cartas_restantes, percepcao.vira, cartas_oponente_em_mao
        )

        # 4. Calcula chance posterior de blefe do oponente usando Teorema de Bayes
        oponente_pediu_truco = (
            percepcao.valor_truco_atual > 1 and 
            self.blackboard.obter_fato("jogador_ativo") != self.nome
        )
        self.beliefs.chance_blefe_oponente = InferenceEngine.calcular_probabilidade_posterior_blefe_bayes(
            self.memory, oponente_pediu_truco
        )

    def decidir_acao(self, percepcao: Perception, pode_pedir_truco: bool) -> Tuple[AcoesJogador, Any]:
        """Tomada de decisão ativa do agente."""
        acao, detalhe, expl = DecisionEngine.processar_decisao_acao(self, percepcao, pode_pedir_truco)
        self.last_explanation = expl
        if self.event_bus:
            self.event_bus.publish(events.DecisionMadeEvent(
                jogador=self.nome,
                decisao=expl.decisao,
                forca_mao=expl.forca_mao,
                tempo_ms=expl.tempo_gasto_ms,
                motivo=expl.motivo,
                estrategia=expl.estrategia_ativa
            ))
        return acao, detalhe

    def responder_truco_proposto(self, percepcao: Perception, valor_proposto: int) -> RespostasTruco:
        """Tomada de decisão reativa (responder truco)."""
        resposta, expl = DecisionEngine.processar_decisao_resposta_truco(self, percepcao, valor_proposto)
        self.last_explanation = expl
        if self.event_bus:
            self.event_bus.publish(events.DecisionMadeEvent(
                jogador=self.nome,
                decisao=expl.decisao,
                forca_mao=expl.forca_mao,
                tempo_ms=expl.tempo_gasto_ms,
                motivo=expl.motivo,
                estrategia=expl.estrategia_ativa
            ))
        return resposta

    # Eventos Handlers
    def _on_card_played(self, event: events.CardPlayedEvent):
        self.memory.registrar_carta_jogada(event.jogador, event.carta)

    def _on_truco_requested(self, event: events.TrucoRequestedEvent):
        self.memory.registrar_pedido_truco(event.jogador, event.valor_proposto)

    def _on_truco_accepted(self, event: events.TrucoAcceptedEvent):
        self.memory.registrar_resposta_truco(event.jogador, "aceitar", event.novo_valor)

    def _on_truco_rejected(self, event: events.TrucoRejectedEvent):
        self.memory.registrar_resposta_truco(event.jogador, "correr", self.beliefs.valor_aposta_atual)

    def _on_truco_raised(self, event: events.TrucoRaisedEvent):
        self.memory.registrar_resposta_truco(event.jogador, "aumentar", event.valor_proposto)

    def _on_round_started(self, event: events.RoundStartedEvent):
        self.memory.reset_curto_prazo()

    def _on_round_finished(self, event: events.RoundFinishedEvent):
        # Ao final de cada mão, avaliamos se houve blefe
        # Se ganhamos sem ver a mão deles (correram), ou se revelaram as cartas no final
        # e a força era baixa, registramos blefe
        # Se o oponente pediu truco mas a força final dele revelada era baixa (< 5.0)
        # isso é um blefe confirmado.
        # Para fins de simplicidade, se ele ganhou ou perdeu mostrando cartas, comparamos.
        pass

    def _on_match_finished(self, event: events.MatchFinishedEvent):
        self.memory.partidas_jogadas += 1
        if event.vencedor == self.nome:
            self.memory.vitorias += 1
        else:
            self.memory.derrotas += 1

        # Ao final da partida, compartilha aprendizado no Blackboard se for cooperativo
        self._salvar_conhecimento_cooperativo()
