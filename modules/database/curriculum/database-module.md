# Database Module — Master Curriculum

**Module ID:** DB  
**Level:** Intermediate backend engineer → system design  
**Estimated learner effort:** 12–16 hours (reading + exercises; excludes deep vendor labs)  
**Status:** Draft V1

## Module outcomes

Learners can model data from access patterns and invariants; reason about index/query plans; choose transaction semantics; explain replication and consistency; distinguish partitioning from sharding; evaluate SQL/NoSQL choices; and include availability, backup and recovery in a system design.

## Lesson sequence

| ID | Lesson | Approx. time | Prerequisites | Assessment |
|---|---|---:|---|---|
| DB-01 | Data modeling and relational foundations | 90 min | SQL basics | Model an order domain with constraints |
| DB-02 | Indexes and query execution | 90 min | DB-01 | Diagnose query plan and propose indexes |
| DB-03 | Transactions and concurrency | 120 min | DB-01 | Explain isolation anomaly and choose isolation/locking |
| DB-04 | Replication and consistency | 90 min | DB-03 | Design read scaling with explicit staleness policy |
| DB-05 | Partitioning and sharding | 90 min | DB-02, DB-04 | Select a partition key; identify hot-key risk |
| DB-06 | SQL vs NoSQL and workload-oriented modeling | 90 min | DB-01, DB-05 | Select storage model for three workloads |
| DB-07 | Availability, backup and recovery | 90 min | DB-04 | Define RPO/RTO and recovery plan |
| DB-08 | Case study: order management data layer | 150 min | DB-01–DB-07 | Present and defend end-to-end design |

## Curriculum rationale

The Primer's Database section introduces RDBMS, replication, federation, sharding, denormalization, SQL tuning, NoSQL data models and SQL-vs-NoSQL. This curriculum preserves those core themes but adds prerequisites needed for robust engineering decisions: constraints/data modeling, query planning, transaction isolation, replication consistency and backup/recovery. These additions are grounded in current vendor documentation and are not claimed to be copied from the Primer.

## Topics and assessment alignment

### DB-01 Data modeling and relational foundations
- Entities, relationships, cardinality, keys, constraints, normalization and controlled denormalization.
- Deliverable: logical model and DDL for orders, customers, order_items and payments.

### DB-02 Indexes and query execution
- B-tree as a common default, composite index ordering, covering/index-only access, selectivity, write amplification, optimizer/statistics, EXPLAIN.
- Deliverable: explain a query plan and justify index choices based on a workload.

### DB-03 Transactions and concurrency
- ACID, transaction boundaries, isolation levels, dirty/nonrepeatable/phantom reads, lost update, MVCC, row locks, deadlocks, retrying serialization failures.
- Deliverable: safe inventory reservation / payment state transition design.

### DB-04 Replication and consistency
- Primary/replica, asynchronous/semi-synchronous/synchronous trade-offs, replication lag, read-after-write, failover, split-brain risk, read routing.
- Deliverable: read-scaling topology with an explicit consistency contract.

### DB-05 Partitioning and sharding
- Table partitioning, partition pruning, horizontal sharding, range/hash/directory strategies, hot partitions, resharding, cross-shard queries and transactions.
- Deliverable: partition/shard decision record for a high-volume event/order table.

### DB-06 SQL vs NoSQL
- Relational constraints and joins; document, key-value, wide-column and graph models; access-pattern-first design; schema flexibility; consistency/transaction support; operational trade-offs.
- Deliverable: decision matrix for three example workloads.

### DB-07 Availability, backup and recovery
- HA vs disaster recovery, backup types, point-in-time recovery, RPO/RTO, restore testing, replica failure and failover runbooks.
- Deliverable: recovery design for a business-critical transactional database.

### DB-08 Case study
- Requirements, access patterns, data model, transactions, indexes, read scaling, partitioning threshold, backup/DR and operational observability.
- Deliverable: architecture decision record and design presentation.

## Out of scope

Detailed administration certification, SQL syntax catalogues, ORM usage, caching strategies (separate module), data warehouse design and vendor-specific cluster operations.
