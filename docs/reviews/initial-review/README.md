# Initial repository review

Reviewed commit: `6b987e65bafe744d115d1a1925adc260681a9592`

Branch: `feature/initial-review`

Review date: 2026-09-25 America/New_York / 2026-09-26 UTC

Scope: both playbooks, templates, fourteen skill packages and their references,
`agentctl` implementation/tests/schemas, packaging, and developer tooling.

## Assessment

The repository has a strong architectural foundation. Its best decisions are
deterministic authorization, explicit capability boundaries, separate inherent
and residual risk, evaluation of whole compositions, simpler-system baselines,
and treating agent output as untrusted. Keep those principles.

The highest-value next step is to make the standards internally consistent and
their claimed enforcement demonstrable. The CLI currently validates selected
declarations; it does not establish production conformance. Some declared
controls can be absent or invalid while checks succeed. The reference
implementations are explicitly illustrative, but there is no runnable example
that connects the contracts to the actual framework and proves the recovery,
approval, budget, and release behavior.

Prioritize these five changes:

1. Make release policies strict and reject non-finite numbers.
2. Separate structural validation from production readiness, and connect risk,
   member evidence, provenance, and approval to release decisions.
3. Choose and test explicit Temporal execution patterns across playbooks,
   skills, and scaffolds.
4. Publish one locked, runnable agent and a small composition before extending
   the topology catalog or building a larger runtime.
5. Establish one canonical contract vocabulary and continuously check every
   template, skill example, and generated artifact against it.

This is a review of a draft standards/tooling repository, not a production
application launch assessment. P1 below means a blocker to relying on the
affected tooling as a production control. No active production incident is
asserted. P2 denotes a material design, reliability, or adoption issue; P3 is
maintenance/clarity work. Proposed owners are role suggestions, not assignments
or accepted risks.

## Evidence and verification

The review combines source inspection, local execution, adversarial contract
fixtures, and [primary-source research](research.md). Facts reproduced locally
are distinguished from design recommendations and documentation-based findings.

| Check | Result |
| --- | --- |
| `nix develop --command just check` | Passed: lock check, Ruff, ShellCheck, 24 unit tests, skill validation |
| Ruff formatting check of existing CLI source/tests | Passed: 17 files already formatted |
| Python compilation of CLI source | Passed |
| `nix flake check` | Passed for the current `aarch64-darwin` host; other systems omitted; no application `checks` output is defined |
| Build CLI sdist and wheel | Passed; wheel contains both packaged JSON schemas |
| Additional review probes | Twelve observations: eleven exit-zero cases and one uncaught malformed-input exception; see qualifications below |
| PydanticAI/Temporal execution, live model evals, deployment recovery | Not run: no implemented, pinned runtime example exists in this repository |
| Other advertised OS/Python combinations and skill clients | Not executed |

Run the isolated probes from the repository root:

```bash
uv run --locked python docs/reviews/initial-review/reproduce_findings.py
```

The [probe script](reproduce_findings.py) creates temporary fixtures, calls the
existing CLI, and removes the fixtures afterward. It does not call models or
external services. Its exit status indicates completion, not conformance.
[Recorded observations](observations.json) identify the reviewed commit and
include diagnostic codes. Warning-only passes are not all bugs by themselves:
draft validation is useful. Their significance is the missing stronger readiness
gate and ambiguity about what a passing command proves.

## Findings requiring changes

### F01 — P1: Release policy omissions silently remove gates

**Evidence:** [release.py](../../../tools/agentctl/src/agentctl/release.py),
lines 76–146. `hard_gates`, `thresholds`, `required_provenance`, and `regressions`
default to empty collections. There is no strict release-policy schema.
The `empty_release_policy` and `unknown_policy_section` probes both return zero.
A report with quality `0.1` passes a policy declaring `quality_min: 0.9` under
the unsupported `quality` section.

**Impact:** A typo or copied playbook example can disable checks without any
diagnostic. This is especially likely because the eval chapters use
`quality`/`operational` sections and the eval skill uses `graded_gates`, while
the CLI consumes `thresholds`/`regressions`.

