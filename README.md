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

### Multi-Agent Systems Playbook

The [Multi-Agent Systems Playbook](multi-agent-playbook/README.md) extends the
Agent Playbook for governed compositions of multiple agents. It adds standards
for topology selection, membership, roles, typed delegation, authority
attenuation, dynamic composition, shared state, system-wide limits, and
composition manifests while retaining the Agent Playbook contract for every
participating agent.

### Agent Development Skills

The [`skills/`](skills/README.md) library turns both playbooks into fourteen
portable Agent Skills for Claude Code, Codex, and compatible runtimes. It
includes focused workflows for agent and multi-agent design, interactions,
risk, Temporal execution, evals, production operations, and readiness reviews.

### Development Toolkit

[`agentctl`](tools/agentctl/README.md) turns the standards into executable
guardrails. It scaffolds agent and multi-agent system packages, validates Agent
Specs, System Specs, risk assessments, and skills, renders composition graphs,
runs version-pinned eval adapters, records provenance, and applies fail-closed
release gates.

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

The [initial repository review](docs/reviews/initial-review/README.md) records
prioritized findings, external research, reproducible validation probes, and a
proposed improvement roadmap against the reviewed commit.
The [backlog](backlog/README.md) tracks the resulting implementation changes,
runtime and repository improvements, and architecture and governance decisions.
