# M05-L02 pedagogy and curriculum coverage review

Reviewed the canonical lesson, assessment and evidence at draft handoff `adc6c52` for middle and senior engineers. The scope is the [approved M05-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l02), its assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the pinned Primer [wide-column and graph sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1039-L1078) and [architecture entries](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1701-L1703), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H112, wide-column store | taught | **Design wide rows for their range queries** explains ordered row keys, families, sparse qualifiers and bucketing. Q1–Q2 and EX-1 apply locality and range fan-out. |
| PR-H114, graph database | taught | **Walk two hops from an indexed seed** models vertices, directed edges, adjacency and index use. Q3, Q6 and EX-1 trace traversal and its costs. |
| PR-ARCH-BIGTABLE | taught | The first two sections explain Bigtable key ordering, timestamped cell versions and family retention. Q1, Q4 and EX-1 apply the model. |
| PR-ARCH-HBASE | taught | **Separate retained versions from conflict timestamps** identifies HBase timestamped cells and family version settings alongside Bigtable, while marking read controls and defaults as product-specific. |
| PR-ARCH-CASSANDRA | taught | The same section contrasts partition and clustering keys and mutation timestamps with retained cell versions. Q5 and EX-1 ask for the distinction. |
| PR-BODY-R1-WIDE-VERSIONS | taught | The first two sections distinguish event time from stored cell-version timestamps and describe retention, delayed garbage collection and explicit read filtering. Q4 and EX-1 apply the semantics. |

## Pedagogy and assessment

The lesson connects a time-first hot range to device-prefixed keys and bounded bucket fan-out. Its worked example explains why four buckets across two days need eight ranges. The graph trace starts from an indexed vertex, expands B and C, removes the seed and duplicate D, and returns D and E. It then connects a remote supernode to explicit incomplete results or asynchronous exhaustive enumeration.

LO1 maps to the range, version and two-hop mechanisms and Q1–Q3 plus EX-1. LO2 maps to the same mechanisms and the selection criteria, with Q4–Q6 plus EX-1 assessing retention, correction history and traversal costs. The companion supplies six explained checks and a practical exercise with sample answer and point-bearing rubric. It accepts alternative designs that meet the stated constraints.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the updated lesson and assessment at `c06c5e6`. The prior eight-range statement above records the initial review. The revised Bigtable key layout places the fixed-width day inside each bucket and device prefix, allowing the stated half-open cross-midnight interval to use one range per bucket, for four total. The lesson gives the exact bounds for bucket 0, and Q2 and EX-1 assess the same range calculation and merge.

The lesson now explains distinct immutable event IDs for same-time events, reuse of the original ID and bucket for corrections, and valid millisecond-granularity cell timestamps. It distinguishes audit retention and version-time reads from latest-value filtering and Cassandra's separate day/bucket partitions and mutation timestamps. The sample solution and rubric assess those choices. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l02) calls for range locality and product-specific version semantics. Both outcome maps and the prior topic dispositions remain supported.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
