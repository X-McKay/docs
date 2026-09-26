# External research supporting the initial review

Research checked on 2026-09-26 UTC (2026-09-25 in America/New_York).
These are primary sources, not evidence that this repository implements their
features. Documentation URLs are mutable; a tested dependency matrix is still
needed. Recommendations and extrapolations are identified in the [review](README.md).

## Frameworks and durable execution

| Source | Verified observation | Implication for this repository |
| --- | --- | --- |
| [PydanticAI Temporal integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/temporal/) | The supported capability path places the agent loop in the workflow and routes model/tool/MCP I/O to activities. Running the agent outside a workflow does not acquire that durability merely by attaching the capability. | Resolve the conflict between the agent chapter and activity-wrapped runs in skills/scaffolds; test recovery granularity explicitly. |
| [Temporal activity execution](https://docs.temporal.io/activity-execution) | Activity timeouts can lead to retries, and cancellation is cooperative. | A whole-agent activity needs a separate restart and side-effect design; a timeout is not proof that a remote effect stopped. |
| [Temporal Python error handling](https://docs.temporal.io/develop/python/best-practices/error-handling) | Retry policies, non-retryable failures, timeouts, heartbeat, and cancellation need SDK-specific handling. | Turn the failure taxonomy into executable examples and crash-point tests. |
| [Temporal Python message passing](https://docs.temporal.io/develop/python/workflows/message-passing) | Signals and Updates have different interaction semantics; handlers can involve concurrent workflow execution. | Demonstrate approval/expiry/cancellation ordering and idempotent update handling rather than leaving approval as pseudocode. |
| [Temporal Worker Versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning) | Current guidance distinguishes Pinned and Auto-Upgrade workflows and discusses upgrading at Continue-As-New boundaries. | Document a chosen deployment strategy, worker retirement conditions, and continuation compatibility. |
| [PydanticAI Agent Specs](https://pydantic.dev/docs/ai/core-concepts/agent-spec/) | `Agent.from_spec` applies the declarative configuration. `output_schema` yields a plain dictionary without validating its schema properties/required fields; `output_type` takes precedence. | Keep typed outputs. Make the scaffold consume the spec instead of manually forwarding only a subset of fields. |
| [PydanticAI version policy](https://pydantic.dev/docs/ai/project/version-policy/) | The page identifies stable V2 and allows some telemetry/event evolution within minor releases. | Separate core, Harness, Evals, SDK, and instrumentation compatibility; avoid treating all APIs as one stability category. |
| [PydanticAI Subagents](https://pydantic.dev/docs/ai/harness/subagents/) | Subagents have separate message histories, but dependencies are forwarded; usage is shared by default and output is returned as text. | History isolation does not establish authority attenuation or a typed delegation boundary. An adapter must enforce both. |
| [PydanticAI Dynamic Workflow](https://pydantic.dev/docs/ai/harness/dynamic-workflow/) | Uses sandboxed model-authored choreography. Nested workflows are disallowed; the sandbox duration limit counts sandbox execution, excluding waits on subagents. | It is not a direct implementation of the playbook's recursive durable system. Add a feature-to-requirement compatibility table. |
| [PydanticAI Spend Limits](https://pydantic.dev/docs/ai/harness/spend/) | Counters are checked before requests and charged afterward. Concurrent calls can overshoot, including with Redis. Retention can reset a resumed conversation's counter after expiry. | Shared accounting is insufficient for strict escrow. Specify reservation semantics, unknown usage, and retention matching durable lifetimes. |

## Evaluation and architectural evidence

| Source | Verified observation | Implication |
| --- | --- | --- |
| [Pydantic Evals multi-run guide](https://pydantic.dev/docs/ai/evals/how-to/multi-run/) | Supports repeated cases and grouped results; aggregate reporting uses group-level summaries. | Provide a real adapter preserving individual failures, denominators, coverage, and case identity rather than only averages. |
| [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Distinguishes finding a successful attempt (`pass@k`) from consistent success across attempts (`pass^k`), and discusses grader choice and environment quality. | Define what each release metric estimates; calibrate judges and separate harness failures from product failures. |
| [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents?slug=helpful-honest-harmless-ai) | Recommends simple, composable patterns and distinguishes predefined workflows from model-directed agents. | Preserve the simpler-baseline requirement, while treating complexity choices as hypotheses to evaluate. |
| [Anthropic: Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Reports a 90.2% improvement on its internal research evaluation and roughly 15 times chat token usage for multi-agent systems. The denominators and tasks differ. | This supports measuring benefits and total cost, not a universal speedup or a 15-times-single-agent claim. Use matched-budget and matched-quality comparisons. |
| [Anthropic: Writing effective tools](https://www.anthropic.com/engineering/writing-tools-for-agents) | Emphasizes task-oriented tool design, concise useful responses, and evaluation-driven iteration. | Add tool usability evals alongside security contracts: names, argument ambiguity, pagination, error repair, and unnecessary calls. |

## Skills, protocols, and observability

| Source | Verified observation | Implication |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Names are limited to 64 characters; metadata maps strings to strings; supporting resources use progressive disclosure. | Fix the missing name-length check and distinguish portable format validation from this organization's stronger governance rules. |
| [PydanticAI Skills](https://pydantic.dev/docs/ai/harness/skills/) | Loads skill instructions but does not enumerate/read/execute bundled resources or resolve client placeholders. Several behavioral frontmatter fields are accepted without implementing their behavior. | The repository correctly warns about this. Add a scoped resource resolver and test standalone skill portability. |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | Current Codex local discovery documentation lists repository and user `.agents/skills` directories and supports symlinks. | Refresh `skills/README.md`, which recommends `.codex/skills`; test supported clients rather than claiming older locations universally fail. |
| [OpenAI: Rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Recommends concise, specific activation descriptions and revisiting accumulated instructions. | Evaluate overlap among design, risk, and readiness skills; shorten only where trigger evidence supports it. |
| [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices) | Covers confused deputy, audience validation, forbidden token passthrough, and other transport/security hazards. | Add an executable MCP security profile; server allowlisting alone does not cover protocol threats. |
| [A2A specification](https://a2a-protocol.org/latest/specification/) | Application policy defines authorization; an authorization-required task state does not itself grant operation authority. | Keep discovery separate from admission. If A2A is added, map task identity, cancellation, authorization, artifacts, and state explicitly. |
| [OpenTelemetry GenAI relocation notice](https://opentelemetry.io/docs/specs/semconv/gen-ai/) and [maintained repository](https://github.com/open-telemetry/semantic-conventions-genai) | The referenced documentation page says the conventions moved and it is no longer maintained there. | Update the reference and pin emitted convention/instrumentation versions with migration tests. |

## Governance and tooling

| Source | Verified observation | Implication |
| --- | --- | --- |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) and [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | Risk management involves governance, context mapping, measurement, and management. | Keep scenario/evidence traceability; label the repository's matrix, tiers, and intervals as organizational choices. |
| [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) | Extends AI risk management to generative-AI-specific risks, including confabulation. | Supplement authorization testing with domain harms and evidence quality; a valid tool call can still cause a harmful outcome. |
| [European Commission AI Act overview](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) | Describes a regulatory framework with differentiated obligations. | Retain a separately maintained applicability screen. This review makes no deployment-specific legal classification or compliance claim. |
| [OWASP agentic threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | Provides an agent-specific threat resource. | Use a threat-to-control-to-test crosswalk rather than merely listing OWASP as a reference. |
| [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | Locked execution checks lockfile currency; environments and dependency synchronization are explicit concepts. | Keep the locked workflow and add CI execution, built-wheel tests, and separately pinned runnable examples. |

## Research boundaries

No paid ISO standard was obtained, and no claim of ISO conformity is made.
Provider-specific pricing, legal obligations for an actual deployment, production
telemetry, runtime authorization implementations, and hosted infrastructure were
not assessed. No live model calls were needed for this review. Framework behavior
was checked in current documentation; it was not integration-tested against a
PydanticAI/Temporal pair because the repository does not pin or implement that
runtime. The review proposes that integration work explicitly.
