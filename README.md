# 🍺 Esportes de Bar — Simulação de Monte Carlo

Simulação de Monte Carlo aplicada ao **Truco Paulista** e ao **Dominó**,
analisando o impacto de diferentes estratégias e o papel da sorte vs. habilidade.

## Pergunta central
> Blefar de forma constante e agressiva vale a pena a longo prazo?

## Estrutura
```
esportes-de-bar/
├── truco/
│   ├── src/          # Lógica do jogo (carta, baralho, mão, rodada, partida)
│   ├── simulacao/    # Runner da simulação Monte Carlo
│   └── analise/      # Geração de gráficos
├── domino/           # Em desenvolvimento
├── data/
│   └── truco/        # CSVs e gráficos gerados automaticamente
└── gerar_graficos.py # Gera todos os gráficos
```

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar simulação do truco
python truco/simulacao/runner.py

# Gerar gráficos
python truco/gerar_graficos.py
```

## Agentes — Truco
| Agente | Estratégia |
|---|---|
| Aleatório | Baseline — decisões ao acaso |
| Conservador | Só arrisca com mão forte (limiar configurável) |
| Agressivo | Blefa com frequência (chance configurável) |
| Probabilístico | Estima força do adversário pelas cartas restantes |

## Confrontos simulados (1000 partidas cada)
| Confronto | Vencedor | Taxa |
|---|---|---|
| Conservador vs Aleatório | Conservador | 81.8% |
| Agressivo vs Aleatório | Agressivo | 77.1% |
| Conservador vs Agressivo | Conservador | 55.3% |
| Probabilístico vs Agressivo | Probabilístico | 85.2% |

## Principais conclusões
- Qualquer estratégia supera o jogo aleatório
- Blefar contra um jogador analítico é altamente desvantajoso
- O agente probabilístico domina todos os confrontos