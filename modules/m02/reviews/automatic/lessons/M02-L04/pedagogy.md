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
