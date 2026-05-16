"""
prompt_builder.py — Monta prompts seguindo a anatomia da Aula 05.

Princípio: separar INSTRUÇÃO (o que fazer) de DADOS (sobre o que fazer).
"""


def montar_prompt(instrucao, contexto, input_dados, formato_output):
    """
    Monta um prompt seguindo a anatomia padrão:
        - Instrução: o que o modelo deve fazer
        - Contexto: informações de apoio (opcional)
        - Input: os dados a serem processados
        - Formato: como a resposta deve ser estruturada
    """
    # Valida que campos críticos não estão vazios
    if not instrucao or not instrucao.strip():
        raise ValueError("Instrução não pode ser vazia.")
    if not input_dados or not str(input_dados).strip():
        raise ValueError("Input de dados não pode ser vazio.")
    if not formato_output or not formato_output.strip():
        raise ValueError("Formato de output não pode ser vazio.")

    partes = []
    partes.append(f"### INSTRUÇÃO\n{instrucao.strip()}")

    if contexto and contexto.strip():
        partes.append(f"### CONTEXTO\n{contexto.strip()}")

    partes.append(f"### FORMATO DE SAÍDA\n{formato_output.strip()}")
    partes.append(f"### INPUT\n{str(input_dados).strip()}")

    return "\n\n".join(partes)


def adicionar_exemplos(prompt, exemplos):
    """
    Adiciona exemplos few-shot ao prompt (Aula 06).
    exemplos: lista de dicts com chaves "input" e "output".
    """
    if not exemplos:
        return prompt

    bloco = ["### EXEMPLOS"]
    for ex in exemplos:
        bloco.append(f'Input: "{ex["input"]}"')
        bloco.append(f'Output: {ex["output"]}')
        bloco.append("")  # linha em branco entre exemplos

    # Insere antes do INPUT final
    return prompt.replace("### INPUT", "\n".join(bloco) + "\n### INPUT")


def adicionar_cot(prompt, passos):
    """
    Adiciona instruções de Chain-of-Thought ao prompt (Aula 06).
    passos: lista de strings descrevendo cada passo de raciocínio.
    """
    if not passos:
        return prompt

    linhas = ["### RACIOCÍNIO PASSO A PASSO", "Analise passo a passo:"]
    for i, passo in enumerate(passos, 1):
        linhas.append(f"{i}. {passo}")
    linhas.append("")
    linhas.append("Depois apresente a resposta final no formato pedido.")

    bloco = "\n".join(linhas)
    return prompt.replace("### INPUT", bloco + "\n\n### INPUT")
