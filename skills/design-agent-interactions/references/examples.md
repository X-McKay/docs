# Agent Interaction Examples

## Delegation Envelope

```yaml
id: investigate-account
from: coordinator-agent
to: support-researcher
mode: delegate
input_schema: InvestigationRequest
output_schema: EvidenceBundle
policy: policies/delegation.yaml#investigate-account
max_calls: 2
timeout_seconds: 30
```

The policy narrows tools to read-only account history, limits data to the current tenant, and reserves budget before dispatch.

## Producer-Reviewer

The producer returns a proposal and evidence references. The reviewer returns `accept`, `revise`, or `escalate`, plus finding codes. A deterministic coordinator applies the outcome; the reviewer cannot execute the proposal.

## Late Result

After a delegation deadline, mark the durable state timed out. A late result is audited and discarded unless an explicit reconciliation state permits it. It must never revive a completed consequential action.
