# 11. Production readiness

Production readiness is an evidence-based decision about one exact composition
manifest. File presence, member readiness, a successful demo, or passing average
quality does not establish system readiness.

## Scope and decision

- [ ] System name, version, composition manifest, release, and environment are identified.
- [ ] Accountable product, engineering, operational, security, and risk owners are named.
- [ ] Intended and prohibited uses, users, affected parties, jurisdictions, and scale are documented.
- [ ] Execution class, governance tier, residual risk, and launch decision agree across artifacts.
- [ ] The multi-agent admission test and simpler baseline comparison are complete.
- [ ] Conditions for `go`, `conditional_go`, or `no_go` have owners and evidence.

## Member conformance

- [ ] Every reachable static member conforms to the Agent Playbook.
- [ ] Dynamic admission proves equivalent required conformance before dispatch.
- [ ] Member names, versions, manifests, owners, and risk assessments are pinned or recorded.
- [ ] Roles narrow rather than expand member capabilities.
- [ ] Required, optional, advisory, substitutable, and fallback members are classified.
- [ ] Independence claims document shared models, context, evidence, infrastructure, and owners.
- [ ] Quarantine and revocation status is enforced before new work.

## System contract

- [ ] The System Spec validates and has no unresolved production placeholders.
- [ ] Topology, orchestrator, coordinator, members, roles, and edges are explicit.
- [ ] Every interaction has typed input, output, policy, timeout, retry, and failure behavior.
- [ ] State ownership, conflict policy, accepted evidence, and terminal outcomes are defined.
- [ ] The composition manifest is reproducible and immutable for the release.
- [ ] Cross-artifact name, version, graph, class, tier, policy, and digest checks pass.

## Authority and data flow

- [ ] Authenticated actor, tenant, environment, and purpose originate outside model control.
- [ ] Authority attenuation is enforced at interaction and tool boundaries.
- [ ] No member receives undeclared credentials, tools, network access, or data.
- [ ] Every edge has data-classification, minimization, residency, retention, and deletion policy.
- [ ] Parent histories, hidden instructions, credentials, and unrelated evidence are not forwarded implicitly.
- [ ] Artifact references require independent authorization and integrity checks.
- [ ] Consequential actions require valid approval bound to the final action and composition.

## Dynamic architecture

- [ ] Dynamic behavior has a documented benefit over the best reasonable static design.
- [ ] Registry identity, publisher, integrity, compatibility, risk, and health controls are enforced.
- [ ] Every admitted member and edge appears in a reconstructable run manifest.
- [ ] Graph size, member count, depth, fan-out, events, rounds, time, tokens, and spend are bounded.
- [ ] Recursive, marketplace, blackboard, mesh, and event-loop failure cases are evaluated as applicable.
- [ ] No-valid-member, registry-outage, malicious-candidate, substitution, and revocation paths are tested.

## Durable coordination

- [ ] Long-running or state-changing execution occurs in Temporal.
- [ ] Workflows contain deterministic coordination only.
- [ ] Agent runs, models, tools, registries, stores, and other I/O execute in activities.
- [ ] Stable workflow, activity, member, interaction, delegation, and branch identities are used.
- [ ] Concurrent aggregation is deterministic and independent of incidental arrival order.
- [ ] Retry ownership and combined maximum execution are documented.
- [ ] Budget reservation and reconciliation survive worker loss and duplicate delivery.
- [ ] Cancellation propagates and compensation behavior is tested.
- [ ] Payloads and histories are bounded; large artifacts remain outside workflow history.
- [ ] Representative static and dynamic histories replay against the proposed worker.

## Termination and degraded modes

- [ ] Success, degraded success, escalation, rejection, cancellation, failure, and partial effect are distinct.
- [ ] No-progress, policy dead-end, budget, deadline, and kill-switch termination are tested.
- [ ] Required work cannot be silently dropped to preserve latency or availability.
- [ ] Degraded modes identify missing evidence, members, checks, and guarantees.
- [ ] Persistent collectives bound each business task and compact durable history safely.

## Evaluation

