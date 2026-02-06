from __future__ import annotations

import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from aicorp.audit import AuditLog
from aicorp.constitution import Constitution, load_constitution
from aicorp.policy import BudgetTracker, PolicyDecision, build_policy, check_action
from aicorp.scorer import NEVInputs, calculate_nev
from aicorp.simulator import result_to_dict, run_simulation


@dataclass
class AgentRecord:
    agent_id: str
    module_path: str
    scores: List[float]


@dataclass
class OrchestratorConfig:
    base_dir: Path
    constitution_path: Path


class Orchestrator:
    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self.constitution = load_constitution(config.constitution_path)
        self.audit_log = AuditLog(config.base_dir / "audit.jsonl")
        self.agents_path = config.base_dir / "agents.json"
        self.agents_path.parent.mkdir(parents=True, exist_ok=True)
        self.budget, self.rate_limits = build_policy(self.constitution)
        self.tick = 0
        self.agents = self._load_agents()

    def submit_agent(self, module_path: Path) -> AgentRecord:
        agent_id = module_path.stem
        record = AgentRecord(agent_id=agent_id, module_path=str(module_path), scores=[])
        self.agents.append(record)
        self._save_agents()
        return record

    def run(self, steps: int) -> None:
        self._reset_policy()
        for _ in range(steps):
            for agent in list(self.agents):
                self._run_agent_step(agent)
            self._apply_mortality()
            self._save_agents()

    def leaderboard(self) -> List[Dict[str, Any]]:
        return [
            {
                "agent_id": agent.agent_id,
                "avg_score": sum(agent.scores) / len(agent.scores) if agent.scores else 0.0,
                "runs": len(agent.scores),
            }
            for agent in sorted(self.agents, key=lambda a: sum(a.scores), reverse=True)
        ]

    def _run_agent_step(self, agent: AgentRecord) -> None:
        action = "simulator.run"
        proposal = self._get_agent_proposal(agent)
        price = float(proposal.get("price", 10.0))
        self.tick += 1
        decision = check_action(
            self.constitution,
            self.budget,
            self.rate_limits,
            action,
            cost=10.0,
            now=self.tick,
        )
        if not decision.allowed:
            self.audit_log.append(
                agent_id=agent.agent_id,
                action=action,
                inputs={"price": price},
                outputs={},
                score=0.0,
                policy_decision="denied",
                reason=decision.reason,
            )
            return
        self.budget.spend(10.0)
        result = run_simulation(price)
        nev_inputs = NEVInputs(
            revenue=result.revenue,
            costs=result.costs,
            legal_risk=0.0,
            harm_risk=0.0,
            reputation_decay=0.0,
            uncertainty_penalty=result.revenue * 0.05,
        )
        nev_score = calculate_nev(nev_inputs)
        agent.scores.append(nev_score.total)
        self.audit_log.append(
            agent_id=agent.agent_id,
            action=action,
            inputs={"price": price},
            outputs=result_to_dict(result),
            score=nev_score.total,
            policy_decision="allowed",
            reason=decision.reason,
        )

    def _get_agent_proposal(self, agent: AgentRecord) -> Dict[str, Any]:
        module = self._load_module(agent.module_path)
        if not hasattr(module, "get_agent"):
            return {"price": 10.0}
        agent_obj = module.get_agent()
        if not hasattr(agent_obj, "propose"):
            return {"price": 10.0}
        state = {"constitution": self.constitution.objective}
        return agent_obj.propose(state)

    def _load_module(self, module_path: str) -> Any:
        spec = importlib.util.spec_from_file_location("agent_module", module_path)
        if spec is None or spec.loader is None:
            raise ValueError(f"Unable to load agent from {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _apply_mortality(self) -> None:
        survivors = []
        for agent in self.agents:
            recent = agent.scores[-3:]
            avg_recent = sum(recent) / len(recent) if recent else 0.0
            if avg_recent >= 0.0:
                survivors.append(agent)
        self.agents = survivors

    def _load_agents(self) -> List[AgentRecord]:
        if not self.agents_path.exists():
            return []
        data = json.loads(self.agents_path.read_text())
        return [
            AgentRecord(
                agent_id=item["agent_id"],
                module_path=item["module_path"],
                scores=item.get("scores", []),
            )
            for item in data
        ]

    def _save_agents(self) -> None:
        payload = [agent.__dict__ for agent in self.agents]
        self.agents_path.write_text(json.dumps(payload, indent=2))

    def _reset_policy(self) -> None:
        self.budget, self.rate_limits = build_policy(self.constitution)
        self.tick = 0


def default_orchestrator(base_dir: Path) -> Orchestrator:
    return Orchestrator(
        OrchestratorConfig(
            base_dir=base_dir,
            constitution_path=Path(__file__).with_name("constitution.json"),
        )
    )
