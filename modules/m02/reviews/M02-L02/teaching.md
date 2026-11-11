# M02-L02 actual coverage and pedagogy review

## Scope and sources

Reviewed the declared teaching and companion pair for middle and senior engineers against SDA-v1. Independently checked the [pinned Primer communication, HTTP, TCP and UDP sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1370-L1440), revision ae9bbd7b02d90b9866215de185217d33f39ab733. Checked the source-era method table against RFC 9110 and RFC 5789. Considered prior M01-L02 feedback on exercise transfer and exact outcome evidence.

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
| PR-BODY-R1-HTTP-METHODS | HTTP requests and method semantics | planned-not-taught | README.md#L1386–L1390. Safety and idempotence are explained, but the source table's five-method cacheability dimension is incomplete. See NET-C1. |

## Pedagogy and assessment

The English lesson motivates protocol selection through file delivery and time-sensitive positions, then develops the transport and HTTP decisions with examples and failure modes. LO1 maps to Core concepts and mechanisms and the worked trace, and is assessed by Q1–Q3 and EX-1. LO2 maps to Decision framework and Trade-offs and failure modes, and is assessed by Q4–Q6 and EX-1. The industrial-dashboard exercise transfers the delivery and retry mechanisms and gives a fresh buffer budget. The 320-connection answer is correct under the buffer-only assumption. The six checks each include an explanation and the rubric accepts justified alternatives. Adjacent coverage boundaries are clear. Advanced shared CDN policies belong in M02-L04.

## Findings

- **NET-C1, major.** In HTTP requests and method semantics, the only specific cacheability rule concerns GET. The text says POST has explicit conditions without stating them, and gives no PATCH, PUT or DELETE cacheability rules. The approved teaching sequence requires the source-era table details to be verified, and the assigned body topic explicitly lists safety, idempotence and cacheability. A learner cannot apply the cacheability dimension to four of the five listed methods. Add the verified response rules concisely. POST and PATCH each require explicit freshness and a matching Content-Location, with eligible reuse for GET or HEAD. PUT and DELETE responses are not cacheable. Keep method semantics distinct from the cache's applicable policy and any response invalidation. [RFC 9110 §§9.3.3–9.3.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.3.3), [RFC 5789 §2](https://www.rfc-editor.org/rfc/rfc5789.html#section-2)

## Verdict

revise.
