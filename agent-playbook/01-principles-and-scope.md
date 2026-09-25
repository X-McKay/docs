# 1. Principles and scope

## Purpose

This playbook standardizes how teams design, implement, evaluate, deploy, and operate AI agents. Its primary goals are:

- Predictable architecture across agent projects
- Explicit trust, authorization, and side-effect boundaries
- Durable recovery for long-running or state-changing work
- Reproducible behavior and release decisions
- Observable quality, safety, latency, and cost
- Clear ownership throughout the lifecycle

## Scope

The standard applies to production agents built with PydanticAI, including agents exposed through APIs, user interfaces, background jobs, schedules, and event-driven workflows.

It covers single-agent and multi-agent systems. In a multi-agent system, each agent MUST satisfy the agent contract independently, and the coordinating workflow MUST satisfy the requirements associated with the highest effective execution class and risk tier.

## Core principles

### Declarative intent, typed enforcement

Use a PydanticAI Agent Spec to declare identity, instructions, model defaults, retry budgets, timeouts, capabilities, and metadata. Use Python and Pydantic types to enforce runtime inputs, dependencies, outputs, policies, and tool contracts.

### Least capability

An agent receives only the skills, tools, data, network access, and credentials needed for its purpose. Capability discovery is not authorization.

### Deterministic control, probabilistic assistance

Use deterministic code for authorization, budget enforcement, approval, routing constraints, validation, and business invariants. Use the model for interpretation, synthesis, planning, and judgment within those boundaries.

### Durable side effects

Any agent that can modify external state MUST run through Temporal. Model requests and I/O execute as activities; deterministic coordination executes in workflows.

### Human control for consequential action

Approval is bound to an exact action, arguments, actor, tenant, and policy version. A model cannot grant or infer approval.

### Evaluation before intuition

Behavioral changes are accepted through evidence: deterministic tests, offline evals, trajectory checks, durability scenarios, and staged production observation.

### Quality-adjusted cost

Optimize cost per successful, compliant outcome. A cheaper run that reduces task success or safety is not an optimization.

### Observable by design

Every production run can be attributed to a specific agent, configuration, model, skill set, tool set, worker build, and evaluation baseline.

## Execution classes

### Ephemeral

Use for short-lived, low-risk, request-response work.

- Temporal is optional.
- Tools MUST be read-only.
- The agent MUST NOT create externally visible side effects.
- Failure may require the caller to retry the run.

Typical uses include classification, extraction, summarization, and read-only retrieval.

### Durable

Use for long-running work, recoverable processes, or any side effect.

- The run MUST execute inside a Temporal workflow.
- Model, tool, MCP, database, filesystem, and network I/O MUST execute in activities.
- Side-effecting activities MUST be idempotent or use stable idempotency keys.
- Retry, timeout, cancellation, and compensation behavior MUST be explicit.

### Human-governed

Use for consequential operations requiring accountable human review.

- All durable requirements apply.
- The workflow MUST pause before consequential action.
- The approver MUST be authenticated outside model control.
- Approval MUST be recorded and bound to a canonical action hash.
- Materially changed arguments MUST require new approval.

## Conformance

A service conforms when:

- All production agents satisfy the canonical contract.
- All exposed tools and skills satisfy their respective standards.
- Execution class and risk controls are enforced at startup and runtime.
- Required evaluation and production gates pass.
- Exceptions are documented, approved, and unexpired.
