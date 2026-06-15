#!/usr/bin/env bash
set -euo pipefail

test -f README.md
test -f docker-compose.yml
test -f cmd/control-plane/main.go
test -f sidecar/app/main.py

! grep -RInE 'TODO|FIXME|placeholder|TBD' . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=build --exclude-dir=dist

echo "audit passed"