**Recommendation:** Publish versioned schemas for reports, policies, and
baselines. Reject unknown fields and unsupported versions. Require a meaningful
policy with an explicit subject/profile and mandatory gates for that profile.
Represent a deliberate absence of checks explicitly; do not infer it from `{}`.
Make the examples use the executable schema or label a conceptual format with
an explicit conversion step.

**Acceptance:** Empty policy, misspelled section, wrong subject, unsupported
version, and unknown comparator all fail. Every published release-policy
example is parsed by the same implementation used in CI.

### F02 — P1: Non-finite numbers bypass numeric thresholds

**Evidence:** [release.py](../../../tools/agentctl/src/agentctl/release.py),
lines 181–237 and 257–325; [evals.py](../../../tools/agentctl/src/agentctl/evals.py),
metric validation. `nan_threshold_metric` supplies YAML `.nan` and passes a
minimum-quality threshold. Comparisons against NaN are false, so the failure
conditions never trigger. Numeric validation checks type, not finiteness.

**Recommendation:** Require finite values in reports, baseline metrics,
threshold bounds, regression deltas, timeouts, and budgets. Use integer types
for counts; define legal metric ranges and reject inconsistent min/max pairs.
Reject nonstandard JSON constants on input and use `allow_nan=False` on output.
For monetary ledgers, use decimal values or integer currency units with defined
rounding rather than binary floats.

**Acceptance:** NaN and both infinities fail in every numeric position, including
baseline and policy values. Boolean counts and fractional request limits fail.
Legitimate zero-use values remain representable where appropriate.

### F03 — P1: There is no integrated production-readiness gate

**Evidence:** [risk.py](../../../tools/agentctl/src/agentctl/risk.py), lines
278–311, checks date ordering but not current expiry. Draft/open-question
diagnostics are warnings; rejected/retired states and `no_go` are not production
blockers in Agent Spec validation. The expired/no-go probe passes. The separate
[release checker](../../../tools/agentctl/src/agentctl/release.py) receives no
Agent/System Spec or risk assessment and cannot join these decisions.

The generated [system release policy](../../../tools/agentctl/src/agentctl/system_scaffold.py),
lines 544–552, requires only the placeholder gate, one quality threshold, and
nonempty `git_commit`. The minimal-system-release probe passes with no member
reports, safety/replay gates, approved baseline, composition manifest, risk
coverage, or real commit identity. This is materially weaker than the generated
single-agent policy, despite the system playbook inheriting member requirements.

**Recommendation:** Preserve a draft/structural mode, but add a production mode
that takes a release manifest and validates the complete evidence graph. Require
approved/current risk decisions, satisfied launch conditions, authenticated
acceptance references, member readiness, system gates, manifest identity,
baseline provenance, and scenario coverage. Report each requirement as
`passed`, `failed`, `not_checked`, or justified `not_applicable`.

**Acceptance:** A structurally valid `no_go`, expired assessment, unapproved
member, missing required scenario, or placeholder control blocks production
release. Development scaffolding can still be validated without pretending it
is production-ready. Document which command CI must use for each purpose.

### F04 — P1: Mandatory governance floors are not consistently enforced

**Evidence:** [validation.py](../../../tools/agentctl/src/agentctl/validation.py),
tool checks beginning at line 342, enforce execution class but not the high-risk
floor for consequential tools. `consequential_tool_low_governance` passes with
a declared consequential tool, human-governed execution, and low governance.
[systems.py](../../../tools/agentctl/src/agentctl/systems.py), lines 610–663,
derives floors from member and scenario tiers but omits declared regulatory
floors. `ignored_system_governance_floor` passes a medium system with a high floor.

**Recommendation:** Centralize tier derivation across agent/system validation,
scaffolding, risk explanation, and readiness. Compute capability floors from
resolved tools/authority, not author-entered risk summaries. Represent
organization-specific floors and conservative overrides explicitly. The agent
validator currently requires exact equality to its calculated floor, which
also needs a documented way to express a deliberately stricter tier.

**Acceptance:** Consequential tools force the published execution and governance
minimums; declared policy floors apply at both levels; all inherited floors are
recomputed from referenced artifacts; raising a tier conservatively is supported
through an explicit policy mechanism.

