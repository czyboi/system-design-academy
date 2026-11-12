# M02-L02 pedagogy and curriculum coverage review

Round 0, 2026-11-12. Reviewed the canonical lesson, companion and evidence for middle and senior engineers against the [approved M02-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02), [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv), and [pinned Primer communication section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1370-L1440) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The archived revised review supplied historical context.

## Finding

| ID | Severity | Status | Location and impact | Targeted correction |
| --- | --- | --- | --- | --- |
| L02-P1 | major | open | `modules/m02/assessments/M02-L02.md`, LO2 front matter and Outcome map. LO2 includes choosing transport behavior and EX-1 asks the learner to choose a datagram delivery policy, but the LO2 teaching-section list omits the lesson's UDP mechanism section. A learner or progress consumer following the map cannot identify the section teaching that assessed choice. | Add the exact heading `UDP datagrams and application responsibility` to both LO2 teaching-section entries. Keep EX-1 and Q4–Q6 mapped to LO2. [Approved M02-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02) · [Authoring format contract](../../../../../../docs/authoring-format-contract-v1.md#required-metadata) |

## Coverage ledger

| Topic ID | Teaching evidence | Disposition |
| --- | --- | --- |
| PR-H144 | [HTTP requests and method semantics](../../../../lessons/M02-L02.md#http-requests-and-method-semantics) explains request/response communication in the file and game workload. | taught |
| PR-H145 | HTTP requests and method semantics describes methods, fields and connection behavior. | taught |
| PR-H147 | [TCP connections, delivery and budgets](../../../../lessons/M02-L02.md#tcp-connections-delivery-and-budgets) explains setup, teardown and ordered delivery. | taught |
| PR-H148 | [UDP datagrams and application responsibility](../../../../lessons/M02-L02.md#udp-datagrams-and-application-responsibility) explains message boundaries and loss, ordering and recovery responsibilities. | taught |
| PR-BODY-R1-TCP-FLOW | TCP connections, delivery and budgets distinguishes the receiver window from network congestion constraints. | taught |
| PR-BODY-R1-TCP-POOL | TCP connections, delivery and budgets explains connection costs and calculates reserved buffer memory. | taught |
| PR-BODY-R1-TCP-CHECK | TCP connections, delivery and budgets explains sequence positions, checksums, acknowledgment and retransmission. | taught |
| PR-BODY-R1-UDP-BROADCAST | UDP datagrams and application responsibility covers IPv4 DHCP bootstrap, application recovery and congestion response. | taught |
| PR-BODY-R1-HTTP-METHODS | HTTP requests and method semantics compares the requested effect, safety, idempotence and caching of all five assigned methods. | taught |

## Outcomes and assessment

LO1's TCP, UDP and request behavior is taught across the three protocol sections and Worked example. Q1–Q3 assess transport acknowledgment, ordered-byte delay and UDP delivery evidence. EX-1 applies missing-message and lost-response reasoning. LO2's decisions are taught in the protocol sections, Trade-offs and failure modes, and Decision framework. Q4–Q6 assess resource budgeting, method effects and safe retries. EX-1 additionally requires a datagram policy and connection calculation. The companion contains six explained checks, a practical exercise, sample answer and ten-point rubric. The lesson identifies M02-L01 as its prerequisite.

**Verdict: revise.** L02-P1 requires an outcome-map correction. This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the correction at `371735c`. The LO2 front matter and narrative outcome map both include the exact `UDP datagrams and application responsibility` teaching heading. EX-1 remains mapped to LO2 and asks the learner to choose delivery behavior for readings, including handling a missing message. The named lesson section teaches the datagram and recovery choices. Q4–Q6 remain mapped to LO2.

| Finding | Status | Supporting curriculum evidence |
| --- | --- | --- |
| L02-P1 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |

**Round 1 verdict: ready-for-human-review.** The revised outcome map addresses the finding.
