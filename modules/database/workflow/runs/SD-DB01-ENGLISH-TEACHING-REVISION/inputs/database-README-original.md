# System Design Academy — Database Module Pilot

**Status:** Draft V1 / human review required  
**Language:** Vietnamese, with standard English technical terms  
**Track:** System Design for backend engineers  
**Primary source:** Donne Martin, *The System Design Primer* (CC BY 4.0), supplemented by official vendor documentation.

## Purpose

This is a pilot module used to validate a repeatable AI-assisted content workflow. It is not a database administration course and it is not a translation of the Primer. It teaches the database decisions that backend engineers need to make when designing scalable and reliable systems.

## Module outcomes

After this module, a learner should be able to:

1. Translate application access patterns and consistency needs into a data model.
2. Explain how indexes and query planners affect read/write performance.
3. Choose transaction boundaries and isolation levels based on correctness requirements.
4. Explain primary/replica architectures, replication lag, failover and read-after-write implications.
5. Distinguish table partitioning from distributed sharding and identify when either is justified.
6. Choose between relational and non-relational data models based on workload and access patterns rather than fashion.
7. Include backups, recovery objectives and operational failure modes in a database design.
8. Defend a database design using explicit trade-offs.

## Lessons

| ID | Lesson | Main output |
|---|---|---|
| DB-01 | Data modeling and relational foundations | Logical model, constraints, keys, normalization/denormalization |
| DB-02 | Indexes and query execution | Index selection and EXPLAIN-based reasoning |
| DB-03 | Transactions and concurrency | ACID, isolation anomalies, locks, MVCC, deadlocks |
| DB-04 | Replication and consistency | Primary/replica topology, lag, consistency and failover |
| DB-05 | Partitioning and sharding | Partition key and shard strategy, hot partition analysis |
| DB-06 | SQL vs NoSQL and workload-oriented modeling | Decision matrix and access-pattern model |
| DB-07 | Availability, backup and recovery | RPO/RTO, restore strategy, HA vs DR |
| DB-08 | Case study: order management data layer | End-to-end design and review |

## Scope boundaries

Included: relational modeling, indexes, query plans, transactions, concurrency, replication, partitioning, sharding, SQL/NoSQL trade-offs, availability, backup/recovery, practical system-design decisions.

Not included in this module: deep vendor-specific administration, database installation tutorials, exhaustive SQL syntax, ORM tutorials, data warehousing/OLAP, stream processing, cache design (separate module), and hands-on production benchmarking at scale.

## How to use this pilot

1. Read `governance/content-guidelines.md` and `workflow/agent-runbook.md`.
2. Inspect `sources/source-registry.csv` and verify URLs before publication.
3. Use `lessons/DB-01-data-modeling.md` as the first complete lesson sample.
4. Review the remaining lesson briefs and expand them using the same template.
5. Run every lesson through `governance/qa-checklist.md`.
6. Do not mark content `PUBLISHED` until a qualified human reviewer approves it.

## Attribution

Certain topic selection and high-level subject organization are informed by *The System Design Primer* by Donne Martin, available under CC BY 4.0. This pilot is an independent educational adaptation; examples, wording, exercises and explanations are newly authored unless explicitly attributed otherwise. See `governance/attribution-policy.md`.

## Status disclaimer

This repository is a working pilot, not a claim that all technical statements have passed independent expert review. `status: draft` is intentional. The source list is a research starting point; individual claims must be tied to the most relevant source in the final lesson.
