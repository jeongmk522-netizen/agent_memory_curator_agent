# Claude Guide: Agentlas Memory Curator Agent

This repository defines one public Agentlas agent.

## Mission

Define a specialist agent that receives memory events from other agents,
classifies the correct memory scope, redacts unsafe content, and proposes or
applies durable memory writes.

## Work Loop

1. Read `README.md`, `agent.md`, `docs/memory-taxonomy.md`,
   `docs/integration-contract.md`, and `docs/repo-decisions.md`.
2. Make the smallest useful change.
3. Update `docs/research-log.md` when the agent design changes.
4. Run `scripts/public_safety_check.sh`.

## Boundaries

- Do not put private project memory into public docs.
- Do not commit root-level `memory.md`.
- Treat this repo as a public research artifact, not a live memory store.
