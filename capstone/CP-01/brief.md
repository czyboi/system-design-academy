---
id: CP-01
status: draft
outcomes: [CP-LO1, CP-LO2, CP-LO3, CP-LO4, CP-LO5, CP-LO6]
---

# Capstone: Design a multi-region community marketplace

A community marketplace lets sellers publish listings with photos; buyers search and browse activity feeds, message sellers, and reserve one-of-a-kind inventory. The product publishes weekly category rankings and account/usage reports. It serves users in two regions. An apparently healthy feed can show a sold item, a search index can lag, and an accepted reservation response can be lost. The critical design question is **which state may be stale and which operation must be exclusive**.

Your task is to design **one end-to-end product**, not list technologies. Use the supplied original workload, pin each invariant to its write owner, and defend where eventual read models are safe. Draw your own diagrams; do not reproduce architecture blog figures.

## Transfer outcomes and assessment map

| Outcome | Evidence expected | Primary teaching transfer |
| --- | --- | --- |
| **CP-LO1** | Bounded requirements and throughput/storage/latency estimates | M00–M01 |
| **CP-LO2** | Trace one public request and async update across API, gateway, source DB, object media, event log, cache, index and projection | M02–M08 |
| **CP-LO3** | Prevent overselling and unauthorized access; recover duplicate, stale and partitioned operations | M04–M09 |
| **CP-LO4** | Compare baseline and two alternatives by cost and failure guarantees | M10–M11 |
| **CP-LO5** | Show interface ownership, diagnostic signals and controlled repair | M09, M12 |
| **CP-LO6** | Defend source evidence, date, assumptions and gaps without copying diagrams | M13 |

These are **transfer outcomes**. The module lesson companions and module portfolios remain responsible for comprehensive course teaching coverage.

## The original workload — all assumptions are synthetic

One day has 86,400 seconds. Two regions A and B serve 100,000 daily active users combined. “Peak 20× mean” is a conservative **design assumption**, not measured traffic; distinguish sustained and burst load during testing.

| Operation / data | Daily original volume | Mean rate | Assumed peak |
| --- | ---: | ---: | ---: |
| Listing/description views, including feed clicks | 1,000,000 | 11.6/s | 232/s |
| Keyword search requests | 500,000 | 5.8/s | 116/s |
| Seller listing creates/updates | 10,000 | 0.116/s | 2.32/s |
| Buyer/seller new text messages | 200,000 | 2.31/s | 46.3/s |
| New original inventory reservation attempts | 20,000 | 0.231/s | 4.63/s |
| New images | 4 per new listing, assume all 10,000 creates | 40,000 | ~0.463 uploads/s |
| Average original image size | 3 MiB | 120,000 MiB/day (~117.2 GiB) | plus derived thumbnails, replicas and retention |
| Retention planning | 365 days original images, before deletion and new versions | ~41.8 TiB raw input-year | not including derived/replicated data, API logs or delete churn |

The listing-create/update volume is treated as **10,000 new listings/day for the image-envelope upper bound**; if some are updates, actual upload volume differs and must be measured. This capacity calculation is intentionally rough. Storage units use binary MiB/TiB. Plan 30-day rolling daily activity and weekly category ranking; no unbounded data retention promise.

Product SLO targets are illustrative **requirements**, not observed guarantees:
- Public search/listing reads: p95 <= 250ms for valid original requests under the declared peak load; allow a documented maximum search/feed projection staleness of **60 seconds** under healthy operation.
- Reservation: a **definitive, correct durable decision within 500ms** for 99% of valid original attempts under healthy-region conditions. Out-of-stock is a correct *decision* but not a successfully reserved item.
- Messaging: a stable accepted-message receipt within 300ms at the owning conversation authority, with offline delivery eventual; a network send attempt is not a delivered/read receipt.
- Media: confirmed publish only when the uploaded object and authorized version are durably readable via the declared object-store contract; transcoding/thumbnail availability may lag and must not misrepresent readiness.
- Regional partition: prioritize reservation correctness and permission checks over writes' availability. Serving stale authorized reads during a known outage is an explicit degraded mode, not normal-staleness compliance.

