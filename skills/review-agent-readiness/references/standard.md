# Agent Readiness Review Standard

## Required Evidence

### Contract and Architecture

- Agent Spec, owner, purpose, non-goals, execution class, governance tier, and
  current risk assessment.
- Typed input, dependencies, output, tool payloads, and durable payloads.
- Explicit package boundaries and capability allowlists.
- Versioned prompts, policies, skills, tools, models, and releases.

### Capability Safety

- Tool authorization and tenancy enforcement.
- Side-effect and retry classifications.
- Idempotency strategy for writes.
- Human approval for applicable high-risk actions.
- Negative tests for denied and prompt-injection paths.

### Durable Execution

- No nondeterministic I/O in workflow code.
- Explicit timeouts, retry policies, and shared retry budgets.
- Bounded payloads and histories.
- Signal authorization and approval expiry.
- Worker-loss, duplicate-delivery, and replay test evidence.

### Evaluation

- Material risk scenarios mapped to eval cases, control evidence, and monitoring.
- Versioned representative dataset with provenance.
- Deterministic hard gates for safety and authorization.
- Calibrated rubric evaluators where necessary.
- Multi-run evidence for stochastic critical paths.
- Baseline comparison across quality, latency, and cost.

### Operations

- End-to-end trace correlation and privacy controls.
- SLOs, dashboards, alerts, and runbooks.
- Per-run and aggregate budgets with exhaustion behavior.
- Incident owner, rollback plan, and release correlation.

## Launch Rule

Issue `no-go` for any P0 or unresolved P1, failed hard gate, missing authorization boundary, unsafe non-idempotent retry, untested high-risk approval, or absent rollback for a material side effect. `Conditional go` requires named owners, deadlines, and monitoring for each condition. Use `go` only when required evidence exists and residual risks are accepted by the proper owner.

## Review Report Shape

1. Scope and recommendation.
2. Findings ordered by severity.
3. Evidence inspected and missing evidence.
4. Hard-gate and SLO scorecard.
5. Accepted risks, owners, and deadlines.
6. Required actions before or after launch.

Every finding includes severity, evidence location, observed behavior, impact, remediation, and verification method.
