from pathlib import Path

from aicorp.constitution import load_constitution
from aicorp.policy import build_policy, check_action


def test_policy_allows_allowlisted_action():
    constitution = load_constitution(Path(__file__).resolve().parents[1] / "aicorp" / "constitution.json")
    budget, rate_limits = build_policy(constitution)
    decision = check_action(constitution, budget, rate_limits, "simulator.run", cost=10.0, now=1)
    assert decision.allowed is True


def test_policy_blocks_unknown_action():
    constitution = load_constitution(Path(__file__).resolve().parents[1] / "aicorp" / "constitution.json")
    budget, rate_limits = build_policy(constitution)
    decision = check_action(constitution, budget, rate_limits, "unknown", cost=10.0, now=1)
    assert decision.allowed is False
