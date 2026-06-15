#!/usr/bin/env bash
set -euo pipefail
git status --short
git tag -a v0.1.0 -m "initial release"
git push origin main --tags
