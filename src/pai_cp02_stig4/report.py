"""
report.py — Tabelas, gráficos e recomendação final.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"
GRAFICOS_DIR = OUTPUT_DIR / "graficos"


def gerar_tabela(resultados):
    """
    Recebe lista de dicts com os resultados de cada execução
    e salva como CSV. Retorna o DataFrame.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(resultados)
    df.to_csv(OUTPUT_DIR / "resultados.csv", index=False, encoding="utf-8")
    return df


def grafico_acuracia(df):
    """Gráfico de barras: acurácia média por técnica × tarefa."""
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    pivot = df.groupby(["tarefa", "tecnica"])["acuracia"].mean().unstack()

    fig, ax = plt.subplots(figsize=(10, 6))
    pivot.plot(kind="bar", ax=ax)
    ax.set_title("Acurácia Média por Técnica e Tarefa")
    ax.set_ylabel("Acurácia (0 a 1)")
    ax.set_xlabel("Tarefa")
    ax.set_ylim(0, 1.1)
    ax.legend(title="Técnica")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "acuracia.png", dpi=120)
    plt.close()


def grafico_custo(df):
    """Gráfico de barras: tokens médios totais por técnica."""
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    df["tokens_total"] = df["tokens_prompt"] + df["tokens_resposta"]
    medias = df.groupby("tecnica")["tokens_total"].mean()

    fig, ax = plt.subplots(figsize=(8, 5))
    medias.plot(kind="bar", ax=ax, color="#6c5ce7")
    ax.set_title("Custo Médio (tokens) por Técnica")
    ax.set_ylabel("Tokens (prompt + resposta)")
    ax.set_xlabel("Técnica")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "custo.png", dpi=120)
    plt.close()


def grafico_temperatura(temp_resultados):
    """
    Gráfico de linha: consistência × temperatura.
    temp_resultados é o dict retornado por evaluator.testar_temperatura.
    """
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    temps = sorted(temp_resultados.keys())
    consistencias = [temp_resultados[t]["consistencia"] for t in temps]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(temps, consistencias, marker="o", linewidth=2, color="#e17055")
    ax.set_title("Consistência por Temperatura (melhor prompt)")
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Consistência (0 a 1)")
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(GRAFICOS_DIR / "temperatura.png", dpi=120)
    plt.close()


def recomendar(df):
    """
    Recomenda a melhor técnica por tarefa, considerando acurácia
    (peso 0.7) e custo invertido (peso 0.3).
    Retorna dict {tarefa: {tecnica, justificativa}}.
    """
    df = df.copy()
    df["tokens_total"] = df["tokens_prompt"] + df["tokens_resposta"]

    agrupado = df.groupby(["tarefa", "tecnica"]).agg(
        acuracia=("acuracia", "mean"),
        tokens=("tokens_total", "mean"),
        tempo=("tempo_ms", "mean"),
    ).reset_index()

    recomendacoes = {}
    for tarefa in agrupado["tarefa"].unique():
        sub = agrupado[agrupado["tarefa"] == tarefa].copy()
        max_tokens = sub["tokens"].max() or 1
        sub["score"] = 0.7 * sub["acuracia"] + 0.3 * (1 - sub["tokens"] / max_tokens)
        melhor = sub.loc[sub["score"].idxmax()]

        recomendacoes[tarefa] = {
            "tecnica": melhor["tecnica"],
            "acuracia": round(float(melhor["acuracia"]), 3),
            "tokens_medios": int(melhor["tokens"]),
            "tempo_medio_ms": int(melhor["tempo"]),
            "justificativa": (
                f"Melhor equilíbrio entre acurácia ({melhor['acuracia']:.2f}) "
                f"e custo ({int(melhor['tokens'])} tokens)."
            ),
        }
    return recomendacoes


def imprimir_recomendacoes(recomendacoes):
    """Imprime a tabela de recomendações no terminal."""
    print("\n" + "=" * 70)
    print("RECOMENDAÇÃO FINAL POR TAREFA")
    print("=" * 70)
    for tarefa, rec in recomendacoes.items():
        print(f"\n📌 Tarefa: {tarefa}")
        print(f"   Melhor técnica: {rec['tecnica'].upper()}")
        print(f"   Acurácia média: {rec['acuracia']}")
        print(f"   Tokens médios: {rec['tokens_medios']}")
        print(f"   Tempo médio: {rec['tempo_medio_ms']} ms")
        print(f"   {rec['justificativa']}")
    print("\n" + "=" * 70)
