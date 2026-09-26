# 10. Security and governance

Multi-agent systems combine the trust boundaries, privileges, data, suppliers,
and failure modes of every member with new risks created by their interactions.
No agent is trusted merely because it belongs to the same system or was selected
by another agent.

## Governance inheritance

Every member retains its Agent Playbook governance tier, execution class, risk
assessment, owners, controls, and approval requirements. The system adds a
separate composition assessment and governance decision.

The system governance tier is the highest of:

1. The maximum inherent system-level scenario tier
2. The tier of every reachable member in its assigned use
3. Applicable legal, regulatory, contractual, or internal-policy floors
4. Capability floors created by the combined system

Composition controls may make launch acceptable, but they do not silently lower
the assurance required by the underlying use or member capability.

## Ownership

Every production system names:

- Accountable product and business owners
- System engineering and operational owners
- Security, privacy, legal, compliance, and domain reviewers as applicable
- Owners for every member, role, edge, registry, policy, and state store
- An incident commander and risk-acceptance authority

Member owners remain accountable for their agent contracts. System owners are
accountable for admission, integration behavior, end-to-end outcomes, and
composition risk. Responsibility MUST NOT disappear between those layers.

## Trust model

Treat these as separate trust boundaries:

- User and external input
- Deterministic orchestrator and policy control plane
- Each member agent and model provider
- Every interaction and transport
- Tool, MCP, retrieval, and external-service boundaries
- Registry, marketplace, package, and deployment supply chain
- Workflow, queue, event bus, blackboard, memory, and artifact stores
- Human approval and operational interfaces
- Telemetry, evaluation, and audit systems

Crossing a boundary requires authenticated identity, explicit authorization,
typed validation, data policy, integrity protection where needed, and correlated
evidence.

## Threat model

At minimum, assess:

- Direct and indirect prompt injection across agent boundaries
- Identity, instruction, evidence, approval, and authority laundering
- Confused-deputy use of a more privileged member
- Unauthorized member, role, edge, tenant, or data access
- Excessive agency through recursive or dynamically created work
- Shared-memory, blackboard, registry, bid, or artifact poisoning
- False consensus, collusion, reviewer capture, and correlated failure
- Malicious or compromised member substitution
- Schema confusion, result forgery, replay, and duplicate delivery
- Race conditions, stale policy, inconsistent graph, and time-of-check/use gaps
- Data aggregation that creates a more sensitive derived dataset
- Denial-of-wallet, queue starvation, event storms, and resource exhaustion
- Hidden or duplicated side effects across concurrent branches
- Kill-switch, audit, telemetry, or evidence-store failure
- Supply-chain compromise of agents, models, skills, tools, policies, or schemas

Threats link to concrete scenarios, preventive, detective, and recovery
controls, tests, adversarial evals, indicators, alerts, and runbooks.

## Identity and authorization

Authenticated actor, tenant, environment, and purpose originate outside model
control. They propagate through typed trusted context, not prompts or
agent-generated messages.

Every interaction re-evaluates authorization using the authority-attenuation
rule. A caller can delegate only a subset of its current delegable scope, and a
callee can exercise only the intersection with its own role and Agent Spec.

Members MUST NOT:

- Assert or change actor or tenant identity
- Grant roles, scopes, membership, or approval
- Forward bearer credentials by default
- Treat another agent's assertion as authorization evidence
- Use a broader service identity when an attenuated identity is available
- Persist delegated authority beyond its task and expiry

Authorization is enforced at the member boundary and again at every tool or
external resource.

## Inter-agent content

All agent-generated content is untrusted. Summarization, voting, review, or
agreement does not make content trusted.

Receivers distinguish:

- Data from instructions
- Claims from verified evidence
- Proposed actions from completed effects
- Agent identity labels from authenticated principals
- Recommendations from policy decisions
- Review results from human approval

Use typed fields and evidence references. Sanitize or isolate untrusted active
content, but do not rely on prompt wording alone to prevent injection.

## Dynamic admission

Dynamic systems use an authenticated registry and deterministic admission
policy. Before work begins, validate:

- Member identity, owner, package or endpoint, and integrity
- Agent and manifest version
- Contract, schema, protocol, and runtime compatibility
- Execution class, governance tier, risk status, and evidence freshness
- Skills, tools, credentials, network, and data-access ceilings
- Jurisdiction, residency, provider, and tenant constraints
- Current health, quarantine, revocation, and incident status
- Cost, latency, and capacity claims against trusted measurements

Model-generated descriptions, bids, self-attestations, and discovery metadata
are inputs to selection, not admission evidence.

The run manifest records the decision and evidence digest. Admission expires;
long-lived systems revalidate members at policy-defined boundaries without
changing in-flight behavior nondeterministically.

## Registries, marketplaces, and supply chain

Registries and marketplaces are privileged infrastructure. They require:

- Authenticated publishers and controlled write access
- Immutable versions and integrity metadata
- Provenance, ownership, review, and revocation status
- Compatibility and policy metadata
- Audit records for publication and change
- Availability, rollback, and compromise runbooks

Production systems SHOULD use allowlisted publishers, repositories, packages,
providers, and manifests. Pin dependencies and scan packages, images, skills,
tools, policies, schemas, and generated artifacts.

A compromised registry MUST NOT automatically alter active workflow behavior.
Quarantine and revocation policy defines whether to stop, isolate, substitute,
or finish already admitted work.

## Shared state and memory

Shared memory, blackboards, event stores, and artifact stores declare:

