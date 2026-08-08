# Review Modes

Choose one primary mode from the user's intent. Do not ask the user to choose when the intent is clear. Use standard when no mode is implied.

| Mode | Use for | Default evidence depth | Output contract |
| --- | --- | --- | --- |
| quick | A fast first pass, excerpt, or time-limited review | Resume only | Score with confidence, concise verdict, top five issues, next action |
| standard | A normal complete review | Resume plus explicitly requested evidence | Scorecard, three lenses, P0/P1/P2 changes, selected rewrites |
| deep | A strict technical audit | Inspect decision-changing evidence when available | Ledger summary, architecture, buzzwords, scores, risks, rewrites |
| jd-tailored | A specific job application | Verify must-have claims when links exist | Requirement mapping, gaps, project selection, targeted rewrites |
| evidence-verify | Authenticity or implementation verification | Inspect all in-scope, decision-changing sources | Claim verdicts, exact evidence anchors, contradictions, limitations |
| interview-defense | Interview preparation from a resume | Reuse existing evidence; inspect new sources only when requested | Risk-ranked defense cards and follow-up questions |

## Route efficiently

- Select quick for requests such as “quick look,” “top issues,” or a short excerpt without a request for depth.
- Select standard for a complete review with no stronger routing signal.
- Select deep for “strict,” “technical deep dive,” architecture reconstruction, buzzword audit, or full credibility review.
- Select jd-tailored when the job description drives the decision.
- Select evidence-verify when the user asks whether claims can be proven from GitHub, a paper, a demo, or documentation.
- Select interview-defense when the user asks to prepare explanations, likely questions, or defenses for listed claims.
- For mixed requests, choose the dominant mode and add only the required modules. Example: use jd-tailored plus evidence location, not two full reports.

## Bound the work

Keep attention on decision-changing claims:

- quick: at most five findings and three claims
- standard: at most ten findings and eight claims
- deep: all material claims, but omit cosmetic observations that do not change the assessment
- jd-tailored: all must-haves plus the highest-value preferred requirements
- evidence-verify: all claims explicitly selected by the user; otherwise the five highest-risk claims
- interview-defense: three to seven defense cards, ordered by risk

Do not emit the full internal ledger in quick or standard mode. Summarize it. Emit the ledger only when the user requests the artifact or evidence-verify mode benefits from a structured appendix.

## Mode-specific omissions

- Do not run a full buzzword table in quick mode.
- Do not calculate JD Match without a job description.
- Do not browse repositories in quick mode unless verification is explicitly requested.
- Do not rewrite the full resume in evidence-verify mode unless requested.
- Do not create polished interview answers when the supporting facts are missing; create a fact-gathering prompt instead.

## Continue statefully

When the user supplies missing facts, a revised resume, or a new job description:

1. Reuse the existing ledger.
2. Update affected claims and invalidate stale derived scores.
3. Preserve source anchors that still apply.
4. Re-run only the affected modules.
5. State what changed from the previous assessment.
