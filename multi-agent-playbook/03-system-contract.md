# 3. Canonical system contract

Every production multi-agent system is represented by a reviewable package
containing a declarative System Spec, typed interaction models, deterministic
coordination and policy code, and a controlled assembly function.

## System Spec

```yaml
name: customer-resolution-system
description: Investigate support cases and propose policy-compliant resolutions.

metadata:
  contract_version: 1
  owner: customer-platform
  operational_owner: customer-operations
  version: 1.0.0
  execution_class: human_governed
  governance_tier: high
  risk_assessment: docs/risk-assessments/customer-resolution-system.yaml
  threat_model: docs/threat-models/customer-resolution-system.md
  evaluation_policy: evals/systems/customer_resolution_system/release-policy.yaml
  data_classification: confidential
  temporal_enabled: true
  approval_policy: src/acme_agents/policy/approvals/customer_resolution.yaml

justification:
  claimed_benefits:
    - Isolate read-only investigation from consequential customer actions.
    - Add independent policy review before presenting a resolution.
  baseline: single-agent-customer-resolution-v2
  success_measures:
    - lower_policy_violation_rate
    - no_cross_tenant_access

topology:
  type: supervisor_worker
  orchestrator: customer-resolution-workflow
  coordinator: resolution-coordinator
  dynamic_membership: false
  recursive_delegation: false

members:
  - agent: resolution-coordinator
    version: 1.2.0
    role: coordinator
    required: true
  - agent: customer-investigator
    version: 2.1.0
    role: investigator
    required: true
  - agent: policy-reviewer
    version: 1.4.0
    role: reviewer
    required: true
  - agent: customer-action-executor
    version: 1.1.0
    role: executor
    required: true

interactions:
  - id: investigate-case
    from: resolution-coordinator
    to: customer-investigator
    mode: delegate
    input_schema: CustomerInvestigationRequest
    output_schema: CustomerInvestigationResult
    policy: policies/delegation.yaml#investigate-case
    max_calls: 2
    timeout_seconds: 60
  - id: review-resolution
    from: resolution-coordinator
    to: policy-reviewer
    mode: review
    input_schema: ResolutionProposal
    output_schema: PolicyReview
    policy: policies/delegation.yaml#review-resolution
    max_calls: 1
    timeout_seconds: 45
  - id: execute-approved-action
    from: customer-resolution-workflow
    to: customer-action-executor
    mode: dispatch
    input_schema: ApprovedCustomerAction
    output_schema: CustomerActionResult
    policy: policies/delegation.yaml#execute-approved-action
    max_calls: 1
    timeout_seconds: 30

limits:
  max_agent_runs: 6
  max_delegation_depth: 2
  max_parallel_agents: 3
  max_rounds: 3
  max_model_requests: 20
  max_tool_calls: 30
  max_input_tokens: 80000
  max_output_tokens: 12000
  max_cost_usd: 2.00
  deadline_seconds: 180

state:
  owner: customer-resolution-workflow
  shared_memory: none
  artifact_policy: policies/data-flow.yaml

termination:
  policy: policies/termination.yaml
  success_states:
    - resolved
    - approved_action_completed
  escalation_state: escalated_to_human
```

Organization-specific fields MAY extend the spec under `metadata` or a
versioned extension namespace. They MUST be validated at construction and MUST
NOT change the meaning of standard fields.

## Identity and versioning

The following versions remain separate:

- `contract_version`: System Spec schema and semantics.
- System version: membership, topology, policies, schemas, and behavior.
- Member agent version: each agent's independent contract and capabilities.
- Workflow and worker build: Temporal replay and deployment compatibility.
- Composition manifest ID: exact resolved release contents.

Changes to membership, roles, interaction edges, schemas, routing, aggregation,
state ownership, limits, or termination require a system version change and
relevant evals. Temporal-incompatible changes additionally require replay-safe
deployment.

Production System Specs MUST pin acceptable member versions or immutable agent
manifest IDs. Floating references such as `latest` are prohibited.

## Justification

The `justification` section records the admission-test result. It MUST state:

- The limitation of the simpler baseline
- The claimed benefit of composition
- The baseline identifier and evidence location
- Metrics or hard gates that can falsify the claim
- The owner and review date for the architectural decision