- Record schemas and provenance
- Authorized readers and writers
- Tenant and purpose binding
- Consistency and conflict semantics
- Integrity, version, and freshness checks
- Moderation or validation before promotion to accepted state
- Retention, deletion, residency, and backup
- Poisoning detection, quarantine, and recovery

Separate proposed, observed, verified, accepted, rejected, and superseded facts.
Agents MUST NOT overwrite provenance or promote their own claims to verified
state without the declared validation path.

Derived collections can be more sensitive than their inputs. Classification and
access policy consider aggregation, inference, linkage, and re-identification.

## Protocol and transport security

Interaction transports provide appropriate confidentiality, integrity, peer
authentication, replay protection, message size limits, timeouts, and
denial-of-service controls.

Messages include stable system, graph, delegation, schema, actor, tenant,
deadline, and policy context. Receivers reject stale, duplicate, malformed,
wrong-tenant, wrong-graph, or unauthorized messages before model execution.

Async and event-driven systems define delivery and settlement semantics. A
transport acknowledgement is not evidence that business work or an external
effect completed.

## Isolation

Use process, container, sandbox, account, network, task-queue, namespace, and
data-store isolation proportionate to risk. Separate agents with different
owners, tenants, credentials, untrusted code, or consequential capabilities.

A coordinator SHOULD NOT share its broad environment, filesystem, credentials,
or network access with specialists. Code-executing and externally supplied
members require strong sandboxing, resource limits, restricted egress, and
artifact inspection.

The control plane remains isolated from member work. Agents cannot edit their
System Spec, policies, limits, registry status, telemetry requirements, or kill
switches.

## Approval and separation of duties

Consequential action requires the Agent Playbook approval contract and records
the system and causal context. Approval interfaces show the final action,
arguments, actor, tenant, relevant evidence, material disagreement, system and
member identities, policy version, expiry, and expected side effects.

Agent consensus, a reviewer role, quorum, reputation, or marketplace selection
is not approval. An agent MUST NOT approve its own output, accept its own risk,
or suppress information required by the approver.

High-risk systems SHOULD separate system development, registry publication,
policy approval, production promotion, and residual-risk acceptance roles.

## Change classes

Treat these as behavioral or security changes requiring focused review:

- Member addition, removal, upgrade, restriction, or substitution
- Topology, routing, aggregation, recursion, or dynamic-admission changes
- Interaction schema, authority, data-flow, retry, or timeout changes
- New shared state, registry, transport, model, tool, skill, or data source
- Increased fan-out, depth, autonomy, duration, population, or transaction value
- Approval, termination, quarantine, kill-switch, or fallback changes
- Telemetry, audit, retention, or redaction changes

Material changes require a system version change, regenerated manifest,
appropriate member and system evals, replay review, risk reassessment, and
rollout and rollback plans.

## Deployment

Production deployments SHOULD use:

- Immutable images and read-only application filesystems
- Pinned manifests, policies, schemas, models, and dependencies
- Separate identities and least-privilege credentials by role
- Restricted network egress and approved service endpoints
- Encrypted transport and managed secrets
- Signed or otherwise integrity-protected release artifacts where appropriate
- Staged rollout by tenant, task class, graph profile, or traffic percentage
- Fast rollback to a known composition manifest

Dynamic admission expands runtime choice but does not replace controlled system
deployment. The admission envelope itself is versioned and released.

## Kill switches and quarantine

Provide controls to:

- Stop new system runs
- Stop new delegation or dynamic admission
- Disable one member, role, edge, model, tool, registry, or topology profile
- Cancel or pause active workflows
- Block consequential actions while preserving read-only investigation
- Revoke credentials and artifact access
- Enter a tested deterministic or human-operated fallback

Kill switches operate outside model control, propagate within a stated SLO, are
tested regularly, and produce audit evidence.

Quarantine prevents new work and defines treatment of active work, cached
results, shared-state contributions, approvals, and artifacts from the affected
member. Removing a member from discovery is not sufficient containment.

## Incident response

Runbooks cover:

- Unauthorized member, edge, scope, tenant, or data flow
- Prompt-injection propagation or shared-state poisoning
- Registry, member, provider, or supply-chain compromise
- False consensus or reviewer failure
- Runaway recursion, events, retries, queues, or spend
- Duplicate or unapproved side effects
- Stuck workflows, inconsistent graph, or failed cancellation
- Audit, telemetry, approval, or artifact-store failure

Preserve workflow history, run manifests, graph versions, interaction ledger,
audit records, policy decisions, evidence hashes, model and member versions, and
affected artifacts subject to privacy and legal requirements.

Incidents and near misses create regression cases and may trigger member
quarantine, system rollback, risk reassessment, control testing, and
affected-party notification.

## Exceptions and review

Exceptions name scope, rationale, compensating controls, evidence, accountable
owner, approver, start, expiry, monitoring, and rollback trigger. They MUST NOT
be granted by an agent or hidden in prompts, registry metadata, or routing code.

Review the system at least as frequently as required by its governance tier and
after material architecture, membership, capability, data, jurisdiction,
incident, or control-effectiveness changes.

## Decommissioning

Decommissioning includes:

- Preventing new runs, admission, and delegation
- Completing, cancelling, migrating, or compensating active workflows
- Revoking member, registry, model, tool, and artifact credentials
- Removing queue subscriptions, events, schedules, callbacks, and endpoints
- Retiring manifests, policies, approvals, caches, shared state, and artifacts
- Applying retention and deletion obligations
- Preserving required audit and incident evidence
- Updating discovery, ownership, runbooks, and dependent systems