Non-goals: live video, real-time auctions, payment settlement, fraud-model training, cross-region atomic checkout+payment, multi-currency tax calculation, end-to-end encrypted messaging, and unlimited global write availability. The design may identify integration points without promising these products.

## Stage 1 — Bound requirements and ownership

Create a requirement ledger with hard invariants and softer projections. At minimum:

1. **Inventory:** for a listing with available unit count 1, at most one active committed reservation can consume that unit; no successful competing reservation may be issued under partition. A listing's authoritative version and owner must be unambiguous. Reservation expiration/release and seller cancellation need guarded transitions. An “available” search hit is advisory.
2. **Authorization:** only a seller or authorized staff role can update a listing; only valid chat participants can send/view permitted messages; private or revoked media cannot be served merely because cached. Product rules for blocked accounts, group roles and history retention must be stated.
3. **Identity/idempotency:** each original intent has a scoped stable key and input binding. Retrying after an ambiguous response cannot create a second reservation, duplicate listing, send or ranking contribution. A changed payload under the same key conflicts.
4. **Projections:** feed, search and weekly ranking are **rebuildable** from durable authoritative events or source snapshots; state the freshness and failure-repair contract. Do not treat a ranking cache as the source of inventory truth.
5. **Geography:** region A initially hosts authoritative transactional reservation/listing data; B is a read/media edge plus allowed asynchronous read projections. Region B cannot acknowledge a strict reservation while unable to coordinate with A or a proven exclusive per-listing owner.

Write explicit nonfunctional constraints for peak traffic, burst duration, retention, error budgets and the client-visible time windows. A request rejected because capacity is full remains a valid original for the user-outcome SLI.

## Stage 2 — Estimate capacity and budget latency

Compute the rates and original-image storage directly from the given data. Estimate metadata separately: assume 3 KiB metadata per new listing, yielding ~29.3 MiB/day (10,000×3 KiB), ignoring indexes and replicas. For messages, choose and document an average encoded payload, then estimate one year of retained raw payload separately from index/replication. Avoid adding an unexplained universal “3× replication” constant; the chosen store and failure domain set the actual factor.

Allocate the 500ms reservation decision budget across ingress/authentication, owner routing, authoritative transaction, response and safe margin. You may propose numbers but must explain they are **budgets**, not benchmarks. Make queuing and retry consume the same original deadline. A slow asynchronous notification is not allowed to block a transaction receipt unless the product contract requires notification visibility.

Calculate a separate search read budget for cache, query and index projection latency, including misses. Design hot-listing load tests, not just global mean QPS: a celebrity seller can concentrate all 232 peak views/s on one listing while writes remain low.

## Stage 3 — First viable architecture

Supply a diagram containing these **roles** and boundaries (product choices may differ if defended):

```text
Clients A/B -> regional API ingress, authentication, request ID
    -> listing owner / transactional DB (authoritative listing, reservation, receipts)
    -> transactional outbox -> event relay / retained log
          -> feed projection, keyword index, weekly category ranking, report jobs
    -> media upload service -> private object staging -> authorized publish
    -> chat conversation owner -> durable message receipts / offline fan-out
Reads -> regional cache + indexed materialized views (stale within explicit bound)
Ops -> trace/metrics/audit, replay checkpoints, dead-letter + reconciliation
```

Define a minimal API/data contract for `createListing`, `publishMedia`, `reserveListing`, `releaseReservation`, `sendMessage`, `search`, and `getWeeklyRanking`. For each write: actor, stable original ID, canonical input, conditional version, durable accepted point, output receipt, and terminal states. For each read: freshness, privacy/authorization and what “not found” means.

## Stage 4 — Core state-machine and interface traces

**A. Inventory reservation race.** Listing L7 has one unit. Buyers U1 in region A and U2 in B concurrently request reservations R1/R2. Trace both into the authoritative listing row/version boundary. One receives `reserved` with a stable receipt and expiration; the loser gets an explicit `out_of_stock` without another unit consumed. Require a transactional compare/update of stock and durable reservation+outbox intent. Do not infer success from a stale cache snapshot.

