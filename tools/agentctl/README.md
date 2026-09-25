# agentctl

`agentctl` is the executable companion to the Agent Playbook. It scaffolds the golden path, validates contracts and Agent Skills, runs version-pinned eval adapters, and applies fail-closed release gates.

## Install or run locally

From the documentation repository:

```bash
uv sync --locked
uv run --locked agentctl --help
```

Install it into an isolated environment when using it from another repository:

```bash
uv tool install ./tools/agentctl
agentctl --help
```

The repository-level [`scripts/agentctl`](../../scripts/agentctl) wrapper uses the locked workspace automatically.

For a fully pinned system-tool environment, enter the Nix development shell first:

```bash
nix develop
just bootstrap
just check
```

## Terminal experience

Interactive terminals receive styled help, semantic colors, responsive tables and panels, and unobtrusive spinners around longer phases. Redirected output automatically drops animation and ANSI styling. JSON modes remain machine-readable.

```bash
agentctl --help
agentctl --no-color --no-animations validate
agentctl --force-color skills validate skills
agentctl validate --format json
```

The standard `NO_COLOR`, `FORCE_COLOR`, `CI`, and `TERM=dumb` conventions are respected.

## Scaffold an agent

```bash
scripts/agentctl scaffold customer-support \
  --root /path/to/project \
  --package acme_agents \
  --owner customer-platform \
  --execution-class durable \
  --risk-tier medium
```

Durable and human-governed agents automatically receive workflow and activity modules. Human-governed agents also receive an approval policy. Medium-, high-, and critical-risk agents receive a threat-model template.

Scaffolding never overwrites an existing file unless `--force` is explicitly supplied.
The generated package is intentionally incomplete: replace the purpose and ownership placeholders, implement the agent and eval adapter, and establish an approved baseline before expecting validation and release checks to pass.

## Validate contracts

```bash
scripts/agentctl validate --root /path/to/project
scripts/agentctl validate --root /path/to/project --format json
```

Validation covers required Agent Spec metadata, semantic versions, execution and risk classes, budgets, Temporal structure, approval policy, threat-model presence, eval policy, capability existence, tool effect, retry safety, authorization declarations, timeouts, and output bounds.

## Validate Agent Skills

```bash
scripts/agentctl skills validate --root /path/to/project
scripts/agentctl skills validate skills/build-agent-evals
scripts/agentctl skills validate --run-skills-ref
```

The built-in validator checks frontmatter, naming, description and body constraints, line limits, internal references, duplicate names, and optional `agents/openai.yaml`. `--run-skills-ref` additionally calls the separately installed Agent Skills reference validator.

## Run evals

```bash
scripts/agentctl eval run customer-support --root /path/to/project
```

By default, this runs `evals/customer_support/run.py`. To wrap a version-pinned Pydantic Evals command:

```bash
scripts/agentctl eval run customer-support \
  --root /path/to/project \
  --report artifacts/evals/customer-support.json \
  --command uv run python -m evals.customer_support.run
```

The adapter receives:

- `AGENTCTL_AGENT`
- `AGENTCTL_REPORT_PATH`

It must write a normalized report:

```json
{
  "schema_version": 1,
  "agent": "customer-support",
  "hard_gates": {
    "critical_safety_pass_rate": 1.0,
    "schema_validity_rate": 1.0,
    "unauthorized_tool_calls": 0,
    "unapproved_consequential_actions": 0
  },
  "metrics": {
    "task_success_rate": 0.94,
    "p95_latency_seconds": 8.2,
    "average_cost_usd": 0.08
  }
}
```

`agentctl` validates the report and adds timestamps, the invoked command, and the Git commit. This adapter boundary lets each agent pin its Pydantic Evals and provider dependencies independently.

The eval adapter should add the remaining release provenance required by its policy, such as dataset and evaluator versions, exact model and settings, prompt, skill and toolset versions, manifest identifier, and run count.

The generated adapter deliberately reports a failing `placeholder_eval_removed` gate. It must be replaced with real datasets and evaluators before release.

## Apply release gates

```bash
scripts/agentctl release check \
  --report artifacts/evals/customer-support.json \
  --policy evals/customer_support/release-policy.yaml \
  --baseline evals/customer_support/baselines/main.json
```

Policies support:

- Exact hard-gate values
- Absolute numeric minimums and maximums
- Direction-aware regression limits against a baseline
- Required provenance fields

Missing gates or metrics fail closed. When a policy defines regressions, an approved baseline is required; omitting it also fails the release check.

## CI example

```yaml
- name: Validate agent contracts and skills
  run: |
    uv sync --locked
    uv run --locked agentctl --no-animations validate
    uv run --locked agentctl --no-animations skills validate

- name: Run smoke evals and release gates
  run: |
    uv run --locked agentctl --no-animations eval run customer-support
    uv run --locked agentctl --no-animations release check \
      --report artifacts/evals/customer-support.json \
      --policy evals/customer_support/release-policy.yaml \
      --baseline evals/customer_support/baselines/main.json
```

## Exit codes

- `0`: checks passed or scaffolding completed.
- `1`: conformance or release-gate failures.
- `2`: invalid invocation, unreadable input, or unsafe overwrite attempt.

## References

- [Agent Playbook](../../agent-playbook/README.md)
- [PydanticAI Agent Specs](https://pydantic.dev/docs/ai/core-concepts/agent-spec/)
- [Pydantic Evals quickstart](https://pydantic.dev/docs/ai/evals/getting-started/quick-start/)
- [PydanticAI Temporal integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/temporal/)
- [Agent Skills specification](https://agentskills.io/specification)
