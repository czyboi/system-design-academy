# M02-L04 pedagogy and curriculum coverage review

Round 0, 2026-11-12. Reviewed the canonical lesson and companion for middle and senior engineers against the [approved M02-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l04), [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv), and [pinned Primer CDN sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L619-L652) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The archived teaching review in PR #38 supplied background context.

## Findings

No open pedagogical or assigned-topic coverage findings.

## Coverage ledger

| Topic ID | Teaching evidence | Disposition |
| --- | --- | --- |
| PR-H062 | [Population and placement](../../../../lessons/M02-L04.md#population-and-placement) explains geographically distributed edges, local hits and upstream misses. | taught |
| PR-H063 | Population and placement explains proactive distribution, predictable releases and unused transfer or storage. | taught |
| PR-H064 | Population and placement explains request-triggered fetch, reuse and cold-edge origin pressure. | taught |
| PR-H065 | [Trade-offs and failure modes](../../../../lessons/M02-L04.md#trade-offs-and-failure-modes) explains freshness, cost, privacy and origin-failure constraints. | taught |

The lesson additionally teaches variant identity, TTL, replacement, invalidation, private responses and provider-specific cache-policy checks in Cache keys, freshness and privacy. The worked example uses two independent edges and a versioned replacement. It distinguishes a stale response for the requested URL and variant from an unavailable cold copy of the new version.

## Outcomes and assessment

LO1 is taught in Population and placement, Cache keys, freshness and privacy, and Worked example. Q1–Q3 assess an independent cold edge, an old reference and an absent stale copy. EX-1 transfers key, language and replacement reasoning to a museum map. LO2 is taught across the same mechanisms, Trade-offs and failure modes, and Decision framework. Q4–Q6 assess variant keys, proactive population and private-response policy. EX-1 asks for replacement, origin-failure and privacy decisions and a trade-off. The front matter and narrative table name the same teaching sections and items for each outcome.

The companion includes six explained checks, a separate exercise, a sample answer and a four-dimension rubric. The rubric accepts alternative designs that satisfy the constraints. The lesson names M02-L03 as its prerequisite.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Human-feedback targeted re-review, 2026-11-13

Reviewed the changed lesson and companion at `fdbe268` against the [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l04) and the prior topic ledger. The previous coverage evidence remains present. The worked example now explains independent collapse domains and the origin measurement boundary. EX-1 requires calculation for four cold edges, an ideal shared tier and a bounded origin policy when collapsing falls short. The rubric separately grades variant/freshness/privacy reasoning, estimates, capacity trade-offs and tests. The practical scenario has stated assumptions, and the original six explained checks and outcome maps remain intact.

| Finding | Severity | Status | Evidence |
| --- | --- | --- | --- |
| P-MS02-HUMAN-L04-1 | note | resolved | [Lesson, Worked example](../../../../lessons/M02-L04.md#worked-example) and [assessment, Answer key / rubric](../../../../assessments/M02-L04.md#answer-key--rubric) |

**Current verdict: ready-for-human-review.** Coverage and pedagogy only.

## Publication-readiness targeted re-review at `0dcef2a`, 2026-11-13

Lesson-mode combined pedagogy and coverage re-review for M02-L04, middle/senior self-study, following [PR #66 feedback](https://github.com/czyboi/system-design-academy/pull/66#issuecomment-6846736588). Inspected the `3c0205c..0dcef2a` lesson and assessment changes, nearby exercise and rubric, the approved [outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l04), and assigned [coverage rows](../../../../../../curriculum/revision-1/coverage.csv). The pinned source remains the [Primer CDN section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L619-L652), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`; the accepted ledger above remains applicable. No matched prevention reminders were supplied.

### Coverage

| Assigned source row and locator | Actual lesson teaching and assessment | Status / depth and rationale |
| --- | --- | --- |
| PR-H062, CDN, README L619 | Population and placement; EX-1 | taught: distributed edges, local reuse and upstream misses. |
| PR-H063, push, README L634 | Population and placement; Q5 | taught: advance distribution, release fit and unused-resource trade-off. |
| PR-H064, pull, README L640 | Population and placement; Q1 and EX-1 | taught: demand-driven fetch, reuse and cold-origin pressure. |
| PR-H065, disadvantages, README L648 | Trade-offs and failure modes; EX-1 | taught: freshness, origin dependence, cost and privacy constraints. |

No assigned source topic has a material teaching gap. The added validation explanation supports the Academy freshness and cache-control scope; it does not displace the mapped CDN mechanisms.

### Pedagogy and assessment

| Finding | Severity | Status | Evidence and learner impact |
| --- | --- | --- | --- |
| P-MS02-HUMAN-L04-1 | note | resolved | The earlier collapse-domain explanation and exercise/rubric remain in [Worked example](../../../../lessons/M02-L04.md#worked-example) and [Answer key / rubric](../../../../assessments/M02-L04.md#answer-key--rubric). |
| P-L04-PUB-1 | note | resolved | [Revalidation and conditional requests](../../../../lessons/M02-L04.md#revalidation-and-conditional-requests) gives the stored English variant, freshness expiry, validator request, unchanged `304` and changed full-response paths, metadata/body reuse, error constraint, and language separation. It teaches `no-cache`, `no-store` and `private` distinctions and warns that CDN configuration and authentication matter. A learner can reason through Q7 from the lesson without its key. |
| P-L04-PUB-2 | note | resolved | [Q7](../../../../assessments/M02-L04.md#q7) has an answer and explanation matching the instruction; both front-matter and narrative outcome maps include it for LO1 and LO2. Seven explained checks, the separate EX-1 and its alternative-accepting rubric remain present. Q7 tests the directive distinction; EX-1 and the other checks provide the broader design decisions for LO2. |

The existing exercise's language-key, old-reference, outage and privacy reasoning remains supported by the lesson. The capacity exercise retains explicit overlap assumptions, origin-boundary measurement and a trade-off for a bounded policy. No new material pedagogy or assigned-coverage finding is open.

**Verdict: ready-for-human-review.** This is a pedagogy and assigned curriculum-coverage verdict, not technical approval, human approval or publication authorization.

## Correction re-review at `54b7566`, 2026-11-13

Reviewed the M02-L04 lesson and companion changes in `0dcef2a..54b7566`, plus adjacent teaching, assessment and the assigned coverage ledger above. The assigned Primer rows PR-H062–PR-H065 retain their taught dispositions. This is a targeted independent pedagogy and coverage re-review.

| Finding | Severity | Status | Evidence and re-review result |
| --- | --- | --- | --- |
| P-L04-PUB-1 | note | resolved | [Revalidation and conditional requests](../../../../lessons/M02-L04.md#revalidation-and-conditional-requests) still traces the matching English variant through conditional GET, bodyless `304` and metadata/body reuse, nonmatching successful GET, and the origin-error limit. It distinguishes unqualified directives and directs learners to check the actual CDN policy. |
| P-L04-PUB-2 | note | resolved | [Q7](../../../../assessments/M02-L04.md#q7) now requires and explains a directive choice for each stated requirement. The lesson teaches the distinction, and both the front-matter and narrative maps include Q7 under LO1 and LO2. |
| P-L04-PUB-3 | note | resolved | [EX-1](../../../../assessments/M02-L04.md#practical-exercise) separates the 100 origin-attempt first-second limit, including retries, from 99% of 1,200 original valid arrivals receiving the correct variant within two seconds of each arrival. Rejected, failed and late work remains in the viewer denominator. The [answer and rubric](../../../../assessments/M02-L04.md#answer-key--rubric) give a conditional imperfect-collapse example, measure both limits, explain the 12-request failure budget, deny capacity-policy credit for a cap alone, and accept credible alternatives or identified failure with mitigation. |

The seven explained checks, language and privacy exercise, mapped outcomes and previously taught CDN choices remain coherent after the changes. No material teaching, assessment or assigned-coverage finding is open.

**Verdict: ready-for-human-review.** Pedagogy and assigned curriculum coverage only; this is not technical approval, human approval or publication authorization.
