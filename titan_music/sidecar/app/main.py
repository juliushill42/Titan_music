from fastapi import FastAPI
from .models import MidiEvent
from .midi_router import MidiRouter
from .state import SessionState
from .workflows.session import route_event

app = FastAPI(title="Orchestration Sidecar")
state = SessionState()
router = MidiRouter()

@app.on_event("startup")
def startup():
	router.start_thread()

@app.on_event("shutdown")
def shutdown():
	router.stop()

@app.get("/healthz")
def healthz():
	return {"ok": True, "mode": state.mode}

@app.post("/events/midi")
def midi_event(event: MidiEvent):
	commands = route_event(event)
	return {"accepted": True, "commands": [c.model_dump() for c in commands]}

@app.post("/session/prompt")
def session_prompt(payload: dict):
	state.last_prompt = str(payload.get("prompt", ""))
	return {"ok": True, "prompt": state.last_prompt}
