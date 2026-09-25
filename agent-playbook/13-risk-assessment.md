# 13. Agent risk assessment

An agent risk assessment turns a broad risk label into a reviewable set of harm
scenarios, controls, evidence, decisions, and monitoring obligations. It applies
across use cases and complements—not replaces—legal, regulatory, security,
privacy, safety, and domain-specific review.

## Required distinctions

- **Execution class** describes how work executes: `ephemeral`, `durable`, or
  `human_governed`.
- **Governance tier** describes the assurance and oversight required: `low`,
  `medium`, `high`, or `critical`.
- **Inherent risk** is risk before risk-reducing controls.
- **Residual risk** is risk remaining after controls whose effectiveness is
  supported by evidence.
- **Launch decision** is `go`, `conditional_go`, or `no_go`.

These concepts MUST remain separate. A read-only system can be high risk, and a
durable system can be medium risk. The Agent Spec `risk_tier` is the governance
tier. It is anchored to inherent risk and mandatory floors; residual risk
determines whether the assessed release is acceptable to launch.

## Assessment principles

1. Assess concrete harm scenarios, not an agent in the abstract.
2. Consider harm to individuals, groups, organizations, society, and dependent
   systems.
3. Record both inherent and residual risk.
4. Do not average away a material scenario or dimension.
5. Give controls risk-reduction credit only when evidence supports their design
   and operation.
6. Record uncertainty explicitly; missing evidence never implies low risk.
7. Apply legal and regulatory classifications independently of the scoring
   matrix.
8. Keep acceptance and accountability with authorized humans. An agent or model
   may help draft an assessment but MUST NOT accept its own risk.

## Risk dimensions

Every assessment considers all eight dimensions. A scenario names one primary
dimension and any number of secondary dimensions.

| Dimension | Representative consequences |
| --- | --- |
| Financial | Direct loss, fraud, erroneous transactions, liability, or uncontrolled spend |
| Operational | Outage, corrupted records, duplicate action, process disruption, or recovery burden |
| Reputational | Loss of customer, partner, employee, regulator, or public trust |
| Legal | Contract, intellectual property, civil liability, rights, or litigation exposure |
| Security | Loss of confidentiality, integrity, or availability; privilege abuse; compromise |
| Privacy | Harmful collection, use, inference, disclosure, retention, or cross-tenant processing |
| Regulatory | Prohibited or controlled use, reporting duties, sanction, or licensing impact |
| Human impact and safety | Physical or psychological harm, discrimination, exclusion, or loss of opportunity |

Financial thresholds, outage durations, affected populations, data categories,
and comparable anchors MUST be calibrated to the adopting organization's risk
appetite. The playbook supplies a common method, not universal materiality
thresholds.

## Context and amplifiers

Before identifying scenarios, document the intended use, prohibited uses,
users, affected parties, jurisdictions, deployment environment, and accountable
owners. Inventory models, prompts, skills, tools, MCP servers, data sources,
memory, workflows, providers, approval paths, and downstream consumers.

Assess these factors as drivers of scenario likelihood or impact rather than as
additional dimensions:

- autonomy and ability to initiate actions;
- tool effect, transaction authority, identity, and privilege;
- data sensitivity, provenance, retention, and data subjects;
- affected population, vulnerable groups, and public reach;
- frequency, transaction value, and maximum blast radius;
- reversibility, compensation, detection, and time to intervention;
- exposure to untrusted or adversarial content;
- human review quality and ability to stop execution;
- model uncertainty, dependency concentration, and supply-chain exposure.

## Regulatory and prohibited-use screen

Run this screen before scoring. Record applicable jurisdictions, sectors,
contractual duties, internal policies, and named legal or compliance reviewers.

- A prohibited use is `no_go` regardless of its matrix score.
- A binding legal or regulatory classification sets a minimum governance tier
  and required controls.
- Uses involving health, employment, education, credit, insurance, housing,
  legal services, biometrics, critical infrastructure, children, or similarly
  consequential decisions require a documented applicability review and MUST
  NOT default to low risk.
- Unknown applicability is an unresolved risk, not evidence that no obligation
  applies.

The assessment MUST NOT claim that its score establishes legal compliance or a
formal regulatory classification.

## Scenario method

Write each material scenario in this form:

> Because **[cause or initiating condition]**, the agent could **[unsafe action,
> output, or omission]**, causing **[harm]** to **[affected party or asset]**.

Consider normal use, foreseeable misuse, adversarial use, dependency failure,
model error, authorization failure, retry and concurrency behavior, operator
error, and control failure. Each scenario records:

- stable ID, title, owner, and status;
- primary and secondary dimensions;
- affected parties and assets;
- causes, preconditions, and consequences;
- inherent impact, likelihood, tier, confidence, and rationale;
- preventive, detective, and recovery controls;
- evidence for each credited control;
- residual impact, likelihood, tier, confidence, and rationale;
- linked eval cases, indicators, alerts, runbooks, and treatment decision.

## Impact scale

Use dimension-specific organizational anchors within this common four-level
scale:

| Score | Meaning |
| --- | --- |
| 1 — Low | Localized, short-lived, readily reversible, and negligible external harm |
| 2 — Medium | Meaningful but contained harm recoverable through normal procedures |
| 3 — High | Material financial, operational, legal, security, privacy, reputational, regulatory, or human harm |
| 4 — Critical | Severe, widespread, systemic, life-safety, organization-threatening, or substantially irreversible harm |

Impact is evaluated at a credible worst case within the documented scope, not
at the average expected outcome. Controls reduce impact only when they truly
limit blast radius, duration, affected population, or reversibility.

