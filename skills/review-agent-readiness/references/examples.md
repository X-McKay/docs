# Agent Readiness Review Examples

## Finding Format

```markdown
### [P1] Prevent duplicate payment execution

Evidence: `src/tools/issue_payment.py` retries POST requests after an unknown
timeout outcome, and the request has no idempotency key.

Impact: A Temporal activity retry can issue the same payment more than once.

Remediation: Derive an idempotency key from the business operation ID, send it
to the payment API, and reconcile unknown outcomes before retrying.

Verification: Add a failure-injection test in which the provider commits and
then times out; assert that one payment exists after activity retry.
```

## Recommendation Example

```text
Recommendation: CONDITIONAL GO

Blocking conditions:
- None.

Pre-launch conditions:
- P2-1: Add a dashboard for cost per successful task. Owner: Agent Platform.
  Due: 2026-10-02.
- P2-2: Retain all high-risk denial traces regardless of normal sampling.
  Owner: Observability. Due: 2026-10-02.

Accepted risk:
- The first release supports one provider region; the service owner accepted
  the documented availability target and rollback behavior.
```

## Evidence Requests

If evidence is missing, ask for the concrete artifact: the last eval report, replay-test output, production dashboard, tool authorization test, redaction configuration, or incident runbook. Do not substitute an author statement for verifiable evidence.

## Edge Cases

- A read-only agent may still be high risk if it can expose regulated data.
- A workflow that passes today may still be unsafe to deploy if changed code cannot replay historical executions.
- An average eval score above threshold does not override one unauthorized action.
- A rollback that cannot undo external side effects must specify containment and reconciliation.
