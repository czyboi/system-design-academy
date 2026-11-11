# M02-L01 actual coverage and pedagogy review

## Scope and sources

Reviewed the declared teaching and assessment pair for middle and senior engineers against SDA-v1. Independently checked the [pinned Primer DNS section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L581-L611), revision ae9bbd7b02d90b9866215de185217d33f39ab733. Checked the M01-L04 learning prerequisite at the commit named in the evidence. Its separation of readiness and traffic shift carries into this lesson's worked example, with a new DNS trace and new assessment data. Considered prior M01-L02 feedback on exercise transfer and heading precision.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H059 | Resolution and record roles | taught | README.md#L581. Explains recursive lookup, delegation, authoritative answers and remaining TTL. LO1, Q1–Q3. |
| PR-H060 | Routing choices and cached answers | taught | README.md#L607. Explains lookup failure, control-plane change failure and cached responses persisting despite a short new TTL. LO1 and LO2, Q3–Q4 and EX-1. |
| PR-B001 | Resolution and record roles | taught | README.md#L591. Teaches the lookup chain and the distinct NS, MX, A and CNAME roles. LO1, Q1–Q2. |
| PR-BODY-R1-DNS-NS | Resolution and record roles | taught | README.md#L593. Parent NS delegation locates the authoritative child zone. LO1, Q1. |
| PR-BODY-R1-DNS-MX | Resolution and record roles | taught | README.md#L594. Identifies mail exchangers and preference as distinct from address records. LO1. |
| PR-BODY-R1-DNS-A | Resolution and record roles | taught | README.md#L595. Explains IPv4 name-to-address mapping and distinguishes AAAA. LO1, Q2. |
| PR-BODY-R1-DNS-CNAME | Resolution and record roles | taught | README.md#L596. Explains alias resolution via the canonical target and restrictions on ordinary records at the alias owner. LO1, Q2. |
| PR-BODY-R1-DNS-WEIGHT | Routing choices and cached answers | taught | README.md#L600. Explains answer weights, cluster sizing and A/B rollout, then uses staged maintenance and resolver sharing to qualify request outcomes. LO2, Q5 and EX-1. |
| PR-BODY-R1-DNS-LATENCY | Routing choices and cached answers | taught | README.md#L604. Explains provider latency input, regional selection and actual client-experience checks. LO2, Q6. |
| PR-BODY-R1-DNS-GEO | Routing choices and cached answers | taught | README.md#L605. Explains location inference, distinction from measured latency, and fallback checks. LO2, Q6. |

All 10 assigned topics have explanatory evidence. AAAA and TXT are covered in the record section. The worked timeline distinguishes normal expiry from stale serving and active connection reuse. The decision framework leaves transport and application balancing to later lessons.

## Pedagogy and assessment

The English lesson starts with readiness versus client routing during maintenance, then builds the resolution and policy mechanism before showing a timed two-resolver transition. LO1 maps to the resolution concepts and worked example and is assessed by Q1–Q3 and EX-1. LO2 maps to the decision framework and trade-offs and is assessed by Q4–Q6 and EX-1. The A/B exercise applies answer weights to two independently cached resolver populations with new ratios and client counts. It also requires mitigation and an observation for the maintenance event. Q3 changes both age and TTL and correctly derives an expiry at t = 80 s. The sample answer and rubric separate answer selection from observed request distribution and accept feasible mitigations under stated assumptions.

No material coverage, pedagogy or language gaps identified.

## Verdict

ready-for-human-review.
