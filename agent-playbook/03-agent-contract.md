# 3. Canonical agent contract

Every production agent is represented by a reviewable package containing a declarative specification, typed runtime interfaces, and a controlled assembly function.

## Agent Spec

```yaml
name: customer-support
description: Investigate customer questions and propose policy-compliant resolutions.

instructions:
  - Resolve the request using verified customer and policy information.
  - Distinguish verified facts from assumptions and proposed actions.
  - Never claim an external action succeeded unless its tool result confirms success.

model_settings:
  temperature: 0.1
  max_tokens: 2000

retries: 2
tool_timeout: 20
end_strategy: graceful
instrument: true

metadata:
  contract_version: 1
  owner: customer-platform
  version: 1.0.0
  execution_class: durable
  risk_tier: medium
  risk_assessment: docs/risk-assessments/customer-support.yaml
  data_classification: confidential
  model_policy: balanced-v1
  enabled_skills:
    - customer-policy
  enabled_toolsets:
    - customer-records
    - knowledge-search
  budgets:
    max_requests: 8
    max_input_tokens: 30000
    max_output_tokens: 5000
    max_tool_calls: 12
    max_cost_usd: 0.50
```

Organization-specific fields belong under `metadata` and MUST be validated by application code during startup.

## Model policy

Production agents SHOULD select a versioned logical model policy rather than hard-code a provider model:

```text
fast-v1       -> low-latency, low-cost model
balanced-v1   -> default production model
reasoning-v1  -> high-complexity model with stricter budget
```

The resolved provider, exact model, settings, and pricing version MUST be recorded in telemetry and eval results. A model pin is permitted when reproducibility, certification, or a provider-specific feature requires it.

## Typed dependencies

Dependencies carry trusted runtime context and reconstructable service interfaces.

```python
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SupportDependencies:
    request_id: UUID
    tenant_id: UUID
    actor_id: UUID
    authorization_scopes: frozenset[str]
    deadline: datetime
```

Dependencies SHOULD include authenticated identity, tenant context, authorization scopes, correlation identifiers, deadlines, and policy context.

They MUST NOT contain model-generated authorization, mutable global state, raw secrets, or objects that will be serialized unsafely into Temporal history. Pass serializable identifiers across workflow boundaries and reconstruct infrastructure clients within activities.

## Typed output

Production agents SHOULD use a Pydantic output type:

```python
from typing import Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source: str
    claim: str


class SupportResolution(BaseModel):
    status: Literal[
        "answered",
        "action_proposed",
        "needs_information",
        "escalated",
    ]
    summary: str
    evidence: list[Evidence]
    confidence: float = Field(ge=0, le=1)
    proposed_action: str | None = None
```

An Agent Spec `output_schema` guides model output but returns a plain dictionary rather than providing the same runtime validation as a typed `output_type`. Typed output is therefore the production default.

## Factory responsibilities

The factory:

1. Loads the Agent Spec.
2. Validates governance metadata.
3. Resolves the model policy.
4. Resolves and allowlists skills and toolsets.
5. Verifies tool effects against the execution class.
6. Attaches usage, spend, observability, and Temporal capabilities.
7. Supplies dependency and output types.
8. Produces the capability manifest.

Construction MUST fail when an owner, execution class, risk tier, risk
assessment, model policy, budget, skill, or toolset is missing or invalid. The
Agent Spec risk tier MUST match the assessment's governance tier. Durable agents
MUST fail construction if durability is absent; human-governed agents MUST fail
if approval policy is absent.

## Versioning

Keep these versions separate:

- `contract_version`: organizational metadata schema.
- Agent version: behavioral configuration and capability set.
- Worker/build version: executable and Temporal compatibility.

Behavior-changing edits to instructions, models, skills, tools, or outputs require an agent version change and relevant evals. Temporal-incompatible changes additionally require replay-safe deployment.
