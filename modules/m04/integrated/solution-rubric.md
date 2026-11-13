---
id: M04-EX1-solution
status: draft
---

# Reference design and rubric

## Diagnose read growth and write growth separately

The baseline inner node emits about 12,000 rows. The candidate emits about 50. Preserve zero counts with an outer join that counts a non-null line ID. Select the ordered 25 headers first when enrichment cannot change eligibility or order, then repeat the deterministic order after enrichment. Propose an index on `(tenant_id, created_at DESC, id DESC)` and a line index led by order ID. Compare actual buffers, loops, rows, execution time, write latency and WAL under the same data, parameters and load. The node output is one diagnostic, not a latency forecast. A read replica can absorb stale-tolerant reads if pressure remains. A derived view can offload repeated reporting aggregation if its lag and recovery fit the one-minute contract. Neither resolves leader write saturation by itself.

At 640 checkouts/s against 500/s sustainable capacity, one owner cannot sustain the offered rate at the target. A separate billing owner gives billing independent capacity, while order checkout stays on the order, stock and customer owner. Tenant-only hashing concentrates 384/s on one 250/s shard. The location model permits a four-shard example. Pair 140 with 96 for 236/s, 105 with 80 for 185/s, and 80 with the other 80 for 160/s, leaving 59/s on the fourth shard. Confirm location-scoped checkout invariants and measure additional headroom for skew and replay. A merchant-wide recent-orders query fans out and merges the location lists on the original ordering. If a merchant-wide constraint must share one atomic commit, keep that constraint under a coordinated authority.

## Protect acknowledgements and freshness

The asynchronous standby can recover 116–118. Position 120 is missing even after promotion. Use one fenced writer per ownership unit and require the designated standby in the other region to flush the order and operation ID before confirmation, including success returned by a retry. The standby identity and enforced durability policy establish the expected history. Verify fencing, recover the protected log and open the new writer only under the resulting authority. If the other region is absent, pause new confirmations until the required durability is restored. A missing reply after admission is unknown. Use the operation identity to reconcile committed state and return success only with the required durability proof.

Carry a confirmed operation watermark with a status read. Require matching history, replay through the watermark and a new snapshot. Route to an eligible owner or return unavailable within the deadline. Keep those misses in the denominator. The observed rate is 980/1,000 = 98%, which misses 99%. The async loss of the confirmed order also fails the durability rule. The supplied data does not establish the checkout timely success rate. Measure it under the same arrival and fault schedule and separately reconcile confirmed operation IDs after replay. Test loss of the active region, loss of the designated standby, an interrupted acknowledgement and a stale read route.

## Move ownership once

Take an aligned snapshot and change position, stream changes, then durably close the old shard's write epoch and drain admitted writes. Catch the destination up through the final position and verify relational invariants and operation IDs. Use a durable directory plan whose activation and abort are mutually exclusive conditional changes. If the activation reply is lost, keep the source fenced and read back the exact plan. An old route is rejected at the shard. Open the new epoch only with directory proof and above the shard's durable closed-through floor. To roll back after accepting writes, fence and drain the destination, transfer its changes to the old side, and open that side at a newer epoch. A delayed old open cannot pass the closed-through check. Measure availability impact during the fence and catch-up interval.

## Rubric

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Query evidence | 3 | Calculates the model outputs, keeps ordering and zero counts, and compares like-for-like read and write measurements. |
| Durability and status | 3 | Traces the loss, scopes remote acknowledgement and replay proof, calculates 98% and keeps the checkout and status outcomes distinct. |
| Partition decision | 2 | Computes a feasible placement and retains the invariant and explicit merchant-wide fan-out. |
| Migration | 2 | Covers snapshot and replay, one writer, an uncertain transition reply, stale epoch handling and preservation of accepted destination writes. |

Accept alternative capacity placements and architectures with an explicit ownership and failure proof. Award partial credit for explained components with missing traces.
