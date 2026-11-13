---
id: M04-decisions
status: draft
---

# Relational scaling decisions

## Match the scaling change to the evidence

Use the query plan to identify expensive operators under the current workload. Move filtering and bounded selection earlier when query semantics allow it. If pressure remains, compare read replicas and derived views against the required freshness. Keep the write authority clear during promotion. When the leader's writes or data outgrow one owner, route on a key that keeps each strict transaction local, and account for a tenant whose traffic overwhelms a shard. Verify the proposed design with the same load, correct-response deadline and failure schedule. [M04-L05](../lessons/M04-L05.md) · [M04-L02](../lessons/M04-L02.md) · [M04-L03](../lessons/M04-L03.md).

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A plan enriches thousands of rows for a small list. | Tune query and index. | Limit a deterministic ordered set before eligible enrichment. | Reduces work at one owner. | Extra index maintenance. | Write WAL rises or an eligibility filter changes results. | Enrichment decides membership or ordering. | [M04-L05](../lessons/M04-L05.md) |
| Stale-tolerant read load remains high. | Add read replicas. | Route qualifying requests to applied copies. | More read capacity. | Network, replay and routing. | Lag or version misses grow. | Leader writes dominate or required freshness cannot be proven. | [M04-L02](../lessons/M04-L02.md) |
| Billing contention is independent of order writes. | Federate by capability. | Keep one database owner per domain. | Independent capacity and changes. | Cross-domain composition. | Remote dependencies prevent a complete answer. | One strict transaction spans the proposed boundary. | [M04-L03](../lessons/M04-L03.md) |
| One owner cannot sustain independent checkout groups. | Shard by invariant scope. | Route by tenant and, for the hot merchant, by location. | Splits write capacity. | Fan-out, skew and migration. | A hot key saturates one shard. | Required invariants span the proposed keys. | [M04-L03](../lessons/M04-L03.md) |
| An expensive summary is read repeatedly. | Store a derived view. | Project committed state and track its version and checkpoint. | Moves aggregation from reads. | Extra writes, lag and rebuild. | View freshness misses increase. | The view would decide a strict write invariant. | [M04-L04](../lessons/M04-L04.md) |
