# 8. Observability standard

Observe the composition as one governed system and each interaction as an
attributable boundary. Member-agent telemetry required by the Agent Playbook
remains in force and is correlated with system, workflow, graph, delegation,
budget, approval, and outcome data.

## Objectives

Operators must be able to determine:

- Which system, manifest, graph, members, models, and policies handled a task
- Why each member and edge was selected or denied
- Which agent had control, responsibility, data, and authority at each point
- How state, evidence, conflicts, and ownership changed
- Where active time, queue time, retries, tokens, tools, and spend accumulated
- Whether limits, admission, authorization, approval, and termination held
- How failures, cancellation, and compensation propagated
- Whether a dynamic run can be reconstructed after registry state changes
- Which version, scenario, or control caused a degraded or unsafe outcome

## Telemetry types

Production systems MUST provide:

- Distributed traces for workflows, interactions, agent runs, models, and tools
- Metrics for health, coordination, quality, capacity, and cost
- Structured logs for restricted diagnostics
- An interaction ledger for the material delegation and state-transition record
- Tamper-resistant audit records for admission, approval, policy, and effects
- Evaluation results for system behavior

Traces are diagnostic evidence. They do not replace the authoritative workflow
state, interaction ledger, or audit record.

## Trace structure

The root system span represents one business task or bounded workflow segment.
It contains workflow, policy, interaction, agent-run, model, and tool spans.

Use parent-child spans for synchronous work with one clear owner. Use span links
for fan-out, queues, events, batches, blackboard reactions, handoffs across
independent lifecycles, and work with multiple causal parents. Propagate a safe
creation context with every message so producers and consumers remain
correlatable.

Trace shape MUST NOT be used as the only representation of system semantics.
Record explicit delegation IDs, parent IDs, graph versions, interaction modes,
and ownership transitions.

## Required correlation

In addition to Agent Playbook fields, spans and material records include:

```text
system.name
system.version
system.contract_version
system.manifest_id
system.run_id
system.execution_class
system.governance_tier
system.topology
system.graph_version
system.workflow_id
system.workflow_run_id
interaction.id
delegation.id
delegation.parent_id
delegation.mode
delegation.depth
delegation.attempt
delegation.caller
delegation.callee
member.role
member.agent_name
member.agent_version
member.manifest_id
```

Dynamic-admission spans also record registry, candidate, policy version,
decision, reason category, evidence hash, assigned role, and admitted manifest.
Do not place arbitrary agent text or rejection explanations in metric labels.

## Graph and state provenance

Every run records its initial graph and each accepted graph change. A graph
record contains:

- Graph version and parent version
- Added, removed, substituted, or quarantined members
- Added, removed, enabled, or disabled edges
- Proposer and deterministic decision authority
- Policy and evidence references
- Timestamp and workflow event identity
- Composition or run manifest digest

State transitions record previous and next state, transition type, initiating
principal, accepted evidence references, policy decision, and workflow event.
Sensitive payloads remain in controlled artifact storage.

## Interaction ledger

The ledger is the compact, authoritative account of material system activity. It
records:

```text
interaction and delegation identity
caller, callee, role, and graph version
objective and input/output schema hashes
effective authority and data-classification decision
budget reserved, measured, and released
dispatch, start, completion, and queue timestamps
outcome, error category, and retry disposition
evidence, approval, side-effect, and compensation references
```

Ledger entries SHOULD be append-only or tamper-evident. The ledger stores safe
metadata and references, not unrestricted prompts, private reasoning, secrets,
or raw customer content.

## Normalized outcomes

System outcomes use a stable taxonomy:

```text
success
success_degraded
needs_information
escalated
rejected
cancelled
budget_exhausted
deadline_exceeded
policy_blocked
admission_failed
conflict_unresolved
no_progress
failed_transient
failed_permanent
partial_effect
compensated
```

Interaction outcomes use the result-envelope taxonomy. Provider and framework
errors map to stable internal categories while retaining original restricted
diagnostics.

## Metrics

Track at least:

| Area | Metrics |
| --- | --- |
| Outcomes | Runs, success, degraded success, escalation, rejection, partial effect |
| Graph | Active members, graph changes, admission decisions, substitutions, quarantines |
| Coordination | Delegations, depth, fan-out, rounds, handoffs, conflicts, no-progress termination |
| Members | Runs, utilization, outcomes, latency, errors, retries, queue time |
| Interactions | Calls, denials, malformed results, duplicates, late results, output bytes |
| Reliability | Workflow errors, timeouts, cancellations, replay failures, compensations |
| Capacity | Active branches, queue depth, saturation, reservations, backpressure |
| Models and tools | Requests, calls, tokens, latency, errors, retries, estimated cost |
| Security | Unauthorized edges, scope denials, data-flow denials, injection propagation |
| Approval | Requested, approved, rejected, expired, changed action, wait duration |
| Quality | Task success, routing, handoff completeness, evidence, conflict resolution |
| Cost | Total, by member and edge, unused reservations, cost per compliant success |

