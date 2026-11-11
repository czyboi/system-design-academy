# Independent technical and provenance review — M02-L02

Reviewed 2026-11-11.

## Technical findings

- **M02-L02-TP1 · Minor · Open.** Lesson, **HTTP requests and method semantics**, method paragraph. “PUT replaces the target's state” omits creation at a client-selected target URI when the server permits it. Say that PUT requests creation or replacement of the target's state using the enclosed representation. If expanding the POST cache sentence, explain that explicit freshness and a matching `Content-Location` permit reuse for later GET or HEAD, rather than reuse to satisfy a later POST. The stated intended-effect and safety distinctions are otherwise sound. [RFC 9110 §§9.3.3–9.3.4](https://datatracker.ietf.org/doc/html/rfc9110#section-9.3.3)
- **M02-L02-TP2 · Note · Open.** Companion **Answer key / rubric**, ticket-creation paragraph. The durable deduplication contract is suitable. An implementation example could make its atomicity explicit by committing the ticket and the scoped idempotency record together, then replaying the recorded result for a matching retry. This closes the crash window in which the ticket commits but the deduplication record is missing. [AWS Builders' Library, making retries safe](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

The transport trace properly separates TCP acknowledgments from business commits, advertised receive window from congestion control, and UDP application policy from QUIC recovery. HTTP/2 multiplexes exchanges but shares TCP head-of-line effects. HTTP/3 runs over QUIC streams. The hypothetical connection calculations are consistent at 1,000 × 128 KiB = 125 MiB, 400 × 64 KiB = 25 MiB, and 30 MiB ÷ 96 KiB = 320 connections. The dashboard exercise distinguishes superseded readings from repeat-safe creation. [RFC 9293 §3.1](https://datatracker.ietf.org/doc/html/rfc9293#section-3.1) [RFC 5681 §3](https://datatracker.ietf.org/doc/html/rfc5681#section-3) [RFC 8085 §§3.1–3.3](https://datatracker.ietf.org/doc/html/rfc8085#section-3.1) [RFC 9113 §2](https://datatracker.ietf.org/doc/html/rfc9113#section-2) [RFC 9114 §2](https://datatracker.ietf.org/doc/html/rfc9114#section-2)

## Provenance findings

No material provenance finding. The RFC citations substantiate the protocol, caching and security claims. The transport and memory examples use explicitly hypothetical inputs rather than published benchmarks. No third-party diagram, code, or other asset is reproduced. Attribution identifies Donne Martin, the pinned revision, and CC BY 4.0. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

## Verdict

`ready-for-human-review`