- [ ] Member, interaction, coordination, end-to-end, durability, and adversarial suites pass.
- [ ] Every hard gate passes; no average or vote hides a violation.
- [ ] Claimed composition benefits hold against the admission baseline.
- [ ] Ablations justify material members and architectural mechanisms.
- [ ] Topology-specific cases cover routing, handoff, aggregation, conflict, and termination.
- [ ] Dynamic systems cover admission, graph drift, malicious candidates, and reproducibility.
- [ ] Stochastic paths use repeated runs and report distributions and worst cases.
- [ ] Material risk scenarios map to cases, gates, indicators, alerts, and runbooks.
- [ ] Reports contain complete system, member, model, graph, policy, dataset, and build provenance.

## Observability and audit

- [ ] One trace and ledger correlate the root task through every interaction, agent, model, and tool.
- [ ] Async fan-out, events, queues, and handoffs propagate safe creation context and links.
- [ ] Initial graph and every accepted graph change are recorded.
- [ ] Required system, member, delegation, policy, budget, and outcome attributes are emitted.
- [ ] Metrics avoid high-cardinality or sensitive labels.
- [ ] Content capture is off by default or has approved minimization and retention controls.
- [ ] Consequential actions, admission, policy, overrides, and interventions create audit records.
- [ ] Dashboards, SLOs, and actionable alerts are owned and exercised.

## Cost and capacity

- [ ] Root and aggregate request, tool, token, time, cost, and capacity budgets are enforced.
- [ ] Child grants reserve from parent budgets and unused reservations reconcile durably.
- [ ] Worst-case graph expansion includes recursion, fan-out, events, and retries.
- [ ] Concurrency, queues, provider limits, backpressure, and overload behavior are tested.
- [ ] Mandatory review, approval, audit, and compensation capacity is reserved.
- [ ] Unknown model or supplier cost is not treated as zero.
- [ ] Cost per successful compliant outcome meets the release policy.

## Security and governance

- [ ] The composition threat model covers every trust boundary and topology-specific threat.
- [ ] Prompt injection, authority laundering, confused deputy, poisoning, collusion, and denial-of-wallet are tested.
- [ ] Registries, packages, images, skills, tools, policies, and schemas have supply-chain controls.
- [ ] Member work is isolated from the policy and orchestration control plane.
- [ ] Shared state distinguishes proposed, verified, accepted, rejected, and superseded facts.
- [ ] Kill switches can disable runs, admission, members, edges, tools, effects, and active work.
- [ ] Quarantine covers active work, state contributions, approvals, caches, and artifacts.
- [ ] Exceptions and residual-risk acceptance are explicit, approved, monitored, and unexpired.

## Operations

- [ ] Runbooks cover member, registry, workflow, queue, provider, model, tool, store, and audit failures.
- [ ] On-call operators can inspect graph, state, budgets, approvals, and active descendants.
- [ ] Operators can safely pause, cancel, quarantine, substitute, compensate, and roll back.
- [ ] Backup, restore, retention, deletion, and evidence-preservation procedures are tested.
- [ ] Deployment uses staged rollout and rollback to a known composition manifest.
- [ ] In-flight workflows remain compatible or migrate through a tested process.
- [ ] Decommissioning covers members, graphs, workflows, events, credentials, state, and artifacts.

## Pull-request evidence

A behavioral change SHOULD include:

```text
system, member, policy, schema, and workflow versions changed
reason and affected topology or graph paths
affected execution classes, governance tiers, and risk scenarios
member, interaction, system, adversarial, and replay suites run
baseline and ablation results where architecture changed
before/after quality, safety, latency, capacity, and cost
rollout, monitoring, rollback, and in-flight workflow plan
```

## Approval record

The release decision records:

```text
system and composition manifest ID
environment and rollout scope
member and run-time admission envelope
evaluation and replay reports
system risk assessment and residual scenarios
accepted risks and exceptions
conditions, owners, deadlines, and monitoring
approvers and decision time
next review date
```

A critical residual scenario, failed hard gate, missing required owner, invalid
member, incompatible replay, or unbounded consequential path is `no_go`.
