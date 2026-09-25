# Agent Risk Assessment Standard

## Required distinctions

- Execution class describes how work executes.
- Governance tier describes assurance required by inherent risk and mandatory
  floors.
- Residual risk describes what remains after verified controls.
- Launch decision states whether the assessed release may proceed.

The Agent Spec `risk_tier` is the governance tier. Determine it from the highest
inherent scenario, applicable legal or policy floor, and organizational
capability floors. Use residual risk for `go`, `conditional_go`, or `no_go`.

## Dimensions

Assess financial, operational, reputational, legal, security, privacy,
regulatory, and human-impact/safety harm. Treat autonomy, privilege, scale,
data sensitivity, reversibility, detectability, adversarial exposure, and human
oversight as drivers of likelihood or impact rather than separate dimensions.

## Scenario record

Write: “Because [cause], the agent could [unsafe action, output, or omission],
causing [harm] to [party or asset].” Record dimensions, parties, causes,
consequences, owner, inherent score, controls, evidence, residual score, evals,
indicators, alerts, runbook, and treatment.

## Scales

Impact:

1. Low — localized, short-lived, readily reversible.
2. Medium — meaningful but contained; normal recovery suffices.
3. High — material organizational or individual harm.
4. Critical — severe, widespread, systemic, life-safety, or substantially
   irreversible harm.

Likelihood:

1. Rare — multiple unusual conditions; evidence supports rarity.
2. Unlikely — credible but not expected in normal operation.
3. Likely — plausible in normal or adversarial operation, or observed before.
4. Frequent — expected, repeated, or already occurring.

| Impact ↓ / Likelihood → | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 1 | Low | Low | Medium | Medium |
| 2 | Low | Medium | Medium | High |
| 3 | Medium | Medium | High | Critical |
| 4 | High | High | Critical | Critical |

Use organization-specific materiality anchors. Score credible worst-case impact
within scope. Rate confidence `low`, `medium`, or `high`; low confidence in a
plausibly severe scenario calls for investigation or conservative treatment.

## Control credit

Classify controls as preventive, detective, or recovery. Credit a control only
when its owner, implementation, and effectiveness evidence are available.
Planned controls receive no credit. Human review is effective only when the
reviewer has authority, time, information, manageable workload, and tested
ability to intervene.

## Floors and decisions

- Prohibited use: `no_go`.
- Critical residual scenario: `no_go`.
- Material irreversible human or safety impact: at least high governance.
- Formal high-risk regulatory classification: at least high governance.
- Consequential external action: `human_governed` and at least high governance
  unless a stricter organizational floor applies.
- Privileged code execution, broad cross-tenant access, or critical-system
  control: at least high governance.
- Missing scope, owner, or material evidence: not low governance.

High residual risk requires independent review, explicit acceptance by the
designated authority, continuous monitoring, and a tested stop mechanism.
Medium residual risk requires an owner, monitoring, and time-bounded review.
Local policy and applicable law may be stricter.

## Traceability

Use scenario IDs in eval cases, traces, alerts, incidents, and risk acceptance.
Map each material scenario to deterministic invariants where possible,
behavioral and workflow cases where needed, production indicators, an alert or
review path, and recovery evidence. Block release when required evidence is
missing or a linked hard gate fails.