**B. Duplicate and reply loss.** R1 committed but its response was lost. U1 retries *same original ID and same payload*. The owner returns R1's receipt, not a second stock decrement. Changing listing or quantity under R1 is a conflict. A worker may redeliver the reservation event; feed/search/ranking consumers deduplicate by stable event/aggregate version before updating projections.

**C. Media publication.** Seller starts staged upload P1 with authenticated ownership and a media version. The object arrives, but the process dies before marking it visible. Design a recovery loop that validates object existence/rights and publishes one versioned listing-media reference, with private staging cleaned later. A stale CDN fill and revocation must not expose private bytes after the promised boundary.

**D. Messaging.** Buyer sends M1, then disconnects before the reply. The conversation owner commits one message ID and returns the old receipt on retry; offline recipient delivery may duplicate and must deduplicate. User removal from a conversation races with a send; the authority determines eligibility at a documented acceptance order, not the sender's cached participant list.

**E. Projections/reporting.** One listing creation emits an event via the same DB transaction as the authoritative state change and outbox. Trace relay duplication, indexing lag, a hot keyword partition, and a weekly ranking computed from bounded event-time windows and unique activity identities. If the week closes before a delayed event arrives, define whether rankings are revised and when a final revision is immutable. Account/usage reports need a versioned snapshot/replay offset, not a mix of independent read replica times.

## Stage 5 — Inject failures and revise

Run five required failure drills with client-level observation:

| Fault | Failure to prevent | Required design decision |
| --- | --- | --- |
| Duplicate event/retry | Double reservation, duplicated ranking counts | Stable original IDs, atomic receipt and consumer idempotence |
| Stale cache/search | Showing a sold listing as available, stale privacy | Advisory read model; checkout revalidates source; authorization on source/edge |
| Hot listing or hot partition | One shard/consumer bottleneck despite low mean QPS | Key/skew instrumentation, partition or read replication, overload |
| Region A/B partition | Split-brain inventory reservation | Fence one owner; fail closed for strict new writes when authority unavailable |
| Recovery after stale owner resumes | Old process applies expired release or stale listing overwrite | Resource-side epoch/version guard, coherent committed prefix, repair/replay |

Revise the baseline design based on at least two measured or synthetic bottlenecks. Show why a “both regions always accept reservations independently then reconcile later” design violates one-unit inventory. Explain what the application tells the buyer when a committed reservation's HTTP response is lost: **unknown until reconciled**, not definite failure.

## Stage 6 — Compare alternatives and defend

Your written/oral defense must compare **at least three complete architectures**, including a justified baseline and two valid variants:

- **Baseline:** single authoritative reservation/listing region with geo read projections/edges, fail-closed partition admission. Favor if write volumes are modest and strict inventory correctness dominates cross-region write availability.
- **Variant A:** per-listing home region with fenced migration. Each listing's stock and reservation ledger has one owner at a time; geo routing reduces owner distance for local listings, but cross-region buyer latency and handoff correctness need measured evidence.
- **Variant B:** genuinely coordinated cross-region transactional store with the required serializable/linearizable inventory contract under documented configuration. May improve global locality/failover behavior under certain assumptions but increases quorum/coordination and operational cost. **Do not claim zero latency, unlimited availability under partition or a vendor feature without specific version evidence.**

Reject two plausible shortcuts: (i) eventually merge independent stock decrements from regions—unsafe for 1 available unit; (ii) use a search/cache “available” flag as the checkout authority—unsafe even without partitions. For each viable variant write a cost/failure/consistency matrix and the conditions under which you would choose it.

## Deliverable and scoring instructions

Submit: requirements and assumptions, quantitative estimates, one original architecture diagram, API/data contracts, reservation and authorization state machines, five failure traces with repair paths, two rejected shortcuts, three full variant comparisons, source ledger, ops/runbook, and an explicit written design defense. Use synthetic numbers only as supplied or clearly labeled assumptions, and do not invent measured SLOs. Provide evidence that could falsify each major claim.

The assessment rubric is weighted: **requirements/estimates 15%; end-to-end mechanisms/traces 25%; invariants/recovery 25%; alternatives/cost 15%; security/operations 10%; clarity/evidence 10%.** A critical double-book or permission leak is a safety blocker even if the aggregate numerical score is high. See the [reference design and rubric](reference-solutions-rubric.md).
