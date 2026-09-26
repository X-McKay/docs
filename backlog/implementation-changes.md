# Implementation changes from the initial review

Recorded: 2026-09-26. These items track the concrete findings separately from the [opinion decisions](opinions-worth-revisiting.md). Priorities retain the [review definitions](../docs/reviews/initial-review/README.md#assessment): P1 blocks reliance on the affected tooling as a production control; P2 is a material design, reliability, or adoption issue.

All items are open and unassigned. Source evidence and verification limits remain in the review; an entry here does not mean the change is implemented.

## F01 — P1: Release policy omissions silently remove gates

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f01--p1-release-policy-omissions-silently-remove-gates).

**Change:** Publish versioned schemas for reports, policies, and
baselines. Reject unknown fields and unsupported versions. Require a meaningful
policy with an explicit subject/profile and mandatory gates for that profile.
Represent a deliberate absence of checks explicitly; do not infer it from `{}`.
Make the examples use the executable schema or label a conceptual format with
an explicit conversion step.

**Completion criteria:** Empty policy, misspelled section, wrong subject, unsupported
version, and unknown comparator all fail. Every published release-policy
example is parsed by the same implementation used in CI.

## F02 — P1: Non-finite numbers bypass numeric thresholds

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f02--p1-non-finite-numbers-bypass-numeric-thresholds).

**Change:** Require finite values in reports, baseline metrics,
threshold bounds, regression deltas, timeouts, and budgets. Use integer types
for counts; define legal metric ranges and reject inconsistent min/max pairs.
Reject nonstandard JSON constants on input and use `allow_nan=False` on output.
For monetary ledgers, use decimal values or integer currency units with defined
rounding rather than binary floats.

**Completion criteria:** NaN and both infinities fail in every numeric position, including
baseline and policy values. Boolean counts and fractional request limits fail.
Legitimate zero-use values remain representable where appropriate.

## F03 — P1: There is no integrated production-readiness gate

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f03--p1-there-is-no-integrated-production-readiness-gate).

**Change:** Preserve a draft/structural mode, but add a production mode
that takes a release manifest and validates the complete evidence graph. Require
approved/current risk decisions, satisfied launch conditions, authenticated
acceptance references, member readiness, system gates, manifest identity,
baseline provenance, and scenario coverage. Report each requirement as
`passed`, `failed`, `not_checked`, or justified `not_applicable`.

**Completion criteria:** A structurally valid `no_go`, expired assessment, unapproved
member, missing required scenario, or placeholder control blocks production
release. Development scaffolding can still be validated without pretending it
is production-ready. Document which command CI must use for each purpose.

## F04 — P1: Mandatory governance floors are not consistently enforced

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f04--p1-mandatory-governance-floors-are-not-consistently-enforced).

**Change:** Centralize tier derivation across agent/system validation,
scaffolding, risk explanation, and readiness. Compute capability floors from
resolved tools/authority, not author-entered risk summaries. Represent
organization-specific floors and conservative overrides explicitly. The agent
validator currently requires exact equality to its calculated floor, which
also needs a documented way to express a deliberately stricter tier.

**Completion criteria:** Consequential tools force the published execution and governance
minimums; declared policy floors apply at both levels; all inherited floors are
recomputed from referenced artifacts; raising a tier conservatively is supported
through an explicit policy mechanism.

## F05 — P1: System policy and schema references are not resolved sufficiently

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f05--p1-system-policy-and-schema-references-are-not-resolved-sufficiently).

**Change:** Add schemas and semantic resolvers for delegation,
data-flow, termination, approval, registry, and admission policies. Resolve every
edge schema and policy fragment; check caller/callee/mode agreement, scope
ceilings, classifications, root/child budgets, required-member reachability,
cycles, and topology-specific obligations. Keep runtime enforcement separate
and expose unverified runtime claims in the output.

**Completion criteria:** Empty or malformed policy, nonexistent schema, wrong fragment,
broader edge authority, unknown classification, conflicting limit, unreachable
required member, and missing quorum/conflict policy produce targeted failures.
The same resolved contract is consumed by startup/runtime code.

## F06 — P1: Temporal instructions describe incompatible default recovery units

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f06--p1-temporal-instructions-describe-incompatible-default-recovery-units).

