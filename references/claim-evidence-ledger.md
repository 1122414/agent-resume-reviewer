# Claim-Evidence Ledger

Use the ledger as the single source of truth for scoring, architecture reconstruction, JD mapping, rewrites, and interview risks.

## Lifecycle

Advance the review through these states:

1. ingested
2. ledger-built
3. evidence-located
4. architecture-reconstructed
5. scored
6. rewritten
7. completed

Skip stages that the selected mode does not need. When an upstream claim changes, invalidate dependent stages rather than preserving stale scores or rewrites.

## Data contract

Use [claim-evidence-ledger.schema.json](../schemas/claim-evidence-ledger.schema.json) when materializing the ledger. Keep it in working state unless the user requests a reusable JSON artifact.

When a ledger file is created, validate it with:

~~~text
python scripts/validate_ledger.py path/to/ledger.json
~~~

## Claim granularity

Create one claim for one testable assertion. Split a bullet when ownership, mechanism, metric, or outcome have different support.

For every claim record:

- Exact resume location and original text
- Claim category and project
- Ownership verb and boundary
- Problem, mechanism, constraint, and metric when present
- Evidence references and their relationship to the claim
- Overall status, confidence, and interview risk
- Missing evidence, contradictions, and rewrite constraints

Use stable IDs such as project-1-bullet-2-claim-1. Never renumber unrelated claims during a follow-up.

## Statuses

- VERIFIED: Direct evidence supports the whole material claim.
- PARTIALLY_VERIFIED: Direct evidence supports only part of the claim.
- SUPPORTED: The resume is specific and internally consistent, but no independent artifact was verified.
- CLAIMED: The assertion lacks enough detail to reconstruct or test.
- UNVERIFIED: Evidence was searched in scope but not found or remained inaccessible. This does not mean false.
- CONTRADICTED: Inspected evidence or another claim materially conflicts with it.
- MISSING: Information required for the selected assessment is absent.

Do not collapse UNVERIFIED into CONTRADICTED.

## Confidence and risk

Treat confidence as confidence in the evidence-to-claim relationship, not confidence that the candidate is truthful.

- 0.90-1.00: Direct, specific, and strongly aligned evidence
- 0.70-0.89: Strong internal support or partial direct verification
- 0.40-0.69: Plausible but incomplete support
- 0.00-0.39: Weak, absent, inaccessible, or conflicting support

Prefer coarse values such as 0.95, 0.80, 0.60, 0.35, and 0.10. Avoid decorative precision.

Set risk from the consequence of failure:

- critical: A contradiction, misleading ownership, or indefensible centerpiece metric
- high: Likely to fail a normal technical follow-up
- medium: Important detail is missing but the core claim remains plausible
- low: Specific, bounded, and defensible

## Evidence relationships

Attach evidence through a relationship, not merely a source URL:

- SUPPORTS
- PARTIALLY_SUPPORTS
- CONTRADICTS
- CONTEXT_ONLY
- NOT_FOUND
- INACCESSIBLE

Record an observation explaining the relationship. A repository home page with no located implementation is not supporting evidence.

## Downstream invariants

- Derive every score explanation from claim IDs.
- Map JD requirements only to claim IDs, never to unsourced prose.
- Rewrite only facts present in the ledger.
- Keep unresolved placeholders tied to missing_evidence.
- Generate interview questions from risk, contradictions, and missing evidence.
- Keep reasonable architecture inference separate from resume and artifact evidence.
- Never upgrade a claim because the rewrite sounds more convincing.
