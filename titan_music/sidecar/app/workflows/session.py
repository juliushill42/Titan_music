from ..models import MidiEvent, AgentCommand

NOTE_MAP = {
    36: "transport_start",
    37: "transport_stop",
    38: "regen_structure",
    39: "regen_bass",
    40: "regen_drums",
    41: "freeze_session",
    42: "unfreeze_session",
    43: "commit_take",
    44: "toggle_variation",
    45: "generate_variation",
    46: "capture_prompt",
    47: "flush_queue",
}

CC_MAP = {
    1: "set_energy",
    2: "set_variation",
    3: "set_density",
    4: "set_brightness",
    5: "set_structure_lock",
    6: "set_harmonic_lock",
    7: "set_rhythm_lock",
    8: "set_texture_lock",
}

def note_to_command(event: MidiEvent) -> AgentCommand | None:
    if event.type != "note_on":
        return None
    action = NOTE_MAP.get(event.note or -1)
    if not action:
        return None
    return AgentCommand(
        action=action,
        payload={"velocity": event.velocity or 0, "channel": event.channel},
        source_event=event,
    )

def cc_to_command(event: MidiEvent) -> AgentCommand | None:
    if event.type != "control_change":
        return None
    action = CC_MAP.get(event.control or -1)
    if not action:
        return None
    value = event.value or 0
    payload = {"value": value, "channel": event.channel}
    if action == "set_energy":
        payload["energy"] = value
    elif action == "set_variation":
        payload["variation"] = value
    elif action == "set_density":
        payload["density"] = value
    elif action == "set_brightness":
        payload["brightness"] = value
    elif action in {"set_structure_lock", "set_harmonic_lock", "set_rhythm_lock", "set_texture_lock"}:
        payload["locked"] = value >= 64
    return AgentCommand(action=action, payload=payload, source_event=event)

def route_event(event: MidiEvent) -> list[AgentCommand]:
    out: list[AgentCommand] = []
    if event.type == "note_on":
        cmd = note_to_command(event)
        if cmd:
            out.append(cmd)
    elif event.type == "control_change":
        cmd = cc_to_command(event)
        if cmd:
            out.append(cmd)
    elif event.type == "aftertouch":
        out.append(
            AgentCommand(
                action="set_pressure",
                payload={"value": event.value or 0, "channel": event.channel},
                source_event=event,
            )
        )
    return out
