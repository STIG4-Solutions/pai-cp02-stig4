"""
evaluator.py — Avaliação de qualidade, custo e consistência.
"""

import json
import re
import tiktoken


# Encoder carregado sob demanda (evita download na importação)
_ENCODER = None


def _get_encoder():
    global _ENCODER
    if _ENCODER is None:
        _ENCODER = tiktoken.get_encoding("cl100k_base")
    return _ENCODER


def contar_tokens(texto):
    """Conta tokens de um texto usando tiktoken."""
    if not texto:
        return 0
    return len(_get_encoder().encode(str(texto)))


def medir_acuracia(resposta, esperado, tipo_tarefa):
    """
    Mede a acurácia comparando resposta com esperado.

    - classificacao: match exato (case-insensitive, sem pontuação)
    - extracao: compara chaves do JSON
    - geracao: match por keywords (presença de palavras-chave do esperado)
    """
    if not resposta or resposta.startswith("[ERRO]"):
        return 0.0

    if tipo_tarefa == "classificacao":
        return _acuracia_classificacao(resposta, esperado)
    elif tipo_tarefa == "extracao":
        return _acuracia_extracao(resposta, esperado)
    elif tipo_tarefa == "geracao":
        return _acuracia_geracao(resposta, esperado)
    return 0.0


def _acuracia_classificacao(resposta, esperado):
    """Match exato ignorando case, espaços e pontuação."""
    limpa = re.sub(r"[^A-Za-zÀ-ÿ]", "", resposta).upper()
    alvo = re.sub(r"[^A-Za-zÀ-ÿ]", "", str(esperado)).upper()
    # Considera acerto se o alvo aparecer na resposta limpa
    return 1.0 if alvo in limpa else 0.0


def _acuracia_extracao(resposta, esperado):
    """
    Tenta extrair JSON da resposta e compara chaves.
    Retorna proporção de chaves corretas.
    """
    # Encontra o primeiro bloco JSON na resposta
    match = re.search(r"\{.*\}", resposta, re.DOTALL)
    if not match:
        return 0.0

    try:
        obtido = json.loads(match.group(0))
    except json.JSONDecodeError:
        return 0.0

    if not isinstance(esperado, dict):
        return 0.0

    acertos = 0
    total = len(esperado)
    for chave, valor_esperado in esperado.items():
        valor_obtido = obtido.get(chave)
        # Comparação tolerante (texto contém o esperado, ignorando case)
        if valor_esperado is None and valor_obtido is None:
            acertos += 1
        elif valor_esperado and valor_obtido:
            if str(valor_esperado).lower() in str(valor_obtido).lower() or \
               str(valor_obtido).lower() in str(valor_esperado).lower():
                acertos += 1

    return acertos / total if total > 0 else 0.0


def _acuracia_geracao(resposta, esperado):
    """
    Para geração não há resposta única certa. Medimos por keywords:
    quantas palavras-chave do esperado aparecem na resposta.
    'esperado' aqui é uma lista de palavras-chave.
    """
    if not isinstance(esperado, list):
        return 0.0

    resposta_lower = resposta.lower()
    acertos = sum(1 for kw in esperado if kw.lower() in resposta_lower)
    return acertos / len(esperado) if esperado else 0.0


def medir_consistencia(respostas):
    """
    Mede % de respostas iguais quando a mesma pergunta é feita N vezes.
    """
    if not respostas:
        return 0.0
    # Normaliza (case + strip)
    normalizadas = [r.strip().lower() for r in respostas]
    mais_comum = max(set(normalizadas), key=normalizadas.count)
    return normalizadas.count(mais_comum) / len(normalizadas)


def testar_temperatura(client, prompt, system, temperaturas, n_repeticoes=3):
    """
    Executa o mesmo prompt N vezes em diferentes temperaturas
    e mede consistência das respostas em cada temperatura.
    """
    resultados = {}
    for temp in temperaturas:
        respostas = []
        for _ in range(n_repeticoes):
            r = client.chat(prompt=prompt, system=system, temp=temp, max_tokens=256)
            respostas.append(r["resposta"])
        resultados[temp] = {
            "respostas": respostas,
            "consistencia": medir_consistencia(respostas),
        }
    return resultados
