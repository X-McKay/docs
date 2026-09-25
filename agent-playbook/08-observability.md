# 8. Observability standard

Observe the agent as an application, not merely as model calls. The standard is vendor-neutral and based on OpenTelemetry. Pydantic Logfire is a supported first-party backend, not a mandatory dependency.

## Objectives

Operators must be able to determine:

- Which agent, version, model, skills, and tools handled a request
- What the agent attempted and where time and money went
- Which retries occurred and why
- Whether a workflow resumed after failure
- Whether approval was required and valid
- Whether policy and budgets were respected
- Whether the result was successful and reproducible

## Telemetry types

Production services MUST provide:

- Distributed traces for execution flow
- Metrics for aggregate health, quality, performance, and cost
- Structured logs for diagnostics
- Audit records for consequential operations
- Evaluation results for behavioral quality

Ordinary telemetry is not a substitute for a tamper-resistant audit record.

## Correlation

PydanticAI emits agent, model, and tool spans. Temporal emits workflow and activity telemetry. Because these may execute in different processes and at different times, every span MUST also carry stable logical correlation identifiers.

Required resource and run attributes include:

```text
service.name
service.version
deployment.environment.name
git.commit.sha
worker.build_id
agent.name
agent.version
agent.contract_version
agent.manifest_id
agent.execution_class
agent.risk_tier
agent.run_id
agent.request_id
temporal.namespace
temporal.task_queue
temporal.workflow_type
temporal.workflow_id
temporal.run_id
```

Model spans SHOULD use applicable OpenTelemetry generative-AI semantic conventions and record provider, request and response model, operation, input tokens, output tokens, cached tokens, request number, retry count, and estimated cost.

Tool spans record tool name, toolset ID, effect, call ID, activity attempt, outcome, duration, authorization result, retry safety, and whether idempotency was applied.

## Outcomes

Normalize run outcomes:

```text
success
needs_information
escalated
rejected
cancelled
budget_exhausted
timeout
policy_blocked
failed_transient
failed_permanent
partial_effect
compensated
```

Provider-specific errors map to a stable internal category while retaining the original class in restricted diagnostics.

## Metrics

Track at least:

| Area        | Metrics                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| Reliability | Runs, errors, duration, timeouts, cancellations, retries, compensations |
| Models      | Requests, duration, errors, tokens, retries, cost                       |
| Tools       | Calls, duration, errors, retries, authorization denials, output bytes   |
| Approval    | Requested, approved, rejected, expired, wait duration, tampering        |
| Quality     | Task success, groundedness, policy adherence, trajectory score          |
| Cost        | Total cost, cost per run, cost per successful compliant outcome         |

Metrics MUST NOT use request IDs, user IDs, workflow IDs, raw prompts, URLs, arbitrary tenant IDs, or error messages as labels. Put high-cardinality values in traces or restricted logs.

## Prompts, completions, and redaction

Prompt and completion capture MUST be off by default in production. Enabling it requires a documented purpose, approval, data classification, redaction, access controls, retention, deletion, sampling, and applicable regional review.

Redaction MUST occur before export and cover credentials, headers, cookies, personal identifiers, customer content, connection strings, signed URLs, tool inputs and outputs, Temporal payloads, and sensitive exception messages.

When content cannot be retained, record a safe hash, size, content type, template version, and whether redaction was applied.

## Audit

Approval, consequential tools, authorization overrides, policy changes, production promotions, manual workflow intervention, data export, and compensation require audit records containing actor, action, target, time, workflow and agent identity, approval reference, policy version, canonical argument hash, result, and idempotency key.

Audit storage SHOULD be append-only or tamper-evident.

## Sampling and retention

- Aggregate metrics continuously.
- Retain errors, approval events, and consequential actions at 100%.
- Sample ordinary successful traces by volume.
- Independently sample online evals.
- Apply data-specific retention and deletion policies.

## Dashboards

Every production agent needs dashboards for:

- Operational health and stuck workflows
- Model, skill, and tool behavior
- Quality and safety trends
- Cost, budgets, and cache effectiveness

## Alerts

Urgently alert on unapproved consequential action, cross-tenant access, sensitive-data leakage, duplicate side effects, audit failure, worker or queue outage, and critical policy violation.

Use lower-urgency alerts for quality regression, token or cost growth, retry increases, cache collapse, latency SLO burn, and unexpected skill-loading changes.

## Service objectives

Each agent declares availability, completion rate, active-processing latency, maximum workflow duration, policy adherence, cost per success, and approval wait targets. Human waiting time is measured separately from active processing.
