---
id: CP-01-reference
status: draft
outcomes: [CP-LO1, CP-LO2, CP-LO3, CP-LO4, CP-LO5, CP-LO6]
---

# Marketplace capstone — reference design, variants and rubric

This is **one defensible reference solution**, not a unique correct architecture. Equivalent alternatives earn credit only when they preserve the stated inventory and authorization invariants under all injected failures. Numbers below come from the original synthetic capstone brief, not observed product workloads.

## CP-LO1 — Bound the product and estimate it

User-facing hard invariants take precedence over eventual read freshness:

- For one-unit listing L7, `active_reserved_quantity + completed_sold_quantity <= 1`, with every unit consumption serialized at one authoritative listing/reservation owner. If a reservation expires, completion cannot race and reconsume its freed unit; condition on the current reservation version/status and deadline.
- An accepted original reservation has exactly one input-bound outcome and durable recoverable intent; it may be notified multiple times, but it must not consume stock twice.
- Any private listing/media/chat read requires current authorization at its declared enforcement point; an index/CDN URL alone is not permission.
- Feed, keyword index and weekly popularity ranking are **materialized views** and may lag within the promised bound, never authorize a stock decrement or reveal protected data.
- The system prioritizes invariant safety over new-write availability when no exclusive regional owner can be established.

The load model computes: 1m views/day /86,400 = 11.57/s mean, ×20=231.5/s peak; 500k searches/day =5.79/s mean, peak115.7/s; 200k messages/day=2.31/s mean, peak46.3/s; 20k reservations/day=0.2315/s mean, peak4.63/s. If 10k daily listings each upload four 3 MiB images, 40k images/day consume 120,000 MiB =117.19 GiB/day; over 365 days ≈41.77 TiB raw, excluding derivatives, replicas and deletion. Listing metadata 10k×3KiB ≈29.3 MiB/day. For messages choose a declared **synthetic average** of 1KiB payload: 200kKiB/day≈195.3MiB/day, ≈69.6GiB/year of payload alone. Actual encoding, indexes, retention and replication increase this; do not silently present exact total disk requirement.

The 500ms reservation response budget could reserve 40ms for ingress+auth, 70ms for regional routing, 190ms for conditional transaction/replication, 50ms for response and **150ms safety/queue margin**; these are allocations, not measured p95s. At peak, a single hot listing can attract a large fraction of reads without proportional writes; measure skew by listing ID, region and search keyword. For the search 250ms p95 target, sample full end-to-end valid original reads including cache misses rather than index-only latency.

## CP-LO2 — Interfaces and end-to-end architecture

```text
Clients A/B -> regional gateway(auth, idempotency, deadline)
    --writes--> Listing/Reservation Owner A -> transactional database
                   |-- same transaction --> Outbox
                   |                           -> relay -> retained event log
                   |                                   -> feed/search/rank/report projections
                   |-- receipt --> gateway -> client
    --> Media Staging -> object store -> authorized guarded publication
    --> Conversation Owner -> message DB/receipt -> offline fanout
    --reads--> edge cache / search index / regional listing projection
Operations: tracing, original-op metrics, queue lag, snapshot offsets, audits
```

**Source models (one viable schema):**

```text
Listing(id, seller_id, state, stock_total, stock_available, version, home_epoch)
Reservation(id, listing_id, buyer_id, qty, state, expires_at, version)
OriginalReceipt(scope, original_id, canonical_input_digest, outcome, created_at)
Outbox(event_id, aggregate_id, aggregate_version, payload, state)
MediaVersion(media_id, listing_id, owner, object_version, status, access_rev)
Conversation(id, owner_epoch, membership_rev, latest_seq)
Message(id, conversation_id, sender_id, sequence, payload, status)
ProjectionOffset(view_id, partition, committed_offset, source_revision)
```

A unique key such as `(buyer_id, original_reservation_id)` prevents new command IDs from colliding across buyers. Input binding compares canonical listing, quantity and expiry policy with the stored receipt. `reserveListing(actor, listing, qty=1, original_id, expected_version?)` checks authenticated buyer and eligibility at the owning DB; the API returns `reserved(reservation_id,expires_at,listing_version)`, `out_of_stock`, `policy_rejected` or `unknown/reconcile` for ambiguous transport. A definite failure after no commit is distinguishable from lost response after commit by querying receipt.

