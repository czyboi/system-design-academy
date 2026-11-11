---
id: M01-EX1
status: draft
outcomes: [M01-S1]
---

# Workload and failure policies for order status

A regional service records order status events and serves customers checking shipment progress. The customer display may show an older status for at most 60 seconds after its data fell behind, with a visible freshness label. A support operation authorizes a refund based on the authoritative status. Treat the authorization as part of the same coordinated operation that checks the status. Both policies require the current authority for writes and refund authorization.

| Input | Planning assumption |
|---|---|
| Traffic | 864,000 customer reads and 86,400 event writes per day. Peak is 12× daily average in each direction. Size for an extra 25% above that peak. |
| Payload | 2 kB per read response and 1 kB per stored or submitted event. Use decimal units. |
| Storage | Constant event rate, 30 days of retention and three full copies. |
| Performance | Good customer reads should have measured p99 of at most 200 ms at the modeled peak. |
| Failure | One serving zone can be lost. A network split can isolate a serving path from storage authority while its local projection remains reachable. Both policies require a shared authorization dependency. |

Compare **Policy A**, where every read uses the authoritative store, with **Policy B**, where the customer display may use a local applied projection during a split. Assume a conservative bound on projection lag is available when using that fallback. Apply the 60-second cap and decline a read if the bound is unknown. Refund authorization and writes still require authority.

## M01-EX1

Produce a one-page workload and failure model. Calculate averages, peak rates, capacity with headroom, payload bandwidth and retained bytes. Give a critical-path latency budget and explain how you would find the limiting resource. Trace a committed shipment update and all affected operations during an isolated read path, including what changes after 60 seconds.

Estimate time availability with an explicit dependency model. For the customer read path, model two alternative branches, each 99.9% available under an assumed workload, and shared authorization at 99.95%. Start with independent failures and immediate routing to a ready, sufficiently sized branch. Then give a common failure or transition that makes this estimate optimistic and one measurement to verify your chosen design.

## M01-S1

Use the workload model to defend consistency and failover decisions for specific operations. This exercise draws on [capacity](../lessons/M01-L01.md), [consistency](../lessons/M01-L03.md) and [failover](../lessons/M01-L04.md).
