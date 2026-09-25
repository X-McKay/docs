from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agentctl.files import DataFileError, dump_json_atomic, load_data
from agentctl.ui import command as show_command
from agentctl.ui import error, status, success


def run_eval_command(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    module_name = args.agent.replace("-", "_")
    report = args.report or Path("artifacts") / "evals" / f"{args.agent}.json"
    report = report if report.is_absolute() else root / report
    command = list(args.eval_argv or [])
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        adapter = root / "evals" / module_name / "run.py"
        if not adapter.is_file():
            raise ValueError(
                f"no default eval adapter at {adapter}; pass --command after other options"
            )
        command = [sys.executable, str(adapter)]

    previous_mtime = report.stat().st_mtime_ns if report.exists() else None
    environment = os.environ.copy()
    environment["AGENTCTL_REPORT_PATH"] = str(report)
    environment["AGENTCTL_AGENT"] = args.agent
    started = datetime.now(UTC)
    show_command(command)
    result = subprocess.run(command, cwd=root, env=environment, check=False)
    if result.returncode != 0:
        error(f"Eval adapter failed with exit code {result.returncode}")
        return result.returncode
    if not report.is_file():
        raise ValueError(f"eval adapter did not create {report}")
    if previous_mtime is not None and report.stat().st_mtime_ns == previous_mtime:
        raise ValueError(f"eval adapter did not update {report}")

    with status("Validating report and recording provenance…"):
        try:
            payload = load_data(report)
        except DataFileError as exc:
            raise ValueError(str(exc)) from exc
        _validate_report(payload, report)
        if payload["agent"] != args.agent:
            raise ValueError(
                f"{report}: report agent {payload['agent']!r} does not match {args.agent!r}"
            )
        provenance = payload.setdefault("provenance", {})
        if not isinstance(provenance, dict):
            raise DataFileError(f"{report}: provenance must be a mapping")
        provenance.update(
            {
                "agentctl_started_at": started.isoformat(),
                "agentctl_completed_at": datetime.now(UTC).isoformat(),
                "eval_command": command,
                "git_commit": _git_commit(root),
            }
        )
        dump_json_atomic(report, payload)
    success(
        "Evaluation complete",
        (("Agent", args.agent), ("Report", str(report))),
    )
    return 0


def _validate_report(payload: dict[str, Any], path: Path) -> None:
    if payload.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    if not isinstance(payload.get("agent"), str) or not payload["agent"].strip():
        raise ValueError(f"{path}: agent is required")
    hard_gates = payload.get("hard_gates")
    if not isinstance(hard_gates, dict):
        raise DataFileError(f"{path}: hard_gates must be a mapping")
    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        raise DataFileError(f"{path}: metrics must be a mapping")
    for key, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise DataFileError(f"{path}: metrics.{key} must be numeric")


def _git_commit(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None
