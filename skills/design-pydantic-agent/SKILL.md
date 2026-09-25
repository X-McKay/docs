---
name: design-pydantic-agent
description: Design, scaffold, or refactor a production PydanticAI agent. Use when defining an Agent Spec, dependencies, typed output, prompts, execution classes, risk tiers, package boundaries, or the standard src/agents directory structure.
---

# Design a PydanticAI Agent

Create an explicit, typed agent package whose contract can be reviewed before implementation details.

## Workflow

1. Inspect repository instructions, dependency pins, existing agent packages, and test conventions.
2. Write the behavioral contract before the prompt:
   - purpose, owner, users, and non-goals;
   - input, dependency, and output types;
   - execution class and risk tier;
   - allowed skills and tools;
   - latency, quality, and cost objectives;
   - escalation and fallback behavior.
3. Select an execution class:
   - `ephemeral` for bounded work without externally visible side effects;
   - `durable` for retries, timers, recovery, or externally visible side effects;
   - `human_governed` for consequential operations requiring approval.
4. Select a risk tier from low, medium, high, or critical based on consequence, reversibility, privilege, exposure, and data sensitivity.
5. Create the standard package layout. Keep orchestration, tools, runtime skills, prompts, types, policy, and tests separate.
6. Implement a factory that receives configuration and dependencies explicitly. Keep imports free of network calls and mutable runtime work.
7. Use Pydantic models for dependencies, structured output, tool inputs, and externally persisted payloads.
8. Add contract tests for construction, output validation, capability allowlists, and failure behavior.
9. Record unresolved decisions rather than silently inventing product policy.

## Required Output

Produce or update:

- an Agent Spec or equivalent manifest;
- a typed agent factory;
- dependency and output models;
- explicit skill and tool allowlists;
- tests and an eval entry point;
- a short decision record for execution class and risk tier.

Read [the design standard](references/standard.md) before changing architecture. Use [the examples](references/examples.md) when drafting a spec or package.

## Guardrails

- Do not hide business policy in system prompts.
- Do not give an agent every registered tool by default.
- Do not use untyped dictionaries at durable or external boundaries.
- Do not couple the PydanticAI agent object to Temporal workflow code.
- Do not declare readiness without eval, observability, and operational owners.

## Completion Check

Confirm that another engineer can answer, from repository artifacts alone: what the agent does, what it may call, what it returns, how it executes, how it fails, and how it is evaluated.
