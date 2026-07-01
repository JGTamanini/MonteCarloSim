# 🃏 Truco Paulista — Sistemas Multiagentes

Simulação de **Truco Paulista** desenvolvida como projeto da disciplina de **Inteligência Artificial** do curso de Engenharia de Software — Católica de Santa Catarina.

O projeto implementa os conceitos de **Sistemas Multiagentes (MAS)** por meio de um jogo real: agentes autônomos com percepção, memória, inferência probabilística e tomada de decisão explicável jogam Truco Paulista entre si e contra humanos.

---

## 🚀 Como Rodar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Simulação Monte Carlo (agentes vs agentes)

```bash
# Sempre da raiz do projeto
python -m truco.simulacao.runner
python -m truco.gerar_graficos
```

### Interface Interativa (humano vs IA)

```bash
python -m streamlit run run_demo.py
```

---

## 📁 Estrutura do Código

```
truco/
├── src/
│   ├── constantes.py        # Hierarquia, naipes, SEQUENCIA_VIRA, get_valor_manilha()
│   ├── carta.py             # Carta com get_forca(vira) e is_manilha(vira)
│   ├── baralho.py           # Baralho com vira variável (self.vira após distribuir)
│   ├── mao.py               # Mão do jogador com vira embutida
│   ├── rodada.py            # Lógica de uma queda com determinar_vencedor(vira)
│   ├── partida.py           # Partida completa usada na simulação Monte Carlo
│   │
│   ├── core/                # Arquitetura MAS formal
│   │   ├── constantes.py    # AcoesJogador, RespostasTruco (Enums)
│   │   ├── carta.py         # Carta (camada MAS)
│   │   ├── baralho.py       # Baralho (camada MAS)
│   │   ├── mao.py           # Mão (camada MAS)
│   │   ├── rule_engine.py   # Motor de regras: força de carta, vencedor de queda, pontos de truco
│   │   ├── perception.py    # Perception e PerceptionEngine — visão filtrada do ambiente por agente
│   │   ├── blackboard.py    # Blackboard — memória coletiva e canal de comunicação
│   │   ├── state_machine.py # Máquina de estados do jogo
│   │   └── ambiente.py      # AmbienteJogo — orquestra todos os componentes MAS
│   │
│   ├── agents/              # Agentes MAS
│   │   ├── base_agent.py    # AgenteBase — ciclo percepção → crenças → decisão → ação
│   │   ├── beliefs.py       # BeliefState — representação subjetiva do mundo
│   │   ├── memory.py        # AgentMemory — memória de curto e longo prazo sobre o oponente
│   │   ├── inference.py     # InferenceEngine — probabilidade hipergeométrica e Teorema de Bayes
│   │   ├── decision_engine.py # DecisionEngine — executa estratégia e gera explicação XAI
│   │   ├── communication.py # Message e MessageTypes — protocolo de mensagens entre agentes
│   │   └── concrete_agents.py # Instâncias concretas dos 11 agentes disponíveis
│   │
│   ├── strategies/          # Estratégias injetáveis (padrão Strategy)
│   │   ├── random.py        # Aleatório
│   │   ├── conservative.py  # Conservador (limiar configurável)
│   │   ├── aggressive.py    # Agressivo (chance de blefe configurável)
│   │   ├── probabilistic.py # Probabilístico (estima força das cartas restantes)
│   │   ├── adaptive.py      # Adaptativo (detecta perfil do oponente e ajusta parâmetros)
│   │   ├── bayesian.py      # Bayesiano (Teorema de Bayes explícito para avaliar blefes)
│   │   ├── bluff.py         # Blefador (explora oponentes que costumam correr)
│   │   ├── risk.py          # Avesso ao risco / Buscador de risco
│   │   └── hybrid.py        # Híbrido (alterna estratégias conforme o placar)
│   │
│   ├── events/              # Sistema de eventos pub/sub
│   │   ├── event_bus.py     # EventBus — subscribe/publish desacoplado
│   │   └── events.py        # Tipos de evento: CardPlayed, TrucoRequested, RoundFinished, etc.
│   │
│   └── agentes/             # Agentes da simulação Monte Carlo (camada simples)
│       ├── aleatorio.py
│       ├── conservador.py
│       ├── agressivo.py
│       └── probabilistico.py
│
├── simulacao/
│   └── runner.py            # Executa confrontos, salva CSVs em data/truco/
├── analise/
│   └── graficos.py          # Gera gráficos a partir dos CSVs
├── tests/                   # Testes unitários
└── gerar_graficos.py        # Ponto de entrada para geração de gráficos
```

