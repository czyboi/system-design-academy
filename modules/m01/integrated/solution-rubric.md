---
id: M01-EX1-solution
status: draft
exercise: M01-EX1
---

# Reference solution and rubric for M01-EX1

## Estimate the workload and surviving capacity

The baseline is `4,320,000 ÷ 86,400 = 50 lookups/s` and `432,000 ÷ 86,400 = 5 updates/s`. The stated simultaneous peak is **300 lookups/s and 20 updates/s**. At the client boundary, lookup responses use `300 × 2,000 × 8 = 4.8 Mbit/s` of payload egress and update requests use `20 × 1,000 × 8 = 0.16 Mbit/s` of payload ingress. Account separately for headers, requests in the other direction, replica traffic and retries. The retained update-log payload is `432,000 × 14 × 1,000 B = 6.048 GB` per copy, or **18.144 GB** across three full copies. The estimate excludes indexes, snapshots and recovery space.

The two operations together cost `300 + 2 × 20 = 340 units/s` across the APIs, and 340 at the data paths in total. Under the stated reserve, each API may use `0.8 × 450 = 360 units/s` and each data path may use `0.8 × 320 = 256 units/s`.

| Peak case | API load | Data-path load | Capacity decision |
| --- | --- | --- | --- |
| A · Both regions serve | East and West share 340 units/s in total. Even all traffic at one API fits its operating ceiling of 360. | East handles all 340 units/s, which exceeds even its rated 320. | Raise authority data-path capacity or reduce accepted demand. Extra API workers leave the data-path constraint in place. |
| B · Both regions serve | Same aggregate API work, assuming one request to an API for each operation. | East handles `180 + 40 = 220 units/s`. West handles 120 units/s. | Both meet the 256-unit ceiling while local reads stay eligible and balanced. A burst of fallbacks can move West's 120 units/s to East. |
| A or B · One serving region remains | The surviving API takes all 340 units/s. | The sole available data path handles all 340 units/s after safe authority and routing recover. | Each candidate survivor needs at least `340 ÷ 0.80 = 425 units/s` rated data-path capacity. A 450-unit configuration is one candidate to test. |

The estimate assumes one logical foreground data operation path per request. If a fallback first spends store work on the local path or retries generate more work, measure and budget those extra operations. The surviving API has only 20 units/s of headroom against its 360-unit operating ceiling.

## Trace the operation history

| Event | A · Current lookup | B · Bounded local lookup |
| --- | --- | --- |
| West lookup at 12 s | Return unavailable. West cannot establish a current read. | Return Packed with a staleness label and a conservative 12 s bound. The unseen Dispatched update was acknowledged 2 s earlier. |
| West update at 15 s | Reject explicitly before forwarding, applying or queueing Delivered. West cannot reach authority. | Reject at the same point. A local snapshot remains eligible only for bounded reads. |
| West lookup at 46 s | Return unavailable while isolated. | Return unavailable. The last proof is 46 s old and exceeds 45 s, even if the actual order happened to be unchanged. |
| West lookup after recovery | The current authority returns Dispatched, the last committed update in this trace. | After applying the new barrier and its prefix, the West snapshot also returns Dispatched. |

At time 0, all already acknowledged updates precede the later committed barrier. Applying its contiguous prefix ensures they are reflected in the snapshot, subject to later updates in that prefix. If the elapsed upper bound is at most 45 s at the response decision, any update acknowledged more than 45 s earlier predates the challenge and is covered. Timestamping the receipt of the barrier would undercount the time already spent waiting for proof. A replica offset alone gives ordering information without a time bound. If timer continuity, barrier correlation or applied prefix evidence is missing, use the authority path or return unavailable.

