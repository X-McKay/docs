set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

bootstrap:
    uv sync --locked

lock:
    uv lock --check

format:
    uv run --locked ruff format tools/agentctl/src tools/agentctl/tests

lint:
    uv run --locked ruff check tools/agentctl/src tools/agentctl/tests
    shellcheck scripts/agentctl

test:
    uv run --locked python -m unittest discover -s tools/agentctl/tests -v

skills:
    uv run --locked agentctl --no-animations skills validate skills

check: lock lint test skills

agentctl *args:
    uv run --locked agentctl {{args}}

nix-check:
    nix flake check
