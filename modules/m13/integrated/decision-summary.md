---
id: M13-decisions
status: draft
---

# Select architecture evidence by constraint and date

## Adapt the invariant, then the infrastructure

A team producing one correct report per night does not inherit Google's early-2000s cluster count or file API. The *transferable mechanism* is deterministic partitionable work, retry from immutable input and a guarded complete output. Keep a dated paper/source ledger; verify present-day product/edition/configuration before asserting current guarantees. For a one-region 20 GiB report, start with a bounded worker and durable manifest; distribute only when the measured critical path misses the 06:00 deadline.

[M13-EX1](brief.md) evaluates the historical comparison and [reference](solution-rubric.md) explains the dated source-to-component map.

## Architecture-evidence decision table

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Finite job exceeds measured single-worker envelope | MapReduce-pattern partition/shuffle/reduce | Recompute deterministic partitions, guard output manifest | Parallel finite compute and recovery | Scheduler/shuffle/data movement | Key skew or missed final deadline | Single worker demonstrably meets deadline | [M13-L01](../lessons/M13-L01.md) |
| Repeated iterative computations reuse input | Spark RDD lineage / reuse | Materialized reusable partitions with lost-partition recomputation | Avoid repeated source reads | Memory pressure and engine complexity | Eviction/recomputation worsens critical path | One-pass simple aggregation | [M13-L01](../lessons/M13-L01.md) |
| Continuously updated results required | Stateful stream processor | Ordered event/checkpoint/replay contract | Better freshness | Watermarks, late data, state recovery | Stale views and lost/duplicate effects | Once-nightly finite report | [M13-L01](../lessons/M13-L01.md) |
| Large data needs key-range locality | Bigtable-inspired sorted index | Partition ordered rows into range/tablets | Locality for ordered access | Hot partition and balancing | Hot prefix or inconsistent read expectation | Small DB with supported indexes adequate | [M13-L01](../lessons/M13-L01.md) |
| Partition-time writes must stay available | Historical Dynamo-inspired versioned KV | Replicated versions with app conflict resolution | Availability under certain failures | Version reconciliation and weak convergence | Divergent versions | A strict single-copy business invariant is required | [M13-L01](../lessons/M13-L01.md) |
| Cross-region externally consistent commits necessary | Spanner-like coordinated transaction | Replicated commit and bounded uncertainty clock protocol | Strong cross-region transaction property | Latency and coordination | Old writer or commit ambiguity | No multi-region transaction requirement | [M13-L01](../lessons/M13-L01.md) |
| Large immutable/append data with custom FS needs | GFS/HDFS family | Chunk/block distribution, metadata authority, recovery | Scale-specific storage controls | Operations and data placement | Missing/corrupt chunk | Existing object storage meets contract | [M13-L01](../lessons/M13-L01.md) |
| Need exclusive metadata owner | Chubby/ZooKeeper coordination plus application fencing | Leader/lease and guarded resource epoch | Clear ownership | Quorum dependency | Old leader writes after election | No shared mutable ownership exists | [M13-L01](../lessons/M13-L01.md) |
| Need visibility or independent log replay | Dapper traces / Kafka log (distinct roles) | Trace propagation / retained partition events | Diagnosis / recovery respectively | Instrumentation or retention/lag | Missing spans or replay beyond retention | Treating observation as enforcement | [M13-L01](../lessons/M13-L01.md) |

A diagram or source catalog is discovery only. Neither product popularity nor a historical paper proves current guarantees without version-scoped primary evidence and explicit failure testing.

## Synthesis outcome

**M13-S1:** trace architecture source assumptions to mechanisms and defend an adaptation constrained by workload. The accompanying [M13-L01 assessment](../assessments/M13-L01.md) separately tests M13-L01-LO1 and LO2. M13-EX1 measures the synthesis only.
