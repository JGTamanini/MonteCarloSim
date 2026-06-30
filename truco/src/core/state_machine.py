from abc import ABC, abstractmethod
import logging
from typing import Dict, List, Optional
from truco.src.core.constantes import AcoesJogador, RespostasTruco
from truco.src.core.rule_engine import RuleEngine
from truco.src.events import events

logger = logging.getLogger("StateMachine")


class JogoState(ABC):
    @abstractmethod
    def entrar(self, ambiente: 'AmbienteJogo'):
        pass

    @abstractmethod
    def processar(self, ambiente: 'AmbienteJogo'):
        pass

    @abstractmethod
    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class SetupState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        logger.info("Entrando no estado de Configuração (SetupState).")
        ambiente.placar_partida = {j.nome: 0 for j in ambiente.agentes}
        ambiente.numero_mao = 0
        ambiente.historico_rodadas = []
        ambiente.blackboard.limpar_quadro()
        ambiente.blackboard.registrar_fato("placar", ambiente.placar_partida)

    def processar(self, ambiente: 'AmbienteJogo'):
        agente_nomes = [j.nome for j in ambiente.agentes]
        ambiente.event_bus.publish(events.MatchStartedEvent(agente_nomes[0], agente_nomes[1]))
        # Escolhe jogador inicial (aleatório ou o primeiro)
        ambiente.jogador_ativo_idx = 0
        ambiente.definir_estado(DealState())

    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class DealState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        logger.info(f"Entrando no estado de Distribuição de Cartas (DealState) para a mão {ambiente.numero_mao + 1}.")
        ambiente.numero_mao += 1
        # Distribui cartas
        distribuicao, vira = ambiente.baralho.distribuir(len(ambiente.agentes), 3)
        ambiente.vira = vira
        ambiente.maos_jogadores = {
            j.nome: distribuicao[i] for i, j in enumerate(ambiente.agentes)
        }
        ambiente.blackboard.registrar_fato("vira", vira)
        ambiente.blackboard.registrar_fato("numero_mao", ambiente.numero_mao)

    def processar(self, ambiente: 'AmbienteJogo'):
        ambiente.definir_estado(RevealViraState())

    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class RevealViraState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        logger.info(f"Vira revelado: {ambiente.vira}")
        ambiente.event_bus.publish(events.RoundStartedEvent(ambiente.numero_mao, ambiente.vira))

        # Configura as variáveis do round
        ambiente.cartas_jogadas_queda = {}
        ambiente.vencedores_quedas = []
        ambiente.valor_truco_atual = 1
        ambiente.proponente_truco = None
        ambiente.truco_pedido_nesta_mao = False
        ambiente.numero_queda_atual = 1

    def processar(self, ambiente: 'AmbienteJogo'):
        ambiente.definir_estado(PlayerTurnState())

    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class PlayerTurnState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        # Garante que o blackboard sabe quem é o jogador ativo
        jogador = ambiente.obter_jogador_ativo()
        ambiente.blackboard.registrar_fato("jogador_ativo", jogador.nome)
        ambiente.blackboard.registrar_fato("cartas_jogadas_queda", ambiente.cartas_jogadas_queda)
        ambiente.blackboard.registrar_fato("valor_truco", ambiente.valor_truco_atual)

    def processar(self, ambiente: 'AmbienteJogo'):
        jogador = ambiente.obter_jogador_ativo()
        percepcao = ambiente.gerar_percepcao_para(jogador)

        # Pergunta ao jogador qual ação ele deseja tomar
        # Ele pode pedir truco se ainda não houver um pedido de truco pendente por ele
        # E se o valor do truco atual for menor que 12.
        pode_pedir_truco = (
            not ambiente.truco_pedido_nesta_mao or 
            ambiente.proponente_truco != jogador.nome
        ) and ambiente.valor_truco_atual < 12

        acao, detalhe = jogador.decidir_acao(percepcao, pode_pedir_truco)

        if acao == AcoesJogador.PEDIR_TRUCO:
            # Transiciona para o estado de decisão de Truco
            ambiente.proponente_truco = jogador.nome
            ambiente.jogador_decidindo_idx = (ambiente.jogador_ativo_idx + 1) % len(ambiente.agentes)
            ambiente.truco_pedido_nesta_mao = True
            proximo_valor = RuleEngine.calcular_pontos_truco(ambiente.valor_truco_atual)
            ambiente.valor_truco_proposto = proximo_valor

            ambiente.event_bus.publish(events.TrucoRequestedEvent(jogador.nome, proximo_valor))
            # O outro jogador responde
            ambiente.definir_estado(TrucoDecisionState())

        elif acao == AcoesJogador.JOGAR_CARTA:
            carta_jogada = detalhe
            # Remove a carta da mão do jogador
            jogador_mao = ambiente.maos_jogadores[jogador.nome]
            # Remove a carta
            for c in list(jogador_mao):
                if c.valor == carta_jogada.valor and c.naipe == carta_jogada.naipe:
                    jogador_mao.remove(c)
                    break

            ambiente.cartas_jogadas_queda[jogador.nome] = carta_jogada
            ambiente.event_bus.publish(events.CardPlayedEvent(jogador.nome, carta_jogada))

            # Verifica se todos os jogadores jogaram nesta queda
            if len(ambiente.cartas_jogadas_queda) == len(ambiente.agentes):
                ambiente.definir_estado(RoundEndState())
            else:
                # Passa a vez para o próximo jogador
                ambiente.alternar_jogador_ativo()
                # Mantém no PlayerTurnState, mas chama entrar de novo
                self.entrar(ambiente)

    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class TrucoDecisionState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        # O jogador que deve responder é o indicado por jogador_decidindo_idx
        decidindo = ambiente.agentes[ambiente.jogador_decidindo_idx]
        logger.info(f"Jogador {decidindo.nome} deve decidir sobre o Truco valendo {ambiente.valor_truco_proposto}.")

    def processar(self, ambiente: 'AmbienteJogo'):
        decidindo = ambiente.agentes[ambiente.jogador_decidindo_idx]
        percepcao = ambiente.gerar_percepcao_para(decidindo)

        resposta = decidindo.responder_truco_proposto(percepcao, ambiente.valor_truco_proposto)

        if resposta == RespostasTruco.ACEITAR:
            ambiente.valor_truco_atual = ambiente.valor_truco_proposto
            ambiente.event_bus.publish(events.TrucoAcceptedEvent(decidindo.nome, ambiente.valor_truco_atual))
            # Retorna para o turno do jogador que jogaria (mantém o jogador_ativo_idx original)
            ambiente.definir_estado(PlayerTurnState())

        elif resposta == RespostasTruco.CORRER:
            # O adversário correu, o proponente ganha a mão
            vencedor = ambiente.proponente_truco
            ambiente.event_bus.publish(events.TrucoRejectedEvent(decidindo.nome))

            # Registra o vencedor da mão
            ambiente.vencedor_mao_truco_corrido = vencedor
            ambiente.definir_estado(RoundEndState())

        elif resposta == RespostasTruco.AUMENTAR:
            # Propõe um novo aumento (ex: se era 3, vai para 6)
            velho_valor = ambiente.valor_truco_proposto
            novo_valor = RuleEngine.calcular_pontos_truco(velho_valor)
            ambiente.valor_truco_proposto = novo_valor
            ambiente.proponente_truco = decidindo.nome  # Quem aumentou agora é o proponente

            ambiente.event_bus.publish(events.TrucoRaisedEvent(decidindo.nome, velho_valor, novo_valor))

            # Altera quem decide: agora o outro jogador responderá
            ambiente.jogador_decidindo_idx = (ambiente.jogador_decidindo_idx + 1) % len(ambiente.agentes)
            # Chama entrar novamente com a nova configuração de decisão
            self.entrar(ambiente)

    def sair(self, ambiente: 'AmbienteJogo'):
        pass


