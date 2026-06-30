import logging
from typing import Any, Dict, List, Tuple
from truco.src.core.ambiente import AmbienteJogo
from truco.src.events.event_bus import EventBus
from truco.src.simulation.statistics import StatisticsTracker

logger = logging.getLogger("Simulator")


class Simulator:
    def __init__(self, agentes: List[Any]):
        self.agentes = agentes

    def rodar(self, n_partidas: int) -> Dict[str, Any]:
        """
        Executa um lote de N partidas entre os agentes configurados.
        Coleta e consolida as estatísticas globais das execuções.
        """
        logger.info(f"Iniciando simulação de {n_partidas} partidas entre {[a.nome for a in self.agentes]}...")

        # Instancia o barramento de eventos compartilhado para a simulação
        event_bus = EventBus()
        tracker = StatisticsTracker(event_bus)

        for i in range(n_partidas):
            # Cria um novo ambiente de jogo a cada partida, passando os agentes e o barramento
            # O construtor do AmbienteJogo registra os listeners de evento de cada agente
            # Nota: recriamos o barramento a cada partida ou limpamos os ouvintes temporários dos agentes
            # para evitar vazamento de memória e acúmulo de listeners.
            partida_bus = EventBus()
            partida_tracker = StatisticsTracker(partida_bus)

            # Transfere os dados acumulados do tracker global para o local ou vice-versa
            # Melhor: usamos um único event_bus global, mas limpamos os ouvintes específicos da partida
            # ou deixamos que o tracker global escute todos os eventos.
            # Vamos usar o event_bus global e apenas re-instanciar o baralho e o estado no ambiente!
            # Para evitar que os listeners dos agentes se acumulem, re-registramos no construtor.
            # Limpamos os listeners antigos do event_bus antes de iniciar a nova partida se necessário,
            # mas como os agentes e o tracker são os mesmos, podemos apenas reutilizar o event_bus global!
            pass

        # Abordagem limpa:
        # Reutilizamos o event_bus e o tracker global. A cada partida, apenas reiniciamos a máquina de estados.
        event_bus = EventBus()
        tracker = StatisticsTracker(event_bus)

        for i in range(n_partidas):
            logger.debug(f"Rodando partida {i + 1} de {n_partidas}...")
            # Recria o ambiente para resetar o Blackboard e o Baralho, mas com o mesmo barramento e agentes
            ambiente = AmbienteJogo(self.agentes, event_bus)
            ambiente.jogar_partida()

        resumo = tracker.obter_resumo()
        logger.info(f"Simulação concluída! Resultados: {resumo['vitorias']}")
        return resumo
