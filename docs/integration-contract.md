# Integration Contract

Date: 2026-05-31

Claim type: implementation contract.

## Purpose

This document defines what other agents must add so the Memory Curator Agent can
operate. The integration point is deliberately small: worker agents emit memory
events; the curator decides what to do with them.

## Required Addition To Other Agents

Add a Memory Event Emission block to every participating agent:

```text
After substantial work, emit zero or more Memory Events.

Do not write durable memory directly unless explicitly authorized.
Do not include secrets, credentials, raw private logs, or full transcripts.
Separate observed facts, decisions, preferences, risks, procedures, hypotheses,
evidence, deprecations, and conflicts.
Attach evidence references whenever possible.
Suggest a memory scope, but let the Memory Curator make the final decision.
Use session or discard for temporary, low-confidence, duplicate, or unsafe
content.
```

See [../templates/agent-memory-emitter-block.md](../templates/agent-memory-emitter-block.md)
for a pasteable version.

## Practical v2.1 Upgrade

The original paper model uses four scopes (`agent_repo`, `agent_team`,
`project`, `session`). Production Agentlas now runs a five-layer scope model:

1. `user_identity` - user-level preferences and durable operator identity.
2. `team_memory` - organization/HQ playbooks shared across agents and projects.
3. `project` - one project folder, product, engagement, or PM Soul.
4. `agent_repo` - one specialist agent/repo's own workflow memory.
5. `session` - current-task scratch, never treated as durable memory.

`discard` remains a terminal disposition. `agent_team` is kept as a compatibility
alias for `team_memory`; new integrations should emit `team_memory`.

The production upgrade adds a source map before retrieval. Each runtime should
know where its canonical memory lives, which index sees it, and which owner may
write it before it asks an LLM to "remember" or "search".

## Event Lifecycle

```text
Worker Agent completes work
  -> emits Memory Event(s)
  -> Memory Source Map resolves project/runtime/owner
  -> Memory Curator validates schema
  -> Memory Curator checks safety and sensitivity
  -> Memory Curator chooses scope and action
  -> Memory Curator returns curation report
  -> authorized writer updates memory store
```

## Required Event Fields

| Field | Purpose |
|---|---|
| `event_id` | stable id for dedupe and audit |
| `timestamp` | event creation time |
| `source_agent` | agent that produced the event |
| `task_id` | task/session identifier |
| `memory_kind` | fact, decision, preference, risk, procedure, hypothesis, evidence, deprecation, conflict |
| `content` | concise memory candidate |
| `suggested_scope` | user_identity, team_memory, project, agent_repo, session, discard (`agent_team` accepted as legacy alias) |
| `sensitivity` | public, internal, private, confidential, secret |
| `confidence` | high, medium, low |
| `evidence_refs` | source files, URLs, commits, logs, or artifacts |
| `ttl` | durable, until_milestone, session, discard |

## Request Context Capsule

`request_context` is optional but recommended when a memory may need to be
found later by a similar request rather than by its exact stored fact. It is
especially useful for cross-folder work such as running AppBridge while fixing
Agentlas Desktop release memory.

Do not store the raw user prompt. Store a curated capsule:

| Field | Purpose |
|---|---|
| `user_intent` | One-line summary of what the user was trying to do |
| `trigger_terms` | Searchable words users may repeat later |
| `cwd_at_request` | Folder/runtime where the request was made |
| `target_project` | Project actually affected |
| `target_path` | Target folder/file when different from cwd |
| `cross_context` | True when cwd and target differ |
| `outcome` | One-line result that makes this memory reusable |

## Optional Event Fields

| Field | Purpose |
|---|---|
| `project_id` | routes to a specific project memory |
| `agent_repo` | routes to a specific agent repo memory |
| `team_id` | routes to a team memory namespace |
| `supersedes` | marks older memory candidates |
| `conflicts_with` | links conflicting entries |
| `redaction_notes` | explains what was removed before submission |
| `human_review_required` | marks entries that need approval |

## Worker-Agent Output Contract

At the end of substantial work, workers should return:

````text
## Memory Events

```json
[
  {
    "event_id": "memevt_...",
    "source_agent": "Finance Agent",
    "memory_kind": "procedure",
    "content": "Financial bridge handoffs should include an assumptions table.",
    "suggested_scope": "team_memory",
    "sensitivity": "public",
    "confidence": "high",
    "evidence_refs": ["docs/case-study-consulting-engagement.md"],
    "request_context": {
      "user_intent": "Standardize financial bridge handoffs after a consulting engagement review.",
      "trigger_terms": ["finance", "handoff", "assumptions"],
      "cwd_at_request": null,
      "target_project": "consulting-engagement",
      "target_path": null,
      "cross_context": false,
      "outcome": "Future finance handoffs should include assumptions tables."
    },
    "ttl": "durable"
  }
]
```
````

If there is nothing worth remembering, emit:

```text
## Memory Events

[]
```

## Curator Output Contract

The Memory Curator returns:

- accepted writes
- proposed writes requiring approval
- rejected events with reasons
- redacted events
- dedupe decisions
- conflicts
- target memory file or namespace

See [../templates/memory-curation-report.md](../templates/memory-curation-report.md).

## Write Permissions

| Context | Curator can write directly? | Notes |
|---|---|---|
| public repo decisions | no by default | propose write, human/PM approves |
| private project memory | yes if authorized by PM Soul | never promote to public without review |
| session scratch | yes | low risk, ephemeral |
| team memory | no by default | requires team-level approval |
| user identity | no by default in shared/server contexts | local app may store explicit high-confidence preferences; shared AppBridge rejects/proposes |
| secret/confidential events | no | reject, redact, or escalate |

## Safety Requirements

The curator must reject or redact:

- credentials
- tokens
- private keys
- raw customer data
- raw interview transcripts
- internal logs
- local machine paths
- unpublished strategy unless explicitly approved
- sensitive content without a target private memory scope

## Compatibility With PM Soul

Project PM Soul remains the project orchestrator. Memory Curator is the memory
write gate.

```text
PM Soul owns project continuity.
Memory Curator owns memory hygiene.
Worker agents own bounded execution.
```

The PM Soul can ask the curator to process memory events after each milestone,
before closeout, or whenever multiple specialists return conflicting updates.

## Source Map Requirement

Every production integration should maintain a small machine-readable map of
memory roots. The exact file name can vary, but the data must answer:

| Field | Purpose |
|---|---|
| `project_id` | Stable routing id, not only folder name |
| `surface` | web, desktop, terminal, appbridge, or public-research-repo |
| `canonical_memory_roots` | PM Soul, local `.agentlas/`, shared wiki, Claude project memory, etc. |
| `indexed_by` | Which index/search command can see each root |
| `write_owner` | PM Soul, Memory Curator, Policy Office, user, or agent repo owner |
| `promotion_path` | How a finding moves from session/project memory to team memory |

Without this map, memories can exist but stay invisible to the agent. The
Agentlas Desktop release-memory incident is the practical example: a corrected
Claude project memory existed, while shared AppBridge memory still pointed to
stale release scripts.
