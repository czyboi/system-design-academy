# M04-L01 technical and provenance review

Round 0 reviewed the lesson, companion and evidence at draft commit `018f0bf` on 2026-11-13.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M04-L01-T1 | major | open | Lesson line 47, Put large attachments on their own path. Companion lines 20 and 64–71, EX-1 and Attachment lifecycle. | The sample names a pending-to-ready guard and assumes retirement prevents a worker from publishing. A status-only guard still matches after a cleaner retires and deletes an old attempt while the invoice remains pending for a retry. A delayed worker can publish the deleted key. Give each attempt a durable current token. Require both pending status and the matching token in the publish update. Invalidate that token before cleanup using a database transition that competes with publish, and retain the winning key if publish commits first. Show both outcomes in the lesson and require the same safety property in the sample and rubric. Also identify the slip as pending while its reservation is already confirmed. | [PostgreSQL 18 Read Committed, predicate recheck after concurrent updates](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED), [Amazon S3 data consistency model, key-level operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel) |
| M04-L01-T2 | minor | open | Lesson lines 21 and 43, constraints and recent-orders access path. Evidence rows REL-1 and REL-4. | The first reference is labeled as covering joins but targets the foreign-key subsection. REL-1 combines primary-key and foreign-key claims at the latter anchor. Split the references and add the exact ordering subsection for the ordered limited scan. The mechanism itself matches the documented behavior. | [PostgreSQL 18 primary keys](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS), [foreign keys](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-FK), [joins](https://www.postgresql.org/docs/18/tutorial-join.html), [indexes and ORDER BY](https://www.postgresql.org/docs/18/indexes-ordering.html) |

The non-null foreign key and restrictive delete maintain the parent reference under either commit order. The stock guard targets one identified row, checks quantity in the update and rolls back stock and order writes together after a failed line write. The success acknowledgement follows commit. The stated Read Committed semantics and the distinction between local commit and durability under an explicit failure model match PostgreSQL 18. [PostgreSQL 18 foreign keys](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-FK), [transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html), [Read Committed](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED), [WAL configuration](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT).

## Provenance

The evidence ledger identifies PostgreSQL 18 and Amazon S3 as factual references and identifies the Primer's pinned database section as a topic map. The lesson and companion use original scenario prose and traces. The package includes no imported diagrams, images or executable code. No material attribution or asset issue was identified. [Pinned System Design Primer, database and relational integrity](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L808-L827).

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the lesson, companion and evidence at draft commit `da9134c` on 2026-11-13.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M04-L01-T1 | resolved | The lesson's attachment section binds publish and retirement to the same pending invoice row and never-reused attempt token. If publish commits first, the ready state blocks retirement and the key survives. If retirement commits first, token invalidation blocks publication before deletion, including when a retry has already started. An upload that finishes after deletion leaves an unreferenced key that remains tracked for cleanup. The companion solution and rubric now require both outcomes and keep the reservation confirmed while the slip is pending. | [PostgreSQL 18 Read Committed](https://www.postgresql.org/docs/18/transaction-iso.html#XACT-READ-COMMITTED), [Amazon S3 data consistency model](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html#ConsistencyModel) |
| M04-L01-T2 | resolved | The lesson cites the primary-key, foreign-key and join sections separately. The recent-orders access path and REL-4 now cite index ordering in addition to leading-column access. | [PostgreSQL 18 primary keys](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS), [foreign keys](https://www.postgresql.org/docs/18/ddl-constraints.html#DDL-CONSTRAINTS-FK), [joins](https://www.postgresql.org/docs/18/tutorial-join.html), [multicolumn indexes](https://www.postgresql.org/docs/18/indexes-multicolumn.html), [indexes and ORDER BY](https://www.postgresql.org/docs/18/indexes-ordering.html) |

The companion's revised checkout trace still requires the waiting transaction to recheck the quantity after the first commit or make its own guarded claim after rollback. The new attachment design claims depend on documented row-update behavior and the scenario's explicit lifecycle rules. The revision introduced no third-party assets.

### Verdict

`ready-for-human-review`
