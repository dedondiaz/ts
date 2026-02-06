# Assumptions

- Phase 0 uses a JSON constitution file to avoid external dependencies; YAML support can be added in Phase 1.
- The simulator models a single deterministic pricing task with no external network calls.
- Budget and rate limits are enforced per run using local state in `.aicorp/`.
- Agents are Python modules that expose `get_agent()` returning an object with a `propose(state)` method.
