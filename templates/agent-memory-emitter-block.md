# Memory Event Emission Block

Add this block to worker agents that participate in curated memory.

````text
## Memory Event Emission

After substantial work, emit zero or more Memory Events for the Memory Curator.

Rules:
- Do not write durable memory directly unless explicitly authorized.
- Emit no event when nothing durable was learned.
- Do not include secrets, credentials, private keys, raw logs, raw transcripts,
  or sensitive customer data.
- Separate facts, decisions, preferences, risks, procedures, hypotheses,
  evidence, deprecations, and conflicts.
- Attach evidence references whenever possible.
- Suggest a scope, but let the Memory Curator decide the final destination.
- Use `user_identity`, `team_memory`, `project`, `agent_repo`, `session`, or
  `discard`. `agent_team` is accepted only as a legacy alias for `team_memory`.
- Use `session` or `discard` for temporary, low-confidence, duplicate, or
  unsupported observations.

Return format:

## Memory Events

```json
[]
```
````
