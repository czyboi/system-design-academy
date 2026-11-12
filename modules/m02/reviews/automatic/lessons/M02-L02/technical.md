# M02-L02 technical and provenance review

Reviewed 2026-11-12 at draft handoff `0ef85c8`. Scope covers the canonical TCP, UDP and HTTP lesson, its assessment and evidence pack.

## Findings

| ID | Severity | Status | Location | Evidence and suggested change |
| --- | --- | --- | --- | --- |
| M02-L02-T1 | note | optional | `modules/m02/lessons/M02-L02.md:27`, cumulative acknowledgment | The current description conveys cumulative transport receipt. To make the field's boundary explicit, say ACK N identifies the next expected sequence number and cumulatively acknowledges bytes before N. [RFC 9293 §3.1](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.1) |
| M02-L02-T2 | note | optional | `modules/m02/lessons/M02-L02.md:60`, command after position datagrams | Separate the reason to acknowledge a command from the reason to deduplicate it. In this scenario an application acknowledgment reports the command outcome, while deduplication prevents duplicate effects if a non-idempotent command is retried. A command already designed to be idempotent can tolerate repetition under its stated contract. [RFC 8085 §3.3](https://www.rfc-editor.org/rfc/rfc8085.html#section-3.3) · [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) |

## Technical checks

- TCP setup and teardown, cumulative receipt, checksum validation, retransmission and ordering are distinct from application commit. The receive window protects receiver capacity and the congestion window constrains sending according to network conditions. The ordered gap correctly explains delay on a shared TCP connection. The modeled buffer calculations yield `1000 × 128 KiB = 125 MiB`, `400 × 64 KiB = 25 MiB` and a 320-connection ceiling for EX-1. [RFC 9293 §§3.1, 3.5, 3.6 and 3.8](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.1) · [RFC 5681 §3](https://www.rfc-editor.org/rfc/rfc5681.html#section-3)
- UDP datagram delivery, reordering and loss are properly scoped. Acknowledgments and congestion behavior belong to the application or an upper-layer protocol. The DHCP example refers to possible IPv4 broadcast during bootstrap. The HTTP section distinguishes persistent HTTP/1.1, multiplexed HTTP/2 streams on TCP and HTTP/3 streams over QUIC. TLS 1.3's security claim is conditional on the connection and authentication assumptions. [RFC 8085 §§3.1–3.4](https://www.rfc-editor.org/rfc/rfc8085.html#section-3) · [RFC 2131 §4.1](https://www.rfc-editor.org/rfc/rfc2131.html#section-4.1) · [RFC 9112 §9.3](https://www.rfc-editor.org/rfc/rfc9112.html#section-9.3) · [RFC 9113 §5](https://www.rfc-editor.org/rfc/rfc9113.html#section-5) · [RFC 9114 §2](https://www.rfc-editor.org/rfc/rfc9114.html#section-2) · [RFC 8446 §1](https://www.rfc-editor.org/rfc/rfc8446.html#section-1)
- The method table distinguishes intended effects, safety, idempotence and cache eligibility. GET is eligible under the cache rules, POST and PATCH require explicit freshness and matching Content-Location for retrieval reuse, and PUT and DELETE responses are ineligible. PATCH can be designed for idempotent effects without implying that the method guarantees them. The invalidation paragraph correctly scopes the 2xx and 3xx rule to a cache receiving the unsafe exchange. Q5 preserves these distinctions. [RFC 9110 §§9.2–9.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2) · [RFC 5789 §2](https://www.rfc-editor.org/rfc/rfc5789.html#section-2) · [RFC 9111 §4.4](https://www.rfc-editor.org/rfc/rfc9111.html#section-4.4)
- A lost create reply leaves commit uncertain. The lesson and EX-1 require a caller-scoped request identity, an atomic durable deduplication and creation contract, and a defined outcome for matching retries. Q1, Q2, Q3, Q4 and Q6 are consistent with the taught transport and application boundaries. [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

## Provenance and assets

The evidence pack links protocol standards for the relevant behavior and labels the memory and workload inputs as illustrative. The lesson credits Donne Martin, the pinned Primer revision and its CC BY 4.0 notice for topic selection. The Archive claim matrix is linked for history. The worked scenarios, method summary and assessment use Academy prose without external diagrams, code or reproduced figures. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt)

**Verdict: ready-for-human-review.** The reviewed package has no open technical or provenance finding requiring a correction round.

## Round 1 targeted re-review

Reviewed `0ef85c8..371735c` for the canonical lesson, assessment and evidence. The companion's LO2 front matter and outcome table now both include `UDP datagrams and application responsibility`. That section teaches the ordering, loss and congestion behavior needed to justify the temperature-reading transport in EX-1. The scenarios, answer keys, protocol claims and cited sources are unchanged in this diff. [RFC 8085 §§3.1 and 3.3](https://www.rfc-editor.org/rfc/rfc8085.html#section-3.1)

| Finding | Status | Evidence |
| --- | --- | --- |
| L02-P1 | resolved | The M02-L02 companion includes the same UDP heading in the YAML outcome map and the narrative row for LO2. |

**Round 1 verdict: ready-for-human-review.**
