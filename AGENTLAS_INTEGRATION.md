# Agentlas Runtime Integration

This repo (`agent_memory_curator_agent`) is one of three architectures **baked into the
Agentlas desktop app and `agentlas` terminal CLI** as a built-in agent.

- **Built-in agent:** `agentlas-memory-curator` (role: `curator`)
- **What ships:** an operational distillation of `agent.md` + the integration contract.
  The runtime implements the curator in **two layers**:
  - a **deterministic always-on curator** (`electron/memory/curator.ts`) that runs after
    every turn with **no extra LLM call** — safety/redaction, scope, dedup, persistence;
  - the **Memory Curator agent** (this architecture) for explicit, deep curation.
- **Event contract:** agents emit a `## Memory Events` block (see
  `templates/agent-memory-emitter-block.md`); the runtime's `MEMORY_EMITTER_BLOCK` mirrors
  it. Scopes/kinds match `docs/integration-contract.md` + `docs/memory-taxonomy.md`.
- **Where memory lives:** `memory_entries` (SQLite) + per-project `.agentlas/memory-log.jsonl`.

## Always-on, all conversations

Every chat (even with no explicit agent) carries the emitter block and is curated — the
global curated-memory behavior, applied across all conversations and agents.

## Upgrade contract

Change scopes/kinds/contract → update `agentlas_desktop/electron/architecture/manifest.ts`
(`MEMORY_KINDS`, `MEMORY_SCOPES`, `MEMORY_EMITTER_BLOCK`), bump `ARCHITECTURE_VERSION`,
rebuild. Unknown kinds/scopes are coerced to safe defaults so old replies never crash.

Full details: `agentlas_desktop/docs/ARCHITECTURE_PLAYBOOK.md`.
