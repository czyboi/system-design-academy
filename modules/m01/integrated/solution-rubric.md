---
id: M01-EX1-solution
status: draft
---

# Reference workload and rubric

## Workload and bottleneck budget

| Measure | Example derivation |
|---|---|
| Requests | Divide by 86,400 s/day for 10 reads/s and 1 write/s on average. Multiply by 12 for 120 and 12 at peak. With 25% above peak, test 150 reads/s and 15 writes/s. |
| Network | At peak, read egress is 240 kB/s or 1.92 Mbit/s. Write ingress is 12 kB/s or 0.096 Mbit/s. At the test rates these become 300 and 15 kB/s. Exclude protocol, replication and retry overhead and measure them separately. |
| Storage | 86,400 events/day × 30 days × 1,000 B = 2.592 GB logical. Three copies give 7.776 GB before indexes, backups and temporary space. |
| Latency | An illustrative 200 ms read budget assigns 25 ms to ingress and auth, 95 ms to the authority call, 35 ms to application and reply work, and 45 ms to queueing and margin. These are allocations. Measure end-to-end p99 under the specified workload. |

As a first hypothesis, examine queueing and the shared store. At the test load, observe request success, latency, queue depth, store wait time and storage activity. Repeat with one serving zone gone and confirm the remaining path can serve all 150 reads/s. Confirm authority and auth still have enough capacity for that request mix and 15 writes/s. If storage dominates while app hosts are idle, adding app capacity leaves the constraint.

## Operation histories

The authoritative store commits version 18, `Shipped`, and acknowledges the write. A partition isolates one serving branch with version 17, `Packed`. Assume auth remains reachable and the coordinator can still operate on its side.

| Request at isolated branch | Policy A | Policy B |
|---|---|---|
| Display at 20 s, with a proved lag bound within 60 s | Decline if the request cannot reach authority. | Return `Packed` with a freshness label. Route to authority if it becomes reachable. |
| Display after lag exceeds 60 s or becomes unknown | Continue to require authority. | Decline unless authority is reachable or a qualifying projection is available. |
| Update or authorize refund | Require the current authority and decline when unreachable. | Same write and refund policy. The old display value grants no refund authority. |

Policy B preserves a bounded degraded display on the isolated branch. Validate it by replaying a known update across the split and asserting that fallback stops when the lag bound expires. Derive the bound from how far the projection has applied a contiguous update stream, including uncertainty. The timestamp of the last changed order alone cannot distinguish inactivity from stalled replication. Verify correctness and measure full-quality and degraded results separately.

## Availability

Under the simplified independent model, either branch works with probability `1 − (1 − 0.999)^2 = 0.999999`. Shared authorization must also succeed, so the result is `0.9995 × 0.999999 = 0.9994990005`, about **99.9499%**. This models the availability of an eligible branch and shared authorization at a time. It supplies an upper bound of 99.95% while authorization is mandatory with that availability. The model inputs and formula alone cannot forecast achieved availability for either policy.

A common authority outage can disable both Policy A branches. Policy B can cover a bounded portion if authorized requests have a qualifying projection. A shared rollout can also disable both branches, and detection plus traffic rerouting can consume time even when the survivor works. Fault-inject a lost zone and a partition under peak load, record user-visible errors and stale responses, and confirm how long it takes to restore qualifying service. Track request success separately from time availability.

## Self-evaluation

Award 2 for complete reasoning, 1 for a correct but incomplete argument and 0 for a missing or contradictory argument.

| Criterion | Evidence for full credit |
|---|---|
| Sizing | Correct units, copy count, peak and margin, bandwidth and retained bytes. |
| Latency and capacity | Explicit critical path and a reproducible load test with a failure case and a bottleneck signal. |
| Partition policy | An operation history that distinguishes display, write and refund authorization. Correct expiry or unknown-lag behavior. |
| Availability | Correct event model, explicit assumptions and a plausible shared or transition failure with a verification step. |

A different justified design may earn full credit. Its degraded reads must respect the stated freshness rule and it must protect refund authorization.
