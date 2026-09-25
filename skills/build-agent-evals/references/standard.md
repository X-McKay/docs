# Agent Evaluation Standard

## Evaluation Layers

| Layer | Purpose | Typical evidence |
| --- | --- | --- |
| Contract | Types and invariants | Schema checks, exact assertions |
| Capability | Tool and skill behavior | Tool arguments, denied calls, trajectory |
| Task | End-user outcome | Domain metrics and rubric scores |
| Workflow | Durable behavior | Retry, approval, timer, replay scenarios |
| System | Production objectives | Quality, latency, reliability, cost |

## Dataset Taxonomy

Every material behavior should have cases for happy paths, boundaries, ambiguous inputs, missing evidence, adversarial content, permission denial, dependency failure, historical regressions, and high-risk operations. Workflow agents also need duplicate delivery, retry, timeout, cancellation, signal race, and worker recovery cases.

Each case should include:

- stable ID and human-readable name;
- source and creation date;
- input and controlled dependencies;
- relevant risk and capability tags;
- expected structured fields or invariants;
- allowed variation;
- redaction and retention classification.

## Evaluator Selection

Use the least subjective evaluator that captures the claim. Deterministic evaluators should own schemas, exact values, forbidden actions, authorization, citations, and budget limits. Use model judges for relevance, tone, or completeness only with a documented rubric, representative calibration set, and periodic human review.

## Stochastic Measurement

Run critical cases multiple times. Report attempt count, pass rate, distribution, variance, and confidence bounds when useful. Keep sampling parameters fixed for comparisons. Store model, provider, prompt, tool, skill, policy, and dataset versions with results.

## Release Gates

Block release on any hard safety or authorization violation. For graded metrics, define baseline, minimum acceptable value, allowed regression, sample size, and owner. Compare quality and safety alongside p50/p95 latency, input/output tokens, tool calls, retries, and cost per successful task.

## Online Evaluation

Sample by risk and failure mode, not only uniformly. Redact before storage. Keep monitoring alerts separate from offline release gates until labels and evaluator reliability are understood. Promote reviewed failures into a versioned regression dataset.