Metrics use low-cardinality labels such as system, version, environment,
topology, role, interaction type, outcome, and policy category. Run IDs,
delegation IDs, user IDs, tenant IDs, dynamic member IDs, URLs, prompts, and
errors belong in traces, ledgers, or restricted logs—not metric labels.

## Dynamic-system observability

Dynamic systems additionally monitor:

- Candidate and admission distributions
- Selection reasons and selection regret
- Registry freshness, errors, and policy mismatches
- Run-graph size and shape distributions
- Previously unseen member, edge, role, or protocol combinations
- Member churn and substitution rates
- Recursive depth, branching, useful-work ratio, and abandoned subtrees
- Blackboard write contention, stale reads, and unresolved records
- Event lag, duplication, reordering, and feedback-loop indicators

Unexpected graph behavior is drift even if models and prompts have not changed.

## Content, privacy, and reasoning

Prompt, completion, interaction payload, blackboard, and event-content capture is
off by default. Enabling any content requires purpose, approval, classification,
minimization, redaction, access, retention, deletion, sampling, residency, and
affected-party review.

Do not require private chain-of-thought or unrestricted internal reasoning for
observability. Record typed decisions, selected alternatives, evidence
references, policy outcomes, safe summaries, hashes, and externally meaningful
rationales.

Redaction occurs before export and includes credentials, identity tokens,
headers, cookies, personal and customer content, hidden instructions, tool
payloads, artifact URLs, Temporal payloads, bids, error messages, and content
copied from other agents.

## Audit

Audit records are required for:

- Dynamic member admission, substitution, removal, and quarantine
- Graph or policy changes
- Authorization overrides and exceptional routing
- Approval and consequential action
- Kill switches, manual workflow intervention, and compensation
- Production promotion and rollback
- Sensitive artifact access or export
- Risk acceptance and exception use

Records contain accountable actor, action, target, time, reason category,
system/run/workflow identity, manifest and graph version, policy version,
canonical argument or change hash, approval reference, result, and idempotency
key where applicable.

## Sampling and retention

- Aggregate metrics continuously.
- Retain admission changes, policy denials, approval, consequential effects,
  partial effects, security events, and audit failures at 100%.
- Retain enough graph and ledger data to reconstruct every production outcome.
- Sample ordinary successful traces based on volume and risk.
- Stratify samples across topology, graph shape, depth, member, role, and outcome.
- Sample online evaluation independently from operational trace sampling.
- Apply data-specific retention and deletion policies to referenced artifacts.

High-risk and dynamic systems SHOULD use tail-based sampling that retains
unusual graphs, deep recursion, degraded outcomes, high cost, high latency,
conflicts, and policy denials.

## Dashboards

Every production system needs dashboards for:

- Outcome, SLO, and workflow health
- Graph shape, admission, membership, and topology behavior
- Delegation, routing, handoff, aggregation, and termination
- Member and interaction reliability
- Quality, safety, and risk indicators
- Capacity, queues, concurrency, and backpressure
- Tokens, tools, budgets, reservations, and cost
- Approval, consequential actions, and compensation

Operators SHOULD be able to move from a system-level symptom to one run, graph,
delegation, agent, model, tool, policy decision, and artifact reference.

## Alerts

Urgently alert on:

- Unauthorized member, edge, scope, tenant, or data flow
- Unapproved consequential action or duplicate side effect
- Manifest, graph, schema, or policy integrity failure
- Runaway recursion, fan-out, event loop, or spend
- Audit or authoritative state failure
- Kill-switch failure
- Persistent workflow, queue, registry, or required-member outage

Use lower-urgency alerts for quality regression, routing drift, member churn,
increased substitutions, conflict growth, no-progress termination, cost or token
growth, reservation leakage, queue saturation, and unexpected graph patterns.

## Service objectives

Each system declares objectives for:

- Successful and compliant completion
- Hard-gate adherence
- Active-processing and end-to-end duration
- Maximum queue and approval wait
- Workflow and required-member availability
- Admission and routing correctness
- Cancellation and kill-switch propagation
- Cost per successful compliant outcome
- Maximum degraded-completion rate

Measure human waiting, queued capacity, and active processing separately so one
does not hide another.
