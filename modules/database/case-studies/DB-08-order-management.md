# DB-08 — Case Study: Design the Database Layer for an Order Management System

**Status:** Draft  
**Estimated effort:** 150 minutes  
**Format:** System design exercise; no single universally correct answer.

## Problem

Design the database layer for an e-commerce order service.

Initial assumptions:
- 2 million registered customers.
- 100,000 orders/day average, with 5× peak traffic during campaigns.
- Each order contains 1–20 items.
- Payment provider callbacks may be duplicated or delayed.
- Customers expect to see their own newly placed order immediately.
- Catalogue pages can tolerate a small amount of staleness.
- Orders must be retained for 7 years; raw browsing events are not in scope.

These numbers are exercise assumptions, not claims about a real service.

## Step 1 — Clarify requirements

Functional: create order, reserve stock, record payment state, query order detail, list customer history, support customer service lookup.

Non-functional: correctness of order/payment state, read latency, peak write load, availability, data retention, recovery objectives, auditability.

Questions for the candidate: What is the source of truth for inventory? Is payment authorization synchronous? Can an order be cancelled after capture? Which queries dominate? What are the required RPO/RTO?

## Step 2 — Starting data model

Use relational tables for the transactional core: customers, orders, order_items, payments, inventory_reservations and an outbox table for publishing domain events. Define primary/foreign keys and uniqueness constraints, including a provider idempotency/reference key.

Store `unit_price` and currency on the order item as the agreed checkout value. Do not derive historical order totals from today's catalogue price.

## Step 3 — Transactions and external payment

Do not assume a database transaction can atomically commit with an external payment provider. Model the workflow as explicit states and idempotent operations. Persist an order/payment intent and an outbox event in the same local transaction, then process provider interaction asynchronously or via a controlled synchronous step with compensating behavior. Define how duplicate callbacks are deduplicated.

## Step 4 — Indexes from access patterns

Candidate indexes (validate with query plans and representative data):
- `orders(customer_id, created_at)` for customer history;
- unique `payments(provider_ref)` for provider callback lookup/deduplication;
- `order_items(order_id, line_no)` as the primary key for order detail;
- an index on the foreign-key/reference columns used by service lookups and delete/update checks where needed.

Avoid creating speculative indexes without measuring their read benefit and write/storage cost.

## Step 5 — Read scaling and consistency

Keep read-your-writes order detail on the primary or use an explicit consistency-aware route. Catalogue reads may go to replicas/cache if bounded staleness is acceptable. Monitor replication lag; define fallback to primary when lag exceeds the allowed threshold.

## Step 6 — Partitioning and sharding decision

Start with one well-sized relational deployment and measure. If retention or table maintenance becomes a bottleneck, time-based partitioning may simplify archival/deletion and prune time-range queries. If one database cannot handle the throughput/storage target after query/index/tuning alternatives, evaluate sharding. A customer-based shard key may localize customer history but risks skew from very large customers and complicates cross-customer operations.

## Step 7 — Availability and recovery

Define RPO/RTO with the business. Use a tested backup/PITR strategy independent from read replicas. Run restore drills and measure actual recovery time. Document failover authority and how stale writers are fenced.

## One defensible reference design (not the only valid answer)

- Use a relational database for the transactional order/payment state because referential integrity, uniqueness and multi-row transaction semantics are central.
- Model `orders`, `order_items`, `payments`, `inventory_reservations` and an `outbox` table. Store purchased price/currency in each order item.
- Enforce provider callback deduplication with a unique provider event/reference key. A duplicate callback returns the previously recorded result rather than creating a second payment transition.
- Keep order state transitions explicit and constrained. Use idempotent commands and a transactional outbox to publish events after the local database transaction commits.
- Use query-driven indexes, beginning with customer history and provider callback lookup. Validate all candidates with the target DBMS plan tool on representative data.
- Keep read-your-writes paths on the primary or implement a documented consistency-aware routing strategy. Allow catalogue reads from replicas if bounded staleness is accepted.
- Begin without cross-node sharding. Consider time partitioning when retention/maintenance/query patterns justify it. Consider sharding only after metrics show a single deployment is the bottleneck and simpler options are insufficient.
- Maintain independent backups and point-in-time recovery, with restore drills that verify the stated RPO/RTO. Use replication for availability/read scaling, not as the sole recovery mechanism.

A candidate may choose a different engine or topology and still score well if the assumptions, correctness guarantees and trade-offs are explicit.


## Candidate deliverables

1. Requirements and assumptions.
2. ER/data model and constraints.
3. Main queries and indexes.
4. Transaction and idempotency design.
5. Read/write topology and consistency contract.
6. Partition/shard decision and trigger thresholds.
7. Backup/restore and failover plan.
8. Top five risks and mitigations.

## Evaluation rubric (100 points)

| Dimension | Points |
|---|---:|
| Requirements and access patterns | 10 |
| Data model and invariants | 15 |
| Query/index reasoning | 10 |
| Transactions, idempotency and concurrency | 20 |
| Replication and consistency | 15 |
| Partitioning/sharding judgment | 10 |
| HA, backup, RPO/RTO and restore | 15 |
| Clarity and trade-off communication | 5 |

## References

Use the official references cited in DB-01 through DB-07. Any solution that makes product-specific claims must specify the engine/version and cite the corresponding vendor documentation.
