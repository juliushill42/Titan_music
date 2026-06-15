# Architecture

- Go control plane owns lifecycle, health, routing, and policy.
- Python sidecar owns orchestration, MIDI translation, and agent workflows.
- LocalAI handles local model inference.
- MIDI loopback is the live control bus.
