---
id: M13-EX1-solution
status: draft
---

# Reference — use a mechanism, not an architecture museum

## Evidence ledger and constraint map

| Historical paper | Relevant mechanism and original assumption | Why not copy wholesale? |
| --- | --- | --- |
| Dean & Ghemawat, *MapReduce*, OSDI 2004, [Google Research](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/), model/implementation sections | Key/value map, shuffle by intermediate key, reduce and failure re-execution at cluster scale | 20 GiB daily finite job may fit one measured worker; no demonstrated need for large scheduler/shuffle cluster |
| Ghemawat et al., *GFS*, SOSP 2003, [Google Research](https://research.google/pubs/the-google-file-system/), workload and architecture sections | Very large/append-heavy files and chunk-placement/recovery assumptions | Versioned immutable object storage may already provide the read/write semantics needed; custom filesystem operational cost is not justified |
| Zaharia et al., *Resilient Distributed Datasets*, NSDI 2012, [USENIX](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia), lineage/partition sections | Recompute lost partitions; materialize/cache reused intermediate data | For one pass with no iteration, memory lineage engine has no automatic benefit; assess CPU/reuse measurements first |

These paper references are historical design evidence. They are **not** modern Spark, Google Cloud, HDFS or storage durability guarantees. Cite current product documentation and edition/configuration for such claims if needed. Link diagrams, do not import them.

## Minimal adapted design and retry

```text
Scheduled trigger(report_day, dataset_version)
 -> run receipt/checkpoint authority (unique run identity)
 -> pin immutable input and verify checksum
 -> bounded-memory worker(s) produce immutable attempt partitions
 -> completeness+integrity verifier
 -> guarded commit of one final immutable manifest/report_version
 -> client reads verified completed manifest; or sees pending/error
```

The DB holds report state `created, running, staged, verified, published, failed`, a generation and a stable run ID. Each attempt writes to a new namespace, not over a published output. The publication operation checks the matching run revision and makes a complete artifact visible atomically at one defined pointer/manifest boundary; if the pointer storage lacks atomic conditional writes, use a transactionally guarded manifest record in the authority.

When a worker dies at 60%, its uncommitted attempt objects remain private and are garbage-collected later. The retry reconstructs remaining or all deterministic partitions from the pinned version. When the publication response is lost, the controller consults the committed run receipt instead of publishing another unrelated version. An old worker cannot overwrite a newer published pointer because the authority checks generation. A “200 jobs executed” count is meaningless unless one complete verified output is available to the user.

## Capacity reasoning and alternatives

20 GiB / 3600 seconds is approximately **5.69 MiB/s** of source throughput (assuming GiB=2^30 bytes; decimal 20 GB would be ~5.56 MB/s). This is only a lower bound for reading bytes; parse, transform, shuffle, output, validation and retry overhead increase required capacity. Run benchmarks on one realistic worker and representative skew before choosing topology. Two hundred logical tasks do not mandate two hundred workers: a pool can schedule them sequentially/in parallel within CPU/I/O/memory limits.

If the measured single-worker critical path misses the deadline, introduce parallel deterministic partitions and bounded retries, maintaining the same final-manifest invariant. For expensive iterative reuse, Spark-style cached partitions may be justified; for large key-grouped aggregations MapReduce-like shuffle/reducer remains relevant. Add GFS/HDFS-like block storage only when a documented existing storage limit makes it necessary. Continuous streaming is unsupported by the stated once-nightly freshness requirement. Compare software/ops costs, network shuffle and recovery overhead, not product names.

## Outcome and falsification

Correct on-time original report success = **27/30=90%**. Late and integrity-invalid results remain misses regardless of whether all subtasks returned success. Instrument end-to-end visibility at 06:00, input version and output hash; separately observe attempt retries, partition skew, worker CPU and I/O.

Test: crash at 60%; retry same run ID; lost final commit reply; concurrent duplicate scheduler events; a changed input version mid-run; corrupted partition checksum; skewed key group; worker pool capacity below deadline; old generation publishing after retry. Validate against actual product APIs/version before claiming any cloud/object-store consistency behavior.

## Rubric (12 points)

| Dimension | Pts | Full-credit evidence |
| --- | ---: | --- |
| Historical evidence | 3 | Three dated primary sources, source scope and current guarantee limits |
| Mechanism transfer | 4 | Correct minimal architecture and guarded complete-output crash/retry |
| Cost/capacity decisions | 3 | 5.69 MiB/s lower bound, measured bottleneck and rationale to remove unnecessary components |
| Verification/rights | 2 | 27/30 success, six falsification tests and rights-safe source plan |

A credible alternative architecture earns full credit if it preserves complete immutable publication and its extra components are grounded in constraints and measurements.