`createListing` validates seller identity and stores listing+outbox in one commit, initial state draft. `publishMedia` commits a reference only after private upload/object verification and a current access revision. `releaseReservation` requires current reservation ID+version and an unused/not-completed unit. `sendMessage` uses stable original ID and conversation-local membership/sequence. `search(query,cursor)` returns index revision and freshness metadata; read stale availability is advisory and private records require authorization. `getWeeklyRanking(category,week)` returns ranking revision and an explicitly named closure/correction policy, never the source of sales or quota truth.

Transactional outbox couples authoritative state changes with recoverable publication intent. The relay can resend, so consumers deduplicate by `event_id` and aggregate version; each stores projection state and consumed progress consistently. A client read hitting cache may see a stale listing while checkout always validates source. Index rebuild can replay a retained log only if necessary history still exists; otherwise reconstruct from a versioned source snapshot plus subsequent events, with a documented gap/offset cutoff.

## CP-LO3 — Reservation state and five failure traces

### Race: two buyers, one unit

Initial L7 has `stock_available=1`, `version=20`. U1 sends R1 from A; U2 sends R2 from B. Both must route to the **same** current owner/transactional authority, not two independent region-local decrement stores.

| Committed order | Stock after | Reservation / response |
| --- | ---: | --- |
| R1 checks in one write transaction, reserves one unit, commits receipt/event | 0, listing v21 | R1 becomes active, U1 gets `reserved` |
| R2 checks current stock, sees 0 | 0 | R2 returns `out_of_stock`, no consumption |
| U1 response lost, identical R1 retry | 0 | Durable original receipt returned, no new reservation |
| Retry with R1 but changed listing/qty | 0 | Input identity conflict |
| R1 expiry worker retries after completed sale | unchanged | Guarded status/version disallows resurrecting/releasing sold unit |

A DB row update can guard `stock_available >= qty` and return affected rows; one coherent transaction records Reservation, Receipt, Listing revision/stock and Outbox. If the chosen infrastructure lacks such a common commit, propose a single-writer reservation state machine with equivalent durable event/receipt semantics and explicitly prove it. An eventually consistent cache update is **not** the stock commit.

Reservation lifecycle: `available → reserved → completed` or `reserved → expired/released`; a released unit may be reserved by a new ID. A scheduled expiration event must check `state=reserved and version=current and clock>=expires_at` before returning stock once. Idempotent stable receipts prevent retries of release from double incrementing available count. If payment/settlement is introduced later, it is a distinct saga and does not imply atomic external charge.

### Duplicate event and index projection

Outbox E21 for listing v21 is published twice after a relay crash. Projection consumer uses stable `event_id` and monotonic `aggregate_version`, so a second E21 cannot double increment weekly ranking or undo a newer listing v22. A consumer records its applied event and progress in one compatible commit, or can reconstruct via idempotent state transitions. A daily/weekly ranking should count unique accepted business event identities, not every delivery attempt.

For example, seller listing creation E1 at 23:59 and event delivery at 00:02 next day belongs to the **event-time week** defined by the product. A replay can revise a preliminary weekly rank before a documented watermark/closure; after immutable final closure late corrections must become an explicit revised report version or a recorded adjustment, not silently shift past numbers. Decide the allowed lateness from measured event delays; no invented zero-lag guarantee.

### Stale cache/search and media privacy

Search index says L7 available even after v21 reservation. The read is stale within the ordinary 60-second projection contract, but reserveListing rechecks v21 and returns out_of_stock. Display a soft `availability_as_of` indicator if needed; never promise a hard stock hold based on a search result.

For media P1, the seller stages bytes privately, completes upload, and crashes before publishing. Recovery confirms owner+listing revision and object readability, then commits one `MediaVersion` reference plus event. The staging key is not a public CDN URL. After revocation, use an **access boundary** (signed/authorized CDN path, versioned cache keys or token invalidation) that satisfies the chosen revocation deadline. A raw long-lived public URL defeats revocation no matter how quickly metadata changes. If CDN invalidation is delayed, either shorten authorized URL validity, route protected content through authorization or explicitly document weaker revocation semantics. Never claim ordinary TTL is immediate privacy enforcement.

### Hot key or hot partition

