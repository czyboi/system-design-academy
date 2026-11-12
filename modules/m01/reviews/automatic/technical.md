# M01 technical and provenance review

Round 0 reviewed on 2026-11-12 against the SDA-v1 draft at `7dc09fc`. Scope includes the teaching, companion assessment and evidence for each of M01-L01 through M01-L04, plus the integrated brief, reference solution and rubric, decision summary, evidence and teaching and outcome maps.

## Findings

| ID | Severity | Status | Location | Evidence and correction |
| --- | --- | --- | --- | --- |
| T-1 | major | open | `modules/m01/integrated/brief.md:46`, partition history, and `modules/m01/integrated/solution-rubric.md:28–30,48`, trace and verification | The history says the West warehouse attempts Delivered. The solution requires only that West withhold success, then gives Dispatched after recovery under an assumption about later successful updates. A missing success reply cannot prove the write was discarded. A command can commit before the reply fails, and a request buffered for later delivery can change the recovered state. Define the exercise's isolated West as explicitly rejecting before forwarding, storing or queueing the write. State that the warehouse does not retry and no later status change commits in this trace. Derive Dispatched from the committed history. Verify both the response and the absence of mutation or later replay. Preserve the unknown outcome of a generic timeout separately. [Ongaro and Ousterhout, Raft extended paper, §8, client interaction](https://raft.github.io/raft.pdf#page=13). |

## Per-artifact verdicts

