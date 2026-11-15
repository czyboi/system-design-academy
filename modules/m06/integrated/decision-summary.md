---
id: M06-decisions
status: draft
---

# Cache decisions

## Work through a cache failure

An equipment catalogue serves repeated public searches and low-reuse staff searches. Cache ordered public result pages in the application and scope by normalized query, variant and source version. A price change that crosses a filter can make a new ID appear. Advance the generation for the complete affected dependency domain with the authoritative write; unaffected domains retain their own generation. A late fill for the earlier generation stays ineligible for a new lookup. After a rank rollout, look up the new tuple and calculate a new route.

Use sharded primary entries to spread the working set. Put the hottest public query on more than one read path when its per-key load exceeds an owner. On node loss, check replica generation and source age before reuse and protect the origin with shared fill coalescing and admission. Copying cannot renew source age; account for refresh and recovery work inside the same budget and pace or shed requests when eligible copies or capacity are insufficient. Track slow, unavailable and ineligible original searches alongside cache hit rate. If repeated scans are evicting useful results, compare selective admission with simple LRU by their measured refill load.

## Choose location, granularity and update behavior together

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Many callers use the same public page | Shared application query cache | Key by authorized variants and cache the ordered page | Avoid repeated ranking | Duplicates entries across similar queries | New matching ID missing from page | Low query reuse or unclear sharing | [M06-L01](../lessons/M06-L01.md) |
| Different queries share assembled records | Object cache | Fetch ranked IDs then load assembled cards by object and variant | Reuse object construction | Query, hydration and object invalidation remain | Repeated card refill or mixed revisions | Whole-page computation dominates | [M06-L01](../lessons/M06-L01.md) |
| A version determines eligibility | Cache-aside with revision keys | Check the authority and bind fill to source snapshot | Late fills remain in their own generation | Adds a lightweight source check and cold misses on change | Generation mismatch or lost origin headroom | Lookup is already as expensive as serving the value | [M06-L02](../lessons/M06-L02.md) |
| Recent access predicts reuse | Bounded LRU | Move the accessed entry to the head and evict from the tail | Keeps frequently revisited recent entries | One-off scans can displace the working set | Evictions followed by costly refills | Stable hot values face repeated large scans | [M06-L03](../lessons/M06-L03.md) |
| Distinct keys exceed one node's memory | Shard plus selective replicas | Route primaries by key and copy hot or recovery-critical entries | Spreads memory and hot-read load | Replica storage and change coordination | Uneven lookup rate, invalid replicas or cold-fill surge | Working set is small and operating cost dominates | [M06-L03](../lessons/M06-L03.md) |