Failure to outperform the baseline on the claimed dimensions SHOULD trigger
simplification or a documented exception. A quality gain does not excuse a hard
gate, security, latency, reliability, or cost failure.

## Topology

The topology declares:

- A supported profile
- The deterministic orchestrator
- Any model-driven coordinator
- Whether membership can change during a run
- Whether a member may delegate recursively
- The aggregation and conflict policy when the profile requires one
- Registry, admission, allocation, and graph-construction policy for dynamic
  profiles

The orchestrator MUST be deterministic code. A coordinator MAY propose routes
within the declared graph but cannot create an edge, admit a member, expand
authority, change policy, approve a consequential action, or waive termination
limits.

In a dynamic profile, the declared graph MAY be a run-specific subgraph of a
reviewed policy envelope rather than a fully enumerated deployment-time graph.
Deterministic admission policy validates every member and edge before use, and
the resulting graph is recorded as part of the run manifest.

## Members

Each member entry assigns a system role to an existing Agent Spec. It may add
system-local restrictions but MUST NOT expand the agent's base capabilities.

A member entry SHOULD support:

```yaml
- agent: customer-investigator
  version: 2.1.0
  manifest_id: optional-immutable-agent-manifest
  role: investigator
  required: true
  restrictions:
    toolsets:
      include: [customer-records-read]
    skills:
      include: [customer-investigation]
    data_classification_max: confidential
    authorization_scopes_max: [customers.read]
```

At construction, restrictions are intersected with the member's own allowlists
and runtime authorization context.

## Interactions

Every permitted directed edge is declared. An interaction includes:

- Stable ID, caller, callee, and mode
- Typed input and output schema identifiers
- Delegation, authority, and data-flow policy reference
- Call, timeout, retry, and output bounds
- Failure, cancellation, and fallback behavior
- Telemetry and audit requirements

An undeclared edge MUST fail before the callee runs. Schema or policy resolution
failure MUST fail system construction.

Agent-to-agent edges and orchestrator-to-agent dispatches share the same typed
boundary requirements. An orchestrator is not an agent and is declared as a
trusted deterministic principal rather than given a fictional Agent Spec.

## Limits

The System Spec declares a root budget for the entire system run. Member and
interaction limits are subdivisions of the root budget, not additional spend.

At minimum, bound:

- Agent runs
- Delegation depth
- Parallel agents
- Coordination rounds
- Model requests
- Tool calls
- Input and output tokens
- Cost
- Wall-clock duration

Systems using recursion or fan-out MUST calculate and test a combined worst-case
upper bound that includes retries. The runtime reserves budget before dispatch
and reconciles consumption after completion.

## State and termination

The contract names the owner and policy for workflow state, artifacts, shared
memory, accepted evidence, conflicts, and final outcomes.

Termination policy MUST define:

- Success, escalation, rejection, cancellation, and failure states
- Maximum rounds and no-progress detection
- Behavior when required and optional members fail
- Behavior at budget or deadline exhaustion
- Handling of late, duplicate, or conflicting results
- Cancellation propagation and compensation
- Which final states permit an external side effect

A coordinator output is a proposal until deterministic code validates it and
commits the corresponding state transition.

## Factory responsibilities

The system factory:

1. Loads and validates the System Spec.
2. Resolves the system risk assessment, threat model, eval policy, and policies.
3. Resolves every pinned member Agent Spec and manifest.
4. Verifies member conformance and role restrictions.
5. Builds and validates the directed interaction graph.
6. Verifies schema compatibility for every edge.
7. Computes effective execution class and governance-tier floors.
8. Verifies authority attenuation and data-flow constraints.
9. Validates combined budget, retry, concurrency, and termination bounds.
10. Attaches Temporal, observability, audit, budget, and policy services.
11. Produces the immutable composition manifest.

Construction MUST fail closed on a missing member, version mismatch, undeclared
or invalid edge, policy error, schema incompatibility, insufficient execution
class or governance tier, unbounded cycle, missing approval path, or incomplete
required evidence.

## Cross-artifact consistency

The System Spec, composition manifest, risk assessment, threat model, eval
policy, deployment, and production telemetry MUST agree on:

```text
system name and version
member agents and versions
topology and policies
execution class and governance tier
risk-assessment version or digest
budget policy
workflow and worker version
```
