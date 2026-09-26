# Playbooks

Practical standards, reusable skills, and executable tooling for building and
operating production software systems.

## What's here

### Agent Playbook

The [Agent Playbook](agent-playbook/README.md) defines an opinionated standard for building production AI agents with PydanticAI and Temporal. It covers:

- Agent specifications and typed contracts
- Repository and package structure
- Runtime skills and executable tools
- Durable execution and human approval
- Evaluation, observability, and cost controls
- Security, governance, and production readiness

### Agent Development Skills

The [`skills/`](skills/README.md) library turns the playbook into seven portable
Agent Skills for Claude Code, Codex, and compatible runtimes. It includes
focused workflows for risk assessment, agent and capability design, Temporal
execution, evals, production operations, and readiness reviews, with examples
and supporting references.

### Development Toolkit

[`agentctl`](tools/agentctl/README.md) turns the standard into executable guardrails. It scaffolds agent packages, validates Agent Specs, risk assessments, and skills, runs version-pinned eval adapters, records provenance, and applies fail-closed release gates.

```bash
scripts/agentctl --help
```

## Development

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

## Status

The Agent Playbook is currently **v0.3 — draft**. Feedback and contributions
are welcome through [issues](https://github.com/X-McKay/playbooks/issues) and
[pull requests](https://github.com/X-McKay/playbooks/pulls).
