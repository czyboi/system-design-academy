---
id: M10-decisions
status: draft
---

# Whole-system decisions across eight M10 cases

## Compare components only after naming the invariant

The **feed/search platform** composes canonical post durability, asynchronous home projections, a versioned crawler page source, query-index source cuts and permission-aware result caching. No one component establishes the user-visible correctness of the whole. If the dominant requirement becomes *no content after confirmed revocation*, a final serialized content-release gate and a policy for already-issued capabilities are necessary; TTL and index generation alone do not prove the promise.

## Case decisions, evidence and cost

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Paste/redirect link must remain unique and safely expirable | Durable mapping + immutable object + tombstone | Claim stable create ID before work, versioned read and cleanup | Replay-safe link and defined expiry | Cross-store reconciliation, cache/CDN purge | Duplicate ID on retry or expired cached bytes | Strict immediate revocation without an authoritative read gate | [M10-L01](../lessons/M10-L01.md) |
| Celebrity post makes two million fan-out writes | Hybrid feed | Canonical post/outbox; push ordinary, pull celebrity; viewer filter on read | Avoids single burst of replicated inbox writes | Hot author reads, fan-in and projection lag | Missing ordinary entry, leaked private entry | Uniform low-follower corpus already meets workload | [M10-L02](../lessons/M10-L02.md) |
| Page changed but search returns old terms | Versioned crawl store and index-generation publish | Durable page/index intent, guarded version, shard source-cut manifest | Distinguishes fetched from query-visible freshness | Reindexing and manifest barriers | v1 reappears after v2, g17 claimed fresh | Explicit best-effort browse with accepted age may be simpler | [M10-L03](../lessons/M10-L03.md) |
| Bank refresh replay changes source transaction state | Provider-cursor/transaction-identity reconciliation | Stage change set, atomically apply current records/cursor, version budget totals | Prevents duplicate spending and false alerts | Provider lag/credentials, corrected view work | Pending+posted double count | Provider lacks documented incremental contract | [M10-L04](../lessons/M10-L04.md) |
| Shortest authorized graph path across partitions | Layer-complete BFS with batched adjacency | Per-query visited/parents, owner routing and visibility revisions | Exact shortest proof under declared snapshot | High-degree expansion and RPC cost | Partition timeout misreported no-path | Approximate recommendation need not guarantee shortest | [M10-L05](../lessons/M10-L05.md) |
| Hot search keys and cache-node failure | Generation/rank/scope-aware cache-aside | Verify complete result, gate late fill, coalesce misses, cap origin | Reduced origin reads with correct staleness policy | Memory duplication, version routing and cold misses | Fast stale top-20 or origin overload | Unique queries or protected read-gate cost outweigh hits | [M10-L06](../lessons/M10-L06.md) |
| Late return changes weekly ranking | Canonical sale revisions and whole result manifest | Dedup source IDs, two-stage sort, publish source-cut version | Reproducible ranking and cheap reads | Shuffle, skew, correction complexity | Old job replaces corrected table | Small SQL aggregation satisfies hourly deadline | [M10-L07](../lessons/M10-L07.md) |
| Web fleet scales but relational writer stays saturated | Measure and evolve EC2/SQL→S3/RDS→ALB/AZ→cache/replicas→Auto Scaling/workers | Separate bottlenecks and failures; queue media; preserve write invariant | Independent resource scaling and resilience | More consistency and operational boundaries | Writer backlog despite more web nodes | One simple host already meets workload and recovery needs | [M10-L08](../lessons/M10-L08.md) |

The synthesis `M10-S1` relies on M10-L02-LO2, M10-L03-LO1 and M10-L06-LO2. **Each lesson's own assessment** remains responsible for its LO1/LO2 coverage; this exercise is not an extra quiz for the other five cases.
