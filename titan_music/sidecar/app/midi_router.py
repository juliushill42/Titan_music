import os
import threading
import time
import mido
from .models import MidiEvent
from .workflows.session import route_event
from .agent_bus import AgentBus

class MidiRouter:
    def __init__(self) -> None:
        self.bus = AgentBus()
        self.running = False
        self.input_port_name = os.getenv("MIDI_INPUT_PORT", "")
        self.poll_delay = float(os.getenv("MIDI_POLL_DELAY", "0.01"))

    def _open_input(self):
        if self.input_port_name:
            return mido.open_input(self.input_port_name)
        ports = mido.get_input_names()
        if not ports:
            raise RuntimeError("No MIDI input ports available")
        return mido.open_input(ports[0])

    def _handle(self, msg):
        if msg.type not in {"note_on", "note_off", "control_change", "program_change", "aftertouch"}:
            return

        event = MidiEvent(
            type=msg.type,
            channel=getattr(msg, "channel", 0),
            note=getattr(msg, "note", None),
            control=getattr(msg, "control", None),
            value=getattr(msg, "value", None),
            program=getattr(msg, "program", None),
            velocity=getattr(msg, "velocity", None),
            source=self.input_port_name or "auto",
        )

        for cmd in route_event(event):
            self.bus.dispatch(cmd)

    def run_forever(self):
        self.running = True
        try:
            with self._open_input() as port:
                while self.running:
                    for msg in port.iter_pending():
                        self._handle(msg)
                    time.sleep(self.poll_delay)
        except Exception as e:
            print(f"MIDI router exception: {e}")

    def start_thread(self) -> threading.Thread:
        t = threading.Thread(target=self.run_forever, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False
