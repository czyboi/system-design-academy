---
id: M01-decision-summary
status: draft
exercise: M01-EX1
---

# M01 decision summary

Apply these decisions to the [order-status workload](brief.md) at 300 lookups/s and 20 updates/s. The comparison assumes 20% free capacity at peak and after failover.

| Trigger | Option | Mechanism | Benefit | Cost or trade-off | Failure signal | Avoid when | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Peak forecast grows or a serving region can disappear | Provision to the surviving path | Convert peak operations to resource work and divide survivor demand by 0.80. In the model, 340 units/s requires 425 units/s of rated capacity. | Capacity remains after losing a region and recovering safe routing and authority. | Pay for capacity in each potential survivor and measure actual per-operation demand. | Survivor exceeds 80% of rated capacity, queues build or timely completions decline. | The workload can explicitly shed enough low-priority demand to meet the agreed failure target with less capacity. | [Capacity and latency budgets](../lessons/M01-L01.md) |
| API queues grow while the store still has capacity | Scale out stateless API workers | Spread independent work across instances and keep the required request state reachable from each. | Improves aggregate throughput if work can be distributed. | Adds instances, routing and coordination. | Per-replica skew or store waits rise while CPU capacity remains idle. | The shared data path is already saturated. | [Performance versus scalability](../lessons/M01-L02.md) |
| Every successful lookup must reflect completed updates | A · Current lookup | Route to a verified current authority. Return unavailable if the read contract cannot be satisfied. | Provides the current-read guarantee. | Cross-region latency and interruptions during isolation or election. | Loss of authority or an increasing fraction of remote reads missing the deadline. | An explicitly bounded stale lookup meets the use case and the authority is on the latency or throughput path. | [Consistency and partition decisions](../lessons/M01-L03.md) |
| A status display accepts a 45 s bound | B · Bounded local lookup | Serve a labeled snapshot backed by a fresh proof, then route or reject when the proof expires. | Local read latency and limited read continuity during isolation. | Proof tracking, replication and expiry handling. A fallback surge can overload the authority. | Proof age, fallback load, expired-snapshot rejections or observed freshness violations increase. | The operation needs the latest committed state or the snapshot age cannot be established. | [Consistency and partition decisions](../lessons/M01-L03.md) |
| Shared edge outage disables both regional paths | Improve or isolate the edge before adding more serving regions | Reduce the common dependency or improve its availability and verify each surviving path. | Reduces outages that regional redundancy alone cannot absorb. | More operational and deployment complexity. | Both regional paths fail during the same edge event. | Measurements show independent regional failures dominate and the shared edge already meets its allocated budget. | [Availability and failover budgets](../lessons/M01-L04.md) |

[Reference solution and rubric](solution-rubric.md)
