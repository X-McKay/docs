# Engineering Playbooks

This repository contains practical standards for building and operating production software systems.

## Agent Playbook

The [Agent Playbook](agent-playbook/README.md) defines an opinionated standard for building production AI agents with PydanticAI and Temporal. It covers:

- Agent specifications and typed contracts
- Repository and package structure
- Runtime skills and executable tools
- Durable execution and human approval
- Evaluation, observability, and cost controls
- Security, governance, and production readiness

The current version is **v0.1 — first draft**.

## Agent Development Skills

The [`skills/`](skills/README.md) library turns the playbook into six portable Agent Skills for Claude Code, Codex, and compatible runtimes. It includes focused workflows for agent design, capability design, Temporal execution, evals, production operations, and readiness reviews, with examples and supporting references.

## Development Toolkit

[`agentctl`](tools/agentctl/README.md) turns the standard into executable guardrails. It scaffolds agent packages, validates Agent Specs and skills, runs version-pinned eval adapters, records provenance, and applies fail-closed release gates.

```bash
scripts/agentctl --help
```

## Reproducible Development

The repository uses one root [uv](https://docs.astral.sh/uv/) workspace and
lockfile for Python dependencies, plus a pinned [Nix](https://nixos.org/) flake
for Python, uv, Just, ShellCheck, Git, and Nix formatting across Linux and
macOS. uv pins the application, Rich terminal stack, and Ruff.

```bash
nix develop
just bootstrap
just check
```

Without Nix, install uv and run the same locked workflow directly:

```bash
uv sync --locked
uv run --locked agentctl --help
uv run --locked python -m unittest discover -s tools/agentctl/tests
```

Use `uv lock --check` and `nix flake check` in CI to reject dependency or flake
drift.
