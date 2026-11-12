# M02 synthesis technical and provenance review

Reviewed 2026-11-12 at integration handoff `7220e6c`. All four Stage A cycles were ready. This review covers the integrated brief, reference solution, decision summary, evidence and their connection to the accepted M02 lessons.

## Findings

| ID | Severity | Status | Location | Evidence and suggested change |
| --- | --- | --- | --- | --- |
| M02-INT-T1 | major | open | `modules/m02/integrated/brief.md:14–15`, peak and origin capacity assumptions, and `modules/m02/integrated/solution-rubric.md:18`, origin demand | The arithmetic correctly counts 200 warm and 2,160 cold viewer-edge misses per second. Calling these exact origin rates assumes that each miss traverses any intermediate cache and issues one origin fetch before coalescing. M02-L04 explicitly allows an upstream cache to satisfy an edge miss. State in the brief and solution that the modeled path has no additional cache hits or upstream retries, and that the cold requests would each miss before coalescing. Keep the condition that each distinct cold key causes at most one origin fetch in the interval. [CloudFront, How regional caches work](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html) · [CloudFront, Simultaneous requests for the same object](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RequestAndResponseBehaviorCustomOrigin.html) |

## Integration and cross-lesson checks

- R1's 120-second TTL from −30 s expires at +90 s. At +60 s it returns the old edge A under the exercise assumptions. R2 has no cached answer and returns the new edge B. The solution separates the modeled expiry from observations of destination addresses, persistent connections and conditional serve-stale behavior. This aligns with M02-L01. [RFC 1034 §5.3.3](https://www.rfc-editor.org/rfc/rfc1034.html#section-5.3.3) · [RFC 8767 §4](https://www.rfc-editor.org/rfc/rfc8767.html#section-4)
- The client-facing connection uses HTTP/3 over QUIC when available or HTTP/2 over TLS and TCP. The origin leg has a separate TLS boundary and names pooled HTTP/2 as an example conditional on support. L4 can distribute flows across equivalent ingress replicas. Selecting media and saved-items pools by path needs access to the HTTP request at L7. This is consistent with M02-L02 and M02-L03 and leaves origin connection, ingress capacity and backend authentication as explicit deployment choices. [RFC 9113 §5](https://www.rfc-editor.org/rfc/rfc9113.html#section-5) · [RFC 9114 §2](https://www.rfc-editor.org/rfc/rfc9114.html#section-2) · [AWS ALB path conditions](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-condition-types.html#path-conditions)
- The reference distinguishes versioned asset identity from freshness of referring metadata. Its stale-age arithmetic is `20 + 90 = 110 s` after freshness expiry, within the stated 300-second window for the eligible public variant. It distinguishes that stored copy from absent objects and disables shared storage and stale fallback for saved items. The proposed `Age` and freshness-lifetime check is paired with evidence from the cache and a two-user isolation test. These choices agree with M02-L04. [RFC 9111 §§4–4.2, 5.1 and 5.2.2](https://www.rfc-editor.org/rfc/rfc9111.html#section-4) · [RFC 5861 §4](https://www.rfc-editor.org/rfc/rfc5861.html#section-4)

## Provenance and assets

The M02 evidence pack links standards for protocol claims and CloudFront or NGINX documentation for provider examples. It identifies the workload and arithmetic as hypothetical and credits the archived Academy draft. The lesson evidence establishes the Primer topic provenance. The integrated package includes no reproduced third-party figures or code. [Archived MS02 draft](https://github.com/czyboi/system-design-academy/pull/38)

**Verdict: revise.** M02-INT-T1 requires the origin measurement boundary to be explicit.

## Round 1 targeted re-review

Reviewed integration handoff `82df90a`. `modules/m02/integrated/brief.md:14–15` identifies the cold traffic as 2,000 viewer-edge misses before coalescing and states that each uncoalesced miss reaches the origin directly, with no intermediate cache hits, extra retries or other origin traffic. `modules/m02/integrated/solution-rubric.md:18` and `modules/m02/integrated/evidence.md:25` use the same model. Warm demand is 10,000 × 2% = 200 fetches/s. Cold demand without coalescing is 8,000 × 2% + 2,000 = 2,160 fetches/s. If each cold key causes at most one fetch in the modeled second within one coalescing domain, cold-interval demand is at most 160 + 80 = 240 fetches/s. CloudFront documents that a regional cache can satisfy an edge miss and that request collapsing depends on matching keys and overlapping requests. The solution directs learners to measure actual origin traffic. [CloudFront, How regional caches work](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html#CloudFrontRegionalEdgeCache) · [CloudFront, Request collapsing](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RequestAndResponseBehaviorCustomOrigin.html#request-custom-request-collapsing)

The M02-P1 portfolio correction points to the existing DNS, routing and cache walkthroughs in the reference solution. The revised locator introduces no technical regression.

| Finding | Status | Supporting primary source |
| --- | --- | --- |
| M02-INT-T1 | resolved | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html |

**Round 1 verdict: ready-for-human-review.**
