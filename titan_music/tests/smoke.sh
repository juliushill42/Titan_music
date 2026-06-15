#!/usr/bin/env bash
set -euo pipefail
curl -fsS http://127.0.0.1:9000/healthz
curl -fsS http://127.0.0.1:9000/readyz
curl -fsS http://127.0.0.1:9001/healthz
