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
