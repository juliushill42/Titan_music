#!/usr/bin/env bash
set -euo pipefail
go build ./cmd/control-plane
cd sidecar && python -m compileall app
