from __future__ import annotations

import argparse
import sys
from pathlib import Path

from agentctl.evals import run_eval_command
from agentctl.release import check_release
from agentctl.scaffold import scaffold_agent
from agentctl.skills import validate_skills
from agentctl.validation import validate_project


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentctl",
        description="Build and verify agents against the Agent Playbook.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    commands = parser.add_subparsers(dest="command", required=True)

    scaffold = commands.add_parser(
        "scaffold", help="create a golden-path agent package"
    )
    scaffold.add_argument("name", help="lowercase hyphenated agent name")
    scaffold.add_argument("--root", type=Path, default=Path.cwd())
    scaffold.add_argument("--package", default="acme_agents")
    scaffold.add_argument(
        "--execution-class",
        choices=("ephemeral", "durable", "human_governed"),
        default="ephemeral",
    )
    scaffold.add_argument(
        "--risk-tier",
        choices=("low", "medium", "high", "critical"),
        default="low",
    )
    scaffold.add_argument("--owner", default="replace-me")
    scaffold.add_argument("--with-temporal", action="store_true")
    scaffold.set_defaults(with_evals=True)
    scaffold.add_argument("--force", action="store_true")

    validate = commands.add_parser("validate", help="validate agent contracts")
    validate.add_argument("--root", type=Path, default=Path.cwd())
    validate.add_argument("--format", choices=("text", "json"), default="text")

    skills = commands.add_parser("skills", help="work with Agent Skills packages")
    skills_commands = skills.add_subparsers(dest="skills_command", required=True)
    skills_validate = skills_commands.add_parser(
        "validate", help="validate Agent Skills packages"
    )
    skills_validate.add_argument("paths", nargs="*", type=Path)
    skills_validate.add_argument("--root", type=Path, default=Path.cwd())
    skills_validate.add_argument("--format", choices=("text", "json"), default="text")
    skills_validate.add_argument("--run-skills-ref", action="store_true")

    eval_parser = commands.add_parser("eval", help="run standardized evaluations")
    eval_commands = eval_parser.add_subparsers(dest="eval_command", required=True)
    eval_run = eval_commands.add_parser("run", help="run an eval adapter")
    eval_run.add_argument("agent")
    eval_run.add_argument("--root", type=Path, default=Path.cwd())
    eval_run.add_argument("--report", type=Path)
    eval_run.add_argument(
        "--command",
        dest="eval_argv",
        nargs=argparse.REMAINDER,
        help="adapter command; defaults to evals/<agent>/run.py",
    )

    release = commands.add_parser("release", help="evaluate release policy")
    release_commands = release.add_subparsers(dest="release_command", required=True)
    release_check = release_commands.add_parser("check", help="apply release gates")
    release_check.add_argument("--report", type=Path, required=True)
    release_check.add_argument("--policy", type=Path, required=True)
    release_check.add_argument("--baseline", type=Path)
    release_check.add_argument("--format", choices=("text", "json"), default="text")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "scaffold":
            return scaffold_agent(args)
        if args.command == "validate":
            return validate_project(args.root, output_format=args.format)
        if args.command == "skills" and args.skills_command == "validate":
            return validate_skills(
                root=args.root,
                paths=args.paths,
                output_format=args.format,
                run_reference_validator=args.run_skills_ref,
            )
        if args.command == "eval" and args.eval_command == "run":
            return run_eval_command(args)
        if args.command == "release" and args.release_command == "check":
            return check_release(
                report_path=args.report,
                policy_path=args.policy,
                baseline_path=args.baseline,
                output_format=args.format,
            )
    except (OSError, ValueError) as exc:
        print(f"agentctl: {exc}", file=sys.stderr)
        return 2
    return 2
