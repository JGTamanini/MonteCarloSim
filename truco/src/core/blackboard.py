import time
from typing import Any, Dict, List


class Blackboard:
    def __init__(self):
        self._public_facts: Dict[str, Any] = {}
        self._opponent_profiles: Dict[str, Dict[str, Any]] = {}
        self._messages: List[Dict[str, Any]] = []

    def registrar_fato(self, chave: str, valor: Any):
        """Registra ou atualiza um fato público no Blackboard."""
        self._public_facts[chave] = valor

    def obter_fato(self, chave: str, padrao: Any = None) -> Any:
        """Obtém um fato público registrado."""
        return self._public_facts.get(chave, padrao)

    def registrar_perfil_adversario(self, nome_adversario: str, perfil: Dict[str, Any]):
        """
        Registra ou mescla informações de perfil de um adversário.
        Permite a cooperação e compartilhamento de conhecimento entre agentes.
        """
        if nome_adversario not in self._opponent_profiles:
            self._opponent_profiles[nome_adversario] = {}
        self._opponent_profiles[nome_adversario].update(perfil)

    def obter_perfil_adversario(self, nome_adversario: str) -> Dict[str, Any]:
        """Recupera o perfil compartilhado de um adversário."""
        return self._opponent_profiles.get(nome_adversario, {})

    def postar_mensagem(self, remetente: str, destinatario: str, tipo_mensagem: str, conteudo: Dict[str, Any]):
        """Registra uma mensagem enviada por um agente no quadro de comunicações."""
        self._messages.append({
            "remetente": remetente,
            "destinatario": destinatario,
            "tipo": tipo_mensagem,
            "conteudo": conteudo,
            "timestamp": time.time()
        })

    def obter_mensagens(self, destinatario: str) -> List[Dict[str, Any]]:
        """Recupera todas as mensagens enviadas para um determinado agente."""
        return [msg for msg in self._messages if msg["destinatario"] == destinatario]

    def limpar_mensagens(self):
        """Limpa as mensagens ativas do canal de comunicação."""
        self._messages.clear()

    def limpar_quadro(self):
        """Zera todos os dados armazenados no Blackboard."""
        self._public_facts.clear()
        self._opponent_profiles.clear()
        self._messages.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Retorna uma cópia dos dados públicos do Blackboard."""
        return {
            "public_facts": dict(self._public_facts),
            "messages": list(self._messages)
        }
