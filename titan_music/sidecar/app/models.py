from pydantic import BaseModel, Field
from typing import Literal, Any

EventType = Literal["note_on", "note_off", "control_change", "program_change", "aftertouch"]

class MidiEvent(BaseModel):
    type: EventType
    channel: int = Field(ge=0, le=15)
    note: int | None = Field(default=None, ge=0, le=127)
    control: int | None = Field(default=None, ge=0, le=127)
    value: int | None = Field(default=None, ge=0, le=127)
    program: int | None = Field(default=None, ge=0, le=127)
    velocity: int | None = Field(default=None, ge=0, le=127)
    source: str | None = None

class AgentCommand(BaseModel):
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    source_event: MidiEvent
