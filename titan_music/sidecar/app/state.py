from dataclasses import dataclass, field
from typing import Any

@dataclass
class SessionState:
    mode: str = "idle"
    energy: int = 64
    variation: int = 0
    density: int = 64
    brightness: int = 64
    last_prompt: str = ""
    transport_running: bool = False
    freeze: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
