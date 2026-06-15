import os
import requests
from .models import AgentCommand

class AgentBus:
    def __init__(self) -> None:
        self.localai_base = os.getenv("LOCALAI_BASE_URL", "http://127.0.0.1:8080")
        self.control_plane_url = os.getenv("CONTROL_PLANE_URL", "http://127.0.0.1:9000")

    def dispatch(self, cmd: AgentCommand) -> dict:
        url = f"{self.control_plane_url}/events/agent"
        r = requests.post(url, json=cmd.model_dump(), timeout=5)
        r.raise_for_status()
        return r.json()

    def ask_localai(self, prompt: str) -> dict:
        url = f"{self.localai_base}/v1/chat/completions"
        body = {
            "model": os.getenv("LOCALAI_MODEL", "default"),
            "messages": [
                {"role": "system", "content": "You are a production music assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.6,
        }
        r = requests.post(url, json=body, timeout=30)
        r.raise_for_status()
        return r.json()