## Likelihood scale

| Score | Meaning |
| --- | --- |
| 1 — Rare | Requires multiple unusual conditions, with evidence supporting rarity |
| 2 — Unlikely | Credible but not expected in normal operation |
| 3 — Likely | Plausible in normal or adversarial operation, or previously observed |
| 4 — Frequent | Expected, repeated, or already occurring without intervention |

Inherent likelihood assumes proposed risk-reducing controls are absent. Residual
likelihood includes only implemented controls with evidence. Base likelihood on
evals, tests, incidents, comparable systems, threat intelligence, domain review,
and production measurements where available.

## Risk matrix

| Impact ↓ / Likelihood → | 1 — Rare | 2 — Unlikely | 3 — Likely | 4 — Frequent |
| --- | --- | --- | --- | --- |
| 1 — Low | Low | Low | Medium | Medium |
| 2 — Medium | Low | Medium | Medium | High |
| 3 — High | Medium | Medium | High | Critical |
| 4 — Critical | High | High | Critical | Critical |

The highest material scenario determines the maximum inherent and residual
tiers. Teams MUST NOT average scenarios or dimensions into a lower tier.

## Confidence and uncertainty

Rate each inherent and residual score as `low`, `medium`, or `high` confidence.
Confidence describes the strength of evidence, not the risk level. A low-
confidence estimate with plausible severe consequences MUST be investigated,
constrained, or conservatively classified.

Record assumptions, unavailable evidence, disputed scores, and the conditions
that would change the rating.

## Controls and evidence

Classify controls as:

- **Preventive:** reduce the chance of the scenario, such as least privilege,
  deterministic authorization, allowlists, isolation, or bound approval.
- **Detective:** shorten time to discovery, such as policy telemetry,
  reconciliation, anomaly detection, or audit review.
- **Recovery:** limit duration or consequence, such as compensation, rollback,
  kill switches, safe workflow cancellation, or notification.

Every credited control names an owner and links to evidence. Acceptable evidence
includes code and configuration review, deterministic tests, eval results,
Temporal replay and failure scenarios, red-team results, audit samples,
operational metrics, exercises, and independent review. A planned control or an
untested policy receives no residual-risk reduction.

## Governance tier and mandatory floors

The governance tier is the highest of:

1. the maximum inherent scenario tier;
2. any legal, regulatory, contractual, or internal-policy floor; and
3. any capability floor established by the organization.

At minimum:

- a prohibited use is `no_go`;
- a material, potentially irreversible human or safety impact is at least
  `high` and may be `critical`;
- a formally classified high-risk regulated use is at least `high`;
- an agent able to execute consequential external actions requires
  `human_governed` execution and is at least `high` unless a documented
  organizational standard establishes a stricter floor;
- privileged code execution, broad cross-tenant access, or control of critical
  systems is at least `high`;
- incomplete scope, missing ownership, or materially insufficient evidence
  prevents a `low` classification.

Controls can make a release acceptable without silently lowering the assurance
level appropriate to the underlying use case.

## Residual-risk decision

Each scenario receives one treatment: `avoid`, `mitigate`, `transfer`, or
`accept`. Acceptance names the accountable role, rationale, conditions, expiry,
and next review date.

- A `critical` residual scenario is `no_go`.
- A `high` residual scenario requires independent review, explicit acceptance
  by the designated risk authority, continuous monitoring, and a tested stop or
  containment mechanism.
- A `medium` residual scenario requires a named owner, monitoring, and
  time-bounded review.
- A `low` residual scenario remains tracked when it could compound with other
  risks or when evidence confidence is low.

A `conditional_go` decision lists every condition, owner, deadline, monitoring
signal, and consequence of non-completion. Local policy or applicable law may
be stricter.

## Risk-to-evidence traceability

Every material scenario MUST link to pre-release and production evidence:

| Risk property | Required evidence |
| --- | --- |
| Authorization or approval | Deterministic denial, tamper, scope, and argument-binding tests |
| Model behavior | Versioned cases, evaluators, repeated runs, and failure distribution |
| Tool and workflow safety | Argument, ordering, retry, replay, duplication, timeout, and recovery tests |
| Security and privacy | Threat cases, isolation tests, redaction checks, and relevant review |
| Human or domain impact | Domain rubric, affected-party analysis, escalation, and expert review |
| Operational control | Indicator, alert, runbook, owner, exercise, and recovery evidence |

Use the scenario ID as an eval tag, trace attribute, risk-register key, and
incident reference. A release MUST fail when a required hard gate fails or when
a material scenario lacks the evidence required by its governance tier.

## Lifecycle and reassessment

Complete the assessment before implementation decisions become expensive, then
update it before release and throughout operation. Reassess after:

- a new model, provider, tool, skill, MCP server, data source, or permission;
- increased autonomy, transaction value, user population, or jurisdiction;
- a material prompt, policy, workflow, retry, approval, or deployment change;
- a failed hard gate, incident, near miss, complaint, or regulatory change;
- evidence that a control is ineffective or monitoring is incomplete.

Maximum review intervals remain 12 months for low, 6 months for medium, 3
months for high, and 1 month for critical governance tiers unless a stricter
obligation applies.

## Canonical artifact

Store one versioned assessment per agent under
`docs/risk-assessments/<agent>.yaml`, following the
[risk-assessment template](templates/risk-assessment.yaml). The Agent Spec
references this artifact, and the capability manifest, eval report, approval
record, and production traces record its version or digest.

The assessment is complete only when scope, scenarios, controls, evidence,
classification, acceptance, and review dates are populated and approved by the
required owners.
