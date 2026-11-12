---
id: M01-EX1
title: Design a regional order-status service
status: draft
outcomes: [M01-S1]
---

# M01-EX1 · Design a regional order-status service

Two regions serve an order-status API for a retailer. A customer checking a shipment can tolerate a brief delay in seeing a status change. A status update from the warehouse must enter the authoritative history. Design the request paths and choose what each one should do when a region becomes isolated.

**M01-S1.** Connect a workload estimate to operation-level consistency and failover choices. Apply [capacity budgets](../lessons/M01-L01.md), [performance and scalability](../lessons/M01-L02.md), [consistency under partition](../lessons/M01-L03.md) and [availability and failover budgets](../lessons/M01-L04.md).

## Workload and service targets

| Input | Assumption |
| --- | --- |
| Normal daily activity | 4.32 million status lookups and 432,000 status updates, one API request per operation |
| Simultaneous peak | Six times the average lookup rate and four times the average update rate |
| Healthy routing | East handles 60% of lookups and West handles 40%. East is normally authoritative for writes. |
| Payload and retention | Each lookup returns 2,000 B of payload. Each update sends and stores 1,000 B. Keep 14 days of update-log payload with three full copies. Use decimal network and storage units. |
| Regional capacity | Each API tier handles 450 work units/s. Each region's data path handles 320 foreground units/s after reserving capacity for log replication and freshness checks. Each lookup costs one unit at its API and selected data path. Each update costs two units at its API and authoritative data path. |
| Capacity target | Keep 20% of rated capacity free during the stated peak, including after one serving region is lost and routing and safe authority have recovered. |
| Lookup targets | Successful-response p99 ≤ 90 ms at peak, with a 250 ms client timeout. Time availability target ≥ 99.95% over 30 days. For the modeled client cohort, the service is available when a route has enough capacity to deliver a result meeting the read contract before the timeout. |
| Update contract | Acknowledge only a committed update in one authoritative order. The two serving regions and a third failure domain each host a durable voter. An election and commit require a majority. The third voter stores the log and serves no API traffic. |

The values are hypothetical. Assume authorized users and a working authorization check inside the shared edge for the modeled route. Keep the request mix and background reserves fixed in capacity comparisons. Treat routing recovery time, traffic skew and timing distributions as measurements to plan.

## Compare two policies

**Policy A · Current lookup.** Lookups and updates go to the authority. A current lookup must be linearizable. Verify authority and catch-up for reads as well as writes. If the required authority cannot be reached before the deadline, return unavailable.

**Policy B · Bounded local lookup.** A lookup may return a labeled local snapshot if its proven age is at most 45 seconds. Without that proof, route to the authority if reachable within the deadline, or return unavailable. Updates still use the same commit contract as policy A. A successful bounded lookup includes or supersedes every status update acknowledged more than 45 seconds before the service makes its response decision.

For this exercise, a West verifier records a local time before sending a freshness challenge. The authority commits a barrier in the same ordered log after receiving that challenge. West certifies and serves a snapshot that contains the complete committed prefix through the corresponding barrier. Age is conservatively bounded by local elapsed time since West **sent** the challenge, including timer uncertainty. Invalidate proof when the verifier's timing continuity or the snapshot prefix cannot be verified. Measure age at the response decision.

Use this partition history for order 41.

| Time | Event |
| --- | --- |
| t = 0 s | West sends a challenge while both regions can reach the authority. The status is Packed. |
| t = 2 s | West applies the corresponding committed barrier and all earlier updates. |
| t = 3 s | West loses connectivity to East and the third voter. Both serving regions still reach local clients through the edge. East can reach the third voter. |
| t = 10 s | East acknowledges a commit changing Packed to Dispatched. West has no later applied barrier or update. |
| t = 12 s | A West client looks up order 41. |
| t = 15 s | A West warehouse tries to record Delivered. |
| t = 46 s | The West client looks up the order again. |
| t = 55 s | Connectivity is restored. West applies the committed updates and a new barrier from a fresh challenge. |

For this trace, use the listed times as conservative elapsed bounds and assume the West client cannot be routed around the partition to East. A region loss with working edge rerouting is a separate capacity case.

## Submit a design

1. Estimate normal and peak operation rates, payload bandwidth, and retained update-log payload. Compare API and data-path load in both policies at peak, then recompute after losing one serving region. Recommend capacity changes or a negotiated reduction in the load the survivor must admit.
2. Trace both read policies and the write at the stated times. Explain why West may or may not respond, how its freshness evidence works, and what must happen before a former minority becomes a writer.
3. Sketch the lookup latency path for each policy. Name the shared failure domains, budget the time SLO, and calculate a route-only availability estimate using a shared edge available 99.95% of the time and each region's route-and-service prerequisites, including sufficient capacity after sizing, usable 99.8% of the time given the edge is up. Assume conditional independence for this estimate. State what additional availability information each data policy requires.
4. Recommend a policy and identify a requirement or measurement that would change your choice. Include a test for the shared dependency and a partition or failover test under peak load.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)
