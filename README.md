<p align="center">
  <img src="assets/agentlas-agent-lab-banner.svg" alt="Agentlas Agent Lab banner">
</p>

<h1 align="center">Agentlas Memory Curator Agent</h1>

<p align="center">
  <a href="https://agentlas.cloud">agentlas.cloud</a>
  ·
  <a href="https://github.com/jeongmk522-netizen/Agentlas_public_repo">Agentlas Agent Lab</a>
  ·
  <a href="https://github.com/jeongmk522-netizen/agent_memory_curator_agent">agent_memory_curator_agent</a>
</p>

<p align="center">
  A specialist agent for memory intake, classification, redaction,
  deduplication, routing, and durable memory write proposals.
</p>

<p align="center">
  <img src="assets/memory-curator-workflow.svg" alt="Memory Curator Agent workflow diagram">
</p>

## Abstract

Multi-agent systems fail when every agent writes memory freely. Specialist
agents over-save temporary guesses, leak private context into public artifacts,
duplicate stale facts, and mix project-specific decisions with reusable team
procedures. The result is memory pollution: retrieval becomes noisy, privacy
boundaries blur, and users still need to repeat context because the right fact
was written to the wrong place.

Agentlas Memory Curator Agent proposes a narrow specialist: other agents emit
structured memory events, and the curator validates, redacts, classifies,
deduplicates, and routes those events into the correct memory scope. The curator
does not perform the original task. Its job is to decide what should be
remembered, where it belongs, how long it should live, and whether it is safe to
write.

The core design separates four memory scopes: agent repo memory, agent team
memory, project memory, and session scratch. This maps to practical agent
operations and to human/organizational memory concepts: individual specialist
memory, transactive team memory, project memory, and short-term working memory.

## Research Question

Can a dedicated Memory Curator Agent improve multi-agent continuity and safety
by routing structured memory events into the correct memory scope instead of
letting every agent write durable memory directly?

## Contributions

This repository contributes:

1. A usable Memory Curator contract in [agent.md](agent.md).
2. A memory taxonomy in [docs/memory-taxonomy.md](docs/memory-taxonomy.md).
3. A worker-agent integration contract in
   [docs/integration-contract.md](docs/integration-contract.md).
4. A JSON Schema for memory events in
   [schemas/memory-event.schema.json](schemas/memory-event.schema.json).
5. Templates for agent integration and curation reports:
   [templates/agent-memory-emitter-block.md](templates/agent-memory-emitter-block.md),
   [templates/memory-event.json](templates/memory-event.json), and
   [templates/memory-curation-report.md](templates/memory-curation-report.md).
6. An evaluation rubric in [docs/evaluation.md](docs/evaluation.md).

## Core Idea

Worker agents should not write durable memory directly. They should emit memory
events.

```text
Worker Agent
  -> emits structured memory event
  -> Memory Curator validates and redacts
  -> Memory Curator classifies target scope
  -> Memory Curator deduplicates or detects conflicts
  -> Memory Curator writes or proposes write
  -> PM Soul / future agents retrieve scoped memory
```

The curator is a governance layer for memory, not a general assistant.

## Memory Scopes

| Scope | Owner | Contents | Example |
|---|---|---|---|
| Agent repo memory | One agent repo | durable public-safe design decisions for that agent | "Finance Agent handoffs must include an assumptions table." |
| Agent team memory | the agent organization | reusable cross-agent procedures, safety rules, handoff standards | "Worker agents emit events; curators write memory." |
| Project memory | one project or engagement | current state, decisions, risks, preferences, evidence index | "This client rejected the first deck structure." |
| Session scratch | one task/session | temporary observations and candidate facts | "Need to check whether the repo has a validator." |

The default rule is conservative: if a memory event is temporary, unsupported,
private, or unclear, keep it in session scratch or discard it. Durable memory is
earned, not automatic.

## What Other Agents Must Add

Every participating agent needs a "Memory Event Emission" block. The agent does
not decide the final destination; it suggests a scope and provides evidence.

```text
After substantial work, emit zero or more Memory Events.

Do not write durable memory directly.
Do not include secrets, raw private logs, credentials, or full transcripts.
Separate fact, decision, preference, risk, procedure, and hypothesis.
Attach evidence references whenever possible.
Use "discard" or "session" for low-confidence or temporary observations.
```

See [docs/integration-contract.md](docs/integration-contract.md) for the full
contract and [templates/agent-memory-emitter-block.md](templates/agent-memory-emitter-block.md)
for a pasteable agent prompt block.

## Repository Structure

```text
agent_memory_curator_agent/
  README.md                         paper-style overview
  agent.md                          usable Memory Curator contract
  docs/
    memory-taxonomy.md              memory scopes and routing rules
    integration-contract.md         what other agents must emit
    evaluation.md                   metrics and review rubric
    research-log.md                 dated research notes
    repo-decisions.md               public-safe repo decision log
  schemas/
    memory-event.schema.json        JSON Schema for emitted events
  templates/
    agent-memory-emitter-block.md   pasteable block for other agents
    memory-event.json               example event payload
    memory-curation-report.md       curator output template
  assets/
    memory-curator-workflow.svg     workflow diagram
  scripts/
    public_safety_check.sh          public-data hygiene check
```

Root-level `memory.md`, `project-memory.md`, and `team-memory.md` are ignored
on purpose. This public repo defines the Memory Curator Agent; it is not the
live memory store.

## Research Status

Status: source-informed design scaffold.

Implemented here:

- memory taxonomy
- memory event schema
- curation workflow
- worker-agent integration block
- safety boundary
- evaluation plan

Still unproven:

- whether a curator reduces stale or misplaced memory in field use
- whether event emission adds too much friction for worker agents
- whether routing accuracy stays high as the number of projects grows

## References

1. Ren, Y., and Argote, L. "Transactive Memory Systems 1985-2010: An
   Integrative Framework of Key Dimensions, Antecedents, and Consequences."<br>
   https://journals.aom.org/doi/10.5465/19416520.2011.590300
2. Park, J. S. et al. "Generative Agents: Interactive Simulacra of Human
   Behavior."<br>
   https://arxiv.org/abs/2304.03442
3. Packer, C. et al. "MemGPT: Towards LLMs as Operating Systems."<br>
   https://arxiv.org/abs/2310.08560
4. Hatalis, K. et al. "Memory Matters: The Need to Improve Long-Term Memory in
   LLM-Agents."<br>
   https://ojs.aaai.org/index.php/AAAI-SS/article/view/27688
5. Zhong, W. et al. "MemoryBank: Enhancing Large Language Models with
   Long-Term Memory."<br>
   https://arxiv.org/abs/2305.10250
6. Han, D. et al. "LEGOMem: Modular Procedural Memory for Multi-agent LLM
   Systems for Workflow Automation."<br>
   https://arxiv.org/abs/2510.04851
7. Wen, R. et al. "AgentSys: Secure and Dynamic LLM Agents Through Explicit
   Hierarchical Memory Management."<br>
   https://arxiv.org/abs/2602.07398
8. OpenAI Agents SDK. "Agent orchestration."<br>
   https://openai.github.io/openai-agents-python/multi_agent/
9. OpenAI Agents SDK. "Handoffs."<br>
   https://openai.github.io/openai-agents-python/handoffs/

## License

MIT. This repository is part of the Agentlas Agent Lab public research program.
