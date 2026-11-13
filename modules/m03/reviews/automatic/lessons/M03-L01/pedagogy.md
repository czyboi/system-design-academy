# M03-L01 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion and evidence in lesson mode after draft handoff at `e496b9a`. The audience is middle and senior engineers. Scope is the [approved M03-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l01), its three assigned rows in [SDA-v1 coverage](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer application-layer section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L773-L798) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The prior archived review supplied context for the updated outcome-map headings and isolated-worker alternative.

## Coverage

| Topic and locator | Status | Teaching evidence and assessment |
| --- | --- | --- |
| PR-H078, application layer, README.md#L773 | taught | **Logical layers and deployment tiers** explains web request handling, application rules and data persistence. **Worked example** traces the catalogue's transaction, durable processing request, processor and result owner. Q1–Q3 and EX-1 assess the responsibilities and ownership. |
| PR-H079, microservices, README.md#L785 | taught | **Logical layers and deployment tiers** compares a modular monolith and separately deployed capabilities. **Worked example** contrasts a separately scaled media processor with entity-per-service fan-out. Q4–Q5 and EX-1 apply the boundary decision. |
| PR-H081, application-layer disadvantages, README.md#L795 | taught | **Costs of a remote boundary** explains network, deployment, observability and cross-service transaction costs, including failed compensations. Q4, Q6 and EX-1 assess consequences and trade-offs. |

The assigned application-layer topics are explained within their mapped lesson. The Primer's service-discovery heading is allocated to M03-L03 in the approved curriculum. This review is limited to M03-L01.

## Pedagogy and assessment

The motivating CPU contention leads into the logical responsibilities and ownership decision. The worked trace explains the pending processing record and its recovery after restart before comparing a separate processor with synchronous entity-level fan-out. The separate companion provides a new ticketing workload with a reservation invariant, an acceptable receipt delay and an operational failure. Its sample answer retains pending receipt work with the reservation owner and accepts an isolated worker pool as an alternative to a separate service. The rubric allocates points to the trace, invariant, bounded work and failure, comparison, and observations.

LO1 identifies request responsibilities and state ownership, with both taught sections named in its metadata and Q1–Q3 and EX-1 assessing the trace. LO2 uses workload, invariants and operating costs, with the remote-boundary and worked-example headings included in the metadata and Q4–Q6 and EX-1 assessing the decision. The companion contains six checks with explanations and a practical exercise with a sample answer and rubric.

## Findings

No open coverage or pedagogical findings. The existing prerequisite M02-L03 supplies ingress context, while M03-L02 and M03-L03 develop interface and discovery details.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and the assigned curriculum topics.

## Round 1 targeted re-review

Reviewed the LAY-T2 correction at `fc8d61a` in the lesson, EX-1 and its outcome map. The revised **Costs of a remote boundary** section teaches how concurrent buyers can race, how a guarded seat claim resolves the race, and when the owner commits the claims, reservation and pending receipt work. The exercise now asks the learner to handle concurrent requests. Its sample answer and rubric assess the guard, rollback and all-or-nothing commit, while accepting an equivalent concurrency-safe mechanism. The LO1 front matter and narrative table both include the teaching section used by EX-1. The other mapped items and the resource-boundary decision remain intact.

| Finding | Status | Evidence |
| --- | --- | --- |
| LAY-T2 | resolved | [M03-L01 lesson, Costs of a remote boundary](../../../../lessons/M03-L01.md#costs-of-a-remote-boundary) · [Approved M03-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l01) |

**Round 1 verdict: ready-for-human-review.** This re-review covers the changed teaching, assessment and outcome mapping.

## Human-feedback targeted re-review, 2026-11-13

Reviewed the changed lesson and companion at `fdbe268` against the [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l01) and the previous source-topic ledger. The layer, microservice and remote-boundary dispositions remain supported. The guarded ownership and durable-work teaching, including the new lost-reply trace, supports the exercise's concurrency, pending work and boundary recovery tasks. EX-1 specifies peak load, capacity and acceptable receipt delay. Its rubric awards points to invariant ownership, durable duplicate-safe processing, trade-offs and failure verification, with a modular application accepted as an alternative. The six checks and mapped outcomes remain aligned.

| Finding | Severity | Status | Evidence |
| --- | --- | --- | --- |
| P-MS02-HUMAN-L01-1 | note | resolved | [Lesson, Costs of a remote boundary](../../../../lessons/M03-L01.md#costs-of-a-remote-boundary) and [assessment, Practical exercise](../../../../assessments/M03-L01.md#practical-exercise) |

**Current verdict: ready-for-human-review.** Coverage and pedagogy only.

## Technical-correction targeted re-review, 2026-11-13

Reviewed `31b2eb0` against `fdbe268`. The [worked example](../../../../lessons/M03-L01.md#worked-example) now teaches the stable output identity, durable completed reference and idempotent result transition. The [exercise answer and rubric](../../../../assessments/M03-L01.md#answer-key--rubric) apply that mechanism to a lost PDF reply and crash, while retaining credit for durable recovery and verification. The lesson outcome mapping and previously reviewed assigned-topic coverage remain supported.

| Finding | Severity | Status | Evidence |
| --- | --- | --- | --- |
| P-MS02-CORRECT-L01-1 | note | resolved | [Approved M03-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l01) |

**Current verdict: ready-for-human-review.** Pedagogy and assigned coverage only.
