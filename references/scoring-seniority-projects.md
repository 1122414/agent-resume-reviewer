# Scoring, Seniority, and Project Selection

Score resume evidence rather than presumed candidate ability.

## Agent Engineer score

| Category | Max |
| --- | ---: |
| Technical Credibility | 20 |
| Agent Architecture Depth | 20 |
| Engineering Difficulty | 15 |
| Ownership | 15 |
| Measurable Impact | 10 |
| Technical Communication | 10 |
| JD Match / ATS | 5 |
| Structure / Readability | 5 |

Without a job description, mark JD Match / ATS N/A. Report raw score out of 95 and a clearly labeled normalized score out of 100.

## Category anchors

- 0-24%: Absent, contradictory, or materially misleading
- 25-49%: Generic claim with little reconstructable detail
- 50-69%: Concrete mechanism or scope with important gaps
- 70-84%: Strong, specific, defensible, and relevant
- 85-100%: Exceptional depth, tradeoff judgment, and evidence

Calibrate:

- Keep architecture near half when claims list components without interactions.
- Keep ownership low when only team results are visible.
- Discount metrics without denominator, baseline, method, sample, or time window.
- Do not reward unsupported JD terms.
- Do not penalize proprietary code automatically.
- Cite claim IDs for every category and label low-evidence totals provisional.

## Seniority calibration

Use demonstrated scope, not years alone:

| Level | Evidence pattern |
| --- | --- |
| Junior | Implements bounded agent features; integrates models, prompts, retrieval, or tools with guidance |
| Mid | Independently designs workflows; handles state, failure, retry, tool contracts, and evaluation |
| Senior | Designs runtimes or production systems; owns reliability, cost, latency, observability, safety, and cross-module tradeoffs |
| Staff / Lead | Defines reusable platform architecture and cross-team strategy for runtime, evaluation, safety, or infrastructure |

Report:

- claimed or target level
- evidence-supported range
- claim IDs supporting the range
- capabilities required for the next level

Do not infer seniority from title, employer, school, or years alone.

## Project resume value

Score each serious project from 0 to 5 on:

- Technical depth: 25%
- Ownership: 20%
- Target relevance: 25%
- Evidence strength: 20%
- Differentiation: 10%

Calculate:

~~~text
value = 20 × (
  0.25 × depth +
  0.20 × ownership +
  0.25 × relevance +
  0.20 × evidence +
  0.10 × differentiation
)
~~~

Classify:

- 80-100: MUST_KEEP
- 65-79: KEEP
- 45-64: OPTIONAL
- 0-44: REMOVE

Explain any override, such as a required JD match, a unique early-career signal, or duplicate coverage. Do not let a polished description rescue a low-value project.
