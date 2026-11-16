---
id: M10-EX1-solution
status: draft
---

# Reference comparison, constraint change and rubric

## Derive load and the smallest correct flow

Naïve full feed fan-out is `100,000 × 200 = 20,000,000` recipient-inbox entries/day, about **231/s average**, *before retries and celebrity skew*. Zee's one post alone represents two million inbox writes. Raw crawl input is `2,000,000 × 50 KiB ≈ 95.4 GiB/day`, before compression, duplicate bodies, indexes and replicas. The raw search-cache value set is `100,000 × 4 KiB ≈ 391 MiB`, excluding keys/metadata. Two **fully replicated** copies would need ≈782 MiB; two **disjoint shards** together still hold ≈391 MiB raw, with a cold-miss blast radius if either fails.

A baseline design uses:
```text
Post API -> atomic canonical post + runnable outbox intent -> durable post store
                                              |-> recipient fan-out projection
                                              |-> eligible search-index event
Crawler frontier -> fetched immutable page version + durable index intent
                                        -> shard workers -> verified source-cut manifest
Home read -> inbox + bounded celebrity pull -> viewer check + dedup/merge -> client
Search read -> versioned/scoped cache -> shard coordinator -> top-K/coverage check -> client
```

Publishing a post does not wait for two million inbox writes; its successful response confirms the declared durable canonical-post contract. The authoritative page store may hold `u1:v2` while generation g17 still contains v1. A valid query pin and the manifest are necessary before claiming g18 freshness, and a cache hit can reuse only a response that satisfies the requested version and permissions.

## Compare observable behavior

| Event | Design A | Design B |
| --- | --- | --- |
| Ada `a10` | Ben's 10:00:03 home feed may miss a10; relying on worker completion as post durability is wrong | Post and outbox already durable; Cara sees a10, Ben's projection lag is measured; unique `(recipient,post_id)` prevents retry duplication |
| Zee `z55` | One job may generate two million writes and starve other authors | Pull a bounded celebrity recent set at read time; this creates a *hot-author read* cost and merge complexity |
| Crawler `u1:v2` | Fetch success may be mislabeled “search updated”; g17 can still return steel filter | Durable index event removes old postings, adds new title/snippet and publishes g18 only after required source-cut acknowledgments |
| Cache node fails | Cold misses can overload origin; TTL may still return obsolete or private-scope results | Bound origin concurrency, coalesce hot misses, propagate client deadline and reject or label staleness per contract |
| Slow shard | Responding shards may omit the highest-scoring unseen result yet answer “complete” | Strict export explicitly fails; browsing can return a labeled partial result if allowed |

Design A can fit a uniformly small-follower, public, bounded-staleness product *after* correcting unsafe contracts. As proposed, it does not satisfy this strict export or private visibility requirement. B improves answer provenance and controls skew but adds durable intent, version routing, storage, source-cut reconciliation, on-read merge and stronger failure/refusal policies. A queue delivery retry must use a stable post ID; an old indexing worker cannot replace v2 with v1; a retried client query retains first-ingress deadline.

## Revocation confirmation is not merely cache expiry

**Neither Design A nor basic B guarantees no disclosure after confirmed revocation.** A correct generation-scoped cached result still risks a stale authorization decision taken before deletion. The product needs a **serialized protected release boundary**: a read permit coupled to actual content release (or a revocable one-time send token checked at release) must order with the authoritative generation/tombstone transaction that confirms revocation. Confirmation cannot be returned while an earlier permit is still free to release bytes afterward. Abort/fence in-flight work or wait for already-permitted releases to finish *before* acknowledging deletion.

```text
R1 reads permission at generation 8 -> starts preparing old result
D1 requests revoke -> new authoritative generation 9
D1 may confirm only after R1's allowed release completes or is cancelled/fenced
R2 after confirmation -> final authoritative gate rejects generation 8
Delayed g8 cache fill -> cannot reinstate an answer under generation 9
Old search snippet / old CDN object -> no protected path bypasses final gate
```

A strictly streaming response may require stream cancellation and an acknowledgment boundary or a narrower contract; a presigned/bearer URL already issued can remain usable outside the gate until expiry unless the architecture prevents direct use. It is impossible to retract bytes already downloaded; do not promise that. For externally crawled public pages, the service can de-index its own copy but cannot guarantee deletion from a third-party origin or client cache.

A deleted document can shift the whole top-20, and its title/snippet can leak even if the body is protected. Make search generation invalidation or dependency proof cover ranking and snippets; apply a final authorization check to protected results. Physical blob deletion and CDN propagation are asynchronous cleanup states separate from the server's revocation confirmation.

## SLIs and falsification

**Home SLI:** of all original valid feed opens first entering API in each five-minute window, 99% must return an authorized up-to-20 page to the managed client within 800 ms, with the documented routine-author visibility delay and stable ordering/ranking. Carry one ID through retries; count rejected, wrong, stale, timed-out, failed and late originals outside the numerator. Track **meaningful coverage** separately so returning an empty page for every request cannot be called success.

**Search SLI:** of all original valid strict export queries, 99% must return an authorized, complete top-20 from a verified matched source-cut generation and ranking policy at the managed client within 300 ms. Missing-shard, old-generation, wrong-content, rejected, failed and late responses are failures, even if admitted-success latency looks good. The targets are **illustrative product requirements**, not vendor performance guarantees.

Falsify by crashing the fan-out worker after partial delivery and replaying; load-test a Zee publication alongside ordinary posts; crash after `u1:v2` persistence but before index dispatch; deliver late v1 after v2; fail half the cache during peak while measuring origin admission; make a shard exceed cutoff; delay an old cache fill; race a private-post read against confirmed deletion and try every text/snippet/media/CDN path. Inspect request IDs, first ingress/client receipt, source cuts, result generation, permissions, outbox state, original failures and actual storage mutations rather than green controller status.

## Self-evaluation rubric (16 points)

| Dimension | Points | Full-credit reasoning |
| --- | ---: | --- |
| Workload and state | 3 | 20m fan-out/day, ≈95GiB crawl/day, ≈391MiB raw values and correct post/crawler/index authority |
| Full-design comparison | 4 | Ben/Cara/Zee, g17/g18, failed cache node, three A errors and real B costs with retry handling |
| Changed invariant | 5 | Serializes revocation with content release; explains in-flight race, snippets, caching, object/CDN and already-issued URL limits |
| User outcomes/tests | 4 | Exact original-operation SLI populations, deadlines, freshness, completeness and concrete falsification tests |

Equivalent designs earn full credit if they prove the same external invariants and account for failure/operational cost. Naming a product is not proof.
