# M02-L02 revised actual coverage and pedagogy review

## Scope and sources

Rechecked the revised draft lesson and companion for middle and senior engineers against the approved SDA-v1 outline, exact evidence and [pinned Primer communication section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1370-L1440), revision ae9bbd7b02d90b9866215de185217d33f39ab733. The first review inspected all source locators. This review compared the revisions and rechecked the full current teaching and companion pair.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H144 | Core concepts and mechanisms | taught | README.md#L1370. Distinguishes application semantics and transport behavior across the protocol sections. LO1 and LO2. |
| PR-H145 | HTTP requests and method semantics | taught | README.md#L1378. Models request and response fields, connections, multiplexing and method effects. LO1 and LO2, Q5–Q6. |
| PR-H147 | TCP connections, delivery and budgets | taught | README.md#L1402. Traces establishment and closure, reliable ordered delivery, head-of-line delay and connection state. LO1, Q1–Q2 and EX-1. |
| PR-H148 | UDP datagrams and application responsibility | taught | README.md#L1426. Explains datagram boundaries, lost or reordered messages, and responsibility for missing reliability and congestion policies. LO1 and LO2, Q3 and EX-1. |
| PR-BODY-R1-TCP-FLOW | TCP connections, delivery and budgets | taught | README.md#L1415. Separates receiver-advertised capacity from congestion constraints in the network. LO1 and LO2. |
| PR-BODY-R1-TCP-POOL | TCP connections, delivery and budgets | taught | README.md#L1417. Explains state and buffers, why pooling avoids setup, and a pool memory calculation. LO2, Q4 and EX-1. |
| PR-BODY-R1-TCP-CHECK | TCP connections, delivery and budgets | taught | README.md#L1412. Explains sequence ranges, checksums, acknowledgments and retransmission, while distinguishing transport receipt from application commit. LO1, Q1–Q2. |
| PR-BODY-R1-UDP-BROADCAST | UDP datagrams and application responsibility | taught | README.md#L1436. Explains local IPv4 DHCP bootstrap and application responsibility for ordering, delivery and congestion. LO1 and LO2, Q3 and EX-1. |
| PR-BODY-R1-HTTP-METHODS | HTTP requests and method semantics | taught | README.md#L1386–L1390. Compares the requested effect, safety, idempotence and response cacheability of five methods. Explains when POST and PATCH results can serve a later retrieval and how successful unsafe requests affect stored responses. LO2, Q5. |

All nine assigned topics are now taught. The added comparison gives practical cacheability rules at the HTTP semantics boundary. The details of edge population, cache keys and rollout remain in M02-L04.

## Pedagogy and assessment

The lesson still moves from reliable file delivery and time-sensitive positions to the mechanisms and the worked trace. LO1 retains Q1–Q3 and the transfer exercise. The method table gives the revised Q5 its exact teaching evidence. Q5 makes learners distinguish intended effects from status codes, then apply separate DELETE and PATCH response rules. LO2 still uses Q4–Q6 and EX-1. The ticketing exercise applies the method to different inputs and adds atomic deduplication to the sample answer, supported by the lesson's create-request example. Both outcome maps and all item references are present. The six explained checks and 10-point rubric remain aligned and accept justified alternatives.

## Findings and prior disposition

- **NET-C1, resolved.** The table explicitly distinguishes GET eligibility, POST and PATCH freshness and matching target requirements, and PUT and DELETE response ineligibility. It separates later GET or HEAD reuse from mutation processing and explains why an unsafe request through one cache does not update every cache. [RFC 9110 §§9.3.3–9.3.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.3), [RFC 5789 §2](https://www.rfc-editor.org/rfc/rfc5789.html#section-2), [RFC 9111 §4.4](https://datatracker.ietf.org/doc/html/rfc9111#section-4.4)

No new material coverage, pedagogy or language finding identified.

## Verdict

ready-for-human-review.
