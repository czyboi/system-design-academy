# M04-L01 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion assessment and evidence at draft handoff commit `018f0bf` for middle and senior engineers. The approved scope is [M04-L01 in the SDA-v1 curriculum](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l01), its assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer database section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L808-L827), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Findings

| ID | Severity | Status | Location and learner impact | Suggested correction |
| --- | --- | --- | --- | --- |
| M04-L01-P1 | major | open | [Lesson, Put large attachments on their own path](../../../../lessons/M04-L01.md#put-large-attachments-on-their-own-path) says an upload attempt must be retired and unable to publish before cleanup, but does not show how that condition is established or checked atomically with the guarded publish. [EX-1 and its rubric](../../../../assessments/M04-L01.md#practical-exercise) ask learners to explain safe retirement after a crash and award points for it. A learner lacks a reproducible sequence for a late worker racing cleanup and cannot derive the expected answer from the lesson. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l01) requires choosing object/blob references using failure criteria. | Teach one concrete attempt state or ownership-token protocol in which retirement revokes publication authority before cleanup, and trace a delayed worker attempting to publish after retirement. Reflect the sequence and acceptable alternatives in EX-1's sample solution and rubric. |
| M04-L01-P2 | minor | open | [EX-1 sample solution](../../../../assessments/M04-L01.md#sample-solution-and-rubric) requires a trace of two requests when the first line insert fails, and its rubric scores the effect of rollback on the other attempt. The sample answer names rollback without tracing the waiting request's subsequent successful claim or its own failure. The lesson's **Walk a checkout race** section supplies the missing sequence. | Extend the sample answer to show that the first transaction rolls back, the waiting request can claim restored stock, and that request succeeds only if its own writes and commit succeed. |

## Coverage

| Assigned topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H083, database, README.md#L808 | taught | **Give each invariant an enforcement point** models orders, customers, lines and stock as persistent records with keys and access relationships. EX-1 asks for the corresponding reservation model. |
| PR-H084, RDBMS, README.md#L816 | taught | **Give each invariant an enforcement point** applies tables, keys, foreign keys and joins. **Shape reads around ownership** matches query patterns to a proposed index. Q1, Q4, Q5 and EX-1 assess these decisions. |
| PR-B003, ACID and relational integrity, README.md#L820 | taught | **Give each invariant an enforcement point** explains ACID and the non-null customer reference. **Walk a checkout race** traces the guarded stock update and rollback. Q1–Q3 and EX-1 assess the mechanisms. |

The outcome map connects LO1 to the constraint and stock-claim trace and LO2 to query, historical-value and attachment decisions. The separate companion includes six checks with explanations and an exercise with point-bearing criteria. The customer delete and last-unit scenarios demonstrate concrete invariants. Finding M04-L01-P1 limits the learner's ability to reproduce the assessed attachment failure path.

**Verdict: revise.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the changed lesson and assessment at `da9134c`. The revised attachment explanation teaches a token-guarded publish and retirement on the same database row, with distinct outcomes for publish-first and retire-first races. It also describes repeated cleanup when a delayed upload finishes after an earlier deletion. EX-1 now asks for the delayed-worker race, and its sample solution and rubric assess both orders and late cleanup. The accepted alternative-design clause remains available. The sample solution also traces the first claimant's rollback and the waiting claimant's subsequent attempt.

| Finding | Status | Evidence |
| --- | --- | --- |
| M04-L01-P1 | resolved | [Lesson, Put large attachments on their own path](../../../../lessons/M04-L01.md#put-large-attachments-on-their-own-path) and [assessment, Sample solution and rubric](../../../../assessments/M04-L01.md#sample-solution-and-rubric). The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l01) calls for the object/blob choice and its failure trade-offs. |
| M04-L01-P2 | resolved | [Lesson, Walk a checkout race](../../../../lessons/M04-L01.md#walk-a-checkout-race) and [assessment, Sample solution and rubric](../../../../assessments/M04-L01.md#sample-solution-and-rubric). The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l01) requires modelling transaction boundaries. |

LO1 remains mapped to the relational and checkout trace, and LO2 remains mapped to the access-path and attachment decisions. The revised exercise and rubric measure the new explanation, including the confirmed reservation remaining available while its slip is pending. The assigned topic dispositions remain supported by the same teaching sections. No new pedagogical or coverage finding arose in the changed sections.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and curriculum coverage re-review.
