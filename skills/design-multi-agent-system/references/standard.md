# Multi-Agent System Design Standard

Read the repository's Multi-Agent Playbook chapters on principles, reference architecture, System Specs, membership, cost, and governance.

## Decision Order

1. Prove one model call, deterministic code, or one agent is insufficient.
2. Name the needed benefit: specialization, isolation, parallelism, independent review, modular ownership, or resilience.
3. Choose a fixed topology before considering an adaptive one.
4. Pin members and constrain their allowed skills, tools, authority, and data.
5. Define typed interactions, budgets, state ownership, and termination.
6. Assess composition risk and define system-level evals.

## Architecture Selection

| Architecture | Good fit | Principal cost or risk |
| --- | --- | --- |
| Pipeline | Ordered transformations | Brittle downstream dependencies |
| Supervisor-worker | Central routing and bounded delegation | Coordinator bottleneck |
| Fan-out/gather | Independent parallel analysis | Cost spikes and aggregation errors |
| Producer-reviewer | Independent critique matters | Latency and correlated-model errors |
| Handoff | Clear transfer of responsibility | Lost context and authority confusion |
| Quorum | Independent judgments with deterministic decision | Higher cost; false consensus |
| Hierarchy | Stable organizational decomposition | Deep latency and authority laundering |
| Blackboard | Shared evolving artifacts | Poisoning, races, unclear ownership |
| Peer mesh | Direct collaboration is essential | Difficult graph, budget, and security control |
| Recursive task tree | Unknown decomposition depth | Runaway expansion and poor termination |
| Dynamic membership | Capabilities truly vary at runtime | Supply-chain and reproducibility risk |
| Market | Explicit allocation utility can be measured | Gaming and allocation instability |
| Event-driven | Decoupled asynchronous domains | Duplicate, late, and reordered events |

Dynamic systems buy adaptability and utilization at the cost of reproducibility, admission complexity, manifest integrity, wider failure modes, and harder evals. Require bounded membership, authenticated registries, immutable versions, and per-run manifests.

## Invariants

- A system is a new governed artifact, not a bag of agents.
- System execution class and governance tier are floors over the composition.
- Runtime authority equals the intersection of caller, callee, edge, user, tenant, and policy authority.
- Every run has finite agent, depth, round, request, tool, token, cost, and time budgets.
- Every externally visible result records the exact composition manifest.
