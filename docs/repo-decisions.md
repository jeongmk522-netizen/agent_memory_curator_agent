# Repo Decisions

This is the public-safe decision log for `agent_memory_curator_agent`.

Root-level `memory.md`, `project-memory.md`, and `team-memory.md` are ignored
because this public repo defines the Memory Curator Agent; it is not a live
memory store.

## Stable Facts

- Agent name: Agentlas Memory Curator Agent
- Agent slug: `memory_curator_agent`
- Repository name: `agent_memory_curator_agent`
- Public site: `https://agentlas.cloud`

## Decisions

### 2026-05-24: Memory Curator As Write Gate

Worker agents should emit structured memory events rather than writing durable
memory directly. The Memory Curator validates, redacts, classifies, deduplicates,
and routes those events.

### 2026-05-24: Four-Scope Memory Taxonomy

The initial taxonomy separates memory into agent repo memory, agent team memory,
project memory, and session scratch. This prevents project-specific memory from
polluting reusable team playbooks or public agent repos.

### 2026-05-24: Public Repo Is Not Live Memory

This repository should contain public-safe research, schemas, and templates.
It should not contain live user/project/team memory stores.

### 2026-05-24: Other Agents Need An Emitter Block

To make Memory Curator operational, every participating agent needs a standard
Memory Event Emission block and must return zero or more memory events after
substantial work.

## Open Questions

- Should the curator write directly to private project memory, or only propose?
- How much evidence is enough for a durable memory write?
- Should conflicts block future retrieval until resolved?
- Should low-confidence hypotheses be retrievable by default?
- What is the best format for append-only audit logs?
