# 9. Cost and capacity standard

Optimize total cost and capacity per successful, compliant system outcome. A
multi-agent design that improves one quality metric while creating uncontrolled
fan-out, queueing, retries, or operational burden is not optimized.

## Cost model

System cost includes:

```text
member model requests and reasoning tokens
tool, retrieval, MCP, and external API usage
workflow, activity, queue, storage, and artifact infrastructure
failed, cancelled, duplicate, speculative, and retried work
review, approval, evaluation, monitoring, and recovery
idle reservations and unavailable capacity
```

Attribute costs to the root run, member, role, interaction, branch, model, tool,
and outcome where possible. Unknown cost remains unknown rather than zero.

## Control order

1. Prevent runaway graphs, loops, retries, and event amplification.
2. Remove unnecessary members, edges, reviews, and duplicated work.
3. Bound depth, fan-out, concurrency, rounds, tools, context, and output.
4. Use deterministic routing and computation where appropriate.
5. Improve task decomposition, handoff, and early termination.
6. Improve prompt caching and safe application caching.
7. Route each role to the least expensive model proven capable.
8. Tune concurrency, speculation, retries, and infrastructure.
9. Consider provider, marketplace, or commercial changes.

## Budget hierarchy

Every run has a root budget. Shared deployments SHOULD also enforce budgets at
conversation, actor, tenant, system, environment, and organization scope.

```yaml
budgets:
  run:
    max_agent_runs: 6
    max_parallel_agents: 3
    max_model_requests: 20
    max_tool_calls: 30
    max_input_tokens: 80000
    max_output_tokens: 12000
    max_cost_usd: 2.00
    deadline_seconds: 180
  tenant_daily:
    warning_cost_usd: 500
    maximum_cost_usd: 750
  deployment_monthly:
    warning_cost_usd: 20000
    maximum_cost_usd: 25000
```

The strictest applicable remaining limit governs. In-memory counters are
insufficient for worker fleets, child workflows, dynamic members, or runs that
resume elsewhere.

## Budget escrow

Before an interaction starts, the system reserves a bounded grant from the
parent's remaining allocation. A grant covers the child's own work and any
descendants it is permitted to create.

The ledger maintains:

```text
root limit
committed consumption
active reservations
remaining unreserved capacity
unknown or disputed usage
```

At all times:

```text
committed + active reservations <= hard limit
```

Unused reservation returns to the parent after the branch reaches a durable
terminal state. Lost workers, late results, and failed usage reporting MUST NOT
cause silent double-spend or reservation leakage.

## Expansion bounds

Depth, fan-out, and retries multiply. For a uniform tree, a conservative node
bound is:

```text
maximum nodes = 1 + fanout + fanout^2 + ... + fanout^depth
maximum executions = maximum nodes * maximum attempts per node
```

Real systems SHOULD calculate bounds from the declared interaction graph and
per-edge limits rather than rely on the uniform formula. `max_agent_runs` and
root request, token, cost, and deadline limits remain authoritative even when a
calculated graph bound is higher.

An event-driven system additionally bounds events produced per event, delivery
attempts, outstanding messages, and maximum causal-chain length.

## Capacity limits

Spend and capacity are separate controls. Bound:

- Active system runs
- Active members and branches per run
- Per-role, member, model, tool, tenant, and provider concurrency
- Queue depth and maximum queue age
- Workflow tasks, activities, and child workflows
- Registry, artifact, and blackboard operations
- Token and request rate

Concurrency reduces wall-clock time only until provider, tool, queue, worker, or
downstream capacity saturates. Above that point it increases queueing, timeouts,
retries, and cost.

## Backpressure and admission control

Apply admission control before expensive work. When capacity is unavailable,
policy chooses among:

- Queue within a stated maximum wait
- Reduce optional fan-out through a tested degraded mode
- Select an admitted fallback with equivalent controls
- Defer non-urgent work
- Reject with a retry-after signal
- Escalate to an operator or human process

The system MUST NOT silently drop required branches, safety reviews, approvals,
or evidence gathering to preserve throughput.

## Architecture economics

### Pipelines and handoffs

Cost grows roughly with the number of stages. Optimize by removing stages that
do not materially change decisions and by passing compact typed state rather
than full histories.

### Supervisor and worker

