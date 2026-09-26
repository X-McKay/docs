# Multi-Agent System Design Examples

## Fixed Research System

A planner delegates independent questions to two read-only researchers and sends collected evidence to a reviewer. Use a supervisor-worker graph with pinned versions, parallelism of two, no recursive delegation, evidence-linked outputs, and deterministic aggregation. Compare quality, latency, and cost against one research agent.

## Dynamic Specialist Pool

Runtime specialist selection is appropriate only when capabilities or availability change materially. Resolve candidates through an authenticated registry; admit only allowlisted publishers, compatible contracts, current risk assessments, and bounded tiers; record selected immutable versions in the run manifest. Fall back to a reviewed static pool when admission fails.

## Simplify Instead

If a proposed writer and formatter use identical models, authority, and context in a strictly sequential path, implement two deterministic stages or one agent with typed phases. The extra agent adds coordination cost without meaningful isolation or independent judgment.
