# Integration Contract

Date: 2026-05-24

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

## Event Lifecycle

```text
Worker Agent completes work
  -> emits Memory Event(s)
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
| `suggested_scope` | agent_repo, agent_team, project, session, discard |
| `sensitivity` | public, internal, private, confidential, secret |
| `confidence` | high, medium, low |
| `evidence_refs` | source files, URLs, commits, logs, or artifacts |
| `ttl` | durable, until_milestone, session, discard |

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
    "suggested_scope": "agent_team",
    "sensitivity": "public",
    "confidence": "high",
    "evidence_refs": ["docs/case-study-consulting-engagement.md"],
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
