# Agent Interaction Standard

Each interaction declares a stable ID, caller, callee, mode, input and output schema, policy reference, maximum calls, timeout, failure behavior, and observability correlation.

## Authority Rule

Effective authority is the intersection of:

- authenticated user and tenant scope;
- caller authorization;
- callee maximum authorization;
- edge policy;
- current workflow state and approval;
- data classification and purpose restrictions.

Use task-scoped credentials or capability tokens where possible. Never forward provider secrets or ambient credentials in prompts.

## Context Rule

Prefer structured task input, minimal summaries, and authorized artifact references. Label untrusted model or tool content as data. Preserve origin, integrity hash, and producer version for shared artifacts.

## Delivery Rule

Coordination owns retry. Callees expose idempotent operations or explicit idempotency keys. Persist delegation IDs and effect receipts. Define handling for duplicate, late, malformed, contradictory, cancelled, and partially applied results.

## Aggregation Rule

Define how evidence is combined before execution. Keep dissent when uncertainty matters. Quorum rules specify eligibility, independence assumptions, abstentions, ties, and a deterministic final decision function.
