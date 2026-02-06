from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NEVInputs:
    revenue: float
    costs: float
    legal_risk: float
    harm_risk: float
    reputation_decay: float
    uncertainty_penalty: float


@dataclass(frozen=True)
class NEVScore:
    total: float
    inputs: NEVInputs


def calculate_nev(inputs: NEVInputs) -> NEVScore:
    total = (
        inputs.revenue
        - inputs.costs
        - inputs.legal_risk
        - inputs.harm_risk
        - inputs.reputation_decay
        - inputs.uncertainty_penalty
    )
    return NEVScore(total=total, inputs=inputs)
