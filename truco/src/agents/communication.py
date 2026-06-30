import time
import uuid
from typing import Any, Dict


class Message:
    """Classe que representa uma mensagem formal enviada entre agentes."""

    def __init__(self, remetente: str, destinatario: str, tipo: str, conteudo: Dict[str, Any], message_id: str = None):
        self.message_id = message_id or str(uuid.uuid4())
        self.remetente = remetente
        self.destinatario = destinatario
        self.tipo = tipo  # ex: "REQUEST_TRUCO", "ACCEPT_TRUCO", "REJECT_TRUCO", "RAISE_TRUCO", "COOPERATE_PROFILE"
        self.conteudo = conteudo or {}
        self.timestamp = time.time()

    def __str__(self):
        return f"[Msg] {self.remetente} -> {self.destinatario} | Tipo: {self.tipo} | Conteúdo: {self.conteudo}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "remetente": self.remetente,
            "destinatario": self.destinatario,
            "tipo": self.tipo,
            "conteudo": self.conteudo,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> 'Message':
        msg = Message(
            remetente=d["remetente"],
            destinatario=d["destinatario"],
            tipo=d["tipo"],
            conteudo=d["conteudo"],
            message_id=d["message_id"]
        )
        msg.timestamp = d["timestamp"]
        return msg


# Tipos formais de mensagem do protocolo de Truco
class MessageTypes:
    REQUEST_TRUCO = "REQUEST_TRUCO"
    ACCEPT_TRUCO = "ACCEPT_TRUCO"
    REJECT_TRUCO = "REJECT_TRUCO"
    RAISE_TRUCO = "RAISE_TRUCO"
    COOPERATE_PROFILE = "COOPERATE_PROFILE"