| Artifact package | Verdict | Technical evidence |
| --- | --- | --- |
| M01-L01 teaching, assessment and evidence | ready-for-human-review | Request-rate, retention, replication, working-set and bandwidth arithmetic reconcile. The 116.64 GB provisioned figure applies separate 20% overhead and 25% margin. The 28 ms serial and 20 ms overlapping cases describe individual traces. Byte/binary units and distinct recent accesses use the stated boundaries. [NIST binary prefixes](https://physics.nist.gov/cuu/Units/binary.html) · [Denning, The Working Set Model, §3](https://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf#page=4). |
| M01-L02 teaching, assessment and evidence | ready-for-human-review | The modeled 60-request API backlog, 0.30 s late-arrival wait, and 0.75 s drain follow from the specified rates. The exercise's 60-request CPU backlog and 90-read store backlog follow from separate capacity cases. Little's Law uses matching populations and a stable boundary. The tail target and rejected work are evaluated separately. [Little, equation 1](https://fisherp.scripts.mit.edu/wordpress/wp-content/uploads/2015/11/ContentServer.pdf#page=1) · [Google SRE, Queue Management](https://sre.google/sre-book/addressing-cascading-failures/#queue-management) · [Dean and Barroso, The Tail at Scale](https://www.barroso.org/publications/TheTailAtScale.pdf#page=1). |
| M01-L03 teaching, assessment and evidence | ready-for-human-review | The completed-write and overlapping histories yield the stated linearizability results. The availability argument uses an asynchronous partition and the requested read/write object contract. The scalar session token depends on a contiguous applied prefix of one shared history. The convergence rule requires the same edits and deterministic resolution. DynamoDB behavior is scoped to MREC global tables version 2019.11.21. [Gilbert and Lynch, §§2–3](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer6.pdf#page=3) · [Terry et al., Session Guarantees, §§3 and 5](https://pages.cs.wisc.edu/~remzi/Classes/739/Papers/bayou-sessions94.pdf#page=3) · [DynamoDB, Versions and Consistency modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html). |
| M01-L04 teaching, assessment and evidence | ready-for-human-review | The 60 s and 70 s read recovery examples use client restoration as the endpoint and distinguish the recovered data cutoff from the read freshness condition at failure. The fencing and no-confirmation paths preserve writer safety. Replication and backup have separate recovery roles. The downtime and conditional dependency calculations reconcile, including 99.79002% in Q6. [PostgreSQL 18, Failover](https://www.postgresql.org/docs/18/warm-standby-failover.html) · [PostgreSQL 18, Synchronous Replication](https://www.postgresql.org/docs/18/warm-standby.html#SYNCHRONOUS-REPLICATION) · [AWS, Recovery objectives](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html) · [AWS, Availability with redundancy](https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-with-redundancy.html). |
| M01 integrated design and supporting artifacts | revise | Peak 340 work units/s, minimum 425 rated survivor units/s at the reserve target, and the 99.9496002% route-only availability reconcile. The conditional estimate is scoped to reachability and capacity, with further data-policy eligibility required. The barrier proof covers the contiguous committed prefix and measures a conservative age from challenge dispatch. The rejected-write history and its test need T-1. [AWS, Availability with dependencies](https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-with-dependencies.html) · [Raft, §§5 and 8](https://raft.github.io/raft.pdf#page=13). |

## Provenance and assets

The evidence files distinguish original workloads, traces, diagrams, exercises and modeled numbers from linked factual sources. The Primer serves as the topic map, with Donne Martin's title, revision and CC BY 4.0 links in the lesson evidence. The worked examples and Mermaid diagrams are Academy material. External figures and executable examples are absent from these artifacts. The cited PostgreSQL version and DynamoDB mode support the scoped implementation illustrations. [Pinned Primer license](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/LICENSE.txt).

Overall verdict **revise**.

## Round 1 targeted re-review

Reviewed the correction from `7dc09fc` through `c1a5f0c` on 2026-11-12. This covers the M01-L01 teaching and companion changes, the M01-L04 companion change, the integrated brief and solution, and the affected outcome portfolio entries.

| Finding | Current status | Evidence |
| --- | --- | --- |
| T-1 | resolved | https://raft.github.io/raft.pdf#page=13 |

The integrated brief now defines a single West attempt explicitly rejected before forwarding, status mutation or queueing. It states that no status update commits after Dispatched. The solution derives the recovered value from the committed history and tests the rejection, local state, queue and committed log after rejoin. The separate timeout case correctly allows an unknown outcome and uses the request identity and authoritative result to guide retry. [Ongaro and Ousterhout, Raft, §8](https://raft.github.io/raft.pdf#page=13).

| Artifact package | Current verdict | Re-review result |
| --- | --- | --- |
| M01-L01 teaching, assessment and evidence | ready-for-human-review | P-1's stipulated 100 ns, 10 µs and 1 ms operation times differ by factors of 100. One hundred serial memory accesses total 10 µs. The lesson labels the example hypothetical and preserves the separate measured workload recommendation. P-2's added items cover the serial/overlap trace, distinct working set, replication payload and budget exercise. Companion and portfolio agree. [Patterson, Latency Lags Bandwidth, Table 1](https://pages.cs.wisc.edu/~markhill/restricted/cacm2004_latency.pdf#page=2). |
| M01-L02 teaching, assessment and evidence | ready-for-human-review | Round 0 verdict carries forward. |
| M01-L03 teaching, assessment and evidence | ready-for-human-review | Round 0 verdict carries forward. The integration's timeout distinction is compatible with the lesson's separate current-read and stale-read contracts. |
| M01-L04 teaching, assessment and evidence | ready-for-human-review | P-3's EX-1 mapping reaches both the 30-day downtime calculation and the recovery decisions. The companion and portfolio agree. The unchanged result of 189.2 s remaining follows from the 259.2 s budget less 70 s. [Google SRE, Availability table](https://sre.google/sre-book/availability-table/). |
| M01 integrated design and supporting artifacts | ready-for-human-review | The trace and verification resolve T-1. Revised portfolio entries agree with both lesson companions. Existing peak sizing, route arithmetic and freshness proof are preserved. [Ongaro and Ousterhout, Raft, §8](https://raft.github.io/raft.pdf#page=13). |

The revised examples remain original Academy material. The new timeout explanation cites the exact primary-source section. The targeted review found no new technical or provenance findings.

Overall verdict **ready-for-human-review**.
