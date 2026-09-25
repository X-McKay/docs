# Agent Capability Examples

## Choose the Mechanism

Request: “Calculate a tax total exactly.” Use deterministic code.

Request: “Explain the investigation procedure and required evidence.” Use a skill.

Request: “Fetch an account balance.” Use a read tool.

Request: “Issue a refund.” Use a human-gated or tightly authorized write tool, not prompt text alone.

## Tool Contract Example

```yaml
name: create-refund-proposal
owner: payments-platform
side_effect: write_reversible
authorization: support.refund.propose
idempotency_key: case_id
timeout_seconds: 10
retryable:
  - timeout_before_commit
terminal:
  - permission_denied
  - invalid_amount
  - policy_denied
input: RefundProposalInput
output: RefundProposal
consumers:
  - support-agent
```

The proposal tool may be retried with the same case ID. A separate approval workflow owns execution of the refund.

## Portable Skill Example

```text
skills/investigate-support-case/
  SKILL.md
  agents/openai.yaml
  references/
    evidence-standard.md
    examples.md
```

```markdown
---
name: investigate-support-case
description: Investigate a support case using account and ticket evidence. Use when asked to diagnose a customer issue, assemble evidence, or recommend escalation.
---

# Investigate a Support Case

1. Confirm the account and case identifiers.
2. Load only the evidence needed for the reported issue.
3. Separate observed facts from inferences.
4. Cite evidence identifiers in the recommendation.
5. Escalate when required evidence is missing or conflicting.
```

## Edge Cases

- A “read” endpoint that marks records viewed is technically a write; classify its real behavior.
- A skill that instructs the agent to call a tool still requires the tool to be allowed and authorized.
- A shared skill with domain-specific policy should be split or parameterized only when ownership remains clear.
- A tool that may commit before timing out requires an idempotency lookup before retry.
