# M02-L01 pedagogy and curriculum coverage review

Round 0, 2026-11-12. Reviewed the canonical lesson and companion for middle and senior engineers against the [approved M02-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l01), [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv), and [pinned System Design Primer DNS section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L581-L611) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The archived review in PR #38 was background context. This review inspects the current artifacts.

## Findings

No open pedagogical or assigned-topic coverage findings.

## Coverage ledger

| Topic ID | Teaching evidence | Disposition |
| --- | --- | --- |
| PR-H059 | [Resolution and record roles](../../../../lessons/M02-L01.md#resolution-and-record-roles) explains recursive resolution, delegation and caching. | taught |
| PR-H060 | [Routing choices and cached answers](../../../../lessons/M02-L01.md#routing-choices-and-cached-answers) explains stale results and resolver and control-plane failures. [Trade-offs and failure modes](../../../../lessons/M02-L01.md#trade-offs-and-failure-modes) connects TTL to recovery. | taught |
| PR-B001 | Resolution and record roles traces resolver-to-authority behavior and distinguishes the assigned record roles. | taught |
| PR-BODY-R1-DNS-NS | Resolution and record roles explains delegation to authoritative name servers. | taught |
| PR-BODY-R1-DNS-MX | Resolution and record roles identifies mail exchangers and preference. | taught |
| PR-BODY-R1-DNS-A | Resolution and record roles explains individual A records and multiple records for a name. | taught |
| PR-BODY-R1-DNS-CNAME | Resolution and record roles traces an alias to its canonical target. | taught |
| PR-BODY-R1-DNS-WEIGHT | Routing choices and cached answers relates weighting to cluster sizes and A/B rollout, and explains resolver sharing. | taught |
| PR-BODY-R1-DNS-LATENCY | Routing choices and cached answers explains provider latency data and its relationship to client experience. | taught |
| PR-BODY-R1-DNS-GEO | Routing choices and cached answers explains selection by inferred location and the need to check fallback. | taught |

## Outcomes and assessment

LO1 is taught in Resolution and record roles, Routing choices and cached answers, and Worked example. Q1 and Q2 assess delegation and alias resolution, Q3 calculates a changed-record cache expiry, and EX-1 applies shared cached answers to maintenance. LO2 is taught in Routing choices and cached answers, Trade-offs and failure modes, and Decision framework. Q4–Q6 assess TTL changes, weighting, regional selection and fallback, while EX-1 asks for an operational decision and mitigation. The front matter and narrative map name the same sections and items.

The lesson moves from the regional routing problem to resolution, policies, a timed two-resolver trace and the operational decision. The separate companion contains six questions with answers and explanations, plus an exercise, sample decision and ten-point rubric. Its new resolver populations test why weighted DNS answer selection cannot guarantee a per-request split. The prerequisite M01-L04 is identified in the lesson.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.
