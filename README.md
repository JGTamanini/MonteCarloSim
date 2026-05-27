# 🍺 Esportes de Bar — Simulação de Monte Carlo

Simulação de Monte Carlo aplicada ao **Truco Paulista** e ao **Dominó**,
analisando o impacto de diferentes estratégias e o papel da sorte vs. habilidade.

## Estrutura

```
esportes-de-bar/
├── truco/         # Simulação do Truco Paulista
├── domino/        # Simulação do Dominó (duplas, 28 peças)
├── data/          # Resultados das simulações (gerado automaticamente)
└── notebooks/     # Análise e visualização dos resultados
```

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar simulação do truco
python truco/simulacao/runner.py

# Rodar simulação do dominó
python domino/simulacao/runner.py
```

## Agentes implementados

### Truco
- **Aleatório** — baseline, decisões ao acaso
- **Conservador** — só arrisca com mão forte
- **Agressivo** — blefa com frequência
- **Probabilístico** — estima força relativa da mão

### Dominó
- **Aleatório** — baseline, joga peça válida ao acaso
- **Ofensivo** — fecha pontas para bloquear o adversário
- **Defensivo** — segura peças pesadas para o fim
- **Probabilístico** — deduz peças do adversário pela mesa