### F05 — P1: System policy and schema references are not resolved sufficiently

**Evidence:** [systems.py](../../../tools/agentctl/src/agentctl/systems.py),
lines 408–578. Several policy checks test file existence. Delegation validation
only checks an interaction ID if `interactions` already happens to be a mapping.
The empty-policy probe passes. Input/output schemas are nonempty strings in the
System Spec schema; the nonexistent-schema probe passes. Policy fragments are
stripped when resolving paths, without validating their actual target.

**Impact:** Passing validation does not prove a usable delegation contract,
authority attenuation, valid data flow, bounded retry behavior, or a resolvable
termination policy. These requirements are explicit in the system contract.

**Recommendation:** Add schemas and semantic resolvers for delegation,
data-flow, termination, approval, registry, and admission policies. Resolve every
edge schema and policy fragment; check caller/callee/mode agreement, scope
ceilings, classifications, root/child budgets, required-member reachability,
cycles, and topology-specific obligations. Keep runtime enforcement separate
and expose unverified runtime claims in the output.

**Acceptance:** Empty or malformed policy, nonexistent schema, wrong fragment,
broader edge authority, unknown classification, conflicting limit, unreachable
required member, and missing quorum/conflict policy produce targeted failures.
The same resolved contract is consumed by startup/runtime code.

### F06 — P1: Temporal instructions describe incompatible default recovery units

**Evidence:** [agent chapter 6](../../../agent-playbook/06-temporal-execution.md),
line 3, requires the agent run inside a workflow. [System chapter 6](../../../multi-agent-playbook/06-durable-coordination.md)
forbids calling agents there and wraps member runs in activities. The
[Temporal agent skill](../../../skills/implement-temporal-agent/SKILL.md),
its references, and [generated activities](../../../tools/agentctl/src/agentctl/scaffold.py)
also say to build/run PydanticAI in an activity. This is a documentation and
scaffold design conflict, not an observed production duplicate.

