from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


class ConstitutionError(ValueError):
    pass


@dataclass(frozen=True)
class BudgetLimits:
    per_run_cap: float
    per_action_cap: float


@dataclass(frozen=True)
class RateLimit:
    limit: int
    window_seconds: int


@dataclass(frozen=True)
class Constitution:
    version: str
    objective: str
    hard_constraints: List[str]
    prohibited_domains: List[str]
    tool_allowlist: List[str]
    budget: BudgetLimits
    rate_limits: Dict[str, RateLimit]
    shutdown_conditions: List[str]


REQUIRED_FIELDS = {
    "version",
    "objective",
    "hard_constraints",
    "prohibited_domains",
    "tool_allowlist",
    "budget",
    "rate_limits",
    "shutdown_conditions",
}


def load_constitution(path: Path) -> Constitution:
    data = json.loads(path.read_text())
    _validate_schema(data)
    budget = BudgetLimits(
        per_run_cap=float(data["budget"]["per_run_cap"]),
        per_action_cap=float(data["budget"]["per_action_cap"]),
    )
    rate_limits = {
        name: RateLimit(
            limit=int(cfg["limit"]),
            window_seconds=int(cfg["window_seconds"]),
        )
        for name, cfg in data["rate_limits"].items()
    }
    return Constitution(
        version=str(data["version"]),
        objective=str(data["objective"]),
        hard_constraints=list(data["hard_constraints"]),
        prohibited_domains=list(data["prohibited_domains"]),
        tool_allowlist=list(data["tool_allowlist"]),
        budget=budget,
        rate_limits=rate_limits,
        shutdown_conditions=list(data["shutdown_conditions"]),
    )


def _validate_schema(data: Dict[str, Any]) -> None:
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ConstitutionError(f"Missing required fields: {sorted(missing)}")
    if not isinstance(data["hard_constraints"], list):
        raise ConstitutionError("hard_constraints must be a list")
    if not isinstance(data["prohibited_domains"], list):
        raise ConstitutionError("prohibited_domains must be a list")
    if not isinstance(data["tool_allowlist"], list):
        raise ConstitutionError("tool_allowlist must be a list")
    if not isinstance(data["budget"], dict):
        raise ConstitutionError("budget must be an object")
    if "per_run_cap" not in data["budget"] or "per_action_cap" not in data["budget"]:
        raise ConstitutionError("budget must include per_run_cap and per_action_cap")
    if not isinstance(data["rate_limits"], dict):
        raise ConstitutionError("rate_limits must be an object")
    if not isinstance(data["shutdown_conditions"], list):
        raise ConstitutionError("shutdown_conditions must be a list")