A majority with the eligible committed history can elect a leader and resume the current read and update paths after the system establishes authority. A heartbeat timeout triggers investigation and election logic. It supplies no proof that an isolated writer stopped. A region that lost authority can serve a valid bounded snapshot when policy B permits it. It must rejoin the authoritative history before participating in current operations. [Ongaro and Ousterhout, Raft, §§5 and 8](https://raft.github.io/raft.pdf#page=13)

The exercise's rejection guarantees that West admitted no update. If the caller instead times out after submitting to a reachable authority, the outcome can be unknown. The authority may have committed the command before its reply was lost. Resolve the request using its identity and the authoritative result before deciding whether a retry should apply a new operation. [Ongaro and Ousterhout, Raft, §8](https://raft.github.io/raft.pdf#page=13)

## Evaluate latency and availability

A West current read travels through the edge and West API, then adds a remote request to the authority, including whatever work establishes a current read there. A local B lookup checks the certificate and reads locally. As an illustrative individual trace, 8 ms of edge and client transfer, 12 ms of API queueing and work, and 8 ms of local read total 28 ms. Replacing that local read with a remote path costing 53 ms would yield 73 ms. These are assumed trace values. Compare the measured client-facing p99 of each path at the prescribed load, including B fallbacks, errors and timeouts.

The 30-day time budget at 99.95% is `0.0005 × 30 × 86,400 = 1,296 s`, or 21m 36s. Under the exercise's conditional independence, the chance of at least one usable regional route given a working edge is `1 − (0.002 × 0.002) = 0.999996`. Requiring the edge gives `0.9995 × 0.999996 = 0.999496002`, or about **99.9496%**. Even this route-only estimate falls short of 99.95% before applying the data policy. An edge outage can affect both paths, so the regional redundancy cannot repair that dependency.

For A, the available route also needs a reachable, current authority. For B, it needs a valid snapshot or a usable authority fallback. Model those conditions jointly with partitions, routing transitions and load. The exercise provides no independent probability for them. Measure their durations and frequencies in the intended topology and budget failover from the first client-visible interruption through detection, safe authority and a successful client response. [AWS, Availability with dependencies and redundancy](https://docs.aws.amazon.com/whitepapers/latest/availability-and-beyond-improving-resilience/availability-with-dependencies.html)

## Recommend and verify

Choose B for customer status lookups if the 45-second contract is acceptable. It gives West a short window of valid responses during isolation and avoids routing all healthy lookups through the authority. Keep writes authoritative. Increase survivor data-path capacity and address the shared edge before committing to the availability target. If a consumer must see a completed update immediately, use the current-read path for that operation and budget its remote traffic and failure behavior.

Replay matched peak traffic during a region loss and measure survivor throughput, queues, p99 and failures. During West isolation, advance the East history, confirm labeled responses inside the proof window and exercise expiry and verifier restart. Verify the explicit rejection of the minority write and check that it leaves no local status change, queued request or committed log entry after rejoin. Disable the shared edge in a separate test and measure recovery of both routes. Validate that production measurements distinguish route reachability, valid data responses and outage time.

## Self-evaluation rubric

Score each row 0 for missing, 1 for partial or 2 for complete reasoning. Accept other choices that satisfy the write invariant and justify any revised service target.

| Criterion | Full credit |
| --- | --- |
| Workload and budget | States units and peak factors. Counts read and write work at the relevant boundaries and sizes a survivor with explicit headroom. |
| Read and write histories | Applies both read contracts and the age proof at each read. Shows why the explicit minority rejection leaves no write to apply after recovery and explains how authority is re-established. |
| Availability and latency | Calculates the time budget and conditional route estimate. Explains the shared limit and the extra conditions each policy needs. Names the request paths and measurements. |
| Design and verification | Uses the workload and consistency contract to make a policy choice. Gives a realistic peak-failover test, a test of a shared dependency and a condition that changes the choice. |

**M01-S1.** M01-EX1 uses M01-L01-LO1 for estimation, M01-L03-LO2 for operation-level semantics and M01-L04-LO2 for failover and dependency reasoning. Each lesson companion measures its own outcomes.
