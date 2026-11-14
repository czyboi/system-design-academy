# M05-L03 pedagogy and curriculum coverage review

Reviewed the canonical lesson, assessment and evidence at draft handoff `82bae71` for middle and senior engineers. The scope is the [approved M05-L03 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l03), its assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer SQL/NoSQL discussion](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L991-L1129), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Assigned topics | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H107 and PR-B004, NoSQL and BASE | taught | **Specify what a response promises** distinguishes ACID state validity, read visibility and the limits of eventual convergence. Q4 and EX-1 apply explicit operational contracts. |
| PR-H117, PR-BODY-R1-SQL-NOSQL-CRITERIA and PR-BODY-R1-SQL-NOSQL-WORKLOADS | taught | **Choose an access path by workload** compares relational, key-value, document, wide-column and graph models by access shape and transaction questions. It considers joins, schema, throughput under skew and operational ecosystem, with basket, clickstream/log, leaderboard, hot-table and metadata examples. Q4–Q6 and EX-1 apply model selection and guarantees. |
| PR-PASTEBIN-H017, PR-TWITTER-H017, PR-WEB_CRAWLER-H018, PR-MINT-H017, PR-SOCIAL_GRAPH-H014, PR-QUERY_CACHE-H017, PR-SALES_RANK-H015 and PR-SCALING_AWS-H040 | taught | The same comparison applies the shared SQL/NoSQL criteria to snippet metadata, feeds, crawler metadata, an account ledger, graph traversal, cached results, rankings and hot-table/hosted workloads. These are workload analogues of the assigned case mappings. EX-1 applies the comparison to favorites, seats and rankings. |
| PR-ARCH-DYNAMODB | taught | **Reserve stock under a concrete contract** scopes a DynamoDB transaction to its items, account and Region, contrasts index visibility and introduces Spanner's transaction contract. Q5 and EX-1 assess the distinction. |

## Pedagogy and assessment

The fixed-set quorum example first establishes A/B and B/C overlap, then the sloppy-quorum example shows disjoint A/D and B/C responders and the conditions for hinted handoff and anti-entropy. The basket example explains why add-only union preserves concurrent additions and why removals need more information. The strict reservation example places the conditional claim and stable receipt under one authority, and asks a retry to use that same identity and durability contract.

EX-1 applies the disjoint quorum trace, repair conditions and one-winner invariant to favorites and seats. Its solution accounts for permanent loss of all copies, requires a single authoritative transaction and stable retry identity, and asks for product-scope verification and a ranking freshness indicator. LO1 maps to Q1–Q3 and EX-1. LO2 maps to Q4–Q6 and EX-1. The separate companion includes six explained checks and a point-bearing rubric that accepts equivalent designs.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the revised lesson and companion at `d250834`. **Follow a write through replicas and repair** now distinguishes preferred, contacted, acknowledging and responding nodes and gives D's hint recipient and the copy-survival condition. EX-1 and its solution and rubric assess those same sets and repair conditions.

**Reserve stock under a concrete contract** teaches the conditional receipt, its immutable input binding, a lookup while the first transaction remains in flight, and a guarded retry across a 24-hour retry window. It scopes native DynamoDB idempotency separately and explains why a conflict or cancellation does not by itself determine the outcome. The Spanner comparison names serializable read-write transactions, a later strong receipt read, commit wait and availability verification. EX-1 and its rubric measure these taught details while accepting equivalent designs. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m05-l03) assigns replication, repair and coordinated transaction comparisons to this lesson.

The outcome mappings and assigned workload coverage remain supported. No new pedagogical or coverage finding arose in the changed material.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
