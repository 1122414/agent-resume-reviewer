# Interview Defense

Build defense cards from high-risk or high-value ledger claims. Do not invent answers that make a weak claim appear defensible.

## Select claims

Prioritize:

1. Precise metrics
2. Broad ownership claims
3. Novel or inflated Agent terminology
4. Architecture centerpieces
5. Production, reliability, safety, or scale claims
6. Claims essential to the target JD

Generate three to seven cards, ordered by risk.

## Defense card

For each claim provide:

- Claim and source location
- Evidence status and risk
- Mechanism
- Why the design was needed
- Candidate ownership
- Key tradeoff
- Representative failure case
- Metric definition and baseline
- Evidence anchor
- Likely follow-up questions
- Facts the candidate must confirm
- 30-second answer outline
- 2-minute answer outline

An outline may contain only supported facts and explicit placeholders. If the claim cannot currently be defended, say so and recommend simplifying, removing, or gathering evidence.

## Challenge metrics

Ask as applicable:

- What is the task set and sample size?
- How is success defined?
- What is the baseline and comparison window?
- Who or what evaluated the result?
- What changed between variants?
- What are the main failure categories?
- Is uncertainty or confidence interval relevant?
- Can the result be reproduced from a benchmark, trace, or report?

## Challenge architecture

Ask for:

- One end-to-end control flow
- Component inputs and outputs
- State transitions and persistence
- Tool validation, permissions, and side effects
- Retry versus replan distinction
- Loop and failure safeguards
- Evaluation, tracing, cost, and latency tradeoffs

## Challenge ownership

Separate:

- personally designed
- personally implemented
- led or reviewed
- contributed to
- team or platform dependency

## Keep answers interview-safe

- Prefer a bounded, technically precise answer over a grand claim.
- State proprietary constraints without apologizing for them.
- Never suggest revealing confidential code, customer data, or internal metrics.
- Prepare an honest limitation statement when evidence cannot be shared.
