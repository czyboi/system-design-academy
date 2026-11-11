# M01-L02 revised actual coverage and pedagogy review

## Scope and source

Reviewed the revised lesson and companion in lesson mode for middle/senior engineers against the approved M01-L02 outline and the System Design Primer at revision ae9bbd7b02d90b9866215de185217d33f39ab733. The first review examined the pinned README sections. This recheck examined the changed content, full current pair, evidence and plan.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H032 | Core concepts and mechanisms | taught | README.md#L412. Defines performance and scalability under a named growth axis and matched constraints, then explains vertical and horizontal alternatives. |
| PR-H034 | Core concepts and mechanisms | taught | README.md#L426. Defines elapsed latency and work completed per unit time, including successful request populations and error counts. |

Both assigned source topics have explanatory teaching, with a workload and explicit decision criteria.

## Pedagogy and assessment

The lesson introduces the burst problem, compares metrics and state placement, then teaches queueing through a modeled example and measurement plan. The revised worked example specifies the backend dispatch assumption and separates frontend from backend queues. The exercise applies the model to 90/150 arrivals, 120/80 capacities, a 12-second burst and 110 operations/s backend, distinct from the teaching example. It requires a justified choice, a failure scenario and measurements. Its answer key derives 360 queued requests, a 12-second drain, a balanced 75 requests/s per server and 480 queued backend operations under the stated dispatch assumption.

Q2 and Q3 use a separate 85/70 and 50/70 workload, with a 120-request backlog and six-second drain. The distinct inputs and results require fresh calculation. The six checks include explanations, and the rubric accepts reasoned alternatives. LO1 maps to Q1–Q3 and EX-1. LO2 maps to Q4–Q6 and EX-1. The new companion note identifies the additional teaching headings for queueing and state placement.

## Findings and prior review disposition

- **P01, resolved.** The exercise and Q2–Q3 use fresh inputs and recomputed outcomes.
- **P02, resolved.** The companion explicitly identifies the other teaching sections underlying the combined decision outcome.

No new material coverage or pedagogical finding was identified.

Verdict: **ready-for-human-review**.
