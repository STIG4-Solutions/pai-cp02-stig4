import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OLLAMA_API_KEY")
print(f"Chave lida: {repr(api_key)}")
print(f"Tamanho: {len(api_key) if api_key else 0}")

resp = requests.post(
    "https://ollama.com/api/chat",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-oss:120b",
        "messages": [{"role": "user", "content": "oi"}],
        "stream": False,
    },
    timeout=30,
)

print(f"\nStatus HTTP: {resp.status_code}")
print(f"Resposta: {resp.text[:500]}")