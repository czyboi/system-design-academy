# Database Module — Assessment Blueprint

## Formative quiz blueprint

| Lesson | Question count | Target skills |
|---|---:|---|
| DB-01 | 6 | Model relationships, invariants, normalization |
| DB-02 | 6 | Index selection, plan interpretation, cost reasoning |
| DB-03 | 6 | Isolation, MVCC, lock/retry design |
| DB-04 | 5 | Replication modes, lag, read routing, failover |
| DB-05 | 5 | Partitioning/sharding distinction, key skew |
| DB-06 | 5 | Workload-based storage model selection |
| DB-07 | 5 | HA/backup/DR, RPO/RTO, restore testing |

The question banks embedded in each lesson are the initial draft. Before publication, add randomized variants and validate every answer against the taught material.

## Capstone assessment

Use `case-studies/DB-08-order-management.md`. Require the learner to submit an architecture decision record and a short presentation. Grade with the rubric in the case study.

## Mastery thresholds (proposed)

- Lesson quiz: 80% to pass; allow review and retry.
- Capstone: 70/100 to pass.
- Critical correctness failures (e.g. no idempotency for duplicate payment callbacks, treating a replica as backup, or using a shard key with an obvious severe hotspot without mitigation) require revision even if the numeric score passes.
