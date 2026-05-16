"""
main.py — Ponto de entrada do Prompt Toolkit.

Fluxo:
1. Carrega configurações e inputs
2. Para cada tarefa, aplica as 4 técnicas em cada input
3. Mede tokens, tempo e acurácia
4. Gera tabela CSV + 3 gráficos PNG
5. Recomenda a melhor técnica por tarefa
6. Roda teste de temperatura no melhor prompt
"""

import json
from pathlib import Path

from src.pai_cp02_stig4.llm_client import LLMClient
from src.pai_cp02_stig4.tasks import listar_tarefas
from src.pai_cp02_stig4.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.pai_cp02_stig4.evaluator import (
    contar_tokens,
    medir_acuracia,
    testar_temperatura,
)
from src.pai_cp02_stig4.report import (
    gerar_tabela,
    grafico_acuracia,
    grafico_custo,
    grafico_temperatura,
    recomendar,
    imprimir_recomendacoes,
)

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def carregar_inputs():
    """Carrega os inputs reais do data/inputs.json."""
    with open(DATA_DIR / "inputs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def executar_tecnica(client, tarefa, input_texto, tecnica_nome):
    """Aplica uma técnica específica e chama o LLM."""
    system = None
    if tecnica_nome == "zero_shot":
        prompt = zero_shot(tarefa, input_texto)
    elif tecnica_nome == "few_shot":
        prompt = few_shot(tarefa, input_texto)
    elif tecnica_nome == "chain_of_thought":
        prompt = chain_of_thought(tarefa, input_texto)
    elif tecnica_nome == "role_prompting":
        system, prompt = role_prompting(tarefa, input_texto)
    else:
        raise ValueError(f"Técnica desconhecida: {tecnica_nome}")

    resp = client.chat(prompt=prompt, system=system, temp=0.2, max_tokens=400)
    return prompt, system, resp


def main():
    print("🚀 Iniciando Prompt Toolkit...\n")

    client = LLMClient()
    print(f"📡 Conectando ao Ollama em {client.host} (modelo: {client.model})\n")

    inputs_por_tarefa = carregar_inputs()
    tarefas = listar_tarefas()
    tecnicas = ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]

    resultados = []

    for tarefa in tarefas:
        nome_tarefa = tarefa["nome"]
        print(f"\n📋 Tarefa: {nome_tarefa} ({tarefa['tipo']})")
        inputs = inputs_por_tarefa.get(nome_tarefa, [])

        for tecnica in tecnicas:
            print(f"  → Aplicando {tecnica}...", end=" ", flush=True)
            for item in inputs:
                input_texto = item["input"]
                esperado = item["esperado"]

                prompt, system, resp = executar_tecnica(
                    client, tarefa, input_texto, tecnica
                )

                # Conta tokens manualmente do prompt
                tokens_prompt_calc = contar_tokens(
                    (system or "") + "\n" + prompt
                )

                acuracia = medir_acuracia(
                    resp["resposta"], esperado, tarefa["tipo"]
                )

                resultados.append({
                    "tarefa": nome_tarefa,
                    "tipo": tarefa["tipo"],
                    "tecnica": tecnica,
                    "input": input_texto[:60] + "...",
                    "resposta": resp["resposta"][:120],
                    "acuracia": acuracia,
                    "tokens_prompt": resp["tokens_prompt"] or tokens_prompt_calc,
                    "tokens_resposta": resp["tokens_resposta"],
                    "tempo_ms": resp["tempo_ms"],
                })
            print("ok")

    print("\n📊 Gerando tabela e gráficos...")
    df = gerar_tabela(resultados)
    grafico_acuracia(df)
    grafico_custo(df)
    print("   ✓ output/resultados.csv")
    print("   ✓ output/graficos/acuracia.png")
    print("   ✓ output/graficos/custo.png")

    # Recomendação final
    recomendacoes = recomendar(df)
    imprimir_recomendacoes(recomendacoes)

    # Teste de temperatura: pega a melhor combinação (tarefa+técnica)
    # da primeira tarefa para ilustrar
    print("\n🌡️  Rodando teste de temperatura no melhor prompt...")
    primeira_tarefa = tarefas[0]
    melhor_tecnica = recomendacoes[primeira_tarefa["nome"]]["tecnica"]
    input_teste = inputs_por_tarefa[primeira_tarefa["nome"]][0]["input"]

    prompt, system, _ = executar_tecnica(
        client, primeira_tarefa, input_teste, melhor_tecnica
    )

    temp_resultados = testar_temperatura(
        client, prompt, system, temperaturas=[0.1, 0.5, 1.0], n_repeticoes=3
    )
    grafico_temperatura(temp_resultados)
    print("   ✓ output/graficos/temperatura.png")

    print("\n   Consistência por temperatura:")
    for temp, dados in temp_resultados.items():
        print(f"     temp={temp}: {dados['consistencia']:.2%}")

    print("\n✅ Concluído! Veja os resultados em output/\n")


if __name__ == "__main__":
    main()