---

## 🎮 Regras do Truco Paulista

- Baralho de **40 cartas** — 4 naipes × 10 valores (4, 5, 6, 7, J, Q, K, A, 2, 3)
- **3 cartas por jogador**; melhor de 3 quedas por mão; primeiro a **12 pontos** vence
- **Manilhas variáveis por mão:** a vira é revelada após a distribuição e a carta imediatamente superior na sequência circular `4→5→6→7→J→Q→K→A→2→3→4` torna-se a manilha daquela mão
- **Força dos naipes nas manilhas:** ouros (11) < copas (12) < espadas (13) < paus (14)
- **Escalada do Truco:** 1 → 3 → 6 → 9 → 12 pontos

---

## 🤖 Arquitetura MAS

### AmbienteJogo (`core/ambiente.py`)
Orquestra toda a partida. Mantém o estado global (mãos, vira, placar, cartas jogadas) e coordena os agentes via **máquina de estados**:

```
SetupState → DealState → RevealViraState → PlayerTurnState ⇄ TrucoDecisionState → RoundEndState → MatchEndState
```

Cada agente é conectado ao `EventBus` e ao `Blackboard` no momento em que entra no ambiente.

### Blackboard (`core/blackboard.py`)
Memória coletiva compartilhada entre todos os agentes. Armazena:
- **Fatos públicos** — placar, vira, turno ativo, cartas jogadas
- **Perfis de adversários** — usados por agentes cooperativos para compartilhar aprendizado
- **Canal de mensagens** — mensagens assíncronas trocadas entre agentes

### Percepção (`core/perception.py`)
O `PerceptionEngine` gera um objeto `Perception` individualizado para cada agente, garantindo que ele veja apenas **suas próprias cartas** e as informações públicas (cartas jogadas na queda, placar, vira, valor do truco). Isso implementa a **informação assimétrica** do Truco.

### Ciclo BDI — Percepção → Crenças → Decisão → Ação

Cada agente executa este ciclo a cada turno:

1. **Percepção** → recebe `Perception` com estado visível do ambiente
2. **Atualização de crenças** (`BeliefState` + `InferenceEngine`) → calcula força da mão, probabilidade de o oponente ter manilha, probabilidade posterior de blefe
3. **Decisão** (`DecisionEngine` + estratégia) → escolhe entre `JOGAR_CARTA` ou `PEDIR_TRUCO`
4. **Ação** → executa no ambiente e publica evento no `EventBus`

### EventBus (`events/event_bus.py`)
Comunicação desacoplada via **publish/subscribe**. Eventos disponíveis:

| Evento | Quando é disparado |
|---|---|
| `MatchStartedEvent` | Início da partida |
| `RoundStartedEvent` | Nova mão distribuída, vira revelada |
| `CardPlayedEvent` | Jogador joga uma carta |
| `TrucoRequestedEvent` | Jogador pede truco |
| `TrucoAcceptedEvent` | Oponente aceita o truco |
| `TrucoRejectedEvent` | Oponente corre do truco |
| `TrucoRaisedEvent` | Oponente aumenta o truco |
| `QuedaFinishedEvent` | Queda encerrada, vencedor apurado |
| `RoundFinishedEvent` | Mão encerrada, pontos distribuídos |
| `MatchFinishedEvent` | Partida encerrada, vencedor definido |
| `DecisionMadeEvent` | Agente tomou uma decisão (inclui explicação XAI) |

Cada agente assina os eventos relevantes para manter sua memória atualizada automaticamente.

---

## 🧠 Agentes Disponíveis

