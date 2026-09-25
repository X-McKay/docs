# Production Operations Standard

## Trace Model

Use a hierarchy that preserves one correlation path:

```text
request
  temporal.workflow
    temporal.activity
      agent.run
        model.request
        tool.call
```

Not every agent uses Temporal; omit those spans for an ephemeral run. Propagate trace context across task queues and external calls.

## Required Attributes

Use safe identifiers or hashes for:

- agent, prompt, policy, skill-set, tool-set, and release versions;
- model provider and model name;
- execution class and risk tier;
- workflow and activity type;
- capability name and outcome;
- input and output token counts;
- latency, retry count, and estimated cost;
- cache hit or miss;
- final status and stable failure class.

Keep raw prompts, model output, tool arguments, credentials, personal data, and cross-tenant identifiers out of default span attributes.

## SLO and Alert Set

Define success rate, safety-gate rate, p95 task latency, durable completion latency where applicable, and cost per successful task. Alert on sustained error-budget burn, any critical safety event, authorization denial spikes, stuck workflows, retry storms, and budget exhaustion. Route every alert to an owner and runbook.

## Budget Hierarchy

Enforce limits per model request, agent run, workflow, tenant or product, and time window as appropriate. Include token, call, tool, retry, wall-time, and currency ceilings. Reserve enough budget for a safe fallback or explanatory response.

## Optimization Order

1. Remove redundant or failed calls.
2. Reduce irrelevant context and cap tool responses.
3. Use structured retrieval instead of transcript accumulation.
4. Route simple cases to a validated smaller model.
5. Cache deterministic or stable results with scoped keys and expiry.
6. Tune retry and concurrency budgets.

Validate every change against quality and hard safety gates.

## Operational Evidence

Maintain dashboards, alert definitions, redaction tests, budget tests, incident runbooks, ownership, dependency maps, rollback procedures, and a version-correlated release view.
