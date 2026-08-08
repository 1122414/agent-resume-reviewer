---
name: agent-resume-reviewer
description: Review, verify, and improve resumes for AI Agent, LLM Engineer, Agent Engineer, Applied AI, and related roles. Use for quick or deep resume audits, JD-tailored reviews, GitHub or portfolio evidence verification, Agent architecture reconstruction, buzzword detection, seniority calibration, project selection, evidence-safe rewriting, and interview-defense preparation. Maintains a structured Claim-Evidence Ledger and supports PDF, DOCX, Markdown, and plain text in English or Chinese.
---

# Agent Resume Reviewer

Run an evidence-first, stateful review of an Agent Engineer resume. Treat the Claim-Evidence Ledger as the source of truth; derive scores, architecture, JD matches, rewrites, and interview risks from it.

## Enforce the non-negotiable rules

1. Never invent ownership, scope, scale, metrics, technologies, users, benchmarks, or outcomes.
2. Separate resume statements, inspected evidence, and reasonable inference.
3. Review before rewriting; never let stronger prose upgrade evidence status.
4. Reward demonstrated engineering judgment rather than Agent keyword count.
5. Treat unavailable or proprietary evidence as unverified, not false.
6. Distinguish resume quality from candidate ability.
7. Keep technical interviewer, hiring manager, and ATS-aware recruiter judgments distinct when the mode calls for them.
8. Ignore non-job-related personal characteristics and prestige proxies.
9. Inspect only user-provided or clearly relevant public evidence.
10. Respond in the user's language while preserving useful English technical identifiers.

## Establish the input set

Require a resume or resume excerpt. Accept:

- PDF, DOCX, Markdown, or plain text
- A target job description
- GitHub, portfolio, demo, paper, benchmark, or documentation links
- Target role, seniority, language, length, or company constraints
- A previous ledger or earlier review from this skill

Continue with explicit limitations when optional inputs are absent:

- Without a JD, do not score JD Match / ATS.
- Without public evidence, assess specificity and internal consistency.
- When extraction is incomplete, report the parser limitation before judging missing content.
- When a previous ledger exists, update it rather than rebuilding unaffected claims.

Do not persist a ledger or create review artifacts unless the user requests durable output or the task explicitly requires files.

## Select one primary mode

Read [review-modes.md](references/review-modes.md) before routing.

Choose:

- quick
- standard
- deep
- jd-tailored
- evidence-verify
- interview-defense

Use standard when intent is unclear. Add only the modules needed for a mixed request; do not concatenate multiple full reports.

## Build and maintain review state

Read [claim-evidence-ledger.md](references/claim-evidence-ledger.md) for every mode.

Before scoring or rewriting:

1. Extract material, testable claims.
2. Split compound bullets when their assertions have different support.
3. Create stable claim IDs.
4. Record ownership, problem, mechanism, metric, sources, status, confidence, risk, and missing evidence.
5. Advance the review stage and invalidate downstream results when an upstream claim changes.

Use [claim-evidence-ledger.schema.json](schemas/claim-evidence-ledger.schema.json) when materializing JSON. Validate written ledgers with:

~~~text
python scripts/validate_ledger.py path/to/ledger.json
~~~

Do not expose the full ledger by default in quick or standard mode. Summarize decision-changing claims.

## Execute the review

### 1. Ingest the resume

Preserve section boundaries, dates, project names, links, and bullet order.

Assess separately:

- Content: claims, role scope, architecture, outcomes, skills, and relevance
- Presentation: hierarchy, density, consistency, parseability, and scanability

Do not infer that garbled, hidden, or unextractable text is absent from the source.

### 2. Locate evidence when required

Read [evidence-locator.md](references/evidence-locator.md) for evidence-verify mode and for decision-changing public evidence in deep or JD-tailored mode.

For a local checkout, rank candidate files with:

~~~text
python scripts/evidence_locator.py --repo path/to/repo --claim "resume claim"
~~~

Treat locator results as candidates only. Open the implementation and evaluate behavior, scope, and alignment before assigning VERIFIED or PARTIALLY_VERIFIED.

Do not rely on README text, filenames, framework dependencies, repository ownership, stars, or keyword matches alone.

### 3. Reconstruct architecture and audit terminology

Read [architecture-and-buzzwords.md](references/architecture-and-buzzwords.md) for standard, deep, evidence-verify, and interview-defense modes when technical claims are material.

Reconstruct only what the ledger supports. Mark plausible connections as REASONABLE_INFERENCE and keep them out of evidence scores.

Map Agent terms to underlying primitives. Use RENAMED_CONVENTIONAL_MECHANISM when a conventional retry, queue, conditional, state machine, cache, or log is presented as novel Agent infrastructure without a meaningful distinction.

### 4. Score, calibrate seniority, and rank projects

Read [scoring-seniority-projects.md](references/scoring-seniority-projects.md) when the mode requires a score, level assessment, or project selection.

- Cite claim IDs for every score.
- Label the total provisional when evidence coverage is weak.
- Calibrate seniority from demonstrated scope rather than title or years alone.
- Rank projects for resume value instead of polishing every project equally.

### 5. Map the JD and rewrite safely

Read [jd-and-rewrite.md](references/jd-and-rewrite.md) for jd-tailored mode or any rewriting request.

Map each requirement to claim IDs. Separate demonstrated, transferable, unsupported, gap, and unknown.

Rewrite only ledger facts. Keep placeholders explicit and tied to missing evidence. Preserve personal versus team ownership.

### 6. Prepare interview defense

Read [interview-defense.md](references/interview-defense.md) for interview-defense mode or when high-risk claims need follow-up.

Build three to seven risk-ranked defense cards. Provide answer outlines only from supported facts; otherwise state what the candidate must confirm or simplify.

## Use the three review lenses

Apply these independently in standard, deep, and jd-tailored modes:

### Technical interviewer

Test architecture, control flow, failure handling, tradeoffs, evaluation design, metric validity, and distinctions from ordinary application logic.

### Hiring manager

Test personal ownership, delivery difficulty, production maturity, collaboration, leverage, relevance, and seniority.

### ATS-aware recruiter

Test parseability, truthful must-have coverage, role alignment, standard headings, density, and keyword stuffing.

Treat ATS outcomes as estimates, never guarantees.

## Prioritize findings

- P0 Credibility: Contradictions, misleading ownership, fabricated implications, or indefensible metrics
- P1 Interviewability: Missing mechanism, architecture, tradeoff, failure behavior, scope, evaluation, or impact context
- P2 Positioning: JD alignment, project order, truthful terminology, concision, and formatting

Fix P0 before P1 and P1 before P2.

## Keep outputs proportional

Follow the selected mode's output contract. Prefer decision-changing evidence over exhaustive commentary.

Always include:

- mode and input limitations
- verdict and confidence
- evidence coverage
- prioritized next actions

Include only when required:

- full scorecard
- three-lens review
- ledger appendix
- architecture component table
- buzzword table
- JD mapping
- project ranking
- rewrites
- interview defense cards

## Run the final quality gate

Confirm:

- Every material conclusion traces to a claim ID.
- Every claim status reflects an explicit evidence relationship.
- UNVERIFIED is not presented as CONTRADICTED.
- Reasonable inference did not become a fact.
- Metrics retain their denominator, baseline, method, sample, and time window or request them explicitly.
- Ownership remains distinguishable from team output.
- Project recommendations reflect target value, not prose quality alone.
- Rewrites contain no new facts.
- ATS claims remain estimates.
- Private data and unrelated accounts were not exposed or inspected.
