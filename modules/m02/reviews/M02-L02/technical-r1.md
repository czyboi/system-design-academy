# Independent technical and provenance recheck — M02-L02

Reviewed 2026-11-11.

## Technical findings

- **M02-L02-TP1 · Minor · Resolved.** The new method table teaches PUT creation or replacement and separates cacheability from safety and intended effects. GET is eligible subject to cache controls. POST and PATCH have explicit freshness and matching target URI requirements for retrieval reuse. PUT and DELETE responses are ineligible. Q5 applies those distinctions to fresh inputs. [RFC 9110 §§9.2–9.3](https://datatracker.ietf.org/doc/html/rfc9110#section-9.2) [RFC 5789 §2](https://datatracker.ietf.org/doc/html/rfc5789#section-2)
- **M02-L02-TP2 · Note · Resolved.** The create explanation and sample answer now scope the request identity and commit the ticket and deduplication record together. A matching retry uses the recorded effect. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

The new invalidation explanation correctly applies to caches in the request path and avoids a global invalidation guarantee. The unchanged transport sections and the assessment's transfer scenario preserve the earlier review conclusions. The buffer maximum remains 320 under the stated assumptions. [RFC 9111 §4.4](https://datatracker.ietf.org/doc/html/rfc9111#section-4.4)

## Provenance findings

No material provenance finding. The added table paraphrases the applicable RFC sections in the Academy's own structure and the invalidation rule has a direct RFC citation. The revised answers remain original. The reviewed pair introduces no third-party assets.

## Verdict

`ready-for-human-review`
