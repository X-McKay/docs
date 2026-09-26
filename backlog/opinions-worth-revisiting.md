# Opinions worth revisiting

Recorded: 2026-09-26. Source: the [initial repository review](../docs/reviews/initial-review/README.md#opinions-worth-revisiting) of commit `6b987e65bafe744d115d1a1925adc260681a9592`.

These are proposed maintainer decisions, distinct from the reproduced tooling defects in the review. Existing requirements remain in force until a decision and any resulting changes are approved. The proposed direction is a hypothesis to assess; retaining the current opinion is also a valid outcome. Consult the [research notes](../docs/reviews/initial-review/research.md) for external sources and verification limits.

## OP-001 — Durability requirements and Temporal

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Every external write requires Temporal.

**Proposed direction:** Keep Temporal as the supported reference backend, but state the underlying durability requirements separately. Clarify whether telemetry, provider billing, caches, and local artifacts count as prohibited ephemeral side effects. Consider an explicitly bounded transactional/idempotent profile for short operations.

**Evidence needed:** Compare recovery, operational burden, latency, and failure windows on representative workloads. Any alternative must meet the same effect and audit requirements.

**Completion criteria:** Publish a decision defining covered side effects, required recovery guarantees, and supported execution profiles. Update both playbooks and their skills/scaffolds consistently, and identify the recovery tests required for each supported profile.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-002 — Durability and human approval

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Execution class combines durability and human approval.

**Proposed direction:** Consider separate `durability` and `approval_mode` dimensions. Preserve per-action approval for unbounded/high-impact work; investigate narrowly pre-authorized action envelopes where delay itself creates risk.

**Evidence needed:** Threat model the envelope, authority, amount/count/time limits, revocation, escalation, and human workload. Do not weaken current gates before that decision is approved.

**Completion criteria:** Record whether to retain the current execution classes or separate durability from approval. Define the migration and compatibility rules if changed, and require tests for approval expiry, revocation, envelope exhaustion, and unauthorized escalation.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-003 — Governance for internal agent roles

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Every reachable member needs a fully independent agent package and governance lifecycle.

**Proposed direction:** Keep runtime capability boundaries, but allow inherited evidence and a lightweight internal role profile for same-owner, same-release, no-new-authority components.

**Evidence needed:** Show which failure/trust boundaries exist. Avoid both blanket duplicated paperwork and treating a privileged remote agent as a mere function.

**Completion criteria:** Define eligibility for an internal role profile, inherited versus independently required evidence, and promotion triggers when authority or ownership changes. Demonstrate the rules on a small composition before changing membership requirements.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-004 — Topology support and scaffolding

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Thirteen topology profiles are listed alongside a uniform scaffold.

**Proposed direction:** Publish an explicit support matrix: described, schema-validatable, scaffolded, runnable, and production-tested. Start runnable support with pipeline and bounded supervisor/fan-out.

**Evidence needed:** The current scaffold generates a coordinator-to-workers graph regardless of selected topology; topology labels do not implement quorum, mesh, or event semantics.

**Completion criteria:** Publish the support matrix and choose the initial runnable topology set. Align CLI options and generated artifacts with that support level; provide a runnable example and topology-specific validation for each supported implementation.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-005 — Deterministic authority and factual truth

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Deterministic code owns accepted facts and final decisions.

**Proposed direction:** Clarify that code owns state transitions, admission, provenance, and acceptance criteria. It cannot mechanically establish arbitrary factual truth. Preserve contested/unknown states and human/domain adjudication.

**Evidence needed:** Evaluate source reliability, conflicting evidence, and downstream harm when a well-typed claim is false.

**Completion criteria:** Document which facts are assertions, evidence-backed claims, or accepted state. Define conflict and unknown outcomes, the authority that can resolve them, and examples showing how false but well-typed claims are handled.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-006 — Human review in evaluation

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Human review appears last in the evaluator hierarchy.

**Proposed direction:** Organize by claim type instead of a universal ranking. Humans define/calibrate domain truth and judge rubrics early; automated evaluators then scale the reviewed criteria.

**Evidence needed:** Measure reviewer agreement, judge false positives/negatives, and drift on held-out cases.

**Completion criteria:** Replace or explicitly justify the evaluator ordering with a claim-to-evaluator mapping. Publish a calibration example with human agreement and automated-judge error measurements, plus the conditions requiring renewed human review.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-007 — Model aliases and release identity

**Status:** Open

**Owner:** Unassigned

**Current opinion:** Versioned logical model aliases are the production default; exact pins are exceptions.

**Proposed direction:** Keep logical routing for authoring, but resolve to immutable release evidence and record every fallback. A provider alias can change behavior without a repository edit.

**Evidence needed:** Verify rollout/re-evaluation policy and distinguish artifact reproducibility from stochastic or provider-level reproducibility.

**Completion criteria:** Define the release model identity, alias resolution, fallback recording, and re-evaluation policy. Specify how releases handle providers without immutable model identifiers, and demonstrate the resulting provenance in an evaluation report.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.

## OP-008 — Risk matrix and governance calibration

**Status:** Open

**Owner:** Unassigned

**Current opinion:** One fixed matrix and highest inherent tier determine governance.

**Proposed direction:** Keep non-averaging floors, but define likelihood time horizon/exposure, catastrophic-impact escalation, control-baseline assumptions, uncertainty handling, and organization calibration.

**Evidence needed:** Compare independent assessors on real cases. NIST guidance supports structured risk management; it does not make this exact matrix or review cadence universal. [NIST RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)

**Completion criteria:** Publish likelihood horizons, exposure assumptions, uncertainty rules, and organization-specific floors. Compare independent assessments of representative scenarios and document calibration changes, including critical-impact escalation and review intervals.

**Resolution:** Pending. Record the decision date, rationale, evidence, and implementation or follow-up links here.
