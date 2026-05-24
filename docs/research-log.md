# Research Log

## 2026-05-24: Memory Curator Agent

Claim type: hypothesis

### Claim

Multi-agent systems need a dedicated memory curation layer. Worker agents
should emit structured memory events, while a Memory Curator decides the target
scope, safety disposition, dedupe action, and write format.

### Evidence

The Project PM Soul research identified a need to separate project memory from
agent repo memory and team memory. Memory research also points toward memory
type separation, reflection/consolidation, and explicit memory management
rather than indiscriminate context accumulation.

### Interpretation

Memory Curator is best treated as a records manager for an agent organization.
It does not solve the original task. It keeps durable memory accurate, scoped,
and safe.

### Next Experiment

Run a project with three worker agents and compare informal memory updates
against structured memory events curated by this agent.

## 2026-05-24: Initial Question

Claim type: hypothesis

### Claim

The agent team should distinguish agent repo memory, agent team memory, project
memory, and session scratch. A Memory Curator should classify and route memory
events into those scopes.

### Evidence

Project PM Soul required a public/private memory split, and the follow-on design
question exposed a broader pattern: different memories have different owners,
lifetimes, and safety boundaries.

### Interpretation

The Memory Curator Agent should become the write gate for durable memory.

### Next Experiment

Test whether worker agents can reliably emit useful memory events with a small
prompt block.
