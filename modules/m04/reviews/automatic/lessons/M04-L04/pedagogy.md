# M04-L04 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion assessment and evidence at draft handoff `86f72bb` for middle and senior engineers. The scope is the [approved M04-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l04), the assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer denormalization section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L923-L941), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H097, denormalization | taught | **Keep the ledger authoritative** compares an on-demand join with a stored summary and identifies the authoritative refund decision. Q1 and EX-1 apply that distinction. |
| PR-H098, denormalization disadvantages | taught | **Trace the failed second write**, **Measure freshness and rebuild**, and **Decide whether to duplicate** explain stale state, propagation, write cost and repair. Q2–Q6 and EX-1 apply those trade-offs. |

## Pedagogy and assessment

The lesson motivates duplication with an order dashboard and explicitly traces a refund that commits while the second summary write fails. It then teaches atomic outbox creation, complete versioned snapshots, duplicate and reversed delivery, guarded application and durable checkpointing. The rebuild sequence aligns a source snapshot with its change position and explains catch-up and cutover. The decision section compares live joins, synchronous summaries and asynchronous views by authority, freshness and cost.

EX-1 applies those ideas to a merchant refund portal. The measured population is all 200 relevant original commits in a ten-minute drill, each observed for five seconds after commit. The sample solution correctly calculates 194/200 as 97% against the 99% target and includes all six misses. It preserves refund eligibility at the ledger and assesses the relay failure, duplicate and reversed snapshots, and rebuild. LO1 is taught in the first three sections and assessed by Q1–Q3 and EX-1. LO2 is taught across all four sections and assessed by Q4–Q6 and EX-1. The companion includes six explained checks and a point-bearing rubric, with equivalent solutions accepted.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the changed lesson and companion at `730b79e`. **Trace the failed second write** now demonstrates why a contributing-facts read must follow the customer serialization lock, then distinguishes durable broker acknowledgement from the projector's apply or skip and contiguous checkpoint. **Measure freshness and rebuild** traces a new snapshot through cursor 120, an old out-of-order application at 130, a cutover boundary at 140 and restart at 141. It also scopes the example to a single comparable cursor.

The revised EX-1 and its solution and rubric assess the concurrent mutation and both acknowledgements, as well as the new generation's cutover and restart. The original 200-commit cohort, five-second observation window and 194/200 result remain unchanged. The [approved M04-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l04) includes propagation, stale views and repair. Both outcome maps remain supported by the teaching and assessment.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
