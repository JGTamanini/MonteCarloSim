# 🏆 Relatório do Torneio Multiagentes — Truco Paulista

Este relatório resume o desempenho de 10 estratégias distintas de agentes simuladas em um campeonato todos-contra-todos, com **200 partidas** por confronto.

## 📊 1. Classificação Geral

| Posição | Agente / Estratégia | Pontos Acumulados |
|:---:|:---|:---:|
| 1º | **Conservador** | 14 |
| 2º | **Probabilístico** | 14 |
| 3º | **Adaptativo** | 14 |
| 4º | **Híbrido** | 12 |
| 5º | **Bayesiano** | 11 |
| 6º | **Agressivo** | 7 |
| 7º | **Blefador** | 7 |
| 8º | **RiscoBuscador** | 6 |
| 9º | **RiscoEvitador** | 5 |
| 10º | **Aleatório** | 0 |

*(Critério: Vitória no confronto = 2 pts, Empate = 1 pt, Derrota = 0 pts)*

## ⚔️ 2. Matriz de Confrontos Diretos (Win Rates %)

Exibe a taxa de vitória do agente da linha (Agente) contra o agente da coluna (Oponente).

| Agente \ Oponente | Aleatório | Conservador | Agressivo | Probabilístico | Adaptativo | Blefador | Bayesiano | RiscoEvitador | RiscoBuscador | Híbrido |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Aleatório** | - | 25.5% | 37.5% | 29.5% | 24.5% | 21.5% | 23.5% | 22.0% | 26.5% | 30.5% |
| **Conservador** | 74.5% | - | 50.5% | 40.0% | 53.0% | 58.0% | 50.5% | 52.0% | 53.0% | 37.5% |
| **Agressivo** | 62.5% | 49.5% | - | 45.5% | 32.5% | 62.5% | 50.0% | 46.0% | 55.5% | 38.5% |
| **Probabilístico** | 70.5% | 60.0% | 54.5% | - | 19.0% | 47.5% | 58.5% | 69.0% | 72.0% | 53.0% |
| **Adaptativo** | 75.5% | 47.0% | 67.5% | 81.0% | - | 50.0% | 66.5% | 50.0% | 75.5% | 74.0% |
| **Blefador** | 78.5% | 42.0% | 37.5% | 52.5% | 50.0% | - | 44.5% | 51.5% | 45.0% | 40.0% |
| **Bayesiano** | 76.5% | 49.5% | 50.0% | 41.5% | 33.5% | 55.5% | - | 57.5% | 53.5% | 52.0% |
| **RiscoEvitador** | 78.0% | 48.0% | 54.0% | 31.0% | 50.0% | 48.5% | 42.5% | - | 47.5% | 36.0% |
| **RiscoBuscador** | 73.5% | 47.0% | 44.5% | 28.0% | 24.5% | 55.0% | 46.5% | 52.5% | - | 37.0% |
| **Híbrido** | 69.5% | 62.5% | 61.5% | 47.0% | 26.0% | 60.0% | 48.0% | 64.0% | 63.0% | - |

## ⚙️ 3. Métricas de Tomada de Decisão e Comportamento

| Agente / Estratégia | Tempo Médio (ms) | Força Média da Mão | Trucos Pedidos | Blefes Tentados | Sucessos | Taxa Sucesso Blefe |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Aleatório** | 0.02 ms | 6.19 | 3465 | 1300 | 943 | 72.5% |
| **Conservador** | 0.02 ms | 7.34 | 8499 | 0 | 0 | 0.0% |
| **Agressivo** | 0.02 ms | 5.62 | 10928 | 2623 | 1794 | 68.4% |
| **Probabilístico** | 0.04 ms | 6.01 | 4913 | 0 | 0 | 0.0% |
| **Adaptativo** | 0.02 ms | 5.93 | 9768 | 2209 | 1575 | 71.3% |
| **Blefador** | 0.02 ms | 5.76 | 12001 | 3883 | 2717 | 70.0% |
| **Bayesiano** | 0.02 ms | 6.14 | 8507 | 0 | 0 | 0.0% |
| **RiscoEvitador** | 0.02 ms | 7.37 | 7656 | 0 | 0 | 0.0% |
| **RiscoBuscador** | 0.02 ms | 5.51 | 8169 | 1531 | 999 | 65.3% |
| **Híbrido** | 0.03 ms | 6.15 | 5902 | 208 | 134 | 64.4% |

## 💡 4. Análise e Conclusões Científicas (MAS)

1. **Dominância da Estratégia**: A estratégia **Conservador** consagrou-se campeã do torneio. Isso mostra a força bruta da estratégia estática configurada.
2. **Exploração do Blefe**: Estratégias como *Blefador* e *Agressivo* exibem alto volume de propostas, mas sofrem contra agentes de inferência (como o *Bayesiano* e *Adaptativo*) que calculam a probabilidade a posteriori de blefe e punem propostas falsas.
3. **Eficiência Computacional**: O tempo de decisão reflete a complexidade do Decision Engine. Estratégias probabilísticas e Bayesianas demandam cálculos extras de combinações de cartas, enquanto estratégias estáticas e aleatórias tomam decisões em tempo quase nulo.
