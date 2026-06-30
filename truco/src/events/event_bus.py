import logging
from typing import Callable, Dict, List, Type
from truco.src.events.events import JogoEvent

logger = logging.getLogger("EventBus")


class EventBus:
    def __init__(self):
        self._listeners: Dict[Type[JogoEvent], List[Callable[[JogoEvent], None]]] = {}

    def subscribe(self, event_type: Type[JogoEvent], callback: Callable[[JogoEvent], None]):
        """Inscreve um callback para ser chamado quando um evento do tipo event_type ocorrer."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
            logger.debug(f"Callback {callback.__name__} inscrito em {event_type.__name__}")

    def unsubscribe(self, event_type: Type[JogoEvent], callback: Callable[[JogoEvent], None]):
        """Desinscreve um callback de um tipo de evento."""
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            logger.debug(f"Callback {callback.__name__} desinscrito de {event_type.__name__}")

    def publish(self, event: JogoEvent):
        """Dispara um evento para todos os ouvintes registrados."""
        event_type = type(event)
        # Notifica ouvintes específicos do tipo de evento
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Erro ao processar callback {callback} para o evento {event_type.__name__}: {e}")

        # Opcionalmente, notifica ouvintes genéricos (se houver interesse no futuro)
        if JogoEvent in self._listeners and event_type != JogoEvent:
            for callback in self._listeners[JogoEvent]:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Erro ao processar callback genérico para o evento {event_type.__name__}: {e}")
