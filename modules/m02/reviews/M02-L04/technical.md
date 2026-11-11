# Independent technical and provenance review — M02-L04

Reviewed 2026-11-11.

## Technical findings

- **M02-L04-TP1 · Minor · Open.** Companion **Answer key / rubric**, sentence beginning “A stated stale policy”. Name the requested URL and matching variant as eligibility conditions. Once the corrected map has a distinct URL, a stale cached response to the old URL is available for a request to the old URL. Answering a request for the new URL with the old object would require a deliberately designed fallback. The adjacent sample answer correctly states that a cold edge cannot invent a cached copy of the new version. [HTTP Caching, response reuse and variant keys](https://datatracker.ietf.org/doc/html/rfc9111#section-4) [RFC 5861 §4, stale-if-error](https://datatracker.ietf.org/doc/html/rfc5861#section-4)

The two-edge trace states its independent cold-cache assumption. Versioned URLs and invalidation are distinguished from old browser or intermediary references. The privacy rule concerns the unqualified `private` response directive, as written, and the positive minimum TTL exception is explicitly scoped to CloudFront. The exercise and key align on the variant omission, a cold miss, and the need to verify the personalized route against CDN policy. [HTTP Caching, response directives](https://datatracker.ietf.org/doc/html/rfc9111#section-5.2.2) [CloudFront cache policy](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache-key-understand-cache-policy.html) [CloudFront invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)

## Provenance findings

No material provenance finding. The source matrix ties the pull flow to CloudFront and treats proactive population as an architecture choice with provider-specific support. The lesson and companion use original hypothetical scenarios and no reproduced diagrams, code or third-party assets. The attribution identifies Donne Martin and CC BY 4.0. [CloudFront delivery flow](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html) [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

## Verdict

`ready-for-human-review`
