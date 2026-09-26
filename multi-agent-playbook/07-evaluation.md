# 7. Evaluation standard

A multi-agent system is incomplete until its claimed composition benefit,
member behavior, interaction contracts, emergent failure modes, operational
limits, and recovery behavior are represented in reproducible tests and evals.

Passing member-agent evals is necessary but does not demonstrate that the
composition works.

## Evaluation layers

| Layer | Purpose | Typical execution |
| --- | --- | --- |
| Policy and schema tests | Deterministic contracts, graph, scopes, and budgets | No model |
| Member tests | Individual Agent Playbook conformance | Mocked and real model |
| Interaction tests | Handoffs, delegation, data flow, and failures | Mocked members |
| Coordination tests | Routing, aggregation, termination, and state | Mocked and real members |
| End-to-end system evals | Outcome quality and composition benefit | Real system |
| Temporal scenarios | Retry, replay, concurrency, cancellation, recovery | Mocked and real members |
| Adversarial system evals | Cross-agent attacks and emergent failure | Realistic sandbox |
| Online evals | Drift, graph behavior, and unknown failures | Sampled production |

Deterministic properties MUST use deterministic tests. A model judge is not an
acceptable evaluator for authorization, admission, tenant isolation, approval,
schema validity, budget enforcement, idempotency, or termination.

## Admission baseline

The multi-agent admission test is executable. The evaluation plan identifies a
reasonable simpler baseline, normally:

- A deterministic implementation
- One agent with the same underlying tools and evidence
- One agent with deferred skills rather than specialist agents
- The previous static composition when proposing a dynamic one

Compare the system and baseline on task success, hard-gate safety, latency,
cost, operational complexity, and the specific claimed benefits. The comparison
controls datasets, tools, permissions, model families where practical, and run
counts.

A system SHOULD NOT proceed merely because it wins one quality metric. The
decision records whether improvement justifies added failure modes, operational
burden, and cost.

## Dataset structure

```text
evals/systems/<system_name>/
├── datasets/
│   ├── smoke/
│   ├── outcomes/
│   ├── routing/
│   ├── handoffs/
│   ├── aggregation/
│   ├── adversarial/
│   ├── durability/
│   ├── dynamic-admission/
│   └── regressions/
├── evaluators/
│   ├── deterministic.py
│   ├── outcome.py
│   ├── graph.py
│   ├── interaction.py
│   ├── safety.py
│   ├── operational.py
│   └── temporal.py
├── experiments/
│   ├── baseline/
│   ├── ablations/
│   └── topology/
├── fixtures/
└── baselines/
```

Every confirmed system defect becomes a sanitized regression case. Cases carry
stable IDs, risk-scenario tags, topology and capability tags, expected
invariants, required branches, and dataset provenance.

## Hard gates

The following are binary release gates when applicable:

- Every member and interaction is admitted by current policy.
- No undeclared edge or incompatible schema is used.
- Delegation never amplifies authority or crosses tenant boundaries.
- No prohibited data crosses an interaction boundary.
- No consequential action executes without valid bound approval.
- Duplicate, retried, or concurrent work creates no duplicate side effect.
- Root and child budgets, concurrency, depth, fan-out, rounds, and deadlines hold.
- Cancellation and kill switches stop new dispatch and propagate correctly.
- Required members, evidence, and reviews cannot be silently skipped.
- System state reaches an accurate terminal or escalation status.
- Temporal replay passes for supported histories.
- Critical system-risk cases have zero known failures.

One hard-gate failure blocks release. Average member quality, majority votes, or
high aggregate task success cannot compensate for it.

## Outcome evaluation

Measure the end-to-end product outcome rather than treating member completion as
success. Metrics may include:

- Task success and factual accuracy
- Groundedness and evidence completeness
- Policy and process adherence
- Conflict recognition and resolution quality
- Calibrated uncertainty and escalation
- User effort and time to useful outcome
- Recovery from incomplete or failed work
- Cost and latency per successful, compliant outcome

The final evaluator receives the authoritative system result, relevant evidence,
and normalized execution summary. It MUST NOT infer success from an agent's
self-reported status.

## Coordination and trajectory evaluation

Evaluate the system path as well as its answer:

- Appropriate topology, member, and role selection
- Correct and minimal delegation
- Correct edge, schema, arguments, authority, and data context
- Handoff completeness and unambiguous ownership
- Required ordering and approval before effects
- Useful parallelism without avoidable duplication
- Preservation of evidence, uncertainty, and dissent
- Correct aggregation and conflict handling
- No ping-pong, deadlock, livelock, or premature termination
- Graceful budget exhaustion, failure, and escalation

Prefer invariants and allowed partial orders over one exact trace because several
safe execution paths may be valid.

## Topology-specific evaluation

### Supervisor and worker

Measure routing precision and recall, unnecessary delegation, unavailable-member
behavior, coordinator bottlenecks, and specialist misuse.

### Fan-out and gather