One celebrity listing receives most of the peak 232 reads/s. Replicate immutable read metadata or cache it under version-aware key; do not shard the one-unit stock decision across concurrent independent writers. For search/ranking partitions, histogram key skew, lag and sink backpressure. A hot keyword may need read-serving replicas or partitioned query cache; a hot ranking category may need a mergeable count map with dedup IDs and explicit consistency between partial reducers. Scale read projections separately from the invariant-preserving write owner.

### Regional partition and recovery

B loses connectivity to authoritative region A. B may serve public read projections within a **degraded stale disclosure** and continue eligible local media/download reads only under authorization. B **must not** acknowledge new strict inventory reservations merely because its cache says L7 has one unit. Fail closed (explicit unavailable/unknown) or queue non-accepted intents that are visibly pending and later resolved by A; do not report them as confirmed stock holds.

If leadership migrates to B, the A owner must be fenced at the **durable listing/write resource** before B starts accepting, and B must recover a known committed history prefix. Old A may return from pause with buffered writes; epoch token/conditional commit prevents v21/v22 forks. Without proof of exclusive authority, stop admitting reservations rather than allowing double sell.

## CP-LO4 — Baseline plus two defensible variants

| Dimension | Baseline: one transactional owner region | Variant A: per-listing home region | Variant B: cross-region coordinated transactional datastore |
| --- | --- | --- | --- |
| Stock invariant | Single durable transaction for listing/receipts | One fenced current owner per listing; safe cutover | Serializable/linearizable transaction under vendor-configured failure model |
| Locality | A-region buyers fast; B buyers cross-region write RTT | Sellers/listings can reside near home; remote buyers route to home | Regional reads/writes may be convenient, but commit still coordinates |
| Partition behavior | B fails closed for new strict stock decisions | Affected listing home unreachable: fail closed or safely fenced migration | Must follow documented quorum/consistency behavior; not universal availability |
| Complexity | Simpler placement; one owner failure domain to manage | Routing, migration, stale owner fencing and rebalance | Higher coordination, operations and pricing/availability dependencies |
| Best fit | Current modest writes and rigorous correctness | Strong geographic locality and many independently owned listings | Validated need for cross-region transactions and operation envelope |
| Reject when | Global write RTT or region outage budget exceeds SLO | Handoff/proven ownership cannot be established | Product cannot afford quorum/cross-region complexity or chosen config can't satisfy contract |

**Explicitly rejected shortcuts:** (1) B and A decrement local stock independently, reconcile negatives later—violates one-unit invariant; (2) read cache/index availability as reservation authority—stale projection oversells. Alternative plans should also compare transactional outbox with a single durable per-listing command log. Kafka/queue transport by itself does not make a database write and external publish atomic.

A cost estimate must itemize write coordination/RTT, indexed read storage, object egress, log retention, per-region cache, replicas, projection backfill and operator toil. Do not claim financial superiority from the synthetic QPS alone; obtain current provider price and measured data movement if doing purchasing analysis.

## CP-LO5 — Security, operations and recovery plan

**Threat model:** compromised client can forge actor/seller IDs, repeat IDs with changed payload, replay media URLs and send after group removal. Authenticate on gateway and authorize again against the **resource's current owner** where invariants demand it. Avoid accepting membership or stock status solely from client state. Protect upload paths with limited signed credentials, object size/content checks, moderation hooks and versioned publication; do not expose staged originals to unauthenticated crawlers. Sensitive records require encryption/retention/access policy, but this capstone does not invent regulatory compliance certification.

**Observability/runbook:** trace original request ID through auth, route, DB commit/receipt, outbox, projection offset and user read. Alerts should distinguish admission failure, stock invariant breach (always critical), consumer lag >60s, replay gap, stale private-media access, reservation-expires-but-still-active, hot key saturation, owner epoch changes, and regional access loss. Maintain a bounded idempotency receipt retention longer than promised retry horizon, tied to the reservation's reconciliation need.

A reconciler independently scans durable outbox/reservation status and expired claims; it does not infer failure from missing queue delivery alone. On index loss, build new projection from consistent snapshot + retained event offsets, verify counts/permissions and atomically switch read routing. On old owner recovery, require resource-side fence and current revision. On incorrect source-of-truth stock, **pause affected listing admission** and reconcile authoritative reservation+sale ledger before reopening, not patch a cache number.