class RoundEndState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        logger.info("Entrando no estado de Fim de Queda/Rodada (RoundEndState).")

    def processar(self, ambiente: 'AmbienteJogo'):
        # Verifica se a mão foi decidida por alguém correndo de um Truco
        if hasattr(ambiente, 'vencedor_mao_truco_corrido') and ambiente.vencedor_mao_truco_corrido is not None:
            vencedor = ambiente.vencedor_mao_truco_corrido
            ambiente.vencedor_mao_truco_corrido = None
            self._finalizar_mao(ambiente, vencedor)
            return

        # Caso contrário, avalia a queda atual
        jogadas = ambiente.cartas_jogadas_queda
        vencedores = RuleEngine.determinar_vencedor_queda(jogadas, ambiente.vira)

        vencedor_queda = "Empate"
        if len(vencedores) == 1:
            vencedor_queda = vencedores[0]

        ambiente.vencedores_quedas.append(vencedor_queda)
        ambiente.event_bus.publish(events.QuedaFinishedEvent(ambiente.numero_queda_atual, vencedor_queda, jogadas))

        # Determina se a mão acabou
        vencedor_mao = self._verificar_vencedor_mao(ambiente.vencedores_quedas)

        if vencedor_mao is not None:
            # Mão encerrada
            self._finalizar_mao(ambiente, vencedor_mao)
        else:
            # Mão continua, prepara próxima queda
            ambiente.numero_queda_atual += 1
            ambiente.cartas_jogadas_queda = {}

            # Quem venceu a queda joga primeiro na próxima
            if vencedor_queda != "Empate":
                for idx, j in enumerate(ambiente.agentes):
                    if j.nome == vencedor_queda:
                        ambiente.jogador_ativo_idx = idx
                        break
            # Se empatar, quem jogou primeiro na queda anterior continua jogando primeiro (mantém jogador_ativo_idx)

            ambiente.definir_estado(PlayerTurnState())

    def sair(self, ambiente: 'AmbienteJogo'):
        pass

    def _verificar_vencedor_mao(self, vencedores_quedas: List[str]) -> Optional[str]:
        # Se algum jogador já venceu 2 quedas, ele ganhou
        for jogador in set(vencedores_quedas) - {"Empate"}:
            if vencedores_quedas.count(jogador) >= 2:
                return jogador

        n = len(vencedores_quedas)
        if n == 2:
            q1, q2 = vencedores_quedas[0], vencedores_quedas[1]
            if q1 != "Empate" and q2 == "Empate":
                return q1
            if q1 == "Empate" and q2 != "Empate":
                return q2
        elif n == 3:
            q1, q2, q3 = vencedores_quedas[0], vencedores_quedas[1], vencedores_quedas[2]
            if q3 != "Empate":
                return q3
            else: # Se a terceira empatar, quem ganhou a primeira ganha a mão
                if q1 != "Empate":
                    return q1
                # Se todas empataram, quem começou a rodada ganha (ou empate total)
                return "Empate"
        return None

    def _finalizar_mao(self, ambiente: 'AmbienteJogo', vencedor: str):
        pontos = ambiente.valor_truco_atual

        if vencedor == "Empate":
            logger.info("Mão finalizada em empate total. Ninguém pontua.")
            # Ninguém pontua
            vencedor_nome = "Ninguém"
        else:
            # Atribui pontos
            ambiente.placar_partida[vencedor] += pontos
            logger.info(f"Mão {ambiente.numero_mao} finalizada. Vencedor: {vencedor} (+{pontos} pts).")
            vencedor_nome = vencedor

        ambiente.blackboard.registrar_fato("placar", ambiente.placar_partida)
        ambiente.event_bus.publish(
            events.RoundFinishedEvent(
                ambiente.numero_mao,
                vencedor_nome,
                pontos if vencedor != "Empate" else 0,
                ambiente.placar_partida
            )
        )

        # Registra no histórico
        ambiente.historico_rodadas.append({
            "numero_mao": ambiente.numero_mao,
            "vencedor": vencedor_nome,
            "pontos": pontos if vencedor != "Empate" else 0,
            "placar_fim": dict(ambiente.placar_partida),
            "vencedores_quedas": list(ambiente.vencedores_quedas),
            "valor_truco": ambiente.valor_truco_atual
        })

        # Verifica fim de partida (12 pontos)
        fim_de_jogo = False
        vencedor_partida = None
        for jogador, pts in ambiente.placar_partida.items():
            if pts >= 12:
                fim_de_jogo = True
                vencedor_partida = jogador
                break

        if fim_de_jogo:
            ambiente.vencedor_partida = vencedor_partida
            ambiente.definir_estado(MatchEndState())
        else:
            # Alterna quem distribui/começa na próxima mão
            # Normalmente, reveza o dealer
            ambiente.jogador_ativo_idx = (ambiente.numero_mao) % len(ambiente.agentes)
            ambiente.definir_estado(DealState())


class MatchEndState(JogoState):
    def entrar(self, ambiente: 'AmbienteJogo'):
        logger.info(f"Partida finalizada! Vencedor da partida: {ambiente.vencedor_partida}")

    def processar(self, ambiente: 'AmbienteJogo'):
        # Dispara evento final
        ambiente.event_bus.publish(events.MatchFinishedEvent(ambiente.vencedor_partida, ambiente.placar_partida))

    def sair(self, ambiente: 'AmbienteJogo'):
        pass
