---
id: DB-06
title: SQL vs NoSQL: Choose by Workload
status: draft
level: intermediate
estimated_time: 90 minutes
prerequisites: [DB-01, DB-05]
source_review_date: 2026-11-09
reviewer: pending
---

# DB-06 — SQL vs NoSQL: Choose by Workload

## Learning outcomes

- Describe relational, document, key-value, wide-column and graph data models.
- Choose a model from access patterns, consistency needs and relationship complexity.
- Explain the cost of flexible schema and denormalized aggregates.
- Avoid simplistic “SQL does not scale / NoSQL is faster” claims.

## 1. Start with workload, not category

Ask what the application reads and writes, which invariants must always hold, what relationships are traversed, what query flexibility is required, and what operational expertise is available. The database category is not the requirement.

## 2. Relational systems

Relational databases provide tables, constraints, joins and transaction facilities. They are strong candidates for domains with important relationships and invariants such as orders, inventory, payment records and financial ledgers. They can scale in multiple ways; the actual limit depends on data size, workload, architecture, engine and operations.

## 3. Common NoSQL models

- **Key-value:** access primarily by key; useful for simple lookup/session/state patterns.
- **Document:** store aggregate-shaped documents; useful when data is commonly read/written together and relationships can be modeled within or across documents.
- **Wide-column:** organize rows by partition key and clustering/sort columns; useful for known high-volume query patterns.
- **Graph:** represent entities and relationships as vertices/edges; useful for relationship traversals where graph operations are central.

These are broad categories, not interchangeable products. Each product has its own query, consistency, transaction, indexing and operational semantics.

## 4. Access-pattern-first modeling

For document/key-value/wide-column stores, list the queries before defining the schema. A relational design often starts by representing entities and relationships, then indexes common query paths. A DynamoDB-style design often starts with access patterns and key design. MongoDB recommends storing data accessed together together, while also supporting references and schema validation where suitable.

## 5. Decision matrix

| Requirement | Relational often fits when… | NoSQL model may fit when… |
|---|---|---|
| Multi-row invariants | Constraints and transactions are central | Product supports needed transaction semantics and model fits |
| Flexible document shape | Schema changes are manageable | Documents naturally represent the aggregate |
| Relationship traversal | Joins/foreign keys are central | Graph traversal is the primary workload |
| Key-based high-throughput access | Indexed relational access is sufficient | Key-value/wide-column access pattern is predictable |
| Ad hoc queries | Broad SQL query flexibility matters | Access patterns are known and bounded |

No row in this table is an automatic rule. Validate concrete engine capabilities and workload requirements.

## Exercise

Choose data models for: (1) a payment ledger, (2) user sessions with TTL, (3) product catalogue with varying attributes, and (4) social graph mutual-friend traversal. State two alternatives and explain why you did not choose them.

## Knowledge check

1. Why is “NoSQL has no schema” inaccurate?
2. Why should an access-pattern list be created before designing a DynamoDB-style table?
3. Why might a relational DB still be the best choice for a high-volume service?
4. When is a graph model a better conceptual fit than a set of relational joins?
5. Name three product-specific capabilities that must be checked before choosing a NoSQL database.

## Answer guide

1. NoSQL products still have data models, key constraints and often schema validation or application-level schema expectations. “Flexible schema” is not “no schema”.
2. Key design determines how data is located and distributed; without known access patterns, a table may not efficiently support the required queries.
3. Relational databases can handle high throughput when the schema, indexes, hardware, partitioning/replication strategy and operational design fit the workload.
4. When traversals over many relationships and path patterns are central enough that graph operations are the natural query model.
5. Transaction scope, consistency/read guarantees, query support, indexing, partition/shard behavior, limits, backup/restore, availability and operational tooling.


## References

- System Design Primer — NoSQL and SQL or NoSQL: https://github.com/donnemartin/system-design-primer#database
- MongoDB — Data Modeling: https://www.mongodb.com/docs/manual/data-modeling/
- Amazon DynamoDB — Best Practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- MySQL 8.4 Reference Manual: https://dev.mysql.com/doc/refman/8.4/en/
