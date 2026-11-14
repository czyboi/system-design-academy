---
id: M05-decisions
status: draft
---

# Storage model decisions

## Choose by access path and invariant

Start from known-key lookup, indexed attributes, ordered time ranges or edge expansion, and identify the amount of data each path reads. Then mark which state changes must become visible together and which reads can lag. Compare actual API and placement guarantees. Use replay and repair for state whose representation can lag, and reserve coordinated writes for invariants that cannot be resolved after independent promises. [M05-L01](../lessons/M05-L01.md) · [M05-L02](../lessons/M05-L02.md) · [M05-L03](../lessons/M05-L03.md).

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Exact lookup with a strict revocation rule | Durable keyed authority | Derive the key and read confirmed state under its authoritative contract. | Direct routing and precise denial. | Authority latency and outages. | Accepted stale positive or unverified failover. | A compound invariant extends beyond the keyed operation without transaction support. | [M05-L01](../lessons/M05-L01.md) |
| A bounded product aggregate has attribute queries | Indexed document | Embed co-updated fields, index predicates, maintain compatible versions. | Convenient aggregate reads and local atomic changes. | Index maintenance and schema rollout. | Missing new documents or freshness misses. | The main queries require broad joins or unbounded embedded data. | [M05-L01](../lessons/M05-L01.md) |
| Time ranges must stay local while ingestion grows | Wide-column | Encode device and time, bucket hot writers, store corrections by version. | Bounded scans with predictable routing. | Bucket fan-out and retention configuration. | Hot ranges or missing correction history. | Required keys or scans are unpredictable. | [M05-L02](../lessons/M05-L02.md) |
| The next lookup follows a relationship | Graph or adjacency representation | Find a seed, traverse relevant edges and track completeness. | Direct expression of relationship queries. | Supernode and remote traversal work. | High edge expansion or frequent incomplete results. | A fixed bounded lookup suffices with lower repair cost. | [M05-L02](../lessons/M05-L02.md) |
| Concurrent writes must preserve one shared invariant | Coordinated transaction | Commit the claim and receipt atomically with scoped isolation and durability. | One authoritative outcome. | Coordination delay and availability trade-off. | Contention or unverifiable success on retry. | Operations can merge safely and the workload benefits from that choice. | [M05-L03](../lessons/M05-L03.md) |
