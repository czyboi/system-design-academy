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

## Human-feedback targeted re-review, 2026-11-13

Reviewed the changed lesson and companion at `fdbe268` against the [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02) and the prior topic ledger. The existing topic dispositions remain supported. TCP acknowledgment, datagram responsibility, retry identity and pool budgeting are taught in the mapped lesson sections. EX-1 requires a latency and connection-budget choice, a lost-response trace, overload handling and measurement. Its scoring awards credit to delivery choices, safe retries, capacity and verification, and permits alternative transports. The six explained checks remain mapped, including the UDP teaching section for LO2.

| Finding | Severity | Status | Evidence |
| --- | --- | --- | --- |
| P-MS02-HUMAN-L02-1 | note | resolved | [Lesson, Worked example](../../../../lessons/M02-L02.md#worked-example) and [assessment, Answer key / rubric](../../../../assessments/M02-L02.md#answer-key--rubric) |

**Current verdict: ready-for-human-review.** Coverage and pedagogy only.

## Human SLO-feedback targeted re-review, 2026-11-13

Reviewed the `3566553..6131840` change to [EX-1](../../../../assessments/M02-L02.md#practical-exercise) and its [answer and rubric](../../../../assessments/M02-L02.md#answer-key--rubric) against [PR #66 feedback](https://github.com/czyboi/system-design-academy/pull/66#issuecomment-6846111131). The scenario defines a 60-second population of intended reading/dashboard pairs, a 98% delivery threshold and a separate 95% display threshold among timely deliveries. The model counts missed and late deliveries in the delivery denominator, counts obsolete discards as display misses, follows end-of-window readings through their deadlines and illustrates a failed delivery target despite acceptable display latency. The rubric awards one point to each measurement. The lesson's datagram delivery and measured workload sections support the assessment, and the existing EX-1 outcome mappings remain appropriate.

| Finding | Severity | Status | Evidence |
| --- | --- | --- | --- |
| P-MS02-PR66-L02-1 | major | resolved | [Approved M02-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02) and [lesson, Worked example](../../../../lessons/M02-L02.md#worked-example) |

**Current verdict: ready-for-human-review.** Targeted pedagogy re-review only.

## Publication-readiness targeted re-review at 0dcef2a, 2026-11-13

Reviewed `3c0205c..0dcef2a` for M02-L02 against [PR #66 feedback](https://github.com/czyboi/system-design-academy/pull/66#issuecomment-6846736588), the [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02), and the assigned [coverage rows](../../../../../../curriculum/revision-1/coverage.csv). Audience: middle/senior engineers in English self-study. The source map is the [Primer communication section, lines 1370–1440](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1370-L1440), pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. This is a targeted re-review; the earlier ledger and finding history are retained.

### Pedagogy and outcome evidence

| ID | Severity | Status | Location, learner impact and evidence |
| --- | --- | --- | --- |
| P-MS02-PR66-L02-2 | note | resolved | [Packet loss across multiplexed requests](../../../../lessons/M02-L02.md#packet-loss-across-multiplexed-requests) traces the lost A data, arrival of B, and recovery for each transport; it explains why the TCP gap holds B and why QUIC stream independence can permit B to progress. Shared congestion, server saturation, within-stream blocking and uncertain business outcomes qualify the comparison. A learner can follow the mechanism without Q7's key. |
| P-MS02-PR66-L02-3 | note | resolved | [Q7 and outcome map](../../../../assessments/M02-L02.md#q7) ask the learner to compare the trace and provide an explanation; both front matter and narrative map name the new teaching section and Q7 for LO1 and LO2. Q7 assesses comparative consequences; LO2's choice and defense are also measured by Q4–Q6 and EX-1. L02-P1 remains resolved in both mappings. |
| P-MS02-PR66-L02-1 | major | resolved | [EX-1 and rubric](../../../../assessments/M02-L02.md#practical-exercise) retain separate intended-delivery and timely-display populations and thresholds, include loss and late work, and accept defensible alternative transports. The changed trace does not contradict the exercise or its assessment of the existing datagram, retry and pool instruction. |

### Targeted coverage disposition

The existing ledger remains supported by actual instruction: PR-H144, PR-H145 and PR-BODY-R1-HTTP-METHODS are taught in HTTP requests and method semantics; PR-H147, PR-BODY-R1-TCP-FLOW, PR-BODY-R1-TCP-POOL and PR-BODY-R1-TCP-CHECK in TCP connections, delivery and budgets; and PR-H148 and PR-BODY-R1-UDP-BROADCAST in UDP datagrams and application responsibility. The new trace adds a concrete cross-stream loss comparison to the HTTP/TCP instruction. No assigned row becomes mention-only, assessment-only or omitted. The approved LO1 trace and LO2 decision outcomes remain taught and assessed; M02-L01 remains the stated prerequisite. No material coverage or sequencing gap was introduced in the reviewed scope.

**Verdict: ready-for-human-review.** This is a pedagogy and assigned curriculum-coverage verdict, not technical or publication approval.

## Correction targeted re-review at 954dba2, 2026-11-13

Reviewed `0dcef2a..954dba2` in the lesson, companion and evidence, with adjacent exercise and outcome mappings, against the [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-l02) and the assigned pinned-Primer rows recorded above.

| ID | Severity | Status | Re-review evidence and learner impact |
| --- | --- | --- | --- |
| P-MS02-PR66-L02-2 | note | resolved | [Packet loss across multiplexed requests](../../../../lessons/M02-L02.md#packet-loss-across-multiplexed-requests) now specifies A-only loss and contiguous, ordered B data, traces recovery and explains that a gap in B, shared congestion or HTTP dependencies can still delay B. The narrowed example supports a causal comparison without promising an overall latency result. The retry paragraph distinguishes known idempotence or non-application from the unknown ticket-creation outcome and points back to its durable deduplication example. |
| P-MS02-PR66-L02-3 | note | resolved | [Q7](../../../../assessments/M02-L02.md#q7) now asks for both the trace and a defended choice for isolating B, with a remaining limitation; its explained answer follows the taught scenario. Front matter and narrative outcome maps include Q7 and the exact trace heading for LO1 and LO2, and the narrative describes the choice. L02-P1 remains resolved: both LO2 maps still name UDP instruction. |
| P-MS02-PR66-L02-1 | major | resolved | [EX-1 and rubric](../../../../assessments/M02-L02.md#practical-exercise) retain the distinct delivery and display populations, deadlines, failure accounting, retry contract and alternative transport credit. The revised trace and retry discussion introduce no adjacent pedagogical contradiction. |

The earlier assigned coverage ledger remains supported by instruction; the changes deepen the mapped HTTP/TCP loss and retry explanation without removing UDP, resource-budget or method teaching. No material coverage or pedagogy gap was found in the changed scope.

**Verdict: ready-for-human-review.** This is a targeted pedagogy and curriculum-coverage verdict, not technical or publication approval.
