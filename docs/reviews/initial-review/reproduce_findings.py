"""Non-destructive review probes; all fixtures live in a temporary directory.

Run with: uv run --locked python docs/reviews/initial-review/reproduce_findings.py
The output records observations, not passing conformance tests. Exit status zero
means the probes completed; consult each observation's diagnostic codes.
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import subprocess
import tempfile
from pathlib import Path

import yaml
from agentctl.cli import main


def write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def invoke(args: list[str]) -> dict:
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = main(["--no-color", "--no-animations", *args])
        try:
            payload = json.loads(output.getvalue())
        except json.JSONDecodeError:
            payload = {}
        return {
            "exit_code": code,
            "diagnostics": [item["code"] for item in payload.get("diagnostics", [])],
        }
    except Exception as exc:  # Capture malformed-input crashes as review evidence.
        return {"exception": type(exc).__name__, "message": str(exc)}


def run(root: Path) -> list[dict]:
    results = []

    def record(name: str, args: list[str], expected: str) -> None:
        results.append(
            {"probe": name, "expected_safe_behavior": expected, **invoke(args)}
        )

    report = root / "report.yaml"
    policy = root / "policy.yaml"
    base_report = {
        "schema_version": 1,
        "agent": "review-agent",
        "hard_gates": {"safe": True},
        "metrics": {"quality": 0.1},
    }
    release_args = [
        "release",
        "check",
        "--report",
        str(report),
        "--policy",
        str(policy),
        "--format",
        "json",
    ]
    write(report, base_report)
    write(policy, {})
    record("empty_release_policy", release_args, "Reject an empty release policy")
    write(
        policy,
        {
            "schema_version": 1,
            "hard_gates": {"safe": True},
            "quality": {"quality_min": 0.9},
        },
    )
    record(
        "unknown_policy_section",
        release_args,
        "Reject unsupported quality section rather than ignore it",
    )
    nan_report = copy.deepcopy(base_report)
    nan_report["metrics"]["quality"] = float("nan")
    write(report, nan_report)
    write(policy, {"schema_version": 1, "thresholds": {"quality": {"min": 0.9}}})
    record("nan_threshold_metric", release_args, "Reject non-finite metric")

    for name in ("planner-agent", "worker-agent"):
        scaffold = invoke(
            [
                "scaffold",
                name,
                "--root",
                str(root),
                "--owner",
                "review-team",
                "--execution-class",
                "durable",
                "--risk-tier",
                "medium",
            ]
        )
        assert scaffold["exit_code"] == 0, scaffold
        spec = root / "src/acme_agents/agents" / name.replace("-", "_") / "agent.yaml"
        value = yaml.safe_load(spec.read_text())
        value["description"] = "Perform a bounded review task."
        write(spec, value)

    risk_path = root / "docs/risk-assessments/planner-agent.yaml"
    original_risk = yaml.safe_load(risk_path.read_text())
    risk = copy.deepcopy(original_risk)
    risk["assessment"].update(
        status="approved",
        approved_by=["reviewer"],
        assessed_at="2020-01-01",
        review_by="2020-02-01",
    )
    risk["acceptance"]["expires_at"] = "2020-02-01"
    risk["classification"]["decision"] = "no_go"
    risk["open_questions"] = []
    write(risk_path, risk)
    record(
        "expired_no_go_agent_contract",
        ["validate", "--root", str(root), "--format", "json"],
        "Production readiness must reject expired/no_go assessments; structural mode must be labeled",
    )
    write(risk_path, original_risk)

    scaffold = invoke(
        [
            "system",
            "scaffold",
            "review-system",
            "--root",
            str(root),
            "--owner",
            "review-team",
            "--operational-owner",
            "review-ops",
            "--execution-class",
            "durable",
            "--risk-tier",
            "medium",
            "--member",
            "planner-agent:coordinator",
            "--member",
            "worker-agent:worker",
        ]
    )
    assert scaffold["exit_code"] == 0, scaffold
    system_path = root / "src/acme_agents/systems/review_system/system.yaml"
    system = yaml.safe_load(system_path.read_text())
    system["description"] = "Coordinate bounded review tasks."
    write(system_path, system)
    system_args = ["system", "validate", "--root", str(root), "--format", "json"]
    record(
        "placeholder_system_contract",
        system_args,
        "Distinguish structural validation from production readiness",
    )
    delegation = system_path.parent / "policies/delegation.yaml"
    original_delegation = delegation.read_text()
    write(delegation, {})
    record(
        "empty_delegation_policy",
        system_args,
        "Reject a policy with no declared interaction contracts",
    )
    delegation.write_text(original_delegation)
    changed = copy.deepcopy(system)
    changed["interactions"][0]["input_schema"] = "NonexistentSchema"
    write(system_path, changed)
    record(
        "unresolved_interaction_schema",
        system_args,
        "Resolve the declared schema or report that it was not checked",
    )
    write(system_path, system)

    system_risk_path = root / "docs/risk-assessments/systems/review-system.yaml"
    system_risk = yaml.safe_load(system_risk_path.read_text())
    changed_risk = copy.deepcopy(system_risk)
    changed_risk["regulatory_screen"]["governance_floors"] = [
        {
            "source": "internal_policy",
            "tier": "high",
            "rationale": "Required internal floor.",
        }
    ]
    write(system_risk_path, changed_risk)
    record(
        "ignored_system_governance_floor",
        system_args,
        "Reject medium governance below declared high floor",
    )
    changed_risk = copy.deepcopy(system_risk)
    changed_risk["scenarios"][0]["residual"] = []
    write(system_risk_path, changed_risk)
    record(
        "malformed_system_risk",
        system_args,
        "Return a structured diagnostic without an exception",
    )
    write(system_risk_path, system_risk)

    system_policy = root / "evals/systems/review_system/release-policy.yaml"
    write(
        report,
        {
            "schema_version": 1,
            "subject": {"kind": "system", "name": "review-system"},
            "hard_gates": {"placeholder_eval_removed": True},
            "metrics": {"task_success_rate": 0.95},
            "provenance": {"git_commit": "arbitrary-nonempty-text"},
        },
    )
    record(
        "minimal_system_release_evidence",
        [
            "release",
            "check",
            "--report",
            str(report),
            "--policy",
            str(system_policy),
            "--format",
            "json",
        ],
        "Production system release requires composition, member, safety, baseline, and risk evidence",
    )

    low_root = root / "low"
    scaffold = invoke(
        [
            "scaffold",
            "action-agent",
            "--root",
            str(low_root),
            "--owner",
            "review-team",
            "--execution-class",
            "human_governed",
            "--risk-tier",
            "low",
        ]
    )
    assert scaffold["exit_code"] == 0, scaffold
    spec_path = low_root / "src/acme_agents/agents/action_agent/agent.yaml"
    spec = yaml.safe_load(spec_path.read_text())
    spec["description"] = "Execute approved consequential actions."
    spec["metadata"]["enabled_toolsets"] = ["actions"]
    write(spec_path, spec)
    write(
        low_root / "src/acme_agents/tools/actions/tool.yaml",
        {
            "name": "action",
            "owner": "review-team",
            "effect": "write_consequential",
            "retry_safety": "idempotency_key_required",
            "authorization_scopes": ["action.write"],
            "timeout_seconds": 10,
            "data_classification": "internal",
            "max_output_bytes": 1024,
        },
    )
    record(
        "consequential_tool_low_governance",
        ["validate", "--root", str(low_root), "--format", "json"],
        "Reject consequential action below high governance floor",
    )

    long_name = "a" * 65
    skill = root / "skills" / long_name / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text(
        f"---\nname: {long_name}\ndescription: Use when reviewing a fixture.\n---\n\nReview the fixture.\n"
    )
    record(
        "skill_name_over_64_characters",
        [
            "skills",
            "validate",
            str(skill.parent),
            "--root",
            str(root),
            "--format",
            "json",
        ],
        "Reject names longer than the Agent Skills limit",
    )
    return results


if __name__ == "__main__":
    repository = Path(__file__).resolve().parents[3]
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repository, text=True
    ).strip()
    with tempfile.TemporaryDirectory(prefix="playbooks-review-") as directory:
        observations = run(Path(directory))
    print(
        json.dumps({"reviewed_commit": commit, "observations": observations}, indent=2)
    )
