# M03-L01 technical and provenance review

Reviewed 2026-11-12 against draft handoff `e496b9a`. Scope covers the teaching lesson, companion assessment, and claim matrix for SDA-M03-L01.

## Technical findings

| ID | Severity | Status | Location | Evidence and suggested correction |
| --- | --- | --- | --- | --- |
| LAY-T2 | major | open | `modules/m03/assessments/M03-L01.md:18,74–76`, EX-1 answer and rubric | The answer puts the availability decision in the application module and the seat and reservation writes in one transaction. It leaves the availability check unguarded under concurrent requests. Two callers can both observe a free seat and then each commit a reservation if their writes do not recheck availability or enforce an equivalent constraint. Specify that the reservation owner conditionally claims each requested seat while it is available and rolls back the whole transaction if any claim fails. Record the reservation and pending receipt work in the same successful transaction, then acknowledge. Give rubric credit for the guarded claim or an equivalent concurrency-safe design. PostgreSQL 18 Read Committed illustrates the mechanism for an update to a predetermined seat row because its predicate is re-evaluated after a competing update commits. This example need not prescribe a database. [PostgreSQL 18, §13.2.1, Read Committed Isolation Level](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED) |

`modules/m03/lessons/M03-L01.md:25–35` distinguishes responsibilities from physical boundaries and scopes independent deployment and scaling to service ownership and compatible dependencies. The synchronous fan-out example explains how a required remote failure can affect the caller. Its saga uses local commits and application-specific compensation, with recovery for failed compensations. The answers to Q1–Q6 agree with those distinctions. [Microsoft Azure Architecture Center, N-tier architecture](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/n-tier) · [Microservices architecture, What are microservices? and Challenges](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/microservices#what-are-microservices) · [Saga pattern, Solution and Problems and considerations](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga#solution)

The archived receipt-admission finding `LAY-T1` is resolved in `modules/m03/lessons/M03-L01.md:41–42` and `modules/m03/assessments/M03-L01.md:74`. Both designs persist the pending job with the owner's business state before dispatch. That record survives a process restart under the stated durable-commit assumption and gives the dispatcher work to resume. The example makes no exactly-once delivery promise. [Microsoft Azure Architecture Center, Transactional Outbox, Solution](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos#solution)

## Provenance and rights

The claim matrix identifies Microsoft architecture guidance for the general layer, deployment and saga mechanisms. The catalogue and receipt scenarios are original Academy material. The evidence links the archived Academy draft, and the lesson credits Donne Martin, the pinned Primer revision, and CC BY 4.0 for topic selection. The artifacts contain no imported figures, assets or executable examples. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt) · [Archived Academy evidence](https://github.com/czyboi/system-design-academy/blob/ec753d7bcfd69ad68e5fff260aeb088059e42540/modules/m03/evidence/M03-L01.md)

## Verdict

`revise`. LAY-T2 requires a concurrency-safe reservation mechanism in the assessment answer and rubric.

## Round 1 targeted re-review

Reviewed correction handoff `fc8d61a` on 2026-11-12.

| ID | Status | Evidence |
| --- | --- | --- |
| LAY-T2 | resolved | https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED |

The lesson now distinguishes the availability observation from the guarded mutation and scopes the predicate recheck to PostgreSQL 18 Read Committed for a predetermined seat row. The companion asks learners to resolve concurrent requests for the same seat. Its answer guards each claim, rolls back every claim if one fails, and commits the claims, reservation, and pending receipt together before acknowledging success. The rubric accepts an equivalent concurrency-safe mechanism with all-or-nothing commit. The LO1 map now points to the section that teaches the guard, and the claim matrix carries the same version and isolation scope. [Lesson, Costs of a remote boundary](../../../../lessons/M03-L01.md#costs-of-a-remote-boundary) · [Companion, EX-1 and rubric](../../../../assessments/M03-L01.md#answer-key--rubric) · [Evidence](../../../../evidence/M03-L01.md)

Round 1 verdict `ready-for-human-review`.

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M03-L01 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

| ID | Severity | Status | Location | Finding and correction | Evidence |
| --- | --- | --- | --- | --- | --- |
| MS02-H-T-LAY-1 | major | open | `modules/m03/lessons/M03-L01.md:49` and `modules/m03/assessments/M03-L01.md:74` | A durable seen-ID record can suppress execution after the PDF is created yet leave the catalogue pending indefinitely if the result was only in the lost reply. Retain a recoverable completed-result reference by work ID, return it for replay or expose authoritative status, and explain the completion transition at the reservation owner. For an external write, use an idempotent destination under the same work ID or couple that effect to the durable completion contract. | [AWS Builders' Library, retries and semantic equivalence](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) |

The guarded all-or-nothing claim and single transactional seat owner remain correct. PostgreSQL 18 at Read Committed rechecks the predicate on a row changed by a competing update after that update commits. [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `revise`.**

## Human-feedback correction re-review, 2026-11-13

Reviewed `fdbe268..31b2eb0` for the finding below and adjacent regressions.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| MS02-H-T-LAY-1 | resolved | `modules/m03/lessons/M03-L01.md:49` and `modules/m03/assessments/M03-L01.md:74–78` persist the result reference before acknowledging completion. A stable output destination handles the window between the external write and that record. Retry or authoritative lookup retrieves the same result within retention, and the owner applies the matching transition idempotently. The atomic seat claim and pending-work creation remain together. | [AWS Builders' Library, retries and semantic equivalence](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) · [PostgreSQL 18 §13.2.1](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED) |

**Correction re-review verdict: `ready-for-human-review`.**
