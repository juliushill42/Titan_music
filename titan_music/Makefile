SHELL := /usr/bin/env bash

.PHONY: fmt lint test build run-local audit clean

fmt:
	@echo "fmt"

lint:
	@echo "lint"

test:
	@echo "test"

build:
	@echo "build"

run-local:
	docker compose up --build

audit:
	@bash scripts/audit.sh

clean:
	rm -rf bin dist build .venv
