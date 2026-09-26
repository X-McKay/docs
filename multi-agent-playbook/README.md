# Multi-Agent Systems Playbook

- **Status:** Draft
- **Version:** 0.1
- **Last updated:** 2026-09-25

This playbook defines a production standard for systems in which multiple AI
agents coordinate to produce one governed outcome. It extends the
[Agent Playbook](../agent-playbook/README.md); it does not replace it.

A multi-agent system conforms only when every participating agent conforms to
the Agent Playbook and the composition conforms to this playbook. The unit of
design, evaluation, release, and operation is the versioned system composition,
not an informal collection of agents.

The playbook is intentionally opinionated. Teams may adopt stricter controls.
Exceptions should be explicit, time-bound, and approved by an accountable
owner.

## Contents

1. [Principles and scope](01-principles-and-scope.md)
2. [Reference architecture](02-reference-architecture.md)
3. [Canonical system contract](03-system-contract.md)
4. [Membership and role standard](04-membership-and-roles.md)
5. [Delegation and interaction standard](05-delegation-and-interactions.md)
6. [Durable coordination standard](06-durable-coordination.md)
7. [Evaluation standard](07-evaluation.md)
8. [Observability standard](08-observability.md)
9. [Cost and capacity standard](09-cost-and-capacity.md)
10. [Security and governance](10-security-and-governance.md)
11. [Production readiness](11-production-readiness.md)
12. [Reference implementation](12-reference-implementation.md)
13. [System risk assessment](13-system-risk-assessment.md)
14. [References](references.md)

## Relationship to the Agent Playbook

The Agent Playbook governs each node. This playbook governs the graph.

| Concern | Governing standard |
| --- | --- |
| Agent identity, instructions, model policy, and typed output | Agent Playbook |
| Skills, tools, authorization, and tool effects | Agent Playbook |
| Individual execution class, budgets, evals, telemetry, and risk | Agent Playbook |
| System purpose, membership, topology, and interaction graph | Multi-Agent Systems Playbook |
| Delegated authority, data flow, shared state, and termination | Multi-Agent Systems Playbook |
| System budgets, emergent behavior, composition risk, and release | Multi-Agent Systems Playbook |

When the standards appear to conflict, the stricter applicable requirement
governs. A system MUST NOT weaken a member agent's execution class, governance
tier, authorization, approval, data-handling, or budget controls.

## Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** indicate
requirement strength:

- **MUST / MUST NOT:** required for conformance.
- **SHOULD / SHOULD NOT:** expected unless a documented reason justifies an
  exception.
- **MAY:** optional.

## The standard in one page

Every production multi-agent system:

1. Documents why multiple agents are preferable to a simpler single-agent or
   deterministic design.
2. Has a stable name, version, owner, System Spec, composition manifest, and
   system risk assessment.
3. References versioned, independently conforming Agent Specs rather than
   duplicating their contracts.
4. Uses a reviewed topology with explicitly pinned or policy-admitted membership
   and interaction edges.
5. Treats every inter-agent boundary as an untrusted, typed, bounded API.
6. Allows delegation to attenuate authority but never to amplify it.
7. Places shared state, conflict resolution, approval, and termination under
   deterministic control.
8. Enforces system-wide and per-interaction limits for depth, fan-out,
   concurrency, rounds, requests, tools, time, tokens, and spend.
9. Uses Temporal for long-running coordination or any path capable of an
   externally visible side effect.
10. Evaluates system outcomes, coordination, failure propagation, security,
    durability, latency, and total cost against an appropriate baseline.
11. Emits correlated telemetry for the complete delegation graph and retains
    auditable evidence for consequential actions.
12. Cannot ship until member and system hard gates pass and residual composition
    risks are accepted by accountable humans.

The standard supports both static and dynamic systems. Dynamic membership,
recursive task trees, shared blackboards, peer meshes, market allocation, and
event-driven collectives remain inside a deterministic control envelope and
carry a higher evidence burden proportional to their adaptability.

## Conformance equation

```text
multi-agent system conformance =
    conformance of every reachable member agent
  + conformance of the versioned composition
  + evidence for their integrated behavior
```

Passing member-agent checks does not establish system conformance. A composition
can introduce risks, costs, and failure modes that no member has in isolation.

## Executable companion

The repository's [`agentctl`](../tools/agentctl/README.md) implements the first
executable System Spec contract:

```bash
scripts/agentctl system scaffold research-system \
  --member planner-agent:coordinator \
  --member researcher-agent:worker
scripts/agentctl system validate
scripts/agentctl system graph src/acme_agents/systems/research_system/system.yaml
scripts/agentctl eval run research-system --system
```

The packaged schema and semantic checks cover topology, membership, pinned
versions, execution and governance floors, policies, limits, referenced member
contracts, system risk, and composition-level evaluation provenance.
