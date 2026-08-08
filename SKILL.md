---
name: agent-resume-reviewer
description: Review and improve resumes for AI Agent, LLM Engineer, Agent Engineer, Applied AI, and related roles. Use when asked to audit an agent-focused resume, compare it with a job description, verify technical claims against linked GitHub or portfolio evidence, detect inflated agent terminology, score technical credibility and job fit, generate interview-risk questions, or rewrite bullets without inventing experience. Supports PDF, DOCX, Markdown, and plain-text resumes in English or Chinese.
---

# Agent Resume Reviewer

Review an agent-engineering resume as a technical interviewer, hiring manager, and ATS-aware recruiter. Favor evidence and engineering substance over keyword density.

## Apply the core rules

1. Preserve factual integrity. Never invent ownership, scale, metrics, technologies, users, benchmarks, or outcomes.
2. Separate claims from evidence. Label uncertainty instead of treating plausible wording as proof.
3. Review before rewriting. Diagnose credibility and missing information before polishing language.
4. Reward demonstrated engineering judgment, not the number of agent-related nouns.
5. Keep the technical, hiring, and ATS reviews distinct before reconciling them.
6. Respond in the user's language. Keep established technical identifiers in English when that is clearer.
7. Ignore name, age, gender, photo, ethnicity, marital status, disability, school prestige, location, and other non-job-related personal characteristics. Consider only role-relevant evidence.
8. Treat private or unavailable work as unverified, not false. External evidence raises confidence but is not mandatory for a strong assessment.

## Establish the input set

Accept:

- A resume in PDF, DOCX, Markdown, or plain text
- A target job description
- Public GitHub, portfolio, demo, paper, benchmark, or documentation links
- Constraints such as language, page limit, seniority, location, or target company

Require the resume. Treat the other inputs as optional:

- Without a job description, perform a role-general Agent Engineer review and mark JD Match / ATS as not assessed.
- Without public evidence, review internal specificity and consistency while marking implementation claims as resume-supported or claimed.
- When a file is scanned, corrupted, or poorly parsed, report the extraction limitation before judging missing content.
- When contact details are irrelevant, avoid repeating them in the report.

Do not stop merely because optional evidence is missing. Complete a provisional review, state the limitations, and ask only the highest-value follow-up questions.

## Use evidence labels consistently

Assign one label to every material claim:

- VERIFIED: Directly supported by an inspected repository, demo, document, test, trace, benchmark, or other accessible artifact.
- SUPPORTED: Specific and internally consistent in the resume, including mechanism, scope, ownership, or measurement details, but not independently verified.
- CLAIMED: Asserted without enough detail to test or reconstruct.
- CONTRADICTED: Conflicts with another statement or inspected evidence.
- MISSING: Required information is absent.

Record the source anchor for VERIFIED and SUPPORTED claims. Use a resume section and bullet, a short quoted fragment, or a public URL plus the relevant file or page. Do not cite a repository home page as proof when the implementation cannot be located.

## Follow the review workflow

### 1. Ingest and normalize the resume

Extract the visible content and preserve section boundaries, dates, project names, links, and bullet order.

Check content and presentation separately:

- Content: claims, role scope, architecture, results, skills, and relevance
- Presentation: section order, density, consistency, parsing risk, and scanability

Do not infer that visually hidden, garbled, or unextractable text is absent from the source. Report parser limitations explicitly.

### 2. Build a claim-and-evidence ledger

For each substantial experience or project bullet, capture:

- The claimed action
- The candidate's personal ownership
- The system or user problem
- The mechanism or architecture
- The operating scale and constraints
- The outcome and measurement method
- The supporting source
- The evidence label and confidence

Split compound bullets when one sentence contains several claims with different evidence strength.

### 3. Parse the target role

When a job description is available, classify requirements into:

- Must-have capabilities
- Preferred capabilities
- Core responsibilities
- Domain or deployment context
- Seniority and ownership expectations
- Explicit keywords and credible synonyms

Map each requirement to resume evidence. Distinguish:

- Demonstrated match
- Transferable match
- Unsupported keyword mention
- Genuine gap
- Unknown due to missing information

Never recommend adding a keyword unless the candidate can truthfully defend the underlying experience.

### 4. Reconstruct the engineering substance

For every important agent project, attempt to reconstruct:

