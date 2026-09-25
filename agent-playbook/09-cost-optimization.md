# 9. Cost optimization standard

Optimize cost per successful, compliant outcome. Do not optimize token price in isolation.

## Control order

1. Prevent runaway execution.
2. Remove unnecessary requests and context.
3. Bound tool output.
4. Improve prompt-cache effectiveness.
5. Route to the least expensive capable model.
6. Cache safe, repeatable results.
7. Tune retries and concurrency.
8. Consider provider or commercial changes.

## Budget hierarchy

Every production agent MUST have per-request and per-run limits. Shared deployments SHOULD also have conversation, tenant, deployment, and organization limits.

```yaml
budgets:
  run:
    max_model_requests: 8
    max_tool_calls: 12
    max_input_tokens: 30000
    max_output_tokens: 5000
    max_cost_usd: 0.50
  conversation:
    max_cost_usd: 3.00
  tenant_daily:
    warning_cost_usd: 50
    maximum_cost_usd: 75
```

Use PydanticAI `UsageLimits` for run-level requests, tools, tokens, and cost. Use shared `SpendLimits` storage for budgets spanning runs or workers. In-memory spend counters are insufficient for a production worker fleet or a durable workflow that may resume elsewhere.

Cost and token limits may be known only after a response, so the request crossing a threshold may still be billed. Treat spend limits as a runtime brake and reconcile with provider billing.

Unknown cost MUST remain unknown rather than be represented as zero. Hard USD budgets SHOULD reject unpriced models unless an approved custom price is supplied.

## Model routing

Resolve versioned policies such as `fast-v1`, `balanced-v1`, and `reasoning-v1`. Routing considers modalities, structured-output and tool reliability, context, risk, complexity, latency, cost, residency, and availability.

Escalation to a more capable model occurs only on explicit signals such as failed validation, verified complexity, low confidence, or a high-risk decision. The runtime constrains available routes and total budget.

Evaluate the total cost of failed attempts plus escalation; blindly trying models in sequence may cost more than starting with the appropriate model.

## Context

- Keep stable instructions concise.
- Move specialized procedure into deferred skills.
- Expose only relevant tools and skills.
- Retrieve only needed evidence.
- Return compact typed tool results.
- Set cumulative and per-request context limits.
- Compact or externalize history before model limits.
- Preserve safety, authorization, approval, evidence, and side-effect state.

Summarizing compaction has its own model cost and information-loss risk. It requires eval coverage. Deterministic trimming strategies are preferred when they preserve required context.

## Tool output

Tools MUST support appropriate filtering, pagination, field selection, result-count limits, and byte limits. Prefer a compact summary plus a stable reference over a raw payload.

When results are large:

- Truncate only when loss is acceptable.
- Spill to approved storage when lossless access is required.
- Summarize only with a measured quality and cost benefit.

## Catalog size

Every exposed tool contributes schema tokens; every skill contributes catalog tokens. Production agents MUST use explicit allowlists. Rare tools SHOULD use deferred discovery when practical. Operational spend data belongs in the UI rather than a model-visible tool unless the agent must reason about it.

## Prompt caching

Keep the cacheable prefix stable:

```text
tool schemas
system instructions
stable policy
conversation history
dynamic user content
```

Do not inject timestamps, random IDs, request metadata, nondeterministically ordered tools, or frequently changing flags into stable prefixes. Track cache reads, writes, hit ratio, savings, and cache-bust warnings.

Long Temporal waits may outlive a provider cache; resumed-workflow estimates SHOULD assume a miss unless observed otherwise.

## Application caching

Cache only safe, repeatable outputs. Keys SHOULD include agent, model, settings, instruction and skill hashes, tool schema, normalized input, authorization scope, tenant partition, and source-data version.

Do not cache consequential execution, poorly versioned authorization decisions, cross-tenant sensitive data, stale time-sensitive answers, or unvalidated output.

## Retry economics

Calculate the upper bound:

```text
semantic attempts
× Temporal activity attempts
× provider transport attempts
× model fallbacks
```

The default under Temporal is bounded semantic retries, bounded activity retries, disabled provider transport retries, limited fallback candidates, and idempotent side effects.

## Durable-workflow economics

- Resume partial progress rather than restart prompts.
- Count ambiguous timeouts as potentially billable.
- Use a shared durable spend store.
- Keep large artifacts outside workflow history.
- Use `Continue-As-New` for long histories.
- Expect prompt-cache expiry during long approval waits.
- Make spend-event consumers idempotent.

## Optimization method

Baseline, identify the dominant cost, change one major variable, run multi-run quality/safety/latency/cost evals, roll out gradually, and monitor quality-adjusted cost. Roll back when a hard gate or approved quality threshold regresses.
