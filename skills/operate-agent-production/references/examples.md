# Production Operations Examples

## Safe Span Attributes

```python
attributes = {
    "agent.name": "support-agent",
    "agent.version": "2026-09-25.1",
    "agent.execution_class": "ephemeral",
    "agent.risk_tier": "medium",
    "llm.model": "configured-model-alias",
    "llm.input_tokens": usage.input_tokens,
    "llm.output_tokens": usage.output_tokens,
    "agent.tool_calls": tool_call_count,
    "agent.estimated_cost_usd": estimated_cost,
    "agent.outcome": "escalated",
}
```

Do not add the customer message, account record, tool credential, or unrestricted model response.

## Budget Policy Example

```yaml
per_run:
  model_calls: 4
  tool_calls: 8
  input_tokens: 24000
  output_tokens: 4000
  retries: 2
  wall_time_seconds: 30
  estimated_cost_usd: 0.12
on_exhaustion:
  stop_new_calls: true
  preserve_completed_evidence: true
  return: partial_result_with_escalation
```

## Alert Example

Alert when the five-minute unauthorized-tool-attempt count is greater than zero for a high-risk agent, or when the one-hour cost-per-success burns more than twice its budget. Include release version, affected capability, sanitized trace link, and runbook.

## Optimization Example

An agent repeatedly sends an entire ticket transcript to the model. Replace it with a typed summary of relevant events and capped evidence excerpts. Compare both versions on the same dataset for task success, citation validity, safety gates, p95 latency, and cost per success. Roll out only if quality remains within tolerance.

## Edge Cases

- Cache keys must include tenant, authorization scope, relevant versions, and data freshness requirements.
- A cheaper route that increases retries may cost more overall; measure per successful task.
- High-cardinality raw IDs may overload telemetry backends; hash or link them through controlled logs.
- Sampling must retain all critical safety and policy failures.
