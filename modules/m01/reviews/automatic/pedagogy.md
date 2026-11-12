# M01 independent pedagogy and curriculum-coverage review

Round 0, 2026-11-12. Scope covers M01-L01–L04, their companion assessments, and the M01 integrated brief, solution and decision summary. Audience is experienced middle/senior engineers. The approved teaching scope and outcome expectations are in [SDA-v1 M01](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01--workload-performance-and-distributed-guarantees). The topic map is the [pinned System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733) at revision ae9bbd7b02d90b9866215de185217d33f39ab733 and the approved [coverage matrix](../../../../curriculum/revision-1/coverage.csv). No matching prevention reminders were supplied.

## Coverage findings

- **P-1 · major · open · M01-L01, Budget the latency of a request path, line 54; PR-H161, PR-H162 and the eight repeated case latency-number references.** The three numerical scales are presented solely as conversions. No operation is assigned to any of the scales, so the learner cannot use them to compare plausible memory, storage and network access costs. The link to the historical table is useful context, but linking alone does not teach the planned topic. The approved outline explicitly assigns latency orders of magnitude and the case repetitions to M01-L01, with dated values treated as intuition. Add a compact operation-linked example using accurately attributed historical values, or explicitly stipulated hypothetical measurements for a named system. Explain that devices, sizes, topology and dates change the figures and that production design requires measurements. Keep the source IDs mapped to the actual explanatory section. [Approved M01-L01 outline](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l01) · [Patterson, historical latency comparison, Table 1](https://pages.cs.wisc.edu/~markhill/restricted/cacm2004_latency.pdf#page=2)

## Pedagogy and outcome findings

- **P-2 · major · open · M01-L01 lesson Learning outcomes; companion front matter and Outcome map; integrated outcome-portfolio.json M01-L01-LO1.** The learner-facing LO1 includes a request-path latency estimate, but the outcome map lists only Q1–Q3, which measure rate, units and storage. Q4 asks for precisely the serial and parallel latency calculation, and Q5/Q6 assess other modeled LO1 elements. The portfolio also lists only Q1–Q3 and omits the actual latency teaching section for LO1. Add Q4 and the latency section to the LO1 map while preserving Q4's decision assessment for LO2. Consider mapping Q5/Q6 or EX-1 to LO1 where their arithmetic is used, and synchronize the companion's front matter, narrative table and integrated portfolio. This preserves the planned Q1–Q3 and Q4–Q6 assignments while making the broader learner-facing claim auditable. [Approved M01-L01 outcome and quick-check plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l01) · [Authoring format contract, Required metadata](../../../../docs/authoring-format-contract-v1.md#required-metadata)
- **P-3 · major · open · M01-L04 lesson Learning outcomes; companion front matter and Outcome map; integrated outcome-portfolio.json M01-L04-LO1.** The learner-facing LO1 includes an availability-budget calculation. Its mapped Q1–Q3 evaluate restoration time, recovery point and dependency probability, but none asks for a time budget. EX-1 explicitly calculates the 30-day budget and maps only to LO2. Map EX-1 to LO1 as well and keep its LO2 mapping, updating the companion front matter, narrative outcome table and portfolio together. The lesson's “Convert an availability target into a budget” section already teaches it. [Approved M01-L04 outcome and quick-check plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04) · [Authoring format contract, Required metadata](../../../../docs/authoring-format-contract-v1.md#required-metadata)

The module's other exercise and knowledge-check items are accompanied by explanations and map to teaching that provides the requested mechanism or decision. The exercise brief teaches its specific barrier assumptions before asking learners to trace them. The four lesson companions each contain a separate exercise, sample solution, rubric and six knowledge checks. Module prerequisite M00-L02 is named and is outside this review's assigned scope.

## Artifact verdicts

| Artifact pair or package | Verdict | Evidence |
| --- | --- | --- |
| M01-L01 lesson and assessment | revise | P-1 and P-2 |
| M01-L02 lesson and assessment | ready-for-human-review | Burst trace, Little's Law assumptions, scaling choices and assessment items are aligned. |
| M01-L03 lesson and assessment | ready-for-human-review | Histories, partition choices, session eligibility and conflict resolution are taught and assessed. |
| M01-L04 lesson and assessment | revise | P-3 |
| M01 integration brief, solution and decision summary | revise | The exercise supports M01-S1. The outcome portfolio must follow the companion mapping fixes in P-2 and P-3. |

## Coverage ledger

The statuses below are reviewer judgments based on the actual explanatory text. `merged` means that a repeated Primer topic is deliberately taught in its owning M01 mechanism. The plan's topic IDs and locators are retained for traceability.

| Topic and source locator | Lesson and actual section | Status and teaching evidence | Assessment |
| --- | --- | --- | --- |
| PR-H016, Back-of-the-envelope calculations, README.md#L270 | [M01-L01, Estimate demand from an activity feed](../../lessons/M01-L01.md) | taught; the named section explains the mapped mechanism or decision | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-H032, Performance vs scalability, README.md#L412 | [M01-L02, Measure the request and the workload](../../lessons/M01-L02.md) | taught; the named section explains the mapped mechanism or decision | [M01-L02 companion](../../assessments/M01-L02.md) |
| PR-H034, Latency vs throughput, README.md#L426 | [M01-L02, Measure the request and the workload](../../lessons/M01-L02.md) | taught; the named section explains the mapped mechanism or decision | [M01-L02 companion](../../assessments/M01-L02.md) |
| PR-H036, Availability vs consistency, README.md#L438 | [M01-L03, Choose operations during a partition](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H037, CAP theorem, README.md#L440 | [M01-L03, Choose operations during a partition](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H038, CP - consistency and partition tolerance, README.md#L456 | [M01-L03, Choose operations during a partition](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H039, AP - availability and partition tolerance, README.md#L460 | [M01-L03, Choose operations during a partition](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H041, Consistency patterns, README.md#L473 | [M01-L03, Read and write histories](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H042, Weak consistency, README.md#L477 | [M01-L03, Read and write histories](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H043, Eventual consistency, README.md#L483 | [M01-L03, Read and write histories](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H044, Strong consistency, README.md#L489 | [M01-L03, Read and write histories](../../lessons/M01-L03.md) | taught; the named section explains the mapped mechanism or decision | [M01-L03 companion](../../assessments/M01-L03.md) |
| PR-H046, Availability patterns, README.md#L499 | [M01-L04, Choose traffic roles and standby readiness](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H047, Fail-over, README.md#L503 | [M01-L04, Trace a two-region recovery](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H048, Active-passive, README.md#L505 | [M01-L04, Choose traffic roles and standby readiness](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H049, Active-active, README.md#L513 | [M01-L04, Choose traffic roles and standby readiness](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H050, Disadvantage(s): failover, README.md#L521 | [M01-L04, Choose traffic roles and standby readiness](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H051, Replication, README.md#L526 | [M01-L04, Replication and recovery points](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H052, Master-slave and master-master, README.md#L528 | [M01-L04, Replication and recovery points](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H053, Availability in numbers, README.md#L535 | [M01-L04, Convert an availability target into a budget](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H054, 99.9% availability - three 9s, README.md#L539 | [M01-L04, Convert an availability target into a budget](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H055, 99.99% availability - four 9s, README.md#L548 | [M01-L04, Convert an availability target into a budget](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H056, Availability in parallel vs in sequence, README.md#L557 | [M01-L04, Model serial, parallel and shared dependencies](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H057, In sequence, README.md#L561 | [M01-L04, Model serial, parallel and shared dependencies](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H058, In parallel, README.md#L571 | [M01-L04, Model serial, parallel and shared dependencies](../../lessons/M01-L04.md) | taught; the named section explains the mapped mechanism or decision | [M01-L04 companion](../../assessments/M01-L04.md) |
| PR-H158, Appendix, README.md#L1577 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | merged; appendix timing scope belongs to this lesson, subject to P-1 | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-H159, Powers of two table, README.md#L1581 | [M01-L01, Budget storage, bandwidth and the working set](../../lessons/M01-L01.md) | taught; the named section explains the mapped mechanism or decision | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-H161, Latency numbers every programmer should know, README.md#L1600 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-H162, Latency numbers visualized, README.md#L1637 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-PASTEBIN-H022, pastebin: Latency numbers, solutions/system_design/pastebin/README.md#L325 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-TWITTER-H022, twitter: Latency numbers, solutions/system_design/twitter/README.md#L326 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-WEB_CRAWLER-H023, web_crawler: Latency numbers, solutions/system_design/web_crawler/README.md#L346 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-MINT-H022, mint: Latency numbers, solutions/system_design/mint/README.md#L434 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-SOCIAL_GRAPH-H019, social_graph: Latency numbers, solutions/system_design/social_graph/README.md#L342 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-QUERY_CACHE-H022, query_cache: Latency numbers, solutions/system_design/query_cache/README.md#L299 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-SALES_RANK-H020, sales_rank: Latency numbers, solutions/system_design/sales_rank/README.md#L331 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |
| PR-SCALING_AWS-H045, scaling_aws: Latency numbers, solutions/system_design/scaling_aws/README.md#L396 | [M01-L01, Budget the latency of a request path](../../lessons/M01-L01.md) | mention-only; P-1, scales are not attached to actual operations | [M01-L01 companion](../../assessments/M01-L01.md) |

## Sequence and scope

The lessons progress from capacity estimation to scaling, consistency and failover, consistent with the approved prerequisites. The integrated exercise combines those decisions without claiming to assess every lesson outcome. No additional missing source heading in the 36 assigned M01 rows was found beyond P-1. P-1 is a material teaching-depth gap rather than an omitted source ID.

**Overall verdict: revise.** Open findings P-1, P-2 and P-3 require targeted correction before a clear review verdict. This assessment covers pedagogy and source-topic coverage.

## Round 1 targeted re-review

Reviewed the changes from commit `7dc09fc` through `c1a5f0c`, their companion assessments and the outcome portfolio. The following statuses supersede the round 0 findings and artifact verdicts above.

| Finding | Status | Supporting curriculum evidence | Re-review observation |
| --- | --- | --- | --- |
| P-1 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md#m01-l01 | [Budget the latency of a request path](../../lessons/M01-L01.md#budget-the-latency-of-a-request-path) now connects explicitly hypothetical memory access, small device read and remote round-trip durations to concrete comparison and profiling decisions. It states measurement conditions and the limits of historical figures. |
| P-2 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md#m01-l01 | The [L01 companion](../../assessments/M01-L01.md#outcome-map) and [portfolio](../../integrated/outcome-portfolio.json) now map Q4 and the latency section to LO1 while retaining Q4 for LO2. The additional mapped items assess the corresponding workload mechanisms. |
| P-3 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04 | The [L04 companion](../../assessments/M01-L04.md#outcome-map) and [portfolio](../../integrated/outcome-portfolio.json) now map EX-1 to both outcomes. The exercise asks for the time budget and its sample solution supplies the calculation. |

The round 0 `mention-only` judgments for PR-H161, PR-H162 and the eight repeated case latency-number references are superseded by **merged, taught**. Their shared latency-scale teaching is now in the L01 section named in the coverage ledger. PR-H158 remains merged into that section. The round 0 table remains as the review history.

The integrated brief now specifies that West rejects the attempted write before forwarding, applying or queueing it, and the solution and rubric use that same event. The recovery trace is answerable without assuming an unobserved retry. The additional timed-out-request note identifies the need to resolve an uncertain outcome and does not change the exercise's specified trace.

| Current artifact pair or package | Verdict |
| --- | --- |
| M01-L01 lesson and assessment | ready-for-human-review |
| M01-L02 lesson and assessment | ready-for-human-review |
| M01-L03 lesson and assessment | ready-for-human-review |
| M01-L04 lesson and assessment | ready-for-human-review |
| M01 integration brief, solution, decision summary and outcome portfolio | ready-for-human-review |

**Round 1 overall verdict: ready-for-human-review.** P-1, P-2 and P-3 are resolved. This verdict covers pedagogy and curriculum coverage.
