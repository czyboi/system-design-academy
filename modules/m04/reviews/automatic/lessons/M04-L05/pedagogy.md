# M04-L05 pedagogy and curriculum coverage review

Reviewed the canonical lesson, assessment and evidence at draft handoff `a01124b` for middle and senior engineers. The scope is the [approved M04-L05 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l05), assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the pinned Primer at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`, including its [SQL tuning section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L941-L982) and [crawler](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/README.md#L295), [social graph](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/social_graph/README.md#L291), [query cache](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/query_cache/README.md#L248) and [scaling AWS](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/scaling_aws/README.md#L345) scaling-pattern entries.

## Coverage

| Assigned topics | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H100, SQL tuning | taught | **Find the expensive work** links statement statistics and measured plans to the workload. Q1–Q3 and EX-1 interpret plan evidence. |
| PR-H101, schema | taught | **Tighten storage and account for index cost** covers domain range, nullability, numeric precision, character types and external bytes. EX-1 asks for a verified schema change. |
| PR-H102, indexes | taught | **Walk two plans under one workload** and **Tighten storage and account for index cost** cover composite B-trees, write and storage costs, bulk loading and index rebuild considerations. Q5 and EX-1 apply the trade-offs. |
| PR-H103 and PR-H104, joins and partitions | taught | **Walk two plans under one workload** limits before enrichment with its semantic condition. **Separate pruning, scaling and caching** explains partition pruning and hot ranges. Q2, Q4 and EX-1 apply these ideas. |
| PR-H105, query cache | taught | **Separate pruning, scaling and caching** scopes server query-cache advice to MySQL 5.7 and its removal in 8.0, then identifies application cache requirements. Q6 assesses the version distinction. |
| PR-WEB_CRAWLER-H017, PR-SOCIAL_GRAPH-H013, PR-QUERY_CACHE-H016, PR-SCALING_AWS-H039 | taught | **Decide by the measured bottleneck** applies the shared scaling comparison to a crawler query, social graph summary, query-service cache and hosted application workloads. It contrasts tuning, replicas, denormalisation, federation, sharding and application caching by workload and transaction boundary. EX-1 compares tuning, replicas and sharding for a specific diagnosis. |

## Pedagogy and assessment

The hypothetical plan trace identifies the per-loop output and changes the query shape only because enrichment does not affect eligibility or ordering. It preserves zero-line headers and qualifies the figures as assumptions for measurement. EX-1 presents a related invoice workload, asks for preserved zero counts and calculates 6,000 versus 40 emitted rows. Its ten-minute cohorts are 1,000 original requests per variant. The sample scores 97% and 98.5% against the 99% within 250 ms target and keeps rejected, timed-out and late requests in the denominator.

LO1 maps to Q1–Q3 and EX-1, and LO2 maps to Q4–Q6 and EX-1, with corresponding teaching sections named in both outcome maps. The separate companion includes six explained checks, a practical exercise, a sample solution and a point-bearing rubric. The design accepts equivalent solutions with the specified semantics.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the revised lesson and companion at `6d5ed71`. **Walk two plans under one workload** now specifies separate average row counts for the baseline and selected population, explains that node output alone does not establish total work or latency, and teaches the left join, non-null count and final ordering needed by the stated query. EX-1 supplies its own separate averages, and its updated answer and rubric use 6,000 and 60 emitted rows while preserving zero adjustments and ordering. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l05) calls for comparing plans and query-shape changes under the same workload.

The original 1,000-request cohorts, 97% and 98.5% timely success results, 250 ms threshold and ten-minute window remain intact. Outcome maps and the previously reviewed topic dispositions remain supported.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
