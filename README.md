# Prompt Toolkit — Checkpoint 02 — Grupo stig4

Toolkit Python que aplica automaticamente **4 técnicas de prompting** (Zero-Shot, Few-Shot, Chain-of-Thought e Role Prompting) a tarefas de negócio do domínio **e-commerce**, compara os resultados e recomenda a melhor abordagem.

## 📦 Sobre o Projeto

O toolkit recebe inputs reais (reviews, reclamações, perguntas de clientes) e roda cada um pelas 4 técnicas, medindo:
- **Acurácia** (acerto vs. resultado esperado)
- **Custo** (tokens consumidos)
- **Consistência** (estabilidade ao variar temperatura)

No final, gera tabela CSV + gráficos PNG + recomendação automática.

## 🛠️ Stack

- Python 3.10+
- **Ollama Cloud** (gratuito, online) — modelo `gpt-oss:120b`
- `ollama` — biblioteca oficial do Ollama
- `python-dotenv` — variáveis de ambiente
- `tiktoken` — contagem de tokens
- `pandas` + `matplotlib` — tabelas e gráficos
- `uv` — gerenciamento de dependências

## 📥 Instalação

### 1. Obter a chave do Ollama Cloud

O projeto usa **Ollama Cloud**, que roda os modelos online de graça — **não precisa instalar nada no PC nem baixar modelos grandes**.

1. Acesse https://ollama.com e crie uma conta gratuita
2. Copie sua **API Key** (em Settings / API Keys)

### 2. Instalar dependências

```bash
cd pai-cp02-stig4

uv sync
```

### 3. Configurar variáveis de ambiente

Copie o `.env.example` para `.env`:

```bash
cp .env.example .env
```

Abra o `.env` e cole sua chave em `OLLAMA_API_KEY`:

```
OLLAMA_API_KEY=cole_sua_chave_aqui
OLLAMA_MODEL=gpt-oss:120b
OLLAMA_HOST=https://ollama.com
```

## ▶️ Como Executar

```bash
python -m src.pai_cp02_stig4.main
```

O script vai:
1. Carregar as tarefas e inputs do `data/`
2. Aplicar as 4 técnicas em cada input
3. Medir tokens, tempo e acurácia
4. Rodar teste de temperatura (0.1, 0.5, 1.0) no melhor prompt
5. Salvar `output/resultados.csv` e gráficos em `output/graficos/`
6. Imprimir a recomendação final no terminal

## 📁 Estrutura

```
prompt-toolkit/
├── README.md
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── llm_client.py        # Conexão com Ollama Cloud
│   ├── main.py
│   ├── prompt_builder.py    # Anatomia do prompt
│   ├── techniques.py        # ZS, FS, CoT, Role
│   ├── tasks.py             # Tarefas do domínio
│   ├── evaluator.py         # Métricas
│   └── report.py            # Tabelas e gráficos
├── data/
│   ├── inputs.json          # 5+ inputs reais por tarefa
│   └── examples.json        # Exemplos para few-shot
├── prompts/
│   ├── system_prompts.json  # Personas
│   └── templates.json       # Templates por tarefa
├── output/
│   ├── resultados.csv
│   └── graficos/
└── docs/
    └── CP02_stig4.pdf
```

## 👥 Grupo: stig4

- Giovanni Merlotti — RM 573721
- Sergio Augusto — RM 570184
- Gabriel Freitas — RM 572943
- Glauco Kelly — RM 572840

## 📚 Domínio Escolhido

**E-commerce** — atendimento ao cliente e análise de reviews.

Tarefas implementadas:
1. **Classificação de sentimento** (positivo / negativo / neutro / misto)
2. **Extração de dados** (produto, preço, defeito em formato JSON)
3. **Geração de resposta** (resposta ao cliente para reclamações)