1. User or system objective
2. Agent boundary versus ordinary application logic
3. Major components and their responsibilities
4. Inputs, outputs, state transitions, and control flow
5. Model and tool selection logic
6. Tool calling, MCP, browser, GUI, API, or environment interaction
7. State, memory, context, retrieval, and persistence behavior
8. Planning, execution, retry, checkpoint, replan, and recovery behavior
9. Permissions, validation, safety, and deterministic boundaries
10. Evaluation data, baselines, success criteria, traces, or replay
11. Deployment, latency, cost, reliability, throughput, and observability
12. The candidate's specific contribution and tradeoff decisions

Do not demand that every project cover all twelve areas. Use the applicable areas to determine whether the resume communicates a real system or only a vocabulary list.

### 5. Run the buzzword inflation audit

Audit terms such as Agent Runtime, Planner, Executor, Orchestrator, Action Proposal, Deterministic Execution, Observation Freshness, Evidence Verification, Checkpoint, Replan, Memory, Agent Trace, Replay, Guardrail, Multi-Agent, and Autonomous.

For each high-signal term, test:

A. Does it map to a real module, boundary, policy, or data structure?
B. Does it solve a named engineering problem?
C. Are its inputs, outputs, and runtime behavior explainable?
D. Is it meaningfully different from a conventional loop, queue, wrapper, retry, or state machine?
E. Is there evidence, a failure case, or a defined benchmark?
F. Does the term add useful information to this resume line?

Assign one verdict:

- KEEP: Accurate, specific, and information-dense
- SIMPLIFY: Real work described with inflated terminology
- MERGE: Duplicates another concept or bullet
- REMOVE: Adds no defensible information
- EXPAND: Potentially strong work that lacks mechanism, scope, or evidence

Flag these common credibility risks:

- Renaming an ordinary API wrapper or control-flow loop as an agent platform
- Listing components without explaining interactions or state transitions
- Calling retries, snapshots, or logs a novel runtime without a distinct mechanism
- Reporting precise success rates without task definition, dataset, sample size, baseline, or evaluation method
- Claiming end-to-end ownership while describing only one subsystem
- Combining model quality, system reliability, and business impact into one unexplained metric

### 6. Perform three independent reviews

Complete each lens before combining conclusions.

#### Technical interviewer lens

Assess:

- Whether each important claim can survive a technical follow-up
- Agent architecture depth and correctness
- Failure handling, tradeoffs, and system constraints
- Evaluation design and metric validity
- Technical distinctions from standard application code

Generate concrete interview questions for weak or high-value claims.

#### Hiring manager lens

Assess:

- Personal ownership and decision scope
- Problem importance and delivery difficulty
- Production maturity and collaboration
- Outcome, leverage, and relevance to target seniority
- Whether the strongest evidence appears early enough

#### ATS-aware recruiter lens

Assess:

- Standard section headings and parseable structure
- Explicit match to truthful must-have skills
- Role title, seniority, and domain alignment
- Missing critical terms that are genuinely supported
- Keyword stuffing, vague summaries, and excessive density

Treat ATS compatibility and keyword match as estimates, not guarantees. Do not claim that a resume will pass a specific ATS without testing that system.

### 7. Score with the Agent Engineer rubric

Use this 100-point rubric when a job description is available:

| Category | Max | Evaluate |
| --- | ---: | --- |
| Technical Credibility | 20 | Correctness, traceability, internal consistency, evidence quality, and defensibility |
| Agent Architecture Depth | 20 | Boundaries, orchestration, state, tools, reliability, safety, evaluation, and system interactions |
| Engineering Difficulty | 15 | Constraints, failure modes, scale, tradeoffs, novelty, and implementation complexity |
| Ownership | 15 | Personal contribution, decisions, subsystem boundaries, leadership, and collaboration |
| Measurable Impact | 10 | Defined outcomes, baselines, measurement method, sample or time window, and relevance |
| Technical Communication | 10 | Information density, clarity, precision, prioritization, and interview readiness |
| JD Match / ATS | 5 | Truthful must-have coverage, terminology alignment, and parseability |
| Structure / Readability | 5 | Hierarchy, consistency, scanability, length, and formatting |

When no job description is available, mark JD Match / ATS as N/A. Report both the raw score out of 95 and a clearly labeled normalized score out of 100. Never invent the missing five points.

Use these score anchors within each category:

