import os
import requests

class LocalAIAdapter:
    def __init__(self) -> None:
        self.base = os.getenv("LOCALAI_BASE_URL", "http://127.0.0.1:8080")
        self.model = os.getenv("LOCALAI_MODEL", "default")

    def generate(self, prompt: str) -> dict:
        url = f"{self.base}/v1/chat/completions"
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a production music assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.6,
        }
        r = requests.post(url, json=body, timeout=30)
        r.raise_for_status()
        return r.json()
