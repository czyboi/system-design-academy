# M01-L01 pedagogy and curriculum coverage review

Reviewed in lesson mode against the approved [M01-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l01), task specification and actual lesson, companion and evidence. The intended audience is middle and senior engineers with the stated M00-L02 prerequisite. No learning-memory reminders were supplied. The source topic map is the [System Design Primer pinned at ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733). Assigned topic locators and their disposition are drawn from the approved [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv).

## Assigned topic coverage

| Topic and source locator | Actual teaching and assessment evidence | Status |
| --- | --- | --- |
| PR-H016, back-of-the-envelope calculations, `README.md#L270` | [Estimate demand](../../../../lessons/M01-L01.md#estimate-demand-from-an-activity-feed) converts event counts into rates and a peak. [Storage, bandwidth and working set](../../../../lessons/M01-L01.md#budget-storage-bandwidth-and-the-working-set) explains the remaining estimates. Companion Q1, Q3, Q5, Q6 and EX-1 assess them. | taught |
| PR-H158, appendix, `README.md#L1577` | [Latency budget](../../../../lessons/M01-L01.md#budget-the-latency-of-a-request-path) connects timing scales and sequential and overlapping calls to measurement, while the storage section explains unit prefixes. Q2 and Q4 assess these elements. | merged with the assigned appendix topics |
| PR-H159, powers of two, `README.md#L1581` | The storage section explains decimal and binary byte prefixes and conversion. Q2 assesses the distinction. | taught |
| PR-H161, latency numbers, `README.md#L1600` | The latency section assigns hypothetical durations to memory, device and remote operations, compares them, and calls for measurements under current conditions. Q4 assesses a request trace. | taught |
| PR-H162, latency visualization, `README.md#L1637` | The same operation-linked comparison explains relative magnitudes in text and identifies why measurements change. Q4 assesses latency reasoning. | merged with PR-H161 |
| PR-PASTEBIN-H022, `solutions/system_design/pastebin/README.md#L325` | The repeated latency topic is explained in the latency section using the same operation-linked example. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-TWITTER-H022, `solutions/system_design/twitter/README.md#L326` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-WEB_CRAWLER-H023, `solutions/system_design/web_crawler/README.md#L346` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-MINT-H022, `solutions/system_design/mint/README.md#L434` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-SOCIAL_GRAPH-H019, `solutions/system_design/social_graph/README.md#L342` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-QUERY_CACHE-H022, `solutions/system_design/query_cache/README.md#L299` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-SALES_RANK-H020, `solutions/system_design/sales_rank/README.md#L331` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |
| PR-SCALING_AWS-H045, `solutions/system_design/scaling_aws/README.md#L396` | The repeated latency topic is explained in the latency section. Q4 assesses trace reasoning. | merged with PR-H161 |

The repeated case references map to the common timing topic in this lesson. The worked comparison explains the mechanism rather than treating the historical table as a current benchmark. No assigned topic has a material missing disposition.

## Lesson-first comprehension and assessment

The feed example provides the initial inputs and boundaries, derives average and peak rates, then computes retention, copies, overhead, margins, per-interface bandwidth and distinct working-set size. The request trace establishes the dependency that makes stages serial, computes the overlapping alternative and names its resource cost. The low/high range and instructions to measure saturation and client-facing latency connect the estimates to the eventual design choice. The stated assumptions enable a learner to reproduce the central reasoning using the lesson itself.

| Outcome | Teaching evidence | Companion assessment evidence |
| --- | --- | --- |
| M01-L01-LO1, model workload and path latency | Demand, storage, bandwidth, working set and request-path examples in the [lesson](../../../../lessons/M01-L01.md). | [Companion](../../../../assessments/M01-L01.md) Q1–Q6 and EX-1 test rates, units, replicated storage, latency, distinct access, bandwidth and an integrated workload. |
| M01-L01-LO2, choose and defend assumptions and alternatives | Peak range, interface boundaries, parallelism cost and measurement in the lesson's latency and refinement sections. | Q4 asks for the concurrency and measurement decision, Q5 and Q6 test assumption boundaries, and EX-1 compares budgets, identifies measurements and asks for a high-case alternative. |

The exercise has a separate sample solution and rubric, accepts defensible alternatives, and is supported by the taught methods. The six explained checks cover the planned outcomes. The material is appropriately scoped to the declared audience and prerequisite, with no material sequence or audience finding.

No open blocker, major or minor findings were identified for the assigned coverage and pedagogy scope.

**Verdict: ready-for-human-review.**
