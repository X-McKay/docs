# 1. Principles and scope

## Purpose

This playbook standardizes how teams justify, design, implement, evaluate,
deploy, and operate production multi-agent systems. Its primary goals are:

- Explicit system boundaries, membership, and ownership
- Reviewable coordination and delegation contracts
- Non-amplifying authority and controlled data flow
- Bounded concurrency, recursion, duration, and spend
- Durable recovery for coordinated or state-changing work
- Reproducible system behavior and release decisions
- Evidence for emergent quality, safety, reliability, and cost

## Scope

The standard applies when two or more model-driven agents participate in one
application outcome through delegation, handoff, review, voting, parallel work,
or shared coordination state.

It applies whether agents run in one process or many services, use the same or
different models, and communicate through in-process calls, Temporal, queues,
RPC, or another transport.

The standard does not classify a deterministic service, ordinary tool call, or
fixed software module as an agent merely because an agent invokes it.

## Multi-agent admission test

A team MUST document why a multi-agent design is justified before adopting it.
At least one of these benefits SHOULD be material and supported by a testable
hypothesis:

- Capability or privilege isolation between specialists
- Context or sensitive-data segregation
- Independent review that measurably reduces important errors
- Parallel work that materially improves latency or coverage
- Distinct ownership, deployment, or operational lifecycles
- A durable business process with separately governed agent responsibilities

A multi-agent design SHOULD NOT be selected only to create personas, divide a
prompt into roles, imitate an organization chart, or hide an oversized tool
catalog. Prefer a single conforming agent with skills and tools when it meets the
same outcome, safety, latency, and cost objectives with less complexity.

The system's evaluation plan MUST include a baseline capable of testing the
claimed multi-agent benefit. The baseline is normally the best reasonable
single-agent or deterministic implementation.

## Core principles

### Inherit, then extend

Every reachable member agent MUST independently satisfy the Agent Playbook. The
system contract adds composition requirements; it MUST NOT copy or silently
override member contracts.

### The graph is a governed capability

Membership, roles, and interaction edges are capabilities. Discovery of an
agent or endpoint is not permission to invoke it. Production systems MUST use an
explicit allowlisted graph.

### Authority only attenuates

An agent cannot grant authority it does not possess. Effective authority for an
interaction is the intersection of system policy, caller-delegable scope,
callee capability, authenticated actor scope, tenant context, and the current
deterministic policy decision.

### Typed boundaries, minimal context

Every interaction uses typed, bounded inputs and outputs. Pass the minimum
context and data required for the assigned objective. A transcript or shared
memory is not an implicit source of authorization or truth.

### Deterministic control, probabilistic collaboration

Use deterministic code for admission, authorization, routing constraints,
budget allocation, state transitions, conflict policy, approval, side effects,
and termination. Models may propose plans, choose among allowlisted routes, and
synthesize evidence within those controls.

### One owner for system truth

The system MUST identify the deterministic authority for workflow state,
accepted evidence, conflict resolution, final status, and externally visible
effects. Agents may propose changes but MUST NOT independently mutate shared
truth without going through that authority.

### Bounded autonomy

Depth, fan-out, concurrency, rounds, agent runs, model requests, tool calls,
time, tokens, and spend have explicit finite limits. Dynamic membership and
recursive delegation are opt-in architectural capabilities. They require
separate justification, admission controls, runtime bounds, and evidence, but
they are valid when a static composition cannot efficiently meet the need.

### Durable composition

Long-running coordination and any path capable of a side effect execute through
Temporal. Workflows own deterministic coordination; activities own agent runs,
model calls, tools, and other nondeterministic I/O.

### Evidence at both levels

Member evals prove individual behavior. System evals prove routing, handoffs,
aggregation, failure containment, termination, and end-to-end outcomes. Neither
substitutes for the other.

### Quality-adjusted system cost

Optimize total cost per successful, compliant system outcome. Count nested
agent runs, failed branches, retries, infrastructure, review, and recovery—not
only the coordinator's model usage.

## Required distinctions

- **Agent:** one independently contracted model-driven component.
- **System:** the versioned composition that coordinates member agents.
- **Role:** a system-specific responsibility assigned to a member.
- **Interaction:** one typed invocation or transfer across an allowed edge.
- **Delegation:** the caller assigns bounded work and later resumes control.
- **Handoff:** control transfers to another member without automatically
  returning to the caller.
- **Orchestrator:** deterministic code that owns system state and coordination.
- **Coordinator:** an agent allowed to propose or select bounded interactions.
- **Composition manifest:** the resolved, immutable bill of materials for a
  system release.

A model-driven coordinator is not the orchestrator and MUST NOT become the sole
authority for policy, approval, state integrity, or termination.

## Effective execution class and governance tier

The system's effective execution class MUST be at least the highest class
required by every reachable interaction, tool, and side effect. It may be higher
than any member's default class because coordination itself may be long-running
or stateful.

The system governance tier MUST be at least the highest tier among its reachable
members, applicable legal or policy floors, capability floors, and inherent
system-level risk scenarios. Composition can raise the tier; a low member tier
does not reduce a higher system tier.

Residual risk affects the launch decision, not the minimum assurance required
by the system's inherent risk and mandatory floors.

## Conformance

A system conforms when:

- The multi-agent admission test is documented.
- Every reachable member conforms to the Agent Playbook.
- The System Spec, composition manifest, and system risk assessment agree.
- Membership and interaction edges are explicitly allowlisted and validated.
- Required execution, authorization, data-flow, budget, and termination
  policies are enforced at startup and runtime.
- Member and system evaluation gates pass with reproducible provenance.
- Production readiness, residual-risk acceptance, and exceptions are complete,
  approved, and unexpired.
