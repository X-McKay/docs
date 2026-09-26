# 4. Membership and role standard

Membership determines which independently governed agents may participate in a
system and what narrower responsibility each receives within that composition.
It is an authorization boundary, not service discovery.

## Admission requirements

Before admission, every member MUST have:

- A valid, versioned Agent Spec
- An accountable owner
- A compatible execution class and approved governance tier
- An unexpired agent risk assessment
- Typed inputs, dependencies, and outputs appropriate to its use
- Explicit skill and tool allowlists
- Required eval, observability, security, and production-readiness evidence
- A stable manifest or reproducible manifest construction process

The system MUST validate these requirements rather than infer conformance from
the presence of files.

## Static and dynamic membership

Production membership SHOULD be resolved before a run and recorded in the
composition manifest. Agents MUST NOT join solely because they are discoverable
through a registry, model context, MCP server, queue, network, or user-supplied
identifier.

Dynamic membership is appropriate when expertise, capacity, locality,
availability, or compatible substitution cannot be predicted economically at
deployment time. It trades reproducibility and a smaller trust surface for
adaptability, extensibility, and resilience.

Dynamic membership requires:

- An authenticated registry and deterministic admission policy
- Allowed publishers, packages, versions, owners, and manifests
- Signature or integrity verification where applicable
- Compatibility, risk, capability, and data-residency checks
- Conservative per-run member and capability limits
- A composition record identifying the exact admitted member
- Additional supply-chain, substitution, and containment evals

The system records a run manifest containing every dynamically admitted member,
version, manifest ID, assigned role, effective capability, policy decision, and
admission reason. Replaying or investigating the run MUST NOT depend on the
registry still returning the same result.

Admitting arbitrary model-generated code, prompts, endpoints, or agent names is
prohibited.

## Roles

A role defines one coherent system responsibility. Role names are stable,
lowercase, and hyphenated. Each role declares:

- Purpose and non-goals
- Permitted callers and callees
- Accepted interaction modes
- Input and output contracts
- Maximum data classification
- Maximum delegable authorization scopes
- Tool and skill restrictions
- Budget and concurrency limits
- Required evidence and completion criteria
- Failure and escalation behavior
- Owner

Roles constrain agents; they do not grant new capability. The same agent MAY
fill multiple roles only when the System Spec declares each assignment and evals
cover the resulting loss of independence.

## Common roles

The following names are descriptive, not privileged:

| Role | Responsibility | Prohibited assumption |
| --- | --- | --- |
| Coordinator | Propose bounded routing and synthesize results | Is not the deterministic orchestrator |
| Specialist | Perform one domain task | Does not inherit caller capabilities |
| Investigator | Gather and structure evidence | Does not decide authorization or truth alone |
| Producer | Create a candidate result | Does not self-approve |
| Reviewer | Evaluate against a rubric | Does not provide human approval or risk acceptance |
| Aggregator | Combine typed results | Does not treat agreement as correctness |
| Executor | Perform an approved action | Does not plan, approve, or expand the action |
| Monitor | Detect conditions and propose escalation | Does not take undeclared remediation action |

Use narrower domain-specific names when they communicate responsibility more
clearly.

## Capability intersection

At run time, effective member capability is:

```text
member Agent Spec allowlist
    intersected with system member restrictions
    intersected with role restrictions
    intersected with authenticated actor and tenant policy
    intersected with current workflow state and approval
```

An empty intersection is a valid denial. The runtime MUST NOT fall back to the
member's broader default capability set.

Credentials SHOULD be minted or selected for the effective scope and lifetime
of the interaction. Members MUST NOT receive the coordinator's credentials,
service identity, full user session, or unrelated tenant context by default.

## Independence claims

A system claiming independent review, voting, or defense in depth MUST document
the relevant sources of independence, including:

- Model and provider
- Instructions and context
- Data and evidence sources
- Tools and retrieval paths
- Implementation and owning team
- Failure modes and deployment infrastructure

Different agent names or personas do not establish independence. Shared models,
prompts, evidence, infrastructure, or owners can create correlated failure and
MUST be represented in risk and evaluation evidence.

## Substitution and fallback

A fallback member MUST be independently admitted and declared for the same role.
The substitution policy defines:

- Conditions that permit substitution
- Compatible schemas and semantic behavior
- Differences in capability, model, data residency, risk, latency, and cost
- Whether approval or user disclosure is required
- Evaluation evidence for the fallback path
- Telemetry and incident thresholds

The system MUST NOT silently substitute a member that changes the effective
execution class, governance tier, authority, data handling, or consequential
behavior.

## Lifecycle

Adding, removing, upgrading, restricting, or substituting a member is a system
behavior change. It requires:

- A system version change
- Composition-manifest regeneration
- Focused interaction and end-to-end evals
- Compatibility and replay review when workflows are active
- Risk reassessment for affected scenarios
- Rollout and rollback plans

In-flight durable workflows MUST remain pinned to a compatible composition or
migrate through a tested, explicit process.

## Quality gates

Member admission requires tests proving:

- Unknown or unpinned members are rejected.
- Role restrictions cannot expand base capabilities.
- Unauthorized callers and interaction modes are denied.
- Tenant, actor, and data boundaries survive delegation.
- Substitution follows the declared policy.
- Removed or quarantined members cannot receive new work.
- Manifest and version mismatches fail closed.
