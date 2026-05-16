"""
techniques.py — 4 técnicas de prompting (Aulas 06 e 07).

Cada função recebe a tarefa + input e retorna o prompt montado.
A função role_prompting retorna uma tupla (system, user).
"""

import json
from pathlib import Path
from src.pai_cp02_stig4.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

PROMPTS_DIR = Path(__file__).parent.parent.parent / "prompts"


def _carregar_personas():
    """Lê o JSON com as personas para role prompting."""
    caminho = PROMPTS_DIR / "system_prompts.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def zero_shot(tarefa, input_dados):
    """
    Aula 06 — Zero-Shot.
    Prompt direto, sem exemplos. Instrução clara + formato definido.
    """
    return montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_dados,
        formato_output=tarefa["formato_output"],
    )


def few_shot(tarefa, input_dados, exemplos=None):
    """
    Aula 06 — Few-Shot.
    Adiciona 2-3 exemplos antes do input.
    """
    if exemplos is None:
        exemplos = tarefa.get("exemplos_fewshot", [])

    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_dados,
        formato_output=tarefa["formato_output"],
    )
    return adicionar_exemplos(prompt, exemplos)


def chain_of_thought(tarefa, input_dados, passos=None):
    """
    Aula 06 — Chain-of-Thought.
    Pede raciocínio explícito passo a passo antes da resposta.
    """
    if passos is None:
        passos = tarefa.get("passos_cot", [])

    prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_dados,
        formato_output=tarefa["formato_output"],
    )
    return adicionar_cot(prompt, passos)


def role_prompting(tarefa, input_dados, persona=None):
    """
    Aula 07 — Role Prompting.
    Usa system prompt com persona detalhada do system_prompts.json.
    Retorna tupla (system, user).
    """
    personas = _carregar_personas()
    chave = persona or tarefa.get("persona")

    if not chave or chave not in personas:
        raise ValueError(f"Persona '{chave}' não encontrada em system_prompts.json")

    system = personas[chave]
    user = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_dados,
        formato_output=tarefa["formato_output"],
    )
    return system, user