| Agente | Classe | Estratégia |
|---|---|---|
| **Aleatório** | `AgenteAleatorio` | Decisões ao acaso — baseline de comparação |
| **Conservador** | `AgenteConservador` | Pede truco apenas com força ≥ 8.5; joga a carta mais fraca para economizar |
| **Agressivo** | `AgenteAgressivo` | Blefa com 35% de chance; escala o truco quando tem mão boa |
| **Probabilístico** | `AgenteProbabilistico` | Estima a força média das cartas restantes para decidir truco e carta |
| **Adaptativo** | `AgenteAdaptativo` | Detecta o perfil do oponente (Conservador/Agressivo/Probabilístico) e ajusta limiar de truco e chance de blefe dinamicamente |
| **Bayesiano** | `AgenteBayesiano` | Usa o Teorema de Bayes para calcular P(Blefe\|Truco) e decide com base nisso |
| **Blefador** | `AgenteBlefador` | Explora oponentes com alta taxa de corrida; blefa com 60% de chance quando detecta medo |
| **Avesso ao Risco** | `AgenteRiscoEvitador` | Só pede truco com força ≥ 9.0; foge do confronto para preservar pontos |
| **Buscador de Risco** | `AgenteRiscoBuscador` | Pede truco com força ≥ 5.0; dobra a aposta quando tem mão boa |
| **Híbrido** | `AgenteHibrido` | Alterna entre Conservador, Agressivo e Probabilístico conforme o placar |
| **Cooperativo** | `AgenteCooperativo` | Adaptativo que compartilha e carrega perfis de adversários via Blackboard entre partidas |

---

## 🔍 Inferência Probabilística (`agents/inference.py`)

### Probabilidade Hipergeométrica
Calcula a chance de o oponente ter pelo menos uma manilha, dado o número de cartas restantes no baralho e as já reveladas:

```
P(oponente tem ≥ 1 manilha) = 1 - C(total_ocultas - manilhas_ocultas, k) / C(total_ocultas, k)
```

onde `k` é o número estimado de cartas na mão do oponente.

### Teorema de Bayes
Calcula a probabilidade posterior de blefe dado que o oponente pediu truco:

```
P(Blefe | Truco) = P(Truco | Blefe) × P(Blefe) / P(Truco)
```

O prior `P(Blefe)` é atualizado pela `AgentMemory` ao longo das partidas, tornando a estimativa mais precisa à medida que o agente observa o comportamento do oponente.

---

## 💬 Explicabilidade (XAI)

O `DecisionEngine` gera um `DecisionExplanation` para cada decisão tomada, publicado via `DecisionMadeEvent`:

```
====== EXPLICAÇÃO DA IA (Adaptativo) ======
Decisão: PEDIR_TRUCO
Motivo: Mão forte adaptada. Oponente Conservador detectado: aumentando blefe para 45%.
---------------- MÉTRICAS ----------------
Força da Mão: 9.33
Prob. Manilha Oponente: 72.4%
Prob. Posterior Blefe (Bayes): 18.2%
Perfil Mapeado do Oponente: Conservador
Estratégia Ativa: AdaptiveStrategy
Tempo de Processamento: 0.43 ms
==========================================
```

---

## 📊 Resultados — Simulação Monte Carlo (1000 partidas por confronto)

| Confronto | Vencedor | Taxa |
|---|---|---|
| Conservador vs Aleatório | Conservador | ~82% |
| Agressivo vs Aleatório | Agressivo | ~75% |
| Conservador vs Agressivo | Conservador | ~61% |
| Probabilístico vs Agressivo | Probabilístico | ~84% |
| Probabilístico vs Conservador | Probabilístico | ~99% |
| Probabilístico vs Aleatório | Probabilístico | ~93% |

---

## 👥 Equipe

Engenharia de Software — 7ª fase | Católica de Santa Catarina

Eric Gabriel Caetano · Felipe da Silva Chawischi · Gabriel Felipe Alves Bandoch · João Guilherme T. Dalmarco

**Disciplina:** Inteligência Artificial — Prof. Claudinei Dias (Ney)
