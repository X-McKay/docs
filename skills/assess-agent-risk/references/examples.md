# Agent Risk Assessment Examples

## Read-only hiring recommendation

The agent does not write to an applicant-tracking system, so its execution class
may be `ephemeral`. Its recommendations can still affect employment opportunity
and may involve sensitive personal data. Screen applicable employment and AI
rules, assess legal, regulatory, privacy, reputational, and human-impact
scenarios, and set at least high governance until applicability and controls are
supported. Read-only does not mean low risk.

## Refund execution

Scenario:

> Because a manipulated conversation could cause an unsupported refund request,
> the agent could issue funds to the wrong party, causing financial loss, fraud,
> and customer harm.

Use `human_governed` execution. Score the unapproved transaction as inherent
risk. Possible controls include deterministic eligibility checks, actor and
tenant authorization, an amount ceiling, approval bound to canonical arguments,
an idempotency key, reconciliation, and reversal. Link each control to tests or
evals; do not reduce residual likelihood for a policy document alone.

## Infrastructure containment

An incident-response agent can isolate a host. Security benefit does not erase
operational risk: incorrect isolation could disrupt a critical service.
Assess both compromise propagation and erroneous containment. Evaluate approval
or pre-authorized emergency policy, blast-radius ceilings, simulation, safe
retries, Temporal recovery, kill switches, and rollback. The execution class is
normally `human_governed`; governance is high or critical depending on scope.

## Example finding

```text
RISK-PRIV-004 — Cross-tenant disclosure
Inherent: impact 4 × likelihood 3 = critical, confidence medium
Control: tenant scope rechecked inside the tool
Evidence: AUTH-021, test_tenant_isolation.py
Residual: impact 4 × likelihood 1 = high, confidence medium
Decision: conditional_go pending independent privacy review and alert exercise
Owner: customer-platform
Review: 2026-12-01
```

The impact stays critical because the authorization control reduces likelihood,
not the consequence of a successful disclosure.
