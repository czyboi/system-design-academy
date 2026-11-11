# M02-L04 actual coverage and pedagogy review

## Scope and sources

Reviewed the declared teaching and companion pair for middle and senior engineers against the approved SDA-v1 outline, inventory and matrix. Checked the pinned [Primer CDN sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L619-L652), revision ae9bbd7b02d90b9866215de185217d33f39ab733. Considered prior M01-L02 feedback on transfer between the worked example and the separate exercise.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H062 | Population and placement | taught | README.md#L619. Explains geographically distributed edge delivery, local hits, upstream fetches and the conditional latency benefit. LO1 and LO2. |
| PR-H063 | Population and placement | taught | README.md#L634. Explains distributing content before demand, predictable-release use and unused-transfer or storage costs. LO2. |
| PR-H064 | Population and placement | taught | README.md#L640. Explains request-triggered fetch and later reuse, cold and expiry misses and burst pressure on the origin. LO1 and LO2. |
| PR-H065 | Trade-offs and failure modes | taught | README.md#L648. Explains cost and freshness trade-offs and the consequences of origin failure, with replacement and cached-reference effects demonstrated separately. LO2. |

The Academy additions on variant identity, TTL, versioned URLs, invalidation, provider-specific overrides and privacy are taught under Cache keys, freshness and privacy, then applied in the example and companion.

## Pedagogy and assessment

The English lesson establishes a real workload problem, teaches cache behavior and privacy, follows a two-edge replacement trace and ends with testable design criteria. LO1 is taught through the worked example and measured by Q1–Q3 and EX-1. LO2 is taught by the decision framework and its preceding mechanism sections and measured by Q4–Q6 and EX-1. The three trace checks are deliberate scaffolding. The independent museum exercise changes the variant dimension, TTL, workload and initial outage state, and requires a new decision about a personalized response. The rubric covers the design constraints, permits alternatives, and expects the learner to distinguish an origin failure on a cold miss from an eligible stale cached response.

All four topics are explained. Both outcomes have teaching and assessment evidence. No material coverage, pedagogy or language gap identified.

## Verdict

ready-for-human-review.
