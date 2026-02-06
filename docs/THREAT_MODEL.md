# Threat Model

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Signal |
| --- | --- | --- | --- | --- |
| Reward hacking | Medium | High | Explicit NEV components and audit logs | Sudden NEV spikes without revenue |
| Collusion | Low | High | Agent isolation and deterministic simulator | Correlated outputs across agents |
| Sybil agents | Medium | Medium | Per-agent registration + rate limits | Many new agents with similar behavior |
| Prompt injection | Medium | High | No external inputs or tools in Phase 0 | Unexpected action attempts |
| Data exfiltration | Low | High | No external network calls | Attempts to access network |
| Runaway spending | Medium | High | Budget caps + circuit breakers | Budget cap alerts |
| Tool misuse | Medium | High | Allowlist + audits | Unauthorized tool usage |
| Illegal strategies | Low | High | Hard constraints + penalties | Policy violation logs |
| Emergent power concentration | Low | Medium | Agent mortality + NEV weighting limits | Single agent dominates leaderboard |
