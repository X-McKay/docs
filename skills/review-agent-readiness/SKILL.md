---
name: review-agent-readiness
description: Review a PydanticAI and Temporal agent for production readiness. Use for architecture reviews, pre-launch audits, pull-request reviews, risk assessments, launch checklists, or go/no-go decisions covering contracts, capabilities, durability, evals, security, observability, and cost.
---

# Review Agent Readiness

Produce an evidence-based launch recommendation with prioritized, actionable findings.

## Workflow

1. Identify scope, proposed release, owner, execution class, risk tier, users, and production environment.
2. Gather evidence from code, Agent Spec, prompts, skill and tool manifests, tests, eval reports, Temporal configuration, telemetry, runbooks, and cost data.
3. Review the agent contract and typed boundaries.
4. Review capability least privilege, authorization, side effects, idempotency, and human approval.
5. Review Temporal determinism, retries, timeouts, payloads, history growth, replay safety, and recovery tests when durable execution is used.
6. Review eval coverage, dataset provenance, hard gates, variance, baseline comparison, and release thresholds.
7. Review privacy, security, observability, SLOs, cost limits, incident response, and rollback.
8. Report findings first, ordered by severity. Include file or artifact evidence, impact, and a concrete remediation.
9. Distinguish blockers from accepted risks and follow-up improvements.
10. Issue `go`, `conditional go`, or `no-go` only from documented evidence.

## Severity

- `P0`: active or inevitable severe harm; stop or roll back immediately.
- `P1`: production launch blocker involving safety, authorization, data loss, non-idempotent duplication, or absent critical evidence.
- `P2`: material reliability, quality, observability, or cost weakness that needs an owner and deadline.
- `P3`: maintainability or clarity improvement with limited immediate risk.

Read [the readiness standard](references/standard.md) for required evidence. Use [the examples](references/examples.md) for finding format and launch recommendations.

## Guardrails

- Do not infer compliance from the presence of files; inspect their contents and results.
- Do not treat passing unit tests as sufficient eval evidence.
- Do not approve a high-risk agent without tested denial and approval paths.
- Do not bury blockers in a summary.
- Do not label unverified assumptions as facts.

## Completion Check

The review must state scope, evidence inspected, findings, hard-gate status, accepted risks, owners and deadlines, and a clear launch recommendation.