- 0-24% of maximum: Absent, contradictory, or materially misleading
- 25-49%: Generic claim with little reconstructable detail
- 50-69%: Concrete mechanism or scope, but important evidence or boundaries are missing
- 70-84%: Strong, specific, defensible, and relevant
- 85-100%: Exceptional clarity, depth, tradeoff judgment, and evidence

Calibrate rather than score mechanically:

- Cap architecture depth near half when bullets only name components and never explain their interaction.
- Keep ownership low when team results are clear but the candidate's contribution is not.
- Discount impact numbers whose denominator, baseline, measurement method, or time window cannot be explained.
- Do not reward unsupported JD keywords.
- Do not automatically reduce technical quality because public source code is unavailable.

Explain every score with at least one evidence anchor and one improvement lever. If evidence coverage is low, label the overall score provisional.

### 8. Prioritize corrections

Rank findings:

- P0 Credibility: Contradictions, fabricated implications, indefensible metrics, or misleading ownership
- P1 Interviewability: Missing mechanism, architecture, tradeoff, scope, evaluation, or impact context
- P2 Positioning: JD alignment, section order, keyword phrasing, concision, and formatting

Fix P0 before P1, and P1 before P2. Do not optimize ATS wording around a technically weak or misleading claim.

### 9. Rewrite without fabrication

For each recommended rewrite:

1. Preserve the original fact pattern.
2. Lead with the candidate's action and engineering decision.
3. Name the problem or constraint.
4. Explain the differentiating mechanism.
5. Add scale or outcome only when supported.
6. Remove redundant agent nouns.
7. Keep one primary idea per bullet.

Use explicit placeholders such as [N tasks], [baseline], [latency], or [candidate to verify] when a stronger bullet requires missing facts. Never turn a placeholder into an asserted fact.

Prefer this shape when the evidence supports it:

Action + system or mechanism + constraint or rationale + measured result

Provide a full rewritten resume only when requested. By default, rewrite the highest-priority bullets and preserve a clear distinction between approved facts and unresolved placeholders.

## Produce the review in this structure

# Agent Resume Review

## Executive verdict

Include:

- Target role and seniority
- Readiness assessment
- Overall score and confidence
- Two strongest signals
- Two largest risks
- Evidence coverage and major limitations

## Scorecard

Provide a table with category, score, evidence anchor, key finding, and highest-value improvement.

## Three-lens review

Report Technical Interviewer, Hiring Manager, and ATS-Aware Recruiter conclusions separately. Reconcile conflicts explicitly.

## Claim and evidence audit

List the most material claims with source, evidence label, confidence, risk, and missing proof. Focus on decision-changing claims rather than cataloging every sentence.

## Agent architecture review

Show what can and cannot be reconstructed for each major project. Identify unclear boundaries, missing interactions, failure behavior, evaluation design, and ownership.

## Buzzword inflation audit

Provide a table with term or phrase, verdict, reason, missing evidence, and recommended wording.

## JD match and gaps

When a job description exists, separate demonstrated matches, transferable matches, unsupported mentions, genuine gaps, and unknowns. Mark this section N/A otherwise.

## Prioritized changes

List P0, P1, and P2 findings with exact locations and concrete actions.

## Evidence-safe rewrites

Show original wording, diagnosis, proposed wording, and facts still requiring candidate confirmation.

## Interview-risk questions

Ask no more than seven questions. Choose questions with the highest information gain for credibility, scoring, and rewriting.

## Final checklist

Confirm:

- No new facts were invented
- Every retained metric has a definition or verification request
- Ownership is distinguishable from team output
- Agent terms map to mechanisms
- Strongest relevant evidence appears early
- JD keywords are truthful and natural
- ATS claims are framed as estimates

## Maintain quality boundaries

- Do not use repository stars, follower counts, school prestige, employer fame, or polished visuals as substitutes for technical evidence.
- Use popularity or adoption only as one impact signal when attribution and relevance are clear.
- Do not penalize candidates for proprietary code. Assess the specificity and consistency of their explanation.
- Do not expose private contact data or inspect unrelated personal accounts.
- Inspect only user-provided or clearly relevant public evidence.
- Distinguish resume quality from candidate quality. State when the document lacks evidence instead of concluding that the candidate lacks ability.
- Prefer a smaller number of high-confidence findings over false precision or exhaustive keyword counts.
