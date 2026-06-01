# 🍺 Esportes de Bar — Simulação de Monte Carlo

Simulação de Monte Carlo aplicada ao **Truco Paulista** e ao **Dominó**,
analisando o impacto de diferentes estratégias e o papel da sorte vs. habilidade.

## Pergunta central

> A estratégia realmente faz diferença ou é tudo sorte?

## Estrutura

```
esportes-de-bar/
├── truco/
│   ├── src/              # Lógica do jogo (carta, baralho, mão, rodada, partida)
│   │   └── agentes/      # Agentes: aleatório, conservador, agressivo, probabilístico
│   ├── simulacao/        # Runner da simulação Monte Carlo
│   └── analise/          # Geração de gráficos
│   └── gerar_graficos.py # Código para imagens dos gráficos
├── domino/
│   ├── src/              # Lógica do jogo (peça, conjunto, mesa, mão, partida)
│   │   └── agentes/      # Agentes: aleatório, defensivo, ofensivo, probabilístico
│   ├── simulacao/        # Runner da simulação Monte Carlo
│   └── analise/          # Geração de gráficos
│   └── gerar_graficos.py # Código para imagens dos gráficos
├── data/
│   ├── truco/            # CSVs e gráficos gerados automaticamente
│   └── domino/           # CSVs e gráficos gerados automaticamente
└── requirements.txt
```

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# --- Truco ---
# Rodar simulação
python -m truco.simulacao.runner

# Gerar gráficos
python -m truco.gerar_graficos

# --- Dominó ---
# Rodar simulação
python -m domino.simulacao.runner

# Gerar gráficos
python -m domino.gerar_graficos
```

> ⚠️ Execute sempre a partir da **raiz do projeto** (`MonteCarloSim/`).

---

## 🃏 Truco Paulista

### Agentes

| Agente | Estratégia |
|---|---|
| Aleatório | Baseline — decisões ao acaso |
| Conservador | Só arrisca com mão forte (limiar configurável) |
| Agressivo | Blefa com frequência (chance configurável) |
| Probabilístico | Estima força do adversário pelas cartas restantes |

### Confrontos simulados (1000 partidas cada)

| Confronto | Vencedor | Taxa |
|---|---|---|
| Conservador vs Aleatório | Conservador | 81.8% |
| Agressivo vs Aleatório | Agressivo | 77.1% |
| Conservador vs Agressivo | Conservador | 55.3% |
| Probabilístico vs Agressivo | Probabilístico | 85.2% |

### Principais conclusões

- Qualquer estratégia supera o jogo aleatório
- Blefar contra um jogador analítico é altamente desvantajoso
- O agente probabilístico domina todos os confrontos

---

## 🁣 Dominó (duplas 2×2)

Simulação em duplas com 4 jogadores — parceiros sentam em posições opostas
e compartilham a pontuação. Cada jogador recebe 7 peças do conjunto duplo-6 (28 peças).
Primeiro par de duplas a atingir 100 pontos vence.

**Regras especiais implementadas:**
- **Batida de chapa** — se o parceiro não jogou nenhuma peça na rodada, os pontos ganhos são dobrados
- **Trancamento** — quando nenhum dos 4 jogadores consegue jogar; vence a dupla com menor soma de pontos nas mãos

### Agentes

| Agente | Estratégia |
|---|---|
| Aleatório | Baseline — escolhe aleatoriamente entre as jogadas válidas |
| Defensivo | Joga sempre a peça mais leve, minimizando pontos na mão |
| Ofensivo | Joga sempre a peça mais pesada, priorizando duplas para travar pontas |
| Probabilístico | Estima peças invisíveis e escolhe jogadas que travam o adversário |

### Confrontos simulados (1000 partidas cada)

| Confronto | Vencedor | Taxa |
|---|---|---|
| Defensivo vs Aleatório | **Aleatório** | 80.3% |
| Ofensivo vs Aleatório | Ofensivo | 94.1% |
| Defensivo vs Ofensivo | Ofensivo | 98.3% |
| Probabilístico vs Ofensivo | Probabilístico | 61.7% |

### Taxa de trancamento por confronto

| Confronto | Rodadas trancadas |
|---|---|
| Defensivo vs Aleatório | 26.9% |
| Ofensivo vs Aleatório | 21.0% |
| Defensivo vs Ofensivo | 17.1% |
| Probabilístico vs Ofensivo | 38.9% |

### Principais conclusões

- A estratégia defensiva é a **única pior que o aleatório** — jogar leve deixa as pontas abertas para os adversários
- O agente ofensivo domina quase todos os confrontos ao travar pontas com peças pesadas e duplas
- O probabilístico reverte o domínio ofensivo ao 61.7%, mostrando que leitura de mesa supera força bruta
- O probabilístico gera significativamente mais trancamentos (38.9%), evidenciando que a estratégia calculada fecha o jogo

---

## Comparativo Truco × Dominó

|  | Truco | Dominó |
|---|---|---|
| Melhor estratégia | Probabilístico | Ofensivo* |
| Papel do blefe | Alto impacto | Não se aplica |
| Influência da sorte | Moderada | Menor |
| Trancamentos | Não existe | 17–39% das rodadas |
| Modo de jogo | 1 vs 1 | Duplas 2×2 |

*O probabilístico supera o ofensivo no confronto direto (61.7%), mas o ofensivo é a estratégia mais dominante no geral.