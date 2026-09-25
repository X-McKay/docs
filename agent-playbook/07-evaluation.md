# 7. Evaluation standard

Evaluation is part of the agent contract. A production agent is incomplete until its expected behavior, prohibited behavior, operational limits, and failure handling are represented in executable tests and evals.

## Evaluation layers

| Layer              | Purpose                                         | Model/API usage    |
| ------------------ | ----------------------------------------------- | ------------------ |
| Unit tests         | Deterministic code and policy                   | None               |
| Component tests    | Agent assembly with controlled models and tools | Mocked             |
| Offline evals      | Behavior on curated datasets                    | Real model         |
| Temporal scenarios | Failure recovery and side-effect safety         | Mocked and real    |
| Online evals       | Production drift and unknown failures           | Sampled production |

## Dataset structure

```text
evals/
├── datasets/
│   ├── smoke/
│   ├── regression/
│   ├── capability/
│   ├── safety/
│   ├── adversarial/
│   └── durability/
├── evaluators/
│   ├── deterministic.py
│   ├── quality.py
│   ├── trajectory.py
│   ├── safety.py
│   ├── operational.py
│   └── temporal.py
├── experiments/
├── fixtures/
└── baselines/
```

Every confirmed production defect MUST become a sanitized regression case.

## Evaluator hierarchy

Prefer, in order:

1. Deterministic assertions
2. Domain-specific programmatic scoring
3. Trajectory and span evaluation
4. LLM-as-a-judge
5. Human review

Pydantic Evals supports output assertions, duration limits, tool correctness, trajectory matching, argument correctness, model/tool-call limits, span-based evaluation, and online evaluation.

## Hard gates

The following are binary release gates:

- Output validates against its declared type.
- No unauthorized or cross-tenant tool call occurs.
- No consequential action executes without valid approval.
- Approved arguments are not materially changed.
- Request, tool, token, time, and cost budgets are respected.
- Secrets and prohibited data are not returned.
- Required evidence is present.
- Temporal replay passes.
- Activity retry creates no duplicate side effect.
- Critical safety cases have zero known failures.

A weighted average MUST NOT hide failure of a hard gate.

## Risk-based evaluation planning

Every material risk scenario has a stable ID used as an eval tag. The scenario
links to deterministic invariants, behavioral cases, workflow failure cases,
production indicators, and recovery evidence appropriate to its dimensions and
governance tier. High- and critical-risk scenarios require repeated runs and
failure-distribution reporting when model behavior is involved.

An eval report identifies covered and uncovered scenario IDs. Missing required
coverage, failed hard gates, or absent control evidence blocks release. Passing
average quality cannot compensate for an uncovered material risk.

## Quality metrics

Select metrics appropriate to the agent:

- Task success and factual accuracy
- Groundedness and citation correctness
- Completeness and relevance
- Clarification and escalation quality
- Policy adherence
- Calibrated uncertainty
- Tone and communication quality

Every metric needs a definition, evaluator, threshold, owner, and regression response.

## Trajectory evaluation

Evaluate the path as well as the answer:

- Correct tool and skill selection
- Correct tool arguments and authorization context
- Prohibited-tool avoidance
- Call ordering where safety requires it
- Approval before consequential action
- Redundant calls and loop behavior
- Appropriate stopping and escalation

Prefer invariants over one exact sequence because several trajectories may be valid.

## Skill evals

Each skill requires cases for correct activation, correct non-activation, ambiguity, procedure adherence, interaction with other skills, tool use, stopping, safety, and context cost.

## LLM judges

An LLM judge MUST use a versioned rubric, return structured scores and reasons, be calibrated against human-reviewed examples, record model and prompt versions, and receive only needed context.

An LLM judge MUST NOT be the sole evaluator for authorization, approval, isolation, schema validity, or other deterministic safety properties.

## Multi-run evaluation

Use repeated runs for changes to models, providers, instructions, skills, tool descriptions, temperature, reasoning, compaction, or retry behavior.

Report distributions:

```text
pass rate and worst-case score
p50/p95 latency and cost
tool-call and model-request distributions
failure-category distribution
```

## Release gates

Each agent declares absolute and relative thresholds:

```yaml
evaluation_policy:
  hard_gates:
    critical_safety_pass_rate: 1.0
    schema_validity_rate: 1.0
    unauthorized_tool_calls: 0
    unapproved_consequential_actions: 0
  quality:
    task_success_rate_min: 0.90
    regression_allowed: 0.02
  operational:
    p95_latency_seconds_max: 25
    average_cost_usd_max: 0.20
    p95_model_requests_max: 5
```

Values are use-case specific. A release fails when any hard gate fails, an absolute threshold is missed, regression exceeds tolerance, or results lack reproducible provenance.

## CI strategy

- Pull request: unit, component, smoke, and focused regression suites.
- Main branch: broad offline and Temporal tests.
- Pre-release: capability, safety, adversarial, and multi-run suites.
- Scheduled: provider comparisons and drift detection.
- Production: privacy-filtered online sampling.

## Online evaluation

Online evaluation MUST be asynchronous, side-effect-free, privacy controlled, version attributed, and stratified by relevant agent and use-case dimensions. Confirmed failures feed the regression dataset.

## Provenance

Every eval report records agent and manifest version, Git commit, datasets, evaluators, model settings, judge rubric, skills, toolsets, worker build, run count, timestamp, case-level results, latency, and cost.
