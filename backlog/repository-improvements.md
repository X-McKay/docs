# Runtime and repository improvements

Recorded: 2026-09-26. All items are open and unassigned. These extend the
[concrete findings](implementation-changes.md) with the broader technical and
repository recommendations from the initial review. They are proposed work,
not implemented controls. Resolve related [opinion decisions](opinions-worth-revisiting.md)
before adopting a conflicting policy.

The [chapter-by-chapter review](../docs/reviews/initial-review/README.md#chapter-by-chapter-opportunities)
remains the editing checklist for all twenty-six chapters. Each item below
should update affected chapters, templates, skills, and generated artifacts
together.

## RI-001 — Prove the reference stack

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch, after the
Temporal execution-pattern and contract decisions in F03/F05/F06.

- Add an isolated example workspace pinning PydanticAI core, Harness, Evals,
  Temporal SDK/server compatibility, and instrumentation.
- Implement one read-only agent, one approved idempotent effect, and a bounded
  two-member composition with typed configuration and resource loading.
- Generate capability/composition manifests and connect risk scenarios to
  evaluation evidence and release decisions.
- Provide mocked-model checks, local Temporal replay/failure tests, and an
  optional budgeted real-model evaluation suite.

**Completion criteria:** A new contributor can run the documented path and
reproduce successful, denied, expired, duplicate, timeout, and recovery cases.
Demonstrate supported topologies instead of inferring support from labels.

## RI-002 — Specify durable effects, approvals, and recovery

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch; informs RI-001.

- Define stable business operation IDs, argument binding, provider idempotency,
  conditional writes, reconciliation, and explicit unknown outcomes.
- Address the remote-commit/local-record crash window, late workers, cancellation
  fencing, retry multiplication, and Continue-As-New identity.
- Implement authenticated approval handling, canonical arguments, single-use
  consumption, expiry, revocation, separation of duties where required, and
  audit-outage behavior.
- Provide a Worker Versioning and continuation migration recipe, including
  old-worker retirement criteria.

**Completion criteria:** Crash-point and race tests cover remote commit versus
timeout, approval versus cancellation, changed arguments, conflicting approvers,
expired/replayed approvals, and worker migration. Document which steps may repeat
and how effects and usage reconcile.

## RI-003 — Enforce budgets through settlement

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch.

- Distinguish usage counters from strict reservation/admission controls.
- Define atomic reserve/settle operations, reservation identities, idempotent
  charging, conservative prices, rounding, retries, and unknown billed usage.
- Retain unresolved liabilities after timeouts; match ledger retention to
  durable lifetimes and reserve budget for reconciliation/finalization.
- Separate spend limits from rate/capacity limits, fairness, queue age, and
  saturation. Permit legitimate zero-capability budgets.

**Completion criteria:** Concurrency and worker-loss tests prove stated bounds
at root, tenant, and deployment levels. Timed-out work cannot prematurely free
money still liable to be billed. Relate numeric validation to F02.

## RI-004 — Strengthen evaluation meaning and tool usability

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch, alongside F09.

- Report denominators, representative strata, uncertainty, held-out cases,
  contamination checks, judge calibration, and baseline approval.
- Distinguish first-attempt success, success after retries, and repeated-run
  consistency; retain case-level failures and correlated-failure analysis.
- Provide a pinned Pydantic Evals adapter and explicit aggregation rules.
- Compare systems at matched budget and matched quality, including all attempt
  costs, latency, denied actions, and legitimate isolation benefits.
- Evaluate tool names, argument ambiguity, pagination, error repair, response
  usefulness, and unnecessary calls alongside security contracts.

**Completion criteria:** Example release reports preserve every hard-gate failure
and expose sample sizes, coverage, uncertainty assumptions, and judge error.
Separate deterministic control checks from stochastic attack-resistance claims.

## RI-005 — Map framework, protocol, and data controls

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch for the chosen
reference capabilities; later extensions for additional protocols.

- Add a capability-to-control matrix for Subagents, Dynamic Workflow, Skills,
  MCP, and any adopted A2A integration.
- Implement dependency projection and typed delegation adapters; distinguish
  history isolation from authority attenuation.
- Document unsupported nesting and duration semantics for model-authored
  choreography; enforce additional bounds explicitly.
- Cover MCP audience validation, token passthrough prohibition, egress/SSRF,
  session identity, tool-description drift, and malicious results.
- Map A2A task identity, cancellation, artifacts, callbacks, and authorization
  requirements to local contracts when that protocol is adopted.
- Add retrieval ACLs, freshness, deletion propagation, provenance, poisoning
  recovery, and authorization at artifact resolution. Include output/egress
  disclosure boundaries and compromised-member containment.

**Completion criteria:** Each adopted capability has a threat-to-control-to-test
mapping. Tests exercise authority expansion, revocation races, untrusted data,
and control-plane isolation; unsupported guarantees are explicitly identified.

## RI-006 — Make observability and audit guarantees executable

**Status:** Open. **Owner:** Unassigned. **Sequence:** Second batch.

- Supply collector/instrumentation configuration and inspect exported data in
  privacy/redaction tests. Keep content capture off by default.
- Bound metric cardinality; do not treat hashing as anonymization or cardinality
  reduction. Define trace links across long waits and mode-specific attributes.
- Map workflow, scaffold, and telemetry outcomes to a common outcome contract.
- Define reconciliation between graph events, ledgers, workflow state, and audit
  evidence; specify exporter/audit failures that block effects and their recovery.
- Refresh the OpenTelemetry GenAI reference and pin convention/instrumentation
  versions with migration tests.

**Completion criteria:** A runnable example exports the documented outcomes and
causal relationships without prohibited data, and preserves critical evidence
during exporter outage and long-running recovery.

## RI-007 — Prevent standards drift in CI

**Status:** Open. **Owner:** Unassigned. **Sequence:** Third batch.

- Add CI workflows and a realistic OS/Python matrix with the documented uv path.
- Include format checks, Markdown lint, internal links, schemas, snippets, and
  generated fixtures in `just check`.
- Add application Nix `checks` outputs if `nix flake check` is advertised as
  application validation.
- Install/test built wheels outside the checkout and pin/build-test the build
  backend.
- Assign stable requirement IDs and map each to schemas, validators, runtime
  checks, and evidence; record source versions for skills and generated snippets.
- Check external references periodically, with human review of semantic changes.

**Completion criteria:** A contract change cannot leave examples, skills,
templates, generated artifacts, or packaged resources silently inconsistent.
CI executes the published contributor workflow.

## RI-008 — Improve adoption and skill distribution

**Status:** Open. **Owner:** Unassigned. **Sequence:** Fourth batch.

- Add a reader map for architecture choice, first agent/system, rollout, and
  exceptions; clearly identify advanced extensions and support levels.
- Add contribution guidance, release notes, review ownership, supported versions,
  and a security-reporting policy. Obtain a maintainer decision on licensing.
- Provide optional versioned skill install/sync tooling with a manifest, drift
  detection, uninstall instructions, and standalone client compatibility tests.
- Evaluate trigger overlap using positive, negative, and ambiguous fixtures
  before narrowing descriptions or consolidating skills.

**Completion criteria:** A contributor can choose a supported path, install a
known skill bundle, resolve all resources, identify ownership, and understand
compatibility and redistribution terms without guessing. Coordinate with F10.

## RI-009 — Harden loaders, identities, and scaffolding

**Status:** Open. **Owner:** Unassigned. **Sequence:** Fourth batch; bring forward
specific defects when needed by F01–F10.

- Reject duplicate YAML keys; define path/symlink trust boundaries and safe
  resolution behavior.
- Centralize semantic-version parsing and make diagnostic codes unique,
  including the current unrelated uses of `AGENT035` and `AGENT036`.
- Define collision rules for agent/system identities, workflow modules, eval
  report paths, artifact stores, and multiple roles held by one agent.
- Validate Python identifiers and serialize user inputs safely in scaffolds.
- Restrict advertised scaffold support to implemented profiles or generate
  topology-specific contracts and fixtures.

**Completion criteria:** Malformed names/paths/duplicate keys yield targeted
diagnostics; concurrent or same-name subjects cannot overwrite unrelated evidence;
generated artifacts parse and match their declared support level.

## Sources and closure

These items cover the review's
[technical additions](../docs/reviews/initial-review/README.md#technical-additions-with-the-highest-payoff),
[chapter opportunities](../docs/reviews/initial-review/README.md#chapter-by-chapter-opportunities),
and [four-batch roadmap](../docs/reviews/initial-review/README.md#repository-and-tooling-roadmap).
Use the [research notes](../docs/reviews/initial-review/research.md) for primary
sources and verification limits. Close items with an owner, evidence, decision
date, and implementation links; split larger items into smaller tasks as work
is scheduled.
