# 11. Production readiness

An accountable owner completes and approves this checklist before production launch.

## Contract

- [ ] Agent name and version are stable.
- [ ] Owner, execution class, and risk tier are declared.
- [ ] The Agent Spec references a current, approved risk assessment.
- [ ] Governance tier matches the assessment and all mandatory floors.
- [ ] Inputs, dependencies, outputs, and errors are typed.
- [ ] Model policy and budgets are declared.
- [ ] Governance metadata validates at startup.
- [ ] Capability manifest is reproducible.

## Skills and tools

- [ ] Skills and tools use explicit allowlists.
- [ ] Runtime skill assets exist in the built deployment artifact.
- [ ] Skill activation and non-activation evals pass.
- [ ] Tool effects and retry safety are classified.
- [ ] Authorization and tenant isolation are enforced in code.
- [ ] Side effects are idempotent.
- [ ] Consequential actions require bound approval.
- [ ] Tool outputs are bounded.

## Temporal

- [ ] Durable runs execute inside workflows.
- [ ] All I/O executes in activities.
- [ ] Workflow and activity identifiers are stable.
- [ ] Timeouts and retry policies are bounded.
- [ ] Provider transport retries are disabled or justified.
- [ ] Cancellation and compensation are defined.
- [ ] Payloads and histories are bounded.
- [ ] Replay tests pass.
- [ ] Compatible worker deployment is planned.

## Evaluation

- [ ] Every material risk scenario maps to required eval and control evidence.
- [ ] Eval reports identify covered and uncovered risk scenario IDs.
- [ ] Unit, component, smoke, regression, capability, and safety suites pass.
- [ ] Trajectory and tool-argument checks pass.
- [ ] Temporal durability scenarios pass.
- [ ] Required multi-run evaluations pass.
- [ ] Quality, cost, and latency meet thresholds.
- [ ] Critical hard gates have no known failures.
- [ ] Results include complete provenance.

## Observability

- [ ] Request, workflow, agent, model, skill, and tool telemetry correlate.
- [ ] Outcomes and errors use normalized categories.
- [ ] Sensitive-content capture is configured intentionally.
- [ ] Redaction tests pass.
- [ ] Health, quality, safety, and cost dashboards exist.
- [ ] Alerts route to named owners.
- [ ] Consequential actions produce audit records.

## Cost

- [ ] Run-level request, tool, token, and cost limits exist.
- [ ] Shared budget counters use durable storage where required.
- [ ] Unknown-price behavior is explicit.
- [ ] Retry multiplication has a documented upper bound.
- [ ] Context-growth and cache behavior are measured.
- [ ] Budget exhaustion produces a safe typed outcome.
- [ ] Cost per successful compliant outcome is visible.

## Security and governance

- [ ] Prohibited-use and regulatory-applicability screening is complete.
- [ ] Inherent and residual risk are scored with rationale and confidence.
- [ ] Residual risks have treatments, owners, acceptance, and review dates.
- [ ] Threat model is current.
- [ ] Required security, privacy, domain, and risk reviews are complete.
- [ ] Credentials, storage, filesystem, and network access are least privilege.
- [ ] MCP servers and dependencies are approved and pinned.
- [ ] Human approval is authenticated and tamper-tested.
- [ ] Kill switches are tested.
- [ ] Incident and rollback runbooks exist.
- [ ] Exceptions are recorded and unexpired.

## Operations

- [ ] Staging, shadow, canary, and promotion criteria match the risk tier.
- [ ] On-call and escalation ownership are established.
- [ ] Provider and dependency failures are tested.
- [ ] Worker shutdown, recovery, and replay are tested.
- [ ] Decommissioning responsibility is assigned.

## Approval record

```text
Agent:
Version:
Manifest ID:
Execution class:
Risk tier:
Risk assessment and version:
Maximum residual risk:
Residual-risk acceptance:
Engineering owner:
Product/domain owner:
Operations owner:
Security/privacy approvers:
Evaluation report:
Threat model:
Deployment plan:
Exceptions:
Approved by:
Approval date:
Next review date:
```
