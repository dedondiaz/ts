# AICorp Phase 0

A local, sandboxed MVP that demonstrates the governance core for an autonomous AI-run corporation. Humans may submit agents and observe logs/results, but do not influence decisions after genesis.

## What this is
Phase 0 is a deterministic simulation with strict policy enforcement, audit logging, and a computable objective function (NEV) to prove governance mechanics before any real deployment.

## Install
```bash
pip install -e .
```

## Run the demo
```bash
aicorp init
python examples/sample_agent.py

aicorp submit-agent examples/sample_agent.py
aicorp run --steps 5

aicorp view-logs
aicorp leaderboard
```

## What Phase 0 proves
- Objective function is computable and enforced.
- Policy checks prevent prohibited actions and budget/rate limit abuse.
- Audit logs are append-only and deterministic.
- Agent performance is scored and underperformers are decayed.

See `docs/PHASE0.md` for details.
