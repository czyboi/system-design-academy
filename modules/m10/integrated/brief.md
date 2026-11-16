---
id: M10-EX1
status: draft
outcomes: [M10-S1]
---

# Compare two full content-platform designs, then change the dominant constraint

The platform offers **author timelines**, **home feeds**, **public page search** and **cached top-K results**. User posts arrive through authenticated publication; an independent crawler fetches permitted public pages. The source streams, visibility rules and index source cuts are distinct. A successful crawler fetch is not proof of a fresh search result, and a successful post commit is not proof every follower received its home-feed entry.

## Scenario: original workload and user-facing contracts

| Work | Declared input (synthetic, not production statistics) |
| --- | --- |
| Social publication | 100,000 posts/day, 200 followers/author on average; one author with 2 million followers |
| Home reads | 500,000 original feed opens/day; 800 ms receipt deadline |
| Crawler | Up to 2 million successful public-page fetches/day, average 50 KiB response body |
| Search | 10 million original queries/day, top 20 from three disjoint index shards |
| Cache | 100,000 hot keys, 4 KiB value/key; two nodes initially own disjoint key ranges |
| Search contract | Strict export: client receives complete, authorized top-20 from one verified current generation within 300 ms; browsing may accept labeled partial results |

Ada publishes post `a10` at 10:00:00; celebrity Zee publishes `z55` at 10:00:01. Ben follows both, Cara follows Ada. Ada's fan-out reaches Cara at 10:00:02 and Ben at 10:00:08. A crawler persists changed public page `u1:v2` at 10:10 after the page changes from “steel filter” to “coffee maker”. At first the query index remains on generation `g17` holding `u1:v1`; an index event for v2 will later permit publishing `g18` after relevant shards confirm its source cut. A cache node serving half of the hot keys fails during a peak, and an old `g17` fill is in flight.

The team proposes **two whole-system architectures**.

**Design A:** eagerly fan out every post to every follower; cache search results only by normalized query and insertion-time TTL; return whatever shard hits arrived before deadline without a completeness/generation label. It optimizes for seemingly fast reads and a simple API.

**Design B:** persist canonical post plus recoverable outbox intent, push ordinary posts with deduplicated inbox writes, pull high-fan-out author posts at read time and re-check viewer visibility; persist immutable crawler page versions and durable index intents; publish verified index-generation/source-cut manifests; key search cache by query, filters, scope, rank model, page and generation; fail strict exports that are incomplete or unproven fresh. It adds metadata/operations and sometimes rejects work to preserve the contract.

Initially prioritize read latency and predictable cost. Then **change only the dominant constraint**: after the API acknowledges revocation of a hosted private post or its generated search/media view, no protected API/managed-cache path may release its bytes, title or snippet. Assume revocation confirmation and content release can be ordered at a common authoritative security boundary. Explain whether either design can uphold that promise *when a read has started before deletion*, and what architectural constraint must be added. No server can retract bytes already delivered to an external client.

## M10-EX1 — Required learner deliverables

1. **Capacity and baseline.** Calculate fan-out entries/day, approximate crawl bytes/day and search-cache raw value memory. Draw the smallest correct durable post, crawler page store, index publication and search request paths. State which steps are asynchronous, where stable operation IDs and current permissions are checked, and which component can prove progress.
2. **Compare A versus B.** Walk Ada, Zee, Ben/Cara, `u1:v2`, `g17→g18` and the cache-node loss through both. Find at least three cases where Design A delivers a fast but wrong answer, and at least three real costs/failure modes in B. Trace a retry of the same post, page event and original query without double effects or new client deadlines.
3. **React to the dominant-constraint change.** Define the revocation-confirmation event, protected content-release event and their serialization. Show the race between an in-flight permission check and deletion; cover old search snippets, ranking changes, stale cache fills, object storage, direct/CDN URLs and physical cleanup. State what stronger authority or bounded relaxation is needed; do not just say “purge the CDN.”
4. **Measure and falsify.** Define original-operation home-feed and strict-search SLIs with population, ingress/receipt events, measurement window, deadline, correct/authorized/completeness/freshness thresholds and treatment of retries, rejections, failures, partial, stale, late and timed-out responses. Propose load, partition and late-event tests capable of disproving the design.

Deliver one coherent architecture critique, a compare-and-change decision table, a user-visible failure trace and a test plan. Use [M10-L02](../lessons/M10-L02.md), [M10-L03](../lessons/M10-L03.md) and [M10-L06](../lessons/M10-L06.md). The other five M10 cases are assessed in their own lesson companions; this integration does not claim they are retested.
