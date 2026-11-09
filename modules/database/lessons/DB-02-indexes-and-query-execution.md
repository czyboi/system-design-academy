---
id: DB-02
title: Indexes and Query Execution
status: draft
level: intermediate
estimated_time: 90 minutes
prerequisites: [DB-01, basic SQL]
source_review_date: 2026-11-09
reviewer: pending
---

# DB-02 — Indexes and Query Execution

## Learning outcomes

- Explain the purpose and costs of an index.
- Select candidate single-column and composite indexes from real query patterns.
- Read the major parts of an `EXPLAIN` plan.
- Explain why an optimizer may choose a sequential scan instead of an index.
- Avoid common over-indexing and low-selectivity mistakes.

## 1. Why indexes exist

Without a useful access path, a database may need to inspect many or all rows to find those matching a predicate. An index is an auxiliary data structure that helps the engine locate candidate rows more efficiently. It is not a magic cache and it does not guarantee that every query becomes faster.

The cost is that the database must maintain the index when rows are inserted, updated or deleted. Indexes consume disk space and memory; too many indexes can slow writes and increase maintenance work.

## 2. B-tree intuition

A B-tree family index maintains keys in an ordered structure, making equality and range searches efficient for supported operator classes. It can also support ordered retrieval in suitable cases. Other index families solve different problems: for example, PostgreSQL offers GiST, GIN and BRIN for different data/operator patterns. Do not assume all database engines expose identical index types or behavior.

## 3. Choose indexes from query patterns

Suppose the application runs:

```sql
SELECT order_id, status, created_at
FROM orders
WHERE customer_id = :customer_id
ORDER BY created_at DESC
LIMIT 20;
```

A candidate index is `(customer_id, created_at)`. For a multicolumn B-tree in PostgreSQL, constraints on leading/leftmost columns are especially important for efficient index access. Reversing the column order may lead to a different access profile.

Index design should be based on:

- Predicates (`WHERE`).
- Join keys.
- Sort order (`ORDER BY`).
- Grouping/aggregation patterns.
- Selectivity and data distribution.
- The columns returned by the query.
- Write volume and update frequency.

Do not create an index for every column that appears in a query. A query may still prefer a sequential scan when a large fraction of the table qualifies, when the table is small, or when random heap access costs more than scanning sequentially.

## 4. Understand the query plan

Use the engine's plan inspection tools. In PostgreSQL:

```sql
EXPLAIN
SELECT order_id, status, created_at
FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC
LIMIT 20;
```

Important concepts in a plan include scan type, estimated rows, cost, join strategy, sort, and whether index conditions or filters are applied. `EXPLAIN ANALYZE` executes the statement and reports actual timing/row counts; use care with data-modifying statements and understand measurement overhead. Its result is not a universal production benchmark.

A good plan is workload-dependent. The same SQL can get a different plan as table size, statistics, parameter values and data distribution change.

## 5. Composite and covering indexes

A composite index stores more than one key column. The leading-column rule matters for B-tree indexes in PostgreSQL. A covering/index-only strategy may reduce heap access when the index contains all columns required by a query, but PostgreSQL's index-only scan also depends on visibility information; do not assume it always avoids heap access.

## 6. Practical exercise

Given these queries:

A. `WHERE customer_id = ? ORDER BY created_at DESC LIMIT 20`  
B. `WHERE status = ?` where 70% of rows have the same status  
C. `WHERE provider_ref = ?` and `provider_ref` is unique  
D. `WHERE created_at >= ? AND created_at < ?`

Propose indexes, explain which may not be useful, and name what measurement or plan evidence you would inspect before keeping each index.

## Knowledge check

1. Name two costs of adding an index.
2. Why can a sequential scan be the correct plan?
3. For a B-tree `(customer_id, created_at)`, why is the first column important?
4. What does `EXPLAIN` estimate, and what extra information does `EXPLAIN ANALYZE` collect?
5. Why should a performance result from a tiny test table not be extrapolated directly to production?

## Answer guide

- **A:** `(customer_id, created_at)` is a reasonable candidate because equality filtering on the leading column is followed by ordering on the second. Validate sort direction and returned columns on the target engine.
- **B:** A low-selectivity status index may not help when most rows match. A partial/filtered index can be useful for a small, frequently queried subset on engines that support it, but this must be tested against the workload.
- **C:** A unique index/constraint on `provider_ref` is appropriate if it is a business invariant and used for lookup. A unique constraint is preferable to an informal application-only check.
- **D:** A B-tree on `created_at` may support a bounded range scan; partition pruning may also matter for very large time-partitioned tables. Do not introduce partitioning only because a date filter exists.
- Measure representative read latency, write overhead, index size and plan stability. Compare estimated rows with actual rows, refresh statistics when appropriate, and test with representative cardinality and skew.


## References

- Primer — Database / SQL tuning: https://github.com/donnemartin/system-design-primer#database
- PostgreSQL 18 — Using EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- PostgreSQL 18 — Multicolumn Indexes: https://www.postgresql.org/docs/current/indexes-multicolumn.html
- PostgreSQL 18 — Index-only scans: https://www.postgresql.org/docs/18/indexes-index-only-scans.html
- MySQL 8.4 — Optimization and Indexes: https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html

## Status and review

Draft. Verify all example plans on the exact DBMS/version used in any accompanying lab before publication.
