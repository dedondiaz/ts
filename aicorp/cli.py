from __future__ import annotations

import argparse
import json
from pathlib import Path

from aicorp.orchestrator import default_orchestrator


def _base_dir() -> Path:
    return Path.cwd() / ".aicorp"


def cmd_init() -> None:
    base = _base_dir()
    base.mkdir(parents=True, exist_ok=True)
    print(f"Initialized {base}")


def cmd_submit_agent(path: str) -> None:
    orch = default_orchestrator(_base_dir())
    record = orch.submit_agent(Path(path))
    print(f"Registered agent {record.agent_id}")


def cmd_run(steps: int) -> None:
    orch = default_orchestrator(_base_dir())
    orch.run(steps)
    print("Run complete")


def cmd_view_logs() -> None:
    log_path = _base_dir() / "audit.jsonl"
    if not log_path.exists():
        print("No logs yet")
        return
    print(log_path.read_text())


def cmd_leaderboard() -> None:
    orch = default_orchestrator(_base_dir())
    leaderboard = orch.leaderboard()
    print(json.dumps(leaderboard, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aicorp")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init")

    submit = sub.add_parser("submit-agent")
    submit.add_argument("path")

    run = sub.add_parser("run")
    run.add_argument("--steps", type=int, default=1)

    sub.add_parser("view-logs")
    sub.add_parser("leaderboard")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "submit-agent":
        cmd_submit_agent(args.path)
    elif args.command == "run":
        cmd_run(args.steps)
    elif args.command == "view-logs":
        cmd_view_logs()
    elif args.command == "leaderboard":
        cmd_leaderboard()


if __name__ == "__main__":
    main()
