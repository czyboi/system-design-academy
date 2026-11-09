---
id: DB-03
title: Transactions and Concurrency Control
status: draft
level: intermediate
estimated_time: 120 minutes
prerequisites: [DB-01]
source_review_date: 2026-11-09
reviewer: pending
---

# DB-03 — Transactions and Concurrency Control

## Learning outcomes

- Explain atomicity, consistency, isolation and durability in an application transaction.
- Recognize common concurrency anomalies.
- Compare common isolation levels without assuming all engines implement them identically.
- Explain MVCC and locking at a high level.
- Design retry behavior for deadlocks and serialization failures.

## 1. The double-spend / oversell problem

A store has one item left. Two requests arrive at almost the same time. Each reads `available_quantity = 1`; each decides the item can be purchased; both decrement it. The final inventory may be wrong unless the operation is protected by an appropriate atomic transaction/constraint/locking strategy.

A transaction groups operations that must succeed or fail as a unit. ACID is a useful framework, but the exact isolation and durability guarantees depend on engine configuration and transaction semantics.

## 2. ACID in practical terms

- **Atomicity:** the transaction's effects are committed as a unit or rolled back.
- **Consistency:** a successful transaction preserves defined invariants (constraints and application rules); the database cannot invent business rules that were never specified.
- **Isolation:** concurrent transactions are controlled so that their interleavings obey the selected isolation semantics.
- **Durability:** once commit is acknowledged under the configured durability policy, committed changes survive the failures covered by that policy.

## 3. Isolation anomalies

- **Dirty read:** a transaction reads another transaction's uncommitted change.
- **Non-repeatable read:** the same row is read twice and returns different committed values within a transaction.
- **Phantom:** repeating a predicate query returns a different set of rows because another transaction inserted/deleted matching rows.
- **Lost update:** concurrent read-modify-write operations overwrite each other's changes.
- **Write skew:** transactions read overlapping predicates and write different rows, jointly violating an invariant.

Isolation-level names alone are not enough to reason about behavior. Check the target engine's documentation. PostgreSQL, for example, treats `READ UNCOMMITTED` as `READ COMMITTED`; its `SERIALIZABLE` mode can abort a transaction with a serialization failure, which the application must be prepared to retry.

## 4. MVCC and locks

Multi-Version Concurrency Control (MVCC) lets readers observe a consistent version/snapshot while writers create new versions, reducing some reader/writer blocking. It does not mean “no locks”: databases still use locks for writes, schema changes and coordination. Long-running transactions can retain old row versions and contribute to storage/vacuum pressure in systems such as PostgreSQL.

Explicit row locks can serialize critical updates, but they create waiting and deadlock possibilities. Keep transactions short, acquire locks in a consistent order where possible, and make retry behavior safe and bounded.

## 5. Safer inventory reservation patterns

One possible SQL pattern is an atomic conditional update:

```sql
UPDATE inventory
SET available_quantity = available_quantity - 1
WHERE product_id = :product_id
  AND available_quantity > 0;
```

The application must inspect the affected-row count. A result of one row means a unit was reserved; zero means no unit was available (or the row was absent). This avoids a separate check-then-update race for this specific invariant. For a multi-row workflow, define transaction boundaries and failure handling explicitly.

## 6. Deadlocks and retries

A deadlock occurs when transactions wait on each other in a cycle. The database detects a victim and aborts one transaction. Applications should handle expected concurrency errors with bounded retries and jitter where appropriate, but only when the entire operation is safe to retry. External side effects (e.g. sending an email or charging a payment provider) should not be blindly repeated inside a retry loop; use idempotency keys and an outbox/workflow design where needed.

## Exercise

Design the transaction for reserving 3 units of a product across an order. Specify:
- the invariant;
- SQL or pseudocode;
- isolation/locking choice;
- what happens if only 2 units remain;
- how a retry avoids duplicate reservations;
- how an external payment is coordinated without pretending the database transaction can atomically commit with an unrelated provider.

## Knowledge check

1. Does ACID consistency mean that the database automatically enforces every business invariant?
2. Why is MVCC not equivalent to “there are no locks”?
3. Why can serializable transactions be aborted?
4. What makes a retry unsafe?
5. How can a conditional update avoid a check-then-update race?

## Answer guide

1. No. ACID consistency means a successful transaction preserves constraints/invariants that have been defined; business rules must be expressed in constraints, transaction logic or application workflows.
2. MVCC reduces some reader/writer blocking by exposing versions, but writes, schema changes and explicit coordination still use locks.
3. A concurrent interleaving may be non-serializable; the engine aborts a transaction rather than allow an outcome inconsistent with serial execution.
4. A retry is unsafe when it repeats a non-idempotent external side effect or can duplicate a business operation. Use idempotency and explicit state transitions.
5. The conditional predicate and update are one database statement; checking affected-row count tells whether the reservation succeeded without a separate race-prone read.


## References

- PostgreSQL 18 — Concurrency Control: https://www.postgresql.org/docs/current/mvcc.html
- PostgreSQL 18 — SET TRANSACTION: https://www.postgresql.org/docs/current/sql-set-transaction.html
- MySQL 8.4 — InnoDB Transaction Model: https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-model.html
- MySQL 8.4 — InnoDB Locking: https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html
