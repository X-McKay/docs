# Agent Capability Standard

## Placement Decision

| Need | Primary mechanism |
| --- | --- |
| Behavioral boundary | Prompt or policy |
| Exact validation or calculation | Deterministic code |
| External read or action | Tool or toolset |
| Reusable procedure and examples | Agent Skill |

Skills teach the agent how to work. Tools let the agent act. Neither replaces authorization or deterministic policy.

## Tool Contract

Each tool must declare:

- stable name and one-sentence purpose;
- typed input and output schemas;
- dependency and credential source;
- authorization check and tenancy boundary;
- side-effect class;
- idempotency behavior and key source;
- timeout, retryable failures, and terminal failures;
- maximum response size and redaction rules;
- trace attributes and safe error mapping;
- owning team and explicit consuming agents.

Avoid ambiguous booleans and free-form dictionaries. Prefer domain types, enums, constrained values, and discriminated unions.

## Skill Contract

Follow the Agent Skills specification:

- Directory name equals frontmatter `name`.
- Name uses lowercase letters, digits, and hyphens; maximum 64 characters.
- Description states both capability and trigger; maximum 1024 characters.
- Keep `SKILL.md` below 500 lines and use imperative instructions.
- Put detailed material in directly linked `references/` files.
- Put deterministic helpers in `scripts/` and output resources in `assets/` only when useful.
- Include common requests and edge cases.
- Never include secrets or assume a capability that is not actually available.

For widest portability, keep required frontmatter to `name` and `description`. Record owner, semantic version, and risk tier in an approved governance manifest or portable `metadata` when all target clients support it. Put product-specific presentation metadata in its product-defined location, such as `agents/openai.yaml`.

## Allowlist Pattern

Maintain a registry of available capabilities and a separate manifest of permitted capabilities for each agent. Resolve the manifest at startup and fail closed on unknown names. Log the resolved version set.

## Required Tests

- Schema acceptance and rejection.
- Authorization and cross-tenant denial.
- Timeout and safe error mapping.
- Idempotent replay where applicable.
- Non-idempotent retry prevention.
- Capability omitted from allowlist.
- Skill trigger and non-trigger examples.
- Prompt-injection content returned by a tool.
