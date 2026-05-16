"""
llm_client.py — Conexão com Ollama Cloud (Aula 05).

Usa a biblioteca oficial `ollama` apontando para https://ollama.com
com autenticação por API key (variável OLLAMA_API_KEY no .env).

Não é necessário rodar Ollama localmente nem baixar modelos.
"""

import os
import time
from ollama import Client
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Cliente para o Ollama Cloud."""

    def __init__(self):
        self.api_key = os.getenv("OLLAMA_API_KEY")
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.host = os.getenv("OLLAMA_HOST", "https://ollama.com")

        if not self.api_key:
            raise RuntimeError(
                "OLLAMA_API_KEY nao encontrada no .env. "
                "Crie um .env baseado no .env.example e adicione sua chave."
            )

        self.client = Client(
            host=self.host,
            headers={"Authorization": "Bearer " + self.api_key},
        )

    def chat(self, prompt, system=None, temp=0.3, max_tokens=300, retries=2):
        """
        Envia um prompt ao Ollama Cloud e retorna um dict com:
            resposta, tokens_prompt, tokens_resposta, tempo_ms
        """
        mensagens = []
        if system:
            mensagens.append({"role": "system", "content": system})
        mensagens.append({"role": "user", "content": prompt})

        ultimo_erro = None
        for tentativa in range(retries + 1):
            try:
                inicio = time.time()
                resp = self.client.chat(
                    model=self.model,
                    messages=mensagens,
                    options={"num_predict": max_tokens, "temperature": temp},
                    stream=False,
                )
                tempo_ms = int((time.time() - inicio) * 1000)

                return {
                    "resposta": resp["message"]["content"].strip(),
                    "tokens_prompt": resp.get("prompt_eval_count", 0),
                    "tokens_resposta": resp.get("eval_count", 0),
                    "tempo_ms": tempo_ms,
                }
            except Exception as e:
                ultimo_erro = f"{type(e).__name__}: {e}"
                if tentativa < retries:
                    time.sleep(1.5)

        return {
            "resposta": f"[ERRO] {ultimo_erro}",
            "tokens_prompt": 0,
            "tokens_resposta": 0,
            "tempo_ms": 0,
        }
