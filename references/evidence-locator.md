# Evidence Locator

Use this module for evidence-verify mode and whenever public evidence can materially change a deep or JD-tailored review.

## Scope first

- Inspect only user-provided or clearly relevant public repositories, demos, papers, benchmarks, and documentation.
- Do not inspect unrelated personal accounts.
- Record inaccessible or private evidence as INACCESSIBLE, not false.
- Pin observations to a commit SHA, release, document version, or access date when possible.

## Locate implementation evidence

For a GitHub repository:

1. Confirm that the repository belongs to the claimed project.
2. Record the default branch and current commit SHA.
3. Scan the tree before reading the README conclusion.
4. Search likely source, test, benchmark, and documentation paths.
5. Translate the resume claim into expected behaviors and underlying primitives.
6. Search symbols, code paths, tests, docs, configs, traces, and relevant commit history.
7. Open the best candidates and trace actual control flow.
8. Triangulate implementation with tests, docs, traces, or benchmarks when the claim includes behavior or metrics.
9. Add exact source anchors and relationships to the ledger.

Prioritize paths such as src, agent, planner, executor, orchestrator, runtime, memory, eval, tests, benchmarks, and docs, but do not assume projects use these names.

## Search semantically

Search behavior families rather than only literal resume terms:

| Resume concept | Candidate primitives |
| --- | --- |
| Replan | planner re-entry, validation failure recovery, new plan generation, retry with changed strategy |
| Checkpoint | persisted state, snapshot, event log, resume token, durable workflow state |
| Memory | history buffer, database, KV state, vector store, retrieval context |
| Verifier | validator, policy check, rule engine, critic, assertion, evidence check |
| Orchestrator | router, state machine, workflow engine, scheduler, dispatcher |
| Trace / Replay | spans, events, audit log, trajectory, run record, deterministic replay |

For a local checkout, use the candidate locator:

~~~text
python scripts/evidence_locator.py --repo path/to/repo --claim "failure-triggered replan"
~~~

The script ranks candidate files only. Never convert its score directly into VERIFIED.

## Grade evidence

| Level | Evidence | Use |
| --- | --- | --- |
| L4 | Implementation plus aligned test, trace, or benchmark | Strong verification of behavior |
| L3 | Implementation or configuration clearly showing the mechanism | Verification of mechanism |
| L2 | Design doc, issue, README, or example without implementation confirmation | Context or partial support |
| L1 | Matching name, directory, dependency, or generic framework use | Locator hint only |
| L0 | Nothing found, inaccessible, or irrelevant | No support |

Require L3 or L4 for VERIFIED. Use PARTIALLY_VERIFIED when only a narrower mechanism is shown. A dependency such as LangChain does not prove planner, memory, multi-agent, or evaluation behavior.

## Check ownership carefully

Inspect commits or blame only when ownership or timing is decision-changing. Do not assume:

- Commit author identity equals the candidate without an explicit link
- Repository ownership proves authorship of every subsystem
- A current implementation existed during the resume's claimed time window
- Stars, forks, or followers prove technical depth

## Report failures honestly

Record:

- searched scope
- revision
- candidate files opened
- evidence found
- evidence not found
- access or tooling limitations

Use UNVERIFIED when a reasonable in-scope search finds no proof. Use CONTRADICTED only for an actual conflict.