**External check:** PydanticAI documents the workflow-hosted agent loop with
model/tool/MCP activity boundaries. Temporal activities can retry after failure;
an activity-wrapped agent can repeat its whole run. These patterns therefore
need different effect identities and restart guarantees.
[PydanticAI integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/temporal/),
[Temporal activities](https://docs.temporal.io/activity-execution).

**Recommendation:** Name two supported patterns. Make workflow-hosted durable
agent execution the tested default for effectful agent loops. Permit coarse
read-only/restartable agent activities when whole-run retry is acceptable and
accounted for. A system may invoke a member's durable workflow when that is the
needed boundary. Do not imply wrapping a normal run in an activity preserves
per-tool progress. Explain when each pattern is conformant.

**Acceptance:** A runnable example crashes after a model response, after an
external commit, and before activity completion. It demonstrates exactly which
steps repeat, how usage is recorded, and why no business effect is duplicated.
Skills, diagrams, chapter examples, and generated files teach the same patterns.

### F07 — P2: The generated factory drops declared Agent Spec behavior

**Evidence:** [scaffold.py](../../../tools/agentctl/src/agentctl/scaffold.py),
lines 129–161. The factory loads a spec but constructs `Agent(...)` manually,
forwarding instructions while omitting explicit name, model settings, retries,
tool timeout, end strategy, instrumentation flag, and spec capabilities. A
settings capability hook exists, but it is not passed these top-level fields.
The scaffold is deliberately incomplete; the specific partial construction can
nevertheless look authoritative and silently diverge from the reviewed YAML.

**Recommendation:** Use a version-tested `Agent.from_spec` path with explicit
trusted overrides, governance validation, and an allowlisted capability
registry. Ensure merged spec capabilities cannot bypass metadata allowlists.
Test effective configuration rather than just the presence of files.
[Agent Spec semantics](https://pydantic.dev/docs/ai/core-concepts/agent-spec/).

**Acceptance:** A mocked-model construction test changes every supported spec
field and verifies runtime behavior/configuration. Unknown capabilities fail;
the stable agent name is explicit; packaged resources load outside the source
tree. Keep framework dependencies in a pinned example package, not necessarily
in the lightweight CLI.

### F08 — P2: System risk validation needs schema parity and robust diagnostics

**Evidence:** [systems.py](../../../tools/agentctl/src/agentctl/systems.py),
lines 169–398, uses hand-written shape checks rather than a System Risk schema.
Setting `residual: []` produces an uncaught `AttributeError`, reproduced in the
probe. The system risk summary does not validate all required approval/evidence
fields, and risk-reduction evidence is checked only when the tier falls, unlike
the agent validator, which also examines impact/likelihood decreases.

**Recommendation:** Build a System Risk schema from shared definitions, then
run typed semantic checks. Verify referenced member assessment identity,
version, digest, tier, status, and review freshness. Parse dates consistently,
including YAML's native date values; use an injected review date for deterministic
tests. Define `risk validate` discovery for both agent and system assessment
directories so generic recursive usage does not apply the wrong schema.

**Acceptance:** Malformed nested arrays/mappings, boolean scores, invalid enums,
unquoted dates, missing approvals, fake evidence references, and same-tier score
reductions return structured diagnostics. Evidence verification distinguishes
an asserted reference from a reviewed, current result.

### F09 — P2: Evaluation provenance is descriptive rather than release-bound

**Evidence:** [evals.py](../../../tools/agentctl/src/agentctl/evals.py), lines
36–78, uses report modification time for freshness and writes the Git commit
after the adapter runs. The release checker checks required field presence,
not semantic validity or equivalence of datasets, evaluators, manifests, and
model settings. A nonempty string can satisfy `git_commit`; no source-tree
dirty state or tested artifact digest is recorded.

**Recommendation:** Issue a unique evaluation ID, write to a per-run temporary
report, record the source/artifact identity before execution, and atomically
publish after validation. Define report schemas with case-level evidence,
typed provenance, exact subject/version/manifest, dataset and evaluator
digests, run counts, and coverage. Require comparable baselines or an explicit
baseline migration. Keep signing/attestation as a later extension for CI trust
boundaries; signatures do not prove that an evaluation itself is correct.

**Acceptance:** Stale/wrong-subject output, dirty or changed inputs, concurrent
runs targeting one path, missing manifest, incompatible baseline, zero run
count, and contradictory legacy/new subject fields cannot silently certify a
release. Add adapter timeout/cancellation handling and redact sensitive command
arguments before persisting invocation provenance.

### F10 — P2: Skills and examples have already drifted from the canonical contracts

**Evidence:** The [design skill's minimal spec](../../../skills/design-pydantic-agent/references/examples.md)
uses top-level governance fields and `version: 1`, unlike the canonical metadata
contract. The [tool example](../../../skills/design-agent-capabilities/references/examples.md)
uses `side_effect` and `authorization`, unlike CLI-required `effect` and
`authorization_scopes`. The [eval example](../../../skills/build-agent-evals/references/examples.md)
uses unsupported `graded_gates`. [System chapter 12](../../../multi-agent-playbook/12-reference-implementation.md),
lines 365–378, says implemented commands are still future work and passes a
system name where `system graph` expects a file path.

**Recommendation:** Declare the source of truth for each artifact; generate or
validate copied snippets. Mark partial conceptual examples explicitly. Add
playbook version, skill version, owner, and compatibility metadata to distributed
skill bundles. Some references assume the whole playbook repository is present,
so verify a copied skill in an otherwise empty target repository.

The [installation guide](../../../skills/README.md) also recommends Codex
`.codex/skills` locations. Current official documentation lists `.agents/skills`
for local repository/user discovery; refresh the instructions and document
client/version compatibility without assuming all older clients behave alike.
[OpenAI skill discovery](https://learn.chatgpt.com/docs/build-skills).

**Acceptance:** Copy-and-run examples validate under the advertised contract.
Skill bundles resolve every required reference after installation. Positive,
negative, and ambiguous trigger fixtures exist for all fourteen skills. Fix the
reproduced missing 64-character name limit and distinguish portable validation
from organization-specific authoring requirements.

## Opinions worth revisiting

These are design decisions for maintainers, not defects proved by a validator.
They are tracked as open items OP-001 through OP-008 in the
[decision backlog](../../../backlog/opinions-worth-revisiting.md).

| Current opinion | Recommended revision | Decision evidence |
| --- | --- | --- |
| Every external write requires Temporal | Keep Temporal as the supported reference backend, but state the underlying durability requirements separately. Clarify whether telemetry, provider billing, caches, and local artifacts count as prohibited ephemeral side effects. Consider an explicitly bounded transactional/idempotent profile for short operations. | Compare recovery, operational burden, latency, and failure windows on representative workloads. Any alternative must meet the same effect and audit requirements. |
| Execution class combines durability and human approval | Consider separate `durability` and `approval_mode` dimensions. Preserve per-action approval for unbounded/high-impact work; investigate narrowly pre-authorized action envelopes where delay itself creates risk. | Threat model the envelope, authority, amount/count/time limits, revocation, escalation, and human workload. Do not weaken current gates before that decision is approved. |
| Every reachable member needs a fully independent agent package and governance lifecycle | Keep runtime capability boundaries, but allow inherited evidence and a lightweight internal role profile for same-owner, same-release, no-new-authority components. | Show which failure/trust boundaries exist. Avoid both blanket duplicated paperwork and treating a privileged remote agent as a mere function. |
| Thirteen topology profiles are listed alongside a uniform scaffold | Publish an explicit support matrix: described, schema-validatable, scaffolded, runnable, and production-tested. Start runnable support with pipeline and bounded supervisor/fan-out. | The current scaffold generates a coordinator-to-workers graph regardless of selected topology; topology labels do not implement quorum, mesh, or event semantics. |
| Deterministic code owns accepted facts and final decisions | Clarify that code owns state transitions, admission, provenance, and acceptance criteria. It cannot mechanically establish arbitrary factual truth. Preserve contested/unknown states and human/domain adjudication. | Evaluate source reliability, conflicting evidence, and downstream harm when a well-typed claim is false. |
| Human review appears last in the evaluator hierarchy | Organize by claim type instead of a universal ranking. Humans define/calibrate domain truth and judge rubrics early; automated evaluators then scale the reviewed criteria. | Measure reviewer agreement, judge false positives/negatives, and drift on held-out cases. |
| Versioned logical model aliases are the production default; exact pins are exceptions | Keep logical routing for authoring, but resolve to immutable release evidence and record every fallback. A provider alias can change behavior without a repository edit. | Verify rollout/re-evaluation policy and distinguish artifact reproducibility from stochastic or provider-level reproducibility. |
| One fixed matrix and highest inherent tier determine governance | Keep non-averaging floors, but define likelihood time horizon/exposure, catastrophic-impact escalation, control-baseline assumptions, uncertainty handling, and organization calibration. | Compare independent assessors on real cases. NIST guidance supports structured risk management; it does not make this exact matrix or review cadence universal. [NIST RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) |

The simpler-baseline requirement is worth retaining. Multi-agent benefit is
task-dependent. Anthropic's research-system results demonstrate potential value
and substantial resource use, not a universal return on additional agents.
Compare both equal-budget quality and equal-quality cost/latency, and account
for isolation or independent ownership benefits that may not raise answer
quality. [Research system report](https://www.anthropic.com/engineering/multi-agent-research-system).

## Technical additions with the highest payoff

### Durable effects, approvals, and cancellation

The existing principles need one detailed failure protocol. Define a durable
business operation ID before a consequential call, bind it to canonical
arguments, and retain it across model retries, activity retries, workflow
recovery, and Continue-As-New. A model tool-call ID may be regenerated by a
whole-run retry; the example key should explain its required stability domain.

A local operation record plus a pre-call lookup does not close the window where
the remote system commits and the worker dies before recording success. Teach
provider idempotency, conditional writes, transactional outbox where applicable,
reconciliation, and an explicit `outcome_unknown` state. Never infer failure
from timeout alone. Concurrent or late workers need effect fencing or equivalent
commit-time authorization, not merely cancellation requests.

Specify an approval gateway that authenticates the human outside the workflow
payload; canonicalization rules; single-use approval consumption; replay/expiry
handling; separation of duties where required; and policy revocation between
approval and execution. Test approval versus cancel, changed arguments, expired
approval, conflicting approvers, remote commit versus timeout, and unavailable
audit storage. Hashes establish integrity only when their source and binding are
trusted. [Temporal message handling](https://docs.temporal.io/develop/python/workflows/message-passing).

Add a deployment recipe choosing Pinned/Auto-Upgrade behavior, continuation
migrations, and old-worker retirement conditions. “Use versioning or patching”
is sound direction but insufficient operating guidance.
[Worker Versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning).

### Budgets: distinguish accounting, admission, and final settlement

The single-agent chapter acknowledges one-request overshoot. Extend that warning
to concurrent workers and interrupted calls. PydanticAI's shared counters,
including Redis, do not provide strict pre-dispatch escrow; counter retention
can also matter after long waits. This is a gap between the proposed system
guarantee and a likely implementation choice, not evidence of a faulty ledger
in this repository. [Spend Limits](https://pydantic.dev/docs/ai/harness/spend/).

Specify reservation IDs, atomic reserve/settle operations, idempotent charging,
conservative upper-bound prices, retries, ambiguous usage, and limits on
unsettled liabilities. A timed-out child must not release a grant merely because
the parent stopped waiting while the provider may still bill it. Reserve capacity
for reconciliation, compensation, and required finalization. Test worker loss at
every ledger transition and concurrency at the root/tenant/deployment levels.

Separate money and capacity: budget checks do not enforce provider rate limits,
fairness, queue age, or downstream saturation. Use zero-tool/zero-model budgets
where roles genuinely require no such capability; positive-only count fields
currently cannot express that useful restriction.

### Evaluation: strengthen the meaning of a pass

The playbooks correctly prohibit averaging away a failed hard gate. Add
denominators, sample sizes, representative strata, uncertainty intervals,
held-out cases, contamination checks, judge calibration, and baseline approval
semantics. Zero observed failures does not establish zero failure probability.
For illustration, under independent identically distributed Bernoulli trials,
zero failures in `n` trials gives a one-sided 95% upper bound
`1 - 0.05 ** (1 / n)`, about 2.95% for 100 trials. Correlated adversarial cases
and production distribution shift do not satisfy that simple assumption.

Distinguish first-attempt reliability, success after retries, and consistency
across repeated trials. Count all attempts, cost, and denied actions. Keep
deterministic enforcement tests separate from stochastic attack-resistance
measurements. [Agent eval methodology](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

Provide a pinned Pydantic Evals adapter with case-level failures, grouped repeat
results, scenario coverage, and normalized release metrics. Choose aggregation
deliberately instead of copying only framework averages.
[Pydantic Evals repeats](https://pydantic.dev/docs/ai/evals/how-to/multi-run/).

### Authority, data, and protocol integrations

Add a capability-to-control matrix. For example, PydanticAI Subagents isolate
history but forward dependencies, and their tool returns text. Wrapping that
primitive does not automatically deliver the typed, attenuated boundary defined
here. Require an explicit dependency projection and result adapter.
[Subagents](https://pydantic.dev/docs/ai/harness/subagents/).

Document which controls must wrap Dynamic Workflow: its sandbox time cap excludes
subagent waiting and it does not support nested workflows. Treat model-authored
choreography as a separate reviewed execution mode rather than implying it
implements arbitrary recursive Temporal graphs.
[Dynamic Workflow](https://pydantic.dev/docs/ai/harness/dynamic-workflow/).

For MCP, add audience validation, no token passthrough, egress/SSRF defenses,
session/transport identity, tool-description change detection, and tests for
malicious results. For A2A, explicitly map tasks, artifacts, cancellation,
authorization-required states, and callback authentication to local contracts.
Neither protocol removes application authorization obligations.
[MCP security](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices),
[A2A specification](https://a2a-protocol.org/latest/specification/).

Add retrieval/memory controls: source ACL filtering before retrieval, freshness,
deletion propagation, evidence provenance, poisoning recovery, and authorization
again when an artifact is resolved. Treat egress and rendered output as effect
boundaries too; read-only tools can still enable disclosure.

### Observability and privacy

Keep content capture off by default, bounded metric cardinality, and the separate
audit record. Add working collector/instrumentation settings and redaction tests
that inspect exported data. A hash of a guessable sensitive identifier is not
necessarily anonymization, and hashing an ID does not reduce cardinality.

Define a common outcome schema and mappings: workflow `completed_degraded`,
telemetry `success_degraded`, and the various scaffold result enums currently
need an explicit relationship. Use bounded spans and causal links across long
waits rather than assuming a single open trace will survive days of execution.
Make attributes conditional on execution mode; ephemeral runs have no Temporal
workflow ID. Specify which audit failures block effects, how audit writes recover,
and how critical evidence survives exporter outage.

Update the OpenTelemetry reference: its GenAI page now points to a separate
maintained repository. Pin the emitted convention and instrumentation versions.
[Relocation notice](https://opentelemetry.io/docs/specs/semconv/gen-ai/).

## Chapter-by-chapter opportunities

The table covers the thirteen chapters in each playbook. Larger findings above
take precedence; these are additional editing targets.

| Chapter | Agent Playbook | Multi-Agent Systems Playbook |
| --- | --- | --- |
| 1 — Principles/scope | Define business side effects and separate backend choice from guarantees. | Retain admission test; define lightweight internal roles and comparable baselines. |
| 2 — Architecture | Add a runnable packaged example and manifest generation. | Add supported-pattern matrix, graph identity, and explicit trust-boundary diagrams. |
| 3 — Contract | Publish metadata/tool schemas; align docs with required `evaluation_policy` and `temporal_enabled`; bind model resolution to releases. | Validate policy/schema references, owners, justification evidence, and graph closure; distinguish member identity from role assignment. |
| 4 — Skills/membership | Add owner/version metadata, trigger evals, resource-loading example, and standalone install tests. | Implement restriction intersections and evidence inheritance; decide how one agent can occupy multiple roles when validation currently forbids duplicate agent names. |
| 5 — Tools/interactions | Specify per-tool effects within mixed-effect toolsets, typed error taxonomy, idempotency domain, and tool usability evals. | Define required scopes, protocol settlement, source trust, and typed partial-effect/unknown outcomes. |
| 6 — Durability | Resolve execution-pattern conflict; demonstrate crash recovery, canonical approvals, continuation, and versioned workers. | Add cancellation fencing, late-effect reconciliation, budget recovery, and graph/manifest continuation tests. |
| 7 — Evaluation | Use executable policy examples and statistical release criteria. | Require member gates plus composition gates; use matched-budget comparisons and preserve correlated-failure analysis. |
| 8 — Observability | Provide exporter configuration, privacy tests, and bounded trace lifetimes. | Tie graph events, ledger, audit, and workflow state together with a reconciliation invariant. |
| 9 — Cost | Distinguish soft runtime brakes from hard reservations and provider billing. | Specify unresolved liabilities and worst-case expansion; add fair admission and finalization reserve. |
| 10 — Security | Map threats to tests; add MCP protocol controls and evidence-store lifecycle. | Add compromised-member containment, control-plane isolation tests, and revocation races. |
| 11 — Readiness | Make each checklist item refer to a requirement ID and evidence type. | Implement a manifest-bound release decision that includes member readiness and exceptions. |
| 12 — Reference implementation | Replace the adoption-critical pseudocode path with a locked working example. | Correct stale CLI claims/path examples; demonstrate one complete small system before generalized runtime APIs. |
| 13 — Risk | Calibrate likelihood horizon, validate freshness/floors, and verify evidence. | Add a schema; verify member digests/status, floors, score reductions, and conditional acceptance. |

## Repository and tooling roadmap

### First batch: correctness and truthful guarantees

Suggested owner: CLI maintainers with a playbook reviewer. Complete before using
the CLI as an authoritative production gate.

- Implement F01/F02 and strict report/policy/baseline schemas.
- Add regression tests for every reproduced defect; keep draft-mode expectations
  explicit instead of changing warning semantics indiscriminately.
- Address F03/F04/F05/F08 with shared risk/policy definitions and a production
  readiness mode. Derive release requirements from a chosen profile.
- Correct the Temporal conflict, factory forwarding, stale command examples,
  and installation instructions. Add a capability/support table to the README.

Success criterion: unsafe/malformed fixtures fail predictably, current behavior
is accurately documented, and a passing command states exactly what was checked.

### Second batch: prove the reference stack

Suggested owner: runtime/example maintainers, with reliability and security
review. Start after the execution-pattern decision.

- Add an isolated example workspace pinning PydanticAI core, Harness, Evals,
  Temporal SDK, supported server version, and instrumentation settings.
- Implement one read-only agent, one approved idempotent effect, and a bounded
  two-member composition. Supply typed configuration and resource loading.
- Use mocked models for fast checks; add local Temporal failure/replay tests and
  an optional, budgeted real-model eval suite.
- Generate capability/composition manifests and demonstrate end-to-end evidence
  from risk scenario through test/eval report to a release decision.

Success criterion: a new contributor can run the documented path and reproduce
successful execution plus denied, expired, duplicate, timeout, and recovery cases.

### Third batch: prevent standards drift

Suggested owner: repository/CI and documentation maintainers.

- Add actual CI workflows. The repository currently contains no checked-in
  `.github/workflows` configuration despite recommending CI checks.
- Make `just check` include formatting validation, Markdown lint, internal-link
  checks, schema validation, snippet validation, and generated-fixture checks.
  `.markdownlint.jsonc` exists but no Markdown checker is wired into the command.
- Add Nix `checks` outputs if `nix flake check` is intended to test application
  behavior. Keep the uv-only path documented and run a realistic OS/Python matrix.
- Test a built wheel from outside the checkout; the current packaged-schema unit
  test runs in an editable source install, although this review confirmed wheel
  inclusion. Pin/build-test the build backend for reproducible releases.
- Assign stable requirement IDs and publish a requirement → schema → validator →
  runtime check → evidence table. Each skill reference should declare its source
  playbook version; generated snippets should carry provenance.
- Add scheduled external-reference checks with human review of semantic changes,
  especially framework behavior and protocol/security versions.

Success criterion: changing a contract cannot leave its templates, skill copies,
examples, or generated outputs silently inconsistent.

### Fourth batch: adoption and long-term maintenance

Suggested owner: repository maintainers, with product/risk owners for policy
decisions. Prioritize after the reference path works.

- Add a short reader map: choosing an architecture, first agent, first system,
  production rollout, and exception process. Keep advanced topologies in clearly
  marked extensions rather than making every adopter absorb the full catalog.
- Add `CONTRIBUTING.md`, change/release notes, review ownership, supported
  versions, and a security-reporting policy. Decide the repository's license;
  do not infer redistribution rights from public availability.
- Provide optional install/sync tooling for versioned skill bundles, with a
  manifest, drift detection, and uninstall instructions. Avoid mutable symlink
  updates changing a supposedly pinned runtime release unnoticed.
- Evaluate narrower skill descriptions and selection overlap. Add repeatable
  trigger/negative-trigger suites before consolidating or expanding the catalog.
  [Official authoring guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
- Harden loaders: reject duplicate YAML keys, define path/symlink trust boundaries,
  centralize semantic-version parsing, and keep diagnostic codes unique
  (`AGENT035`/`AGENT036` currently have unrelated meanings).
- Define identity collision rules across agents, systems, workflow modules, eval
  output paths, and artifact stores. Agent/system default reports share
  `artifacts/evals/<name>.json`; names need partitioning or enforced uniqueness.
- Restrict scaffolding to implemented topology profiles or generate
  topology-specific fixtures; validate Python identifiers and serialize user
  inputs safely rather than interpolating them into YAML templates.

## Suggested decision order

Resolve three maintainer decisions before broad implementation: the supported
Temporal execution patterns; the exact meaning of structural validation versus
production conformance; and the canonical schemas/evidence model. Then deliver
the first two batches together as a small, tested adoption path. Additional
topologies, UI work, or policy breadth will be more valuable once that path is
reliable.

This branch contains review documentation and isolated reproduction evidence.
It does not silently change organizational policy or claim that proposed
controls have been implemented. See [research scope and sources](research.md)
for verification limits and current external guidance.
