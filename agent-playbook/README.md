# Agent Playbook

- **Status:** Draft
- **Version:** 0.2
- **Last updated:** 2026-09-25

This playbook defines a production standard for building AI agents with [PydanticAI](https://pydantic.dev/docs/ai/) and [Temporal](https://docs.temporal.io/). It treats an agent as a governed software system: a typed contract, a constrained set of capabilities, a durable execution model when required, and measurable quality, safety, reliability, and cost.

The playbook is intentionally opinionated. Teams may adopt stricter controls. Exceptions should be explicit, time-bound, and approved by an accountable owner.

## Contents

1. [Principles and scope](01-principles-and-scope.md)
2. [Reference architecture](02-reference-architecture.md)
3. [Canonical agent contract](03-agent-contract.md)
4. [Skill standard](04-skills.md)
5. [Tool standard](05-tools.md)
6. [Temporal execution standard](06-temporal-execution.md)
7. [Evaluation standard](07-evaluation.md)
8. [Observability standard](08-observability.md)
9. [Cost optimization standard](09-cost-optimization.md)
10. [Security and governance](10-security-and-governance.md)
11. [Production readiness](11-production-readiness.md)
12. [Reference implementation](12-reference-implementation.md)
13. [Agent risk assessment](13-risk-assessment.md)
14. [References](references.md)

## Executable guidance

The companion [Agent Development Skills](../skills/README.md) translate this standard into focused workflows for Claude Code, Codex, and compatible Agent Skills clients. [`agentctl`](../tools/agentctl/README.md) provides the executable golden path for scaffolding, contract and skill validation, eval adapters, provenance, and release gates.

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate requirement strength:

- **MUST / MUST NOT:** required for conformance.
- **SHOULD / SHOULD NOT:** expected unless a documented reason justifies an exception.
- **MAY:** optional.

## The standard in one page

Every production agent:

1. Has a stable name, version, owner, execution class, and evidence-based risk
   assessment.
2. Uses a PydanticAI Agent Spec for its declarative definition and Python types for runtime validation.
3. Explicitly allowlists its skills and tools.
4. Classifies every tool as read-only, reversible write, or consequential write.
5. Uses Temporal for long-running work or any externally visible side effect.
6. Requires human approval for consequential operations.
7. Enforces request, tool, token, time, and spend budgets.
8. Is evaluated for outcomes, trajectory, safety, durability, latency, and cost.
9. Emits correlated OpenTelemetry data across requests, workflows, models, skills, and tools.
10. Cannot ship until residual risks are accepted and its production-readiness
    checklist is complete.

## Execution classes

| Class            | Temporal |               Side effects |                     Human approval |
| ---------------- | -------: | -------------------------: | ---------------------------------: |
| `ephemeral`      | Optional |                 Prohibited |                           Optional |
| `durable`        | Required | Allowed through activities |                       Policy-based |
| `human_governed` | Required |     Allowed after approval | Required for consequential actions |

An individual workflow may elevate an agent's declared execution class, but it MUST NOT silently downgrade it. The effective class is at least the minimum required by the most consequential enabled tool.

## Relationship between execution class and risk

Execution class describes **how work executes**. Governance tier describes the
assurance required by the agent's inherent risk and mandatory floors. Residual
risk describes what remains after verified controls. They are independent: a
read-only medical assistant can be ephemeral and high risk, while a reversible
internal update agent can be durable and medium risk. See the
[risk-assessment standard](13-risk-assessment.md).
