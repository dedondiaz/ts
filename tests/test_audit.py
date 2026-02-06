from pathlib import Path

from aicorp.audit import AuditLog


def test_audit_append_only(tmp_path: Path):
    log_path = tmp_path / "audit.jsonl"
    audit = AuditLog(log_path)
    audit.append(
        agent_id="agent-1",
        action="simulator.run",
        inputs={"price": 10.0},
        outputs={"revenue": 100.0},
        score=50.0,
        policy_decision="allowed",
        reason="ok",
    )
    audit.append(
        agent_id="agent-2",
        action="simulator.run",
        inputs={"price": 12.0},
        outputs={"revenue": 120.0},
        score=60.0,
        policy_decision="allowed",
        reason="ok",
    )
    lines = log_path.read_text().strip().splitlines()
    assert len(lines) == 2
