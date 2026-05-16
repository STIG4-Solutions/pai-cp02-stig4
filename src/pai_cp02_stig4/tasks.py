"""
tasks.py — Tarefas do domínio E-COMMERCE (Aula 08).

3 tipos obrigatórios: classificação, extração e geração.
"""

TAREFAS = [
    {
        "nome": "classificacao_sentimento",
        "tipo": "classificacao",
        "contexto": "Análise de reviews de produtos em loja online.",
        "instrucao": (
            "Classifique o sentimento da review do cliente em uma das "
            "categorias: POSITIVO, NEGATIVO, NEUTRO ou MISTO."
        ),
        "formato_output": (
            "Responda APENAS com uma única palavra: POSITIVO, NEGATIVO, "
            "NEUTRO ou MISTO. Sem explicações, sem pontuação, sem formatação."
        ),
        "exemplos_fewshot": [
            {"input": "Adorei o produto, super recomendo!", "output": "POSITIVO"},
            {"input": "Péssimo, quebrou no primeiro uso.", "output": "NEGATIVO"},
            {"input": "Bom preço, mas a qualidade deixa a desejar.", "output": "MISTO"},
        ],
        "passos_cot": [
            "Identifique os aspectos positivos mencionados na review.",
            "Identifique os aspectos negativos mencionados na review.",
            "Compare o peso de cada lado.",
            "Decida a classificação final.",
        ],
        "persona": "analista_cx",
    },
    {
        "nome": "extracao_dados",
        "tipo": "extracao",
        "contexto": "Extração de informações estruturadas de reclamações de clientes.",
        "instrucao": (
            "Extraia as seguintes informações da reclamação do cliente: "
            "produto, preço (se mencionado) e defeito relatado."
        ),
        "formato_output": (
            "Responda APENAS com um objeto JSON válido nas chaves: "
            '{"produto": "...", "preco": "...", "defeito": "..."}. '
            "Se algum campo não estiver na reclamação, use null."
        ),
        "exemplos_fewshot": [
            {
                "input": "Comprei um Notebook Dell por R$3500 e veio com pixels mortos na tela.",
                "output": '{"produto": "Notebook Dell", "preco": "R$3500", "defeito": "pixels mortos na tela"}',
            },
            {
                "input": "A Smart TV LG que comprei não liga mais.",
                "output": '{"produto": "Smart TV LG", "preco": null, "defeito": "não liga"}',
            },
        ],
        "passos_cot": [
            "Identifique o produto mencionado.",
            "Procure por valores monetários.",
            "Identifique o problema/defeito descrito.",
            "Monte o JSON final.",
        ],
        "persona": "especialista_suporte",
    },
    {
        "nome": "geracao_resposta",
        "tipo": "geracao",
        "contexto": "Atendimento ao cliente em loja de e-commerce.",
        "instrucao": (
            "Escreva uma resposta cordial e profissional para a mensagem do "
            "cliente, oferecendo uma solução clara."
        ),
        "formato_output": (
            "Responda com um texto de 2 a 4 frases. Use tom educado, "
            "demonstre empatia e proponha um próximo passo concreto."
        ),
        "exemplos_fewshot": [
            {
                "input": "Meu pedido está atrasado há 5 dias e ninguém me responde!",
                "output": (
                    "Olá! Lamentamos muito pelo atraso e pela falta de retorno. "
                    "Vamos priorizar seu pedido agora mesmo e enviar o código de "
                    "rastreio atualizado em até 24h. Pode nos confirmar o número "
                    "do pedido?"
                ),
            },
            {
                "input": "O produto chegou diferente do que aparece no site.",
                "output": (
                    "Olá! Sentimos muito pelo ocorrido. Você pode iniciar a "
                    "troca gratuita pelo nosso portal em até 7 dias. Se preferir, "
                    "envie uma foto do item recebido que abrimos o chamado por aqui."
                ),
            },
        ],
        "passos_cot": [
            "Identifique a emoção e a queixa do cliente.",
            "Reconheça o problema com empatia.",
            "Proponha uma solução concreta.",
            "Encerre com um próximo passo claro.",
        ],
        "persona": "atendente_senior",
    },
]


def listar_tarefas():
    """Retorna a lista de tarefas definidas."""
    return TAREFAS


def buscar_tarefa(nome):
    """Busca uma tarefa pelo nome."""
    for t in TAREFAS:
        if t["nome"] == nome:
            return t
    return None