Coordinator calls add routing overhead. Use deterministic routing for known
cases, keep the catalog small, and avoid asking multiple coordinators to make
the same choice.

### Fan-out, voting, and review

Parallel work can improve latency, coverage, or confidence but multiplies
requests. Size the panel to measured marginal benefit and stop optional branches
when enough evidence has arrived, if the stopping rule is deterministic and
evaluated.

### Hierarchies

Every layer adds summarization and management work. Prefer shallow hierarchies,
route directly when policy permits, and measure the cost of coordination versus
specialist work.

### Blackboards and events

Shared coordination can avoid repeated context transfer but creates storage,
indexing, polling, notification, and compaction cost. Prefer event-driven reads
over wasteful polling and expire obsolete tasks and artifacts deterministically.

### Recursive systems

Recursion has the highest expansion risk. Use task-value estimates, strict node
and subtree grants, no-progress detection, duplicate-task detection, and early
subtree cancellation.

### Dynamic membership and markets

Discovery, admission, bidding, compatibility checks, and cold starts add cost
before task work begins. Cache safe registry metadata, limit candidate sets, and
evaluate whether dynamic selection improves outcome or capacity enough to
justify this overhead.

## Model routing

Resolve a versioned model policy for each role. Routing considers task
complexity, modality, schema and tool reliability, risk, context, latency,
residency, price, availability, and evidence from system evals.

The coordinator SHOULD NOT default every specialist to its own model choice.
The system constrains available routes and prices, while role policy selects
from evaluated options.

Escalation to a more capable model uses explicit signals such as failed
validation, measured complexity, unresolved conflict, or a high-risk decision.
Account for failed attempts plus escalation; model cascades can cost more than
starting with the appropriate route.

## Context and artifact economics

- Pass task-specific typed summaries and evidence references.
- Do not copy full parent histories to every child.
- Keep role instructions and capability catalogs narrow.
- Retrieve artifacts lazily and in bounded chunks.
- Deduplicate evidence and shared immutable context.
- Compact blackboards and long-lived state by typed policy.
- Bound member output before aggregation.
- Preserve provenance when summarizing or caching.

Context reduction is accepted only when handoff-completeness, evidence, and
outcome evals continue to pass.

## Caching

Use provider prompt caching for stable prefixes such as system policy, role
instructions, and tool schemas. Keep volatile task, membership, and user content
later where provider semantics permit.

Application caching requires a typed key containing relevant tenant, actor,
authorization, policy, model, agent, data, and schema versions. Never reuse:

- Approval decisions
- Consequential tool results as permission to repeat an action
- User-specific or tenant-specific data across boundaries
- Dynamic admission decisions after their evidence or policy expires
- Security-sensitive results without explicit freshness semantics

Shared immutable evidence MAY be cached when authorization, provenance,
integrity, expiry, and invalidation are enforced.

## Speculation and hedging

Speculative parallel calls or hedged requests MAY reduce tail latency but create
duplicate work and potential effects. They require:

- Read-only or safely idempotent execution
- Explicit duplicate cancellation and result selection
- Reserved budget for every branch
- Provider and tenant concurrency compliance
- Eval evidence that latency benefit justifies cost

Do not hedge consequential actions or approval decisions.

## Retry economics

Retries consume the same global budgets as initial attempts. Measure retry cost
by layer and failure category. Eliminate nested retries that respond to the same
failure and use circuit breakers for provider, registry, tool, and member
outages.

Retry storms across a dynamic graph are a capacity incident. The control plane
MUST be able to stop new dispatch without waiting for models to comply.

## Exhaustion behavior

Every hard limit has a user- and operator-visible outcome. Depending on policy,
the system may return the best validated partial result, request information,
enter a tested degraded mode, escalate, or fail safely.

Budget exhaustion MUST NOT bypass a required reviewer, deterministic policy,
human approval, audit write, or compensation. Reserve capacity for mandatory
finalization and safety work before allocating optional tasks.

## Optimization method

For each change:

1. Measure baseline outcome, safety, latency, capacity, and total cost.
2. Identify the dominant member, edge, retry, context, queue, or infrastructure
   contributor.
3. Change one architectural or policy variable where practical.
4. Run member, interaction, system, adversarial, and durability evals.
5. Compare distributions and worst cases, not only averages.
6. Promote only when hard gates hold and cost per successful compliant outcome
   improves without unacceptable capacity or reliability regression.
