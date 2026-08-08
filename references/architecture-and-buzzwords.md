# Architecture Reconstruction and Buzzword Audit

Reconstruct each material Agent project from ledger claims and evidence. Do not fill gaps with a plausible generic architecture.

## Reconstruction model

Evaluate applicable components:

| Component | Questions |
| --- | --- |
| Goal and agent boundary | What requires model-driven decisions rather than fixed application logic? |
| Planner / proposal | What is produced, in what schema, and under what constraints? |
| Executor / tools | How are actions validated, authorized, made idempotent, and executed? |
| Environment / observation | What state is observed and how are stale or conflicting observations handled? |
| State / memory / context | What is persisted, retrieved, summarized, or discarded? |
| Verifier | What is checked, by which mechanism, and what happens on failure? |
| Retry / replan / recovery | What triggers recovery and how are loops or duplicate side effects prevented? |
| Safety / permissions | Where are deterministic boundaries and policy checks enforced? |
| Evaluation / tracing | What tasks, labels, baselines, traces, and release gates exist? |
| Deployment | What latency, cost, throughput, reliability, and observability constraints apply? |

For each component, assign:

- VERIFIED: Direct artifact evidence
- PARTIALLY_VERIFIED: Direct evidence for only part of the behavior
- SUPPORTED: Explicit and specific resume evidence
- CLAIMED: Named without reconstructable behavior
- REASONABLE_INFERENCE: Plausible connection needed to form a hypothesis
- MISSING: Not available

Never use REASONABLE_INFERENCE to raise evidence status or score. Display it as a question to confirm.

## Audit underlying primitives

Translate high-signal terminology into the concrete primitive it may represent:

| Agent term | Underlying primitive to identify |
| --- | --- |
| Agent Memory | KV/DB state, vector store, history buffer, retrieval policy |
| Checkpoint | State snapshot, event persistence, resume token, durable workflow |
| Replan | Planner re-entry, ordinary retry, new task graph, strategy change |
| Reflection | LLM critique, verifier, rule check, self-evaluation prompt |
| Orchestrator | Router, state machine, scheduler, workflow engine |
| Agent Trace | Log, span, event stream, trajectory, replayable run record |
| Deterministic Executor | Schema validation, policy gate, action dispatcher, idempotent worker |

## Assign a verdict

- KEEP: Accurate, specific, and information-dense
- SIMPLIFY: Real mechanism described with unnecessary abstraction
- MERGE: Duplicates another concept or bullet
- REMOVE: Adds no defensible information
- EXPAND: Strong potential but missing mechanism, scope, or evidence
- RENAMED_CONVENTIONAL_MECHANISM: A conventional retry, queue, conditional, state machine, cache, or log is presented as a novel agent subsystem without a meaningful distinction

Do not use RENAMED_CONVENTIONAL_MECHANISM merely because a standard primitive is present. Apply it only when the resume implies novelty or autonomy that the mechanism does not support.

## Test each term

1. Map it to a module, boundary, policy, data structure, or behavior.
2. Name the engineering problem it solves.
3. Explain inputs, outputs, and runtime behavior.
4. Distinguish it from the conventional primitive.
5. Locate a failure case, test, trace, or benchmark.
6. Decide whether the term earns space on the resume.

Output a component table and a buzzword table only when the selected mode requires them.
