---
id: M04-EX1-solution
status: draft
---

# Reference design and rubric

## Diagnose read growth and write growth separately

The baseline inner node emits about 12,000 rows. The candidate emits about 50. Preserve zero counts with an outer join that counts a non-null line ID. Select the ordered 25 headers first when enrichment cannot change eligibility or order, then repeat the deterministic order after enrichment. Propose an index on `(tenant_id, created_at DESC, id DESC)` and a line index led by order ID. Compare actual buffers, loops, rows, execution time, write latency and WAL under the same data, parameters and load. The node output is one diagnostic, not a latency forecast. A read replica can absorb stale-tolerant reads if pressure remains. A derived view can offload repeated reporting aggregation if its lag and recovery fit the one-minute contract. Neither resolves leader write saturation by itself.

At 640 checkouts/s against 500/s nominal sustainable capacity, one owner cannot sustain the offered rate in that model. A separate billing owner gives billing independent capacity, while order checkout stays on the order, stock and customer owner. Tenant-only hashing concentrates 384/s on one nominal 250/s shard. The location model permits a four-shard example. Pair 140 with 96 for 236/s, 105 with 80 for 185/s, and 80 with the other 80 for 160/s, leaving 59/s on the fourth shard. This placement is provisional because the capacity inputs exclude the synchronous regional path. Measure its latency, throughput and headroom under that path, skew, replay and faults.

Route each checkout by its stable `(tenant_id, location_id)` owner key. In that owner, use composite customer, stock and order keys including both components. Composite foreign keys from orders to customers, and from lines to both orders and stock, enforce same-location references. The transaction conditionally claims stock and creates the order, lines and operation receipt together. A merchant-wide constraint needs its own coordinated authority. The recent-orders query fans out to all required locations and merges their lists using the original ordering. If any required location is unavailable, return an explicitly incomplete or unavailable result under the API contract rather than presenting the merged subset as complete.

## Protect acknowledgements and freshness

The asynchronous standby can recover 116–118. Position 120 is missing even after promotion. Use one fenced writer per ownership unit and require the designated standby in the other region to flush the order and operation ID before confirmation, including success returned by a retry. The standby identity and enforced durability policy establish the expected history. Verify fencing, recover the protected log and open the new writer only under the resulting authority. If the other region is absent, pause new confirmations until the required durability is restored. A missing reply after admission is unknown. Use the operation identity to reconcile committed state and return success only with the required durability proof.

Carry the stable operation/order ID, tenant/location owner key and a minimum logical order revision in a confirmed status token. Within a physical replication history, use a matching WAL history and replay position before opening a fresh snapshot. Across a move to an independently initialized shard, the old WAL token alone cannot prove the destination's state. Instead, the destination verifies the copied order revision and matching durable receipt against the migration's final source boundary, then serves a fresh snapshot at or above the logical revision. The same rule applies after rollback. Route to an eligible owner or return unavailable within the deadline.

The observed status rate is 980/1,000 = 98%, which misses 99%. The asynchronous loss of the confirmed order also fails the durability rule. For the separate proposed-policy drill, 640/s for 900 seconds yields 576,000 original eligible checkouts. Any arriving in the first 29.25 seconds of the 30-second no-confirmation interval has its 750 ms deadline expire during the fault. At the assumed uniform rate, at least 18,720 requests miss, so at most 557,280/576,000 = 96.75% can succeed on time. This lower bound misses 98% even if every other request succeeds. The actual rate can be lower.

Measure the numerator as correct confirmations by each original request's 750 ms deadline and the denominator as every original eligible checkout arriving in the 15-minute window. Fold retries into their original identity. Count late, rejected, failed, timed-out and unresolved requests as misses. Separately reconcile all confirmed operation IDs against recovered state. Test the proposed synchronous path under the same offered rate, hottest locations and fault schedule. Meeting 98% requires a different fault response or architecture that still proves the durability rule.

## Move ownership once

Take an aligned snapshot and change position, stream changes, then durably close the old shard's write epoch and drain admitted writes. Catch the destination up through the final position and verify relational invariants, order revisions and operation receipts. After those imports commit on the destination, commit a barrier record on its own WAL history and verify that its designated opposite-region standby has durably flushed through the barrier. This proves that the standby has received the earlier imported commits on that history. Keep the protected source recovery path authoritative until that proof and the directory transition succeed. Local copy validation alone cannot establish remote recoverability.

Use a durable directory plan whose activation and abort are mutually exclusive conditional changes. If the activation reply is lost, keep the source fenced and read back the exact plan. An old route is rejected at the shard. Open the new epoch only with directory proof and above the shard's durable closed-through floor. For example, a checkout may commit before the source fence while its reply times out. Its stock claim, order revision and operation receipt move together. The retry refreshes the location route, finds that same receipt on the destination and returns success only after the destination's required durability proof. It does not claim stock a second time. A pre-move status token resolves against the copied logical revision, with fresh-read proof on the destination's history.

To roll back after accepting writes, fence and drain the destination, transfer its changes and receipts back, and establish the same opposite-region durable barrier for the old side before replacing the recovery authority and opening its newer epoch. A delayed old open cannot pass the closed-through check. Test a pre-move token and timed-out retry after cutover and again after rollback. Remove the new writer region immediately after each activation and verify recovery of previously confirmed order IDs and receipts from its designated standby. Measure availability during fencing, catch-up and restoration of remote protection.

## Rubric

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Query evidence | 3 | Calculates the model outputs, keeps ordering and zero counts, and compares like-for-like read and write measurements. |
| Durability and status | 3 | Traces the confirmed-order loss, scopes same-history replay proof and stable logical status across moves, calculates 98% status, and separately defines the 576,000 checkout cohort, 750 ms deadline, 98% target and every miss category. Calculates at least 18,720 checkout misses and the 96.75% upper bound for the proposed fault. Reconciles confirmed IDs after recovery. |
| Partition decision | 2 | Computes provisional placement, enforces location-scoped references, identifies coordinated cross-location invariants and makes incomplete fan-out explicit. |
| Migration | 2 | Covers snapshot and replay, one writer, uncertain transition reply, stale epochs, stable receipts and logical revisions. Requires remote durability barriers before cutover and rollback authority changes, and tests immediate writer-region loss. |

Accept alternative capacity placements and architectures with an explicit ownership and failure proof. Award partial credit for explained components with missing traces.
