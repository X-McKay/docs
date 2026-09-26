# Backlog

Proposed work and decisions awaiting maintainer prioritization. An open item is
not an approved policy change or an assigned implementation task.

## Implementation changes

The [concrete findings](implementation-changes.md) track all ten changes from
the initial review with the original priorities and completion criteria. All
are open and unassigned.

| ID | Priority | Change |
| --- | --- | --- |
| F01 | P1 | Strict release-policy, report, and baseline schemas |
| F02 | P1 | Finite numeric values and valid count/budget bounds |
| F03 | P1 | Integrated production readiness and release evidence |
| F04 | P1 | Consistent capability and regulatory governance floors |
| F05 | P1 | Resolved system policies, schemas, and graph contracts |
| F06 | P1 | Consistent, tested Temporal execution patterns |
| F07 | P2 | Complete Agent Spec configuration in generated factories |
| F08 | P2 | System risk schema parity and robust diagnostics |
| F09 | P2 | Release-bound evaluation identity and provenance |
| F10 | P2 | Canonical examples, portable skills, and current instructions |

## Runtime and repository improvements

The [broader improvement backlog](repository-improvements.md) preserves the
technical additions, chapter editing targets, and tooling roadmap:

| ID | Workstream |
| --- | --- |
| RI-001 | Pinned runnable reference stack |
| RI-002 | Durable effects, approvals, cancellation, and deployment recovery |
| RI-003 | Reservations, settlement, spend, and capacity controls |
| RI-004 | Evaluation evidence, statistics, baselines, and tool usability |
| RI-005 | Framework, protocol, retrieval, and authority controls |
| RI-006 | Observable outcomes, privacy, and durable audit evidence |
| RI-007 | CI, packaging, compatibility, and standards drift prevention |
| RI-008 | Contributor adoption, licensing decisions, and skill distribution |
| RI-009 | Loader, identity, and scaffold hardening |

Each workstream includes proposed sequencing and completion criteria. All are
open and unassigned. Begin with the concrete correctness findings, prove a
small reference stack, then expand CI and adoption support as described in the
[review roadmap](../docs/reviews/initial-review/README.md#repository-and-tooling-roadmap).

## Architecture and governance decisions

The [opinions worth revisiting](opinions-worth-revisiting.md) come from the
[initial repository review](../docs/reviews/initial-review/README.md#opinions-worth-revisiting).
Each item records the current opinion, a proposed direction, evidence needed,
and completion criteria. All eight items are open and unassigned.

| ID | Decision |
| --- | --- |
| [OP-001](opinions-worth-revisiting.md#op-001--durability-requirements-and-temporal) | Durability requirements and Temporal |
| [OP-002](opinions-worth-revisiting.md#op-002--durability-and-human-approval) | Durability and human approval |
| [OP-003](opinions-worth-revisiting.md#op-003--governance-for-internal-agent-roles) | Governance for internal agent roles |
| [OP-004](opinions-worth-revisiting.md#op-004--topology-support-and-scaffolding) | Topology support and scaffolding |
| [OP-005](opinions-worth-revisiting.md#op-005--deterministic-authority-and-factual-truth) | Deterministic authority and factual truth |
| [OP-006](opinions-worth-revisiting.md#op-006--human-review-in-evaluation) | Human review in evaluation |
| [OP-007](opinions-worth-revisiting.md#op-007--model-aliases-and-release-identity) | Model aliases and release identity |
| [OP-008](opinions-worth-revisiting.md#op-008--risk-matrix-and-governance-calibration) | Risk matrix and governance calibration |

When resolving an item, record the owner, decision date, rationale, evidence,
and implementation or follow-up links. Retaining the current policy is a valid
resolution when supported by evidence. Keep the original review as a historical
snapshot and track subsequent decisions here.
