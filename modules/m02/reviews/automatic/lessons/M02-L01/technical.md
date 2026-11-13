# M02-L01 technical and provenance review

Reviewed 2026-11-12 at draft handoff `29e2cf2`. Scope covers the canonical DNS lesson, companion assessment and evidence pack for SDA-M02-L01.

## Findings

| ID | Severity | Status | Location | Evidence and suggested change |
| --- | --- | --- | --- | --- |
| M02-L01-T1 | note | optional | `modules/m02/assessments/M02-L01.md:18,74`, EX-1 and sample decision note | The exercise says the DNS service applies the weights, while “Each resolver makes one selection” and “the 800-client resolver could select either region” could blur which component chooses. Use “each resolver obtains one answer selected by the authoritative service” and “the 800-client resolver could receive either answer.” This wording refinement leaves the probabilities and rubric intact. [Route 53 weighted routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html) |

## Technical checks

- The resolver follows delegation on cache misses and can reuse cached delegations. The A and AAAA cardinality is explicit, and Q1–Q2 correctly apply delegation and alias roles. [RFC 1034 §§4.3.2 and 5.3.3](https://www.rfc-editor.org/rfc/rfc1034.html#section-5.3.3) · [RFC 1035 §§3.3 and 3.4.1](https://www.rfc-editor.org/rfc/rfc1035.html#section-3.4.1) · [RFC 3596 §2](https://www.rfc-editor.org/rfc/rfc3596.html#section-2)
- The modeled TTL expiry times are 60 s and 270 s. Q3 gives an expiry of 80 s, so a request at 50 s can still use the old answer. The lesson states ordinary expiry assumptions, treats serve-stale as conditional, and distinguishes cached discovery from an existing connection. The worked trace assumes B passed its readiness check and traces traffic migration independently. The cited prerequisite establishes why routing and standby eligibility are separate checks. [RFC 8767 §4](https://www.rfc-editor.org/rfc/rfc8767.html#section-4) · [M01-L04 recovery trace](../../../../../m01/lessons/M01-L04.md#trace-a-two-region-recovery)
- The 3:1 teaching example and 2:1 exercise describe DNS answer-selection shares with eligible records. Two resolver cohorts of unequal size demonstrate why observed request shares can differ. The lesson scopes latency, geolocation, and all-unhealthy fallback to the provider and policy. [Route 53 routing policies](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html) · [Route 53 health-aware record selection](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-how-route-53-chooses-records.html)

## Provenance and assets

The evidence pack separates IETF protocol behavior and current AWS policy behavior from the Academy scenarios. Donne Martin and the pinned Primer revision are credited for topic selection. The archived Academy matrix is linked, and the lesson and assessment contain original scenarios without external diagrams, code or other reproduced assets. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

**Verdict: ready-for-human-review.** No open technical or provenance finding requires a correction round.

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M02-L01 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

| ID | Severity | Status | Location | Finding and correction | Evidence |
| --- | --- | --- | --- | --- | --- |
| MS02-H-T-DNS-1 | major | open | `modules/m02/assessments/M02-L01.md:18,76` | The objective can be read as 99% of all requests issued during the first minute succeeding. The proposed 20-second interruption can miss that target even at uniform traffic. Define a post-recovery sample window beginning by t = 60 s and its denominator, or revise the failover design and assumptions to meet a first-minute request SLO. | [RFC 1034 §3.2.1](https://www.rfc-editor.org/rfc/rfc1034.html#section-3.2.1) |

The authoritative service performs the 2:1 selection. Recursive reuse changes the request distribution, and −30 + 300 gives expiry at t = 270 s. The ingress path depends on clients receiving its address in advance and on West capacity. Serving stale depends on the resolver's refresh-failure policy. [Route 53 weighted routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html) · [RFC 8767 §4](https://www.rfc-editor.org/rfc/rfc8767.html#section-4)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `revise`.**

## Human-feedback correction re-review, 2026-11-13

Reviewed `fdbe268..31b2eb0` for the finding below and adjacent regressions.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| MS02-H-T-DNS-1 | resolved | `modules/m02/assessments/M02-L01.md:18,74–78` defines both the recovery deadline and the per-group denominator. Requests issued at `60 ≤ t < 120 s` form the post-recovery sample. An available ingress reroute at 20 s precedes that window, while the modeled larger resolver can still supply the East address throughout it because expiry remains at 270 s. The 2:1 authoritative-selection explanation is intact. | [RFC 1034 §3.6](https://www.rfc-editor.org/rfc/rfc1034.html#section-3.6) · [Route 53 weighted routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html) |

**Correction re-review verdict: `ready-for-human-review`.**