**Outcomes:** for an illustrative five-minute cohort of **10,000 valid original reservation intents**, 9,100 correct reserved outcomes arrive within 500ms, 600 legitimate out-of-stock decisions arrive timely, 150 time out, 100 fail and 50 arrive late. **Successful reservation** rate is 9,100/10,000=91%. **Timely correct decision** rate is (9,100+600)/10,000=97% **if** the 600 out-of-stock responses were indeed within the deadline. Neither meets the 99% decision target; the miss rate is 3%, above the 1% allowed budget for this cohort. Retry attempts are not new denominators. A double-book violation is a correctness blocker regardless of aggregate success.

## CP-LO6 — Architecture defense and evidence ledger

| Claim / decision | Primary or owning source | Source applicability / gap |
| --- | --- | --- |
| Retry with same identity must not duplicate effect | [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), caller request IDs | Stable input-bound receipts are **this design's requirement**, not a property automatically supplied by HTTP |
| DB commit and asynchronous notification intent | [AWS Prescriptive Guidance: Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), transactions and duplicate messages | External broker send can duplicate; consumer dedup required |
| Conditional guarded stock transitions | [PostgreSQL 17 transaction isolation](https://www.postgresql.org/docs/17/transaction-iso.html), isolation levels / conflict handling | Example mechanism, not evidence that this capstone runs PostgreSQL |
| Regional ownership/fencing | [M09-L03](../../modules/m09/lessons/M09-L03.md), distributed ownership topic | Upstream MS05 PR #100 unmerged, independent QA pending |
| Search indexes and log projection offsets | [M07-L03](../../modules/m07/lessons/M07-L03.md), [M08-L02](../../modules/m08/lessons/M08-L02.md), plus their evidence | Upstream MS05 M08 still unmerged; offsets/retention product-dependent |
| Media and CDN access/revocation | [M11-L04](../../modules/m11/lessons/M11-L04.md) and [M11-L02](../../modules/m11/lessons/M11-L02.md) | Upstream MS07 #121 unmerged; chosen CDN auth semantics must be validated |
| Cross-region datastore variants | [Spanner historical paper, Corbett et al. 2012](https://research.google/pubs/spanner-googles-globally-distributed-database/), [M13-L01](../../modules/m13/lessons/M13-L01.md) | No current vendor/version purchase or SLA guarantee asserted |

All diagrams, workload numbers, traces, failures and rubrics in this dossier are original. Do not reproduce research/industry graphics or assert license to republish third-party code. A current source/date/feature review is needed if an implementation chooses specific services.

## Weighted rubric (100 points, six outcomes)

| Category | Weight | Transfer outcomes | Full-credit evidence |
| --- | ---: | --- | --- |
| Requirements and estimates | 15 | CP-LO1 | Scope, non-goals, coherent QPS/storage/budget, hotspot and user SLI |
| Mechanisms and end-to-end traces | 25 | CP-LO2, CP-LO5 | Interfaces, authority, read/write separation, outbox, media, chat, projection and report path |
| Invariants and recovery | 25 | CP-LO3 | One-unit stock safety, privacy guard, idempotent receipt, five failure drills and recovery/fencing |
| Alternatives and costs | 15 | CP-LO4 | Baseline plus two viable variants, two rejected shortcuts, assumptions/operating costs |
| Security and operations | 10 | CP-LO5 | Permission model, source-side checks, privacy, detection/repair and runbook |
| Clarity and evidence | 10 | CP-LO6 | Coherent original diagrams, source date/section/version limits and justified design defense |
| **Total** | **100** | CP-LO1–CP-LO6 | Cross-module transfer, not every lesson outcome |

### Scoring thresholds and blocker rule

A proposed **formative** scoring guide is 85–100 strong, 70–84 needs targeted improvement, under 70 substantial rework. This is a *rubric*, not evidence of successful QA. **Critical invariant blockers override the total:** any realistic trace permitting two active reservations for a one-unit listing, unauthorized private media access, stale old-owner write acceptance, unreconciled acknowledged duplicate effect, or materially ungrounded current product guarantee requires a correction and re-review even if numerical score exceeds 85. The author must show an end-to-end falsifying test and repair for every such finding.

### Self-evaluation check

Before submission, mark each CP-LO1–LO6 with artifact section/trace, one decision rationale, one failure signal, and a source/evidence limitation. If any has no specific evidence, the capstone is incomplete. Independent technical/provenance and pedagogy/coverage reviews and human approval remain separate required gates; this reference answer cannot self-certify them.
