# Phase 0

## Includes
- Local sandboxed simulator for a pricing demo business.
- NEV scoring with explicit penalties.
- Policy enforcement (allowlist, budget caps, rate limits).
- Append-only audit logs and leaderboard.
- Agent mortality rules based on rolling NEV.

## Excludes
- Real money, customers, or external APIs.
- Human approvals or overrides.
- Network calls of any kind.

## Go/No-Go Gates for Phase 1
- ✅ Deterministic simulator produces stable results across runs.
- ✅ Policy violations are blocked and logged.
- ✅ Audit logs are append-only and match schema.
- ✅ NEV components are computed and explainable.
- ✅ Leaderboard updates after each run.

## Demo Business (Sandboxed)
A deterministic pricing experiment where agents propose a price. Demand is a linear function of price; revenue and costs are computed deterministically to yield NEV.