Measure coverage gain, branch diversity, redundant work, stragglers, merge
correctness, partial results, and whether parallelism improves wall-clock time.

### Producer and reviewer

Measure reviewer detection and false-rejection rates, correlated failures,
rubber-stamping, correction effectiveness, and retry loops.

### Quorum or voting

Measure error correlation, calibration, tie policy, minority correctness,
aggregation sensitivity, and performance against the strongest single member.

### Hierarchy and handoff

Measure information loss at every level, summary fidelity, ownership transfer,
compounded latency, and whether escalation reaches the correct authority.

### Blackboard and event-driven systems

Measure stale reads, conflicting writes, provenance loss, poisoning, duplicate
or reordered events, feedback loops, convergence, and recovery after consumer
outage.

### Recursive task trees

Measure decomposition quality, useful versus redundant nodes, depth and fan-out
distributions, subtree cancellation, synthesis completeness, and worst-case
resource expansion.

### Dynamic membership and allocation

Measure admission correctness, compatibility, registry failure, substitution,
selection regret, malicious or misleading capability claims, reproducibility,
quarantine, and behavior when no valid member is available.

## Fault injection

System suites SHOULD inject:

- Member timeout, crash, malformed output, and budget exhaustion
- Slow or unavailable registry, model, tool, queue, or artifact store
- Duplicate, missing, delayed, and reordered messages
- Stale graph version or member manifest mismatch
- Conflicting evidence and simultaneous writes
- Worker loss before and after dispatch or side effect
- Approval expiry or argument tampering
- Telemetry and audit export failure
- Quarantine or kill switch during active work

Assertions cover final status, state integrity, budget reconciliation, side
effects, recovery, alerts, and evidence retained for investigation.

## Adversarial evaluation

Include cross-agent scenarios for:

- Direct and indirect prompt injection propagation
- Instruction, identity, approval, and authority laundering
- Confused-deputy use of a more privileged member
- Shared-memory or blackboard poisoning
- Data exfiltration through summaries, evidence, bids, or error messages
- Collusion, false consensus, and reviewer capture
- Sybil-style dynamic members or registry substitution
- Denial-of-wallet through recursion, fan-out, retries, or event loops
- Malicious result timing intended to bypass cancellation or policy

Adversarial inputs remain untrusted throughout the graph. Sanitizing or
summarizing them through another agent does not make them trusted.

## Ablation and topology experiments

For material changes, compare:

- The system against its admission baseline
- The system with each optional member removed
- Static and dynamic routing
- Sequential and parallel execution
- Alternative aggregation or conflict policies
- Homogeneous and intentionally diverse member configurations
- Current and candidate limits for depth, fan-out, rounds, and concurrency

Ablation identifies whether each member and architectural mechanism contributes
enough value to justify its cost and risk.

## Repeated runs and distributions

Repeat cases affected by models, routing, concurrency, arrival order, dynamic
selection, reviewer behavior, or stochastic decomposition. Report:

```text
end-to-end and hard-gate pass rates
worst-case and failure-category distributions
member, edge, depth, fan-out, and round distributions
p50/p95/p99 active latency and completion duration
model, tool, token, and cost distributions
routing, handoff, conflict, and termination metrics
```

Rare high-impact failures remain visible; aggregate means MUST NOT hide them.

## Release policy

A system policy declares absolute and relative requirements, for example:

```yaml
hard_gates:
  unauthorized_edges: 0
  authority_amplification_events: 0
  unapproved_consequential_actions: 0
  duplicate_side_effects: 0
  termination_limit_violations: 0
  temporal_replay_pass_rate: 1.0
quality:
  task_success_rate_min: 0.92
  regression_allowed: 0.02
coordination:
  valid_routing_rate_min: 0.98
  handoff_completeness_rate_min: 0.99
  unnecessary_delegations_per_run_max: 0.5
operational:
  p95_active_latency_seconds_max: 30
  average_cost_usd_max: 1.50
admission:
  baseline_quality_improvement_min: 0.03
  maximum_cost_multiplier: 2.0
```

Thresholds are system-specific. Release fails on a hard gate, missed absolute
threshold, excessive regression, absent required scenario coverage, or missing
provenance.

## Online evaluation

Online evaluation is asynchronous, side-effect-free, privacy controlled, and
version attributed. Sampling is stratified by topology, graph version, role,
interaction, depth, member selection, outcome, risk scenario, and degraded mode.

Monitor graph drift as well as model drift. Unexpected members, edges, depth,
fan-out, role assignment, selection distribution, or termination status require
investigation even when final-answer quality appears stable.

## Provenance

Every report records:

```text
system and composition manifest versions
member agent manifests and models
topology, graph, schemas, and policies
workflow and worker build
datasets, cases, evaluators, and risk tags
judge models and rubrics
baseline and ablation configuration
run count, concurrency, timing, and random seeds where relevant
case-level outcomes, traces, latency, usage, and cost
```
