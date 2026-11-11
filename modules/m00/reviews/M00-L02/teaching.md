# M00-L02 coverage and pedagogy review

Reviewed 2026-11-11 in lesson mode for middle/senior backend engineers. Scope is the approved M00-L02 outline and its separate companion, against Donne Martin's System Design Primer pinned at ae9bbd7b02d90b9866215de185217d33f39ab733. Independently inspected README.md lines 218–273 at the pinned revision.

## Actual source coverage

| Topic ID | Exact teaching heading | Disposition | Evidence and depth |
|---|---|---|---|
| PR-H011 | Time-bounded design review | taught | A review timebox walks scope, paths, a risky component and alternatives; it closes with the choice, costs, open risks and evidence. Q6 assesses the communication. |
| PR-H012 | Core concepts and mechanisms | taught | Frame the design identifies actors, operations, explicit revocation constraint, a traffic assumption and non-goals. Q1 and EX-1 exercise that framing. |
| PR-H013 | Core concepts and mechanisms | taught | Draw the paths identifies client, service and authoritative store, with create, read and revoke flows. Q3 and EX-1 trace component roles. |
| PR-H014 | Core concepts and mechanisms | taught | The focused revocation-status deep dive states the store assumption and connects completion order to a later read. Q2 and EX-1 test the path. |
| PR-H015 | Core concepts and mechanisms | taught | Estimate, measure, and revise defines a representative test, operational signals, profiling, one bottleneck change and a repeat test. The worked example and Q5 apply this process. |

## Pedagogy and assessment

The revocation problem motivates requirements and interface decisions before scaling. An explicit trace, alternatives and a conditional profile/change/retest example connect the mechanism to the host-failure trade-off. LO1 maps to Core concepts and mechanisms and Q1–Q3. LO2 maps to Worked example and Q4–Q6 plus EX-1; the time-bounded design review also teaches the communication item Q6. All items are taught and the separate companion provides one exercise, six explained checks, a model response and a five-point rubric that accepts justified alternatives. The technical terms and reading load suit the stated prerequisites.

## Findings and scope

No material source coverage, sequence, assessment or language finding. The prior plan note N1 applies to M03-L02 and M06-L01, outside this package. Technical correctness and provenance remain assigned to the separate independent review.

Verdict: ready-for-human-review.
