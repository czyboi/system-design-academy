---
id: M06-EX1
status: draft
outcomes: [M06-S1]
---

# Keep a parts search usable when a cache node fails

A public parts directory ranks matching listings. Results vary by parsed query, locale, filters and page. A rights check runs before access. In the drill all queries are authorized. An edit can add a record that was missing from the old first page, and a ranking rollout changes order. The origin can make catalogue edits and their generation visible in one transaction. Define how a response proves which snapshot and ranking rule it represents.

| Quantity | Assumed envelope |
| --- | --- |
| Offered traffic | 600 original searches/s for ten seconds. One query accounts for 300/s. |
| Cache fleet | Three primary shards, 96 MiB per node, 20% reserved. Each node can process 350 total lookups/s including misses. Each live node owns 40 MiB of the steady primary working set. |
| Entry budget | 30,720 useful primary entries at 4 KiB per entry including metadata. Reserve at most 8 MiB per node for selective copies. During a node loss each survivor receives at most 20 MiB of primary entries; plan its cache-miss warm-up. |
| Routing after loss | The ordinary traffic spread is at most 160 lookups/s on either survivor. The hot query can be split across both survivors. |
| Origin after loss | For the non-hot workload, 40 normal cold requests/s plus 110 distinct additional cold keys/s would need expensive reads before the proposed protection. These sets are disjoint. Selective copies can cover 45 of those additional distinct requests/s when current and healthy. |
| Dependency capacity | At most 120 expensive query starts in any rolling second. Lightweight authorization and generation checks have a separate allowance of 800 reads/s. The primary can return both in one lightweight read. An attempt charges the relevant allowance, including retries and warm-up. |

During the ten-second drill, lose one cache node and commit one change affecting the hot first page. Freeze other fixture changes. Count one outcome per original search arriving during the window, including retries under that original. An on-time success returns a complete ordered page within 200 ms of first arrival. It must match the authoritative generation observed by that request's generation check, use its required ranking version, and use a source observation no older than two seconds at response. A check that overlaps a change may observe the older generation. Use comparable clocks with margin for error. Obtain generation and ordering evidence from the actual returned page. Complete the observation window for the last arrivals. The target is 98% of originals. A candidate returned 5,770 on-time eligible results, 170 unavailable responses and 60 late or ineligible results.

## M06-EX1

1. Choose a cache location, granularity, key and eviction rule. Compute the storage and lookup envelopes after one failure.
2. Trace a cache hit, an in-flight fill overlapping the edit, and warm recovery or cold fallback on node loss. Include owner selection, generation and rank tests, shared coalescing, and exhaustion of either dependency budget.
3. Compare selective replication with the unprotected origin demand. Score the observed trial and explain which traces and metrics would show where the candidate missed the target.

[Reference solution and rubric](solution-rubric.md) · [Decision summary](decision-summary.md)

## M06-S1

Connect cache granularity, a coherence trace and distributed layout. [Cache boundaries](../lessons/M06-L01.md) · [Coherence policies](../lessons/M06-L02.md) · [Query-cache routing](../lessons/M06-L03.md).
