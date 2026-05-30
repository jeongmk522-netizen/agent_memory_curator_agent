# Memory Taxonomy

Date: 2026-05-31

Claim type: design hypothesis.

## Thesis

Multi-agent systems need memory ownership, not just memory storage. The useful
question is not "should agents remember?" but "which memory should own this
entry, and who is allowed to write it?"

Agentlas Memory Curator separates production memory into five durable/scratch
scopes plus one terminal disposition:

1. user identity memory
2. team memory
3. project memory
4. agent repo memory
5. session scratch
6. discard

This separation keeps specialist agents narrow while preserving continuity
where it belongs.

## Scope Table

| Scope | Owner | Lifetime | Examples | Write gate |
|---|---|---|---|---|
| User identity memory (`user_identity`) | user/operator profile | durable | stable language, approval style, notification channel, identity-level preferences | explicit user edit or local high-confidence preference gate |
| Team memory (`team_memory`) | organization / HQ / policy office | durable | handoff standards, safety policies, shared routing conventions | team-level curator approval / promotion request |
| Agent repo memory | one public or private agent repo | durable | agent purpose, design decisions, failure modes, evaluation criteria | curated repo decision |
| Project memory | one project folder or engagement | project lifetime | project state, user preferences, decisions, risks, evidence index | PM Soul or curator approval |
| Session scratch | one task or session | ephemeral | temporary findings, candidate hypotheses, todo fragments | default capture, usually not durable |
| Discard | no owner | none | unsafe, duplicate, unsupported, secret, stale noise | reject/redact |

`agent_team` remains a legacy alias for `team_memory` because early paper
artifacts and exported agent bundles used that name.

## Why This Matters

Without scope separation:

- public repos can accidentally receive private project context
- worker agents can duplicate or contradict one another
- temporary guesses can become permanent facts
- retrieval becomes noisy
- users repeat context because the relevant fact was saved in the wrong place

With scope separation:

- specialists stay mostly stateless
- PM Soul retrieves project memory without loading every agent's history
- reusable procedures can be promoted to team memory
- public agent repo memory can stay clean and publication-safe

## Human/Organization Analogy

| Human/organization concept | Agentlas scope |
|---|---|
| operator/user profile | user identity memory |
| organization playbook / "how we work" | team memory |
| an individual's professional memory | agent repo memory |
| engagement/project file | project memory |
| working memory during a meeting | session scratch |
| "who knows what" in a team | team memory plus agent registry |

The Memory Curator is not the whole memory system. It is the librarian and
records manager that decides where each item belongs.

## Memory Kinds

| Kind | Definition | Durable by default? |
|---|---|---|
| `fact` | observed and evidence-backed state | yes, with evidence |
| `decision` | chosen direction plus rationale | yes |
| `preference` | stable user, stakeholder, or team preference | yes, if repeated or explicit |
| `risk` | unresolved blocker, exposure, or uncertainty | yes until closed |
| `procedure` | reusable way of working | yes if cross-task |
| `hypothesis` | plausible but unverified interpretation | no unless clearly labeled |
| `evidence` | source pointer or verification reference | yes if useful for retrieval |
| `deprecation` | stale or superseded entry marker | yes |
| `conflict` | two credible entries disagree | yes until resolved |

## Routing Matrix

| Event pattern | Target scope | Action |
|---|---|---|
| "User always wants Korean audit reports under 600 words" | user_identity | propose or append only in an explicit user/profile store |
| "This agent should always return memory events" | team_memory | append procedure via approval/promotion |
| "Project PM Soul README should be paper-style" | agent repo | append decision |
| "Client rejected version 1 deck structure" | project | append preference/decision |
| "Need to inspect API logs later" | session | keep scratch |
| "Maybe the issue is auth" with no evidence | session or discard | do not promote |
| "Token appears in logs" | discard and security alert | never write raw value |
| "Old project path moved" | project | update/deprecate prior entry |
| "Two agents disagree about release state" | project | create conflict entry |

## Promotion Rules

Session scratch can be promoted only when:

- it is still relevant after the task
- it has evidence or an explicit decision source
- it has a stable owner
- it belongs to a known scope
- it is safe to store

Project memory can become team memory only when:

- the lesson applies across multiple projects
- private details have been removed
- the procedure is stated generally
- the PM Soul or human reviewer approves promotion

Agent repo memory can become team memory only when:

- it changes how multiple agents should work
- it is not just a local implementation detail

## Anti-Patterns

- Every worker writes directly to shared memory.
- Memory entries contain full reasoning traces instead of durable conclusions.
- Public repos store private project notes.
- Project memory stores generic team policies.
- Team memory stores one-off project preferences.
- Stale entries are silently overwritten.
- Memory has no evidence references or last-checked dates.

## Minimum Viable Memory Stack

```text
memory-map.json           source map for roots, indexes, owners, promotion paths

events/
  incoming.jsonl          emitted by worker agents
  curation-report.md      written by Memory Curator

user-identity/
  profile.md              explicit operator preferences

team-memory/
  playbooks.md            shared playbook and policies

project/
  project-soul-memory.md  current project state

agent-repo/
  docs/repo-decisions.md  public-safe agent decisions

session/
  scratch.md              temporary context
```

The exact file layout can vary. The scope boundary should not.
