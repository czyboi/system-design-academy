# M02-L04 technical and provenance review

Reviewed 2026-11-12 at draft handoff `e496b9a`. Scope covers the canonical CDN lesson, assessment and evidence pack.

## Findings

| ID | Severity | Status | Location | Evidence and suggested change |
| --- | --- | --- | --- | --- |
| M02-L04-T1 | note | optional | `modules/m02/lessons/M02-L04.md:43` and `modules/m02/assessments/M02-L04.md:74`, stale-on-error policy | The example gives the correct match and policy conditions. To make the bound operationally concrete, name `stale-if-error` and state that its window is measured from freshness expiry, for an eligible upstream error. [RFC 5861 §4](https://www.rfc-editor.org/rfc/rfc5861.html#section-4) |

## Technical checks

- The pull path distinguishes an edge miss from origin work when there is an upstream tier. The proactive alternative states prepositioning and capacity assumptions without promising a provider API. The worked example expressly assumes independent cold edges. Q1 and EX-1 use that assumption consistently. [CloudFront delivery flow and regional edge caches](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html)
- The language and size examples correctly identify the collision when a representation selector is omitted. The lesson separates authorization from a cache key and scopes unqualified `private` and `no-store` to HTTP semantics. The CloudFront warning about a positive minimum TTL is verified. The exercise asks for actual cache policy enforcement and Q6 identifies the relevant setting. [RFC 9111 §§3.5, 4–4.1 and 5.2.2](https://www.rfc-editor.org/rfc/rfc9111.html#section-4) · [CloudFront TTL and cache-key settings](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-key-understand-cache-policy.html#cache-key-understand-cache-policy-ttl)
- A changed URL distinguishes the corrected image or map while older referring metadata can retain the old URL. CDN invalidation has a different scope from copies in a browser or corporate cache. Q2 follows the old reference and Q3 identifies a missing representation. The EX-1 answer confines stale reuse to an existing response for the requested URL and matching language under an eligible policy. The corrected URL requires its own matching cached response or a reachable upstream. [CloudFront invalidation and versioned names](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html) · [RFC 9111 §§4–4.1](https://www.rfc-editor.org/rfc/rfc9111.html#section-4) · [RFC 5861 §4](https://www.rfc-editor.org/rfc/rfc5861.html#section-4)

## Provenance and assets

The evidence pack separates general HTTP behavior from CloudFront configuration and labels examples as Academy designs. The lesson credits Donne Martin, the pinned Primer revision and CC BY 4.0 for topic selection. The archived Academy matrix is linked. The text uses original Academy examples and contains no reproduced third-party diagrams, code or other assets. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

**Verdict: ready-for-human-review.** No open technical or provenance finding requires a correction round.

## Human-feedback technical re-review, 2026-11-13

Reviewed `e805261..fdbe268` for M02-L04 in response to [issue #64](https://github.com/czyboi/system-design-academy/issues/64#issuecomment-6841513179). Scope covers the changed teaching, companion and canonical evidence.

No open technical or provenance findings in the changed scope.

`modules/m02/assessments/M02-L04.md:20,76–78` derives 160 direct origin fetches, 40 with ideal cross-edge collapsing, and 80 with two independent groups. These are conditional on overlap and shared keys. Origin attempts include retries against the 100-fetch scenario limit. The outage trace distinguishes eligible stale copies from absent variants and tests privacy with two users. [CloudFront, request collapsing](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RequestAndResponseBehaviorCustomOrigin.html#request-custom-request-collapsing) · [RFC 9111 §4.1](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.1) · [RFC 5861 §4](https://www.rfc-editor.org/rfc/rfc5861.html#section-4)

The exercise and model are original illustrative material. No third-party asset was added. The prior attribution remains in the lesson.

**Human-feedback re-review verdict: `ready-for-human-review`.**
