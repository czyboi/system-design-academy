---
id: M04-EX1
status: draft
outcomes: [M04-S1]
---

# Evolve an order database under growth

A merchant platform owns customers, SKU stock, orders and lines in one relational database. An order references an existing customer, and reserving stock and creating the order and lines must commit together. Customers and stock are location-scoped within a tenant. A merchant may list recent orders across all of its independent sales locations. Each order, stock unit and customer reference in the hot merchant's workload belongs to exactly one location. Global billing reporting can tolerate a one-minute delay. Immediate order status must include any order the caller has already been told was confirmed, including after a location moves to an independently initialized shard. A checkout carries a stable operation ID and routed tenant/location key across retries.

The following figures are hypothetical. A peak read test finds that the recent-orders statement enriches 4,000 orders before retaining the newest 25. Its inner node emits three rows per loop. A rewrite that limits first preserves the order of results and zero-line orders, and in the model its inner node emits two rows per loop over 25 loops. On a later write-heavy test, optimized reads have spare capacity but one primary can sustainably process 500 checkouts/s at the target. Offered load is 640 checkouts/s. The hot merchant contributes 384/s. A separate model predicts peak per-location writes of 140, 105, 80 and 59/s for its four busiest locations, together accounting for the hot merchant. Each physical shard has a nominal 250 checkouts/s capacity under the same read mix. These capacity figures do not include the proposed synchronous cross-region acknowledgement or its failure behavior, so placement is provisional until tested with that path. Place the other tenants (256/s total) as whole tenants with measured rates of 96, 80 and 80/s.

During a regional drill under an asynchronous policy, the leader confirms an order at position 120, the surviving standby has flushed through 118 and replayed through 115, and the missing tail is lost. In that same drill, of 1,000 original valid status requests, 980 receive a correct response within 300 ms, 10 get a correct response late, 4 receive stale data, 3 time out and 3 return unavailable.

For a separate proposed-policy drill, assume exactly 640 eligible checkout arrivals per second at a uniform rate throughout a 15-minute window, for 576,000 original requests. Five minutes into the window, one region is unavailable for 30 seconds. The proposed two-region policy pauses all new confirmations during this interval and restores remote protection at its end. Assume all offered requests continue during the fault.

## M04-EX1

1. Diagnose the read and write tests separately. Show approximate inner-node outputs and propose the query and index changes. State how to verify the results and when a read replica or derived view is justified.
2. Trace the failover. Specify the policy that protects every confirmed order from loss of either single region, along with the read routing, fencing and retry contract. The owner may return unavailable when its correctness contract cannot be proven.
3. Compare splitting billing, hashing by tenant and assigning the hot merchant by location. Show one provisional placement, enforce the location-scoped references and identify the fan-out query and its incomplete-result behavior. Trace a lost activation reply and a timed-out checkout retried across cutover. Preserve confirmed status and receipt evidence across migration and rollback, including a region loss immediately after activation.
4. Score the status drill against a 99% target. The cohort includes all original valid status requests arriving in a 15-minute drill. The deadline is 300 ms from first arrival to a correct response that meets its version requirement. Retries share that original identity and deadline. Follow every operation through its deadline. For the separate proposed-policy drill, calculate a lower bound on checkout misses during the 30-second fault and assess the 98% target. Measure timely success for all original eligible checkouts in the 15-minute arrival window within 750 ms of first arrival. Late, rejected, failed, timed-out and unresolved operations miss the target. Separately reconcile confirmed IDs missing after recovery. Verify the full result under the same offered workload, including the busiest locations.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M04-S1

Select a scaling change and show the query and replication evidence that justifies it. Use [replication](../lessons/M04-L02.md), [sharding](../lessons/M04-L03.md) and [SQL tuning](../lessons/M04-L05.md).
