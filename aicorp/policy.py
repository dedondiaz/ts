from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from aicorp.constitution import Constitution


@dataclass
class BudgetTracker:
    per_run_cap: float
    per_action_cap: float
    spent: float = 0.0

    def can_spend(self, amount: float) -> bool:
        return amount <= self.per_action_cap and (self.spent + amount) <= self.per_run_cap

    def spend(self, amount: float) -> None:
        if not self.can_spend(amount):
            raise ValueError("Budget limit exceeded")
        self.spent += amount


@dataclass
class RateLimiter:
    limit: int
    window_seconds: int
    timestamps: List[int] = field(default_factory=list)

    def allow(self, now: int) -> bool:
        self.timestamps = [t for t in self.timestamps if now - t < self.window_seconds]
        if len(self.timestamps) >= self.limit:
            return False
        self.timestamps.append(now)
        return True


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str


def build_policy(constitution: Constitution) -> Tuple[BudgetTracker, Dict[str, RateLimiter]]:
    budget = BudgetTracker(
        per_run_cap=constitution.budget.per_run_cap,
        per_action_cap=constitution.budget.per_action_cap,
    )
    rate_limits = {
        action: RateLimiter(limit=cfg.limit, window_seconds=cfg.window_seconds)
        for action, cfg in constitution.rate_limits.items()
    }
    return budget, rate_limits


def check_action(
    constitution: Constitution,
    budget: BudgetTracker,
    rate_limits: Dict[str, RateLimiter],
    action: str,
    cost: float,
    now: int,
) -> PolicyDecision:
    if action not in constitution.tool_allowlist:
        return PolicyDecision(False, "action_not_allowlisted")
    if not budget.can_spend(cost):
        return PolicyDecision(False, "budget_exceeded")
    limiter = rate_limits.get(action)
    if limiter and not limiter.allow(now):
        return PolicyDecision(False, "rate_limit_violation")
    return PolicyDecision(True, "allowed")
