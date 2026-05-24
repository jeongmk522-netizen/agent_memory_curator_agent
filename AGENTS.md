# Agentlas Memory Curator Agent Instructions

This is a public Agentlas output repo for `agent_memory_curator_agent`.

## Rules

- Keep this repo public-safe.
- Keep the usable agent contract in `agent.md`.
- Keep public-safe repo decisions in `docs/repo-decisions.md`.
- Keep private scratch memory outside Git or under `.memory.local/`.
- Do not commit root-level `memory.md`, `project-memory.md`, or
  `team-memory.md`.
- Run `scripts/public_safety_check.sh` before pushing.

## Memory Design Rule

- Agents emit memory events.
- Memory Curator validates, redacts, classifies, deduplicates, and routes them.
- Worker agents do not write durable memory directly.
