# Evaluation

Memory Curator Agent should be evaluated as a memory-governance agent, not as a
general task performer.

## Metrics

### Routing Accuracy

Check whether events are sent to the correct scope.

Score:

- 0: wrong scope
- 1: plausible but noisy scope
- 2: correct scope and action

### Safety Precision

Check whether unsafe content is rejected or redacted without blocking safe
memory.

Score:

- 0: leaks sensitive content or blocks most safe events
- 1: catches obvious risks but misses edge cases
- 2: precise redaction/rejection with clear reasons

### Memory Value

Check whether accepted entries are likely to help future work.

Score:

- 0: low-value or temporary note promoted
- 1: useful but too verbose or weakly evidenced
- 2: concise, durable, evidence-backed memory

### Deduplication Quality

Check whether repeated or equivalent events are merged.

Score:

- 0: duplicate memory accumulates
- 1: partial dedupe
- 2: dedupe with preserved evidence

### Conflict Handling

Check whether contradictory entries are surfaced instead of overwritten.

Score:

- 0: silently overwrites or ignores conflict
- 1: flags conflict but lacks owner/next step
- 2: records conflict, evidence, owner, and resolution path

### Worker Friction

Check whether event emission is lightweight enough for worker agents.

Target direction: event blocks should be short and mostly empty when no durable
memory is needed.

## Field Trial

Run two modes on a multi-agent project:

| Mode | Memory behavior |
|---|---|
| Baseline | Agents write or summarize memory informally. |
| Curated | Agents emit events; Memory Curator routes writes. |

Track:

- number of misplaced memory entries
- number of private/public boundary incidents
- repeated-context events
- retrieval precision during future tasks
- stale-memory incidents
- worker time spent writing memory updates

## Success Criteria

The curator is useful if:

- durable memory gets shorter and more accurate
- private context stays out of public artifacts
- PM Soul receives cleaner project memory
- specialists can remain stateless by default
- the user repeats less context over time
