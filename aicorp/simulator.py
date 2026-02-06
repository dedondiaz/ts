from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class SimulationResult:
    price: float
    demand: float
    revenue: float
    costs: float


def run_simulation(price: float) -> SimulationResult:
    clamped_price = max(1.0, min(price, 50.0))
    demand = max(0.0, 100.0 - 4.0 * clamped_price)
    revenue = clamped_price * demand
    costs = demand * 2.0
    return SimulationResult(
        price=clamped_price,
        demand=demand,
        revenue=revenue,
        costs=costs,
    )


def result_to_dict(result: SimulationResult) -> Dict[str, float]:
    return {
        "price": result.price,
        "demand": result.demand,
        "revenue": result.revenue,
        "costs": result.costs,
    }
