from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


@dataclass(frozen=True)
class AuditRecord:
    timestamp: str
    agent_id: str
    action: str
    inputs_hash: str
    outputs_hash: str
    score: float
    policy_decision: str
    reason: str


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(
        self,
        agent_id: str,
        action: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        score: float,
        policy_decision: str,
        reason: str,
    ) -> AuditRecord:
        record = AuditRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            agent_id=agent_id,
            action=action,
            inputs_hash=_hash_payload(inputs),
            outputs_hash=_hash_payload(outputs),
            score=score,
            policy_decision=policy_decision,
            reason=reason,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record.__dict__) + "\n")
        return record


def _hash_payload(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