**Change:** Name two supported patterns. Make workflow-hosted durable
agent execution the tested default for effectful agent loops. Permit coarse
read-only/restartable agent activities when whole-run retry is acceptable and
accounted for. A system may invoke a member's durable workflow when that is the
needed boundary. Do not imply wrapping a normal run in an activity preserves
per-tool progress. Explain when each pattern is conformant.

**Completion criteria:** A runnable example crashes after a model response, after an
external commit, and before activity completion. It demonstrates exactly which
steps repeat, how usage is recorded, and why no business effect is duplicated.
Skills, diagrams, chapter examples, and generated files teach the same patterns.

## F07 — P2: The generated factory drops declared Agent Spec behavior

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f07--p2-the-generated-factory-drops-declared-agent-spec-behavior).

**Change:** Use a version-tested `Agent.from_spec` path with explicit
trusted overrides, governance validation, and an allowlisted capability
registry. Ensure merged spec capabilities cannot bypass metadata allowlists.
Test effective configuration rather than just the presence of files.
[Agent Spec semantics](https://pydantic.dev/docs/ai/core-concepts/agent-spec/).

**Completion criteria:** A mocked-model construction test changes every supported spec
field and verifies runtime behavior/configuration. Unknown capabilities fail;
the stable agent name is explicit; packaged resources load outside the source
tree. Keep framework dependencies in a pinned example package, not necessarily
in the lightweight CLI.

## F08 — P2: System risk validation needs schema parity and robust diagnostics

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f08--p2-system-risk-validation-needs-schema-parity-and-robust-diagnostics).

**Change:** Build a System Risk schema from shared definitions, then
run typed semantic checks. Verify referenced member assessment identity,
version, digest, tier, status, and review freshness. Parse dates consistently,
including YAML's native date values; use an injected review date for deterministic
tests. Define `risk validate` discovery for both agent and system assessment
directories so generic recursive usage does not apply the wrong schema.

**Completion criteria:** Malformed nested arrays/mappings, boolean scores, invalid enums,
unquoted dates, missing approvals, fake evidence references, and same-tier score
reductions return structured diagnostics. Evidence verification distinguishes
an asserted reference from a reviewed, current result.

## F09 — P2: Evaluation provenance is descriptive rather than release-bound

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f09--p2-evaluation-provenance-is-descriptive-rather-than-release-bound).

**Change:** Issue a unique evaluation ID, write to a per-run temporary
report, record the source/artifact identity before execution, and atomically
publish after validation. Define report schemas with case-level evidence,
typed provenance, exact subject/version/manifest, dataset and evaluator
digests, run counts, and coverage. Require comparable baselines or an explicit
baseline migration. Keep signing/attestation as a later extension for CI trust
boundaries; signatures do not prove that an evaluation itself is correct.

**Completion criteria:** Stale/wrong-subject output, dirty or changed inputs, concurrent
runs targeting one path, missing manifest, incompatible baseline, zero run
count, and contradictory legacy/new subject fields cannot silently certify a
release. Add adapter timeout/cancellation handling and redact sensitive command
arguments before persisting invocation provenance.

## F10 — P2: Skills and examples have already drifted from the canonical contracts

**Status:** Open

**Owner:** Unassigned

**Source:** [Review finding](../docs/reviews/initial-review/README.md#f10--p2-skills-and-examples-have-already-drifted-from-the-canonical-contracts).

**Change:** Declare the source of truth for each artifact; generate or
validate copied snippets. Mark partial conceptual examples explicitly. Add
playbook version, skill version, owner, and compatibility metadata to distributed
skill bundles. Some references assume the whole playbook repository is present,
so verify a copied skill in an otherwise empty target repository.

The [installation guide](../skills/README.md) also recommends Codex
`.codex/skills` locations. Current official documentation lists `.agents/skills`
for local repository/user discovery; refresh the instructions and document
client/version compatibility without assuming all older clients behave alike.
[OpenAI skill discovery](https://learn.chatgpt.com/docs/build-skills).

**Completion criteria:** Copy-and-run examples validate under the advertised contract.
Skill bundles resolve every required reference after installation. Positive,
negative, and ambiguous trigger fixtures exist for all fourteen skills. Fix the
reproduced missing 64-character name limit and distinguish portable validation
from organization-specific authoring requirements.
