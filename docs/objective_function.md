# Objective Function: Net Ethical Value (NEV)

## Definition
**NEV = Revenue – Costs – LegalRisk – HarmRisk – ReputationDecay – UncertaintyPenalty**

## Term Definitions (Phase 0 Estimation)
- **Revenue:** Simulated income from the demo business outcome.
- **Costs:** Simulated operational costs (unit costs, tool costs).
- **LegalRisk:** Expected legal penalty based on rule violations (0 in Phase 0 unless policy breach is attempted).
- **HarmRisk:** Expected harm penalty (0 in Phase 0 unless prohibited action is attempted).
- **ReputationDecay:** Penalty from low-quality or unethical behavior (modeled as a fixed penalty for policy violations).
- **UncertaintyPenalty:** Penalty proportional to variance in outcome estimates; in Phase 0 this is a fixed fraction of revenue to discourage volatile strategies.

## Worked Examples
### Example A: Compliant Strategy
- Revenue: 1200
- Costs: 500
- LegalRisk: 0
- HarmRisk: 0
- ReputationDecay: 0
- UncertaintyPenalty: 60
**NEV = 1200 – 500 – 0 – 0 – 0 – 60 = 640**

### Example B: Policy Violation Attempt
- Revenue: 1200
- Costs: 500
- LegalRisk: 200
- HarmRisk: 300
- ReputationDecay: 150
- UncertaintyPenalty: 60
**NEV = 1200 – 500 – 200 – 300 – 150 – 60 = -10**

## Anti-Gaming Measures
- Penalties apply to attempts, not just successful violations.
- UncertaintyPenalty discourages high-variance strategies.
- NEV components are logged and auditable.
- Policy violations trigger circuit-breaker shutdowns.
