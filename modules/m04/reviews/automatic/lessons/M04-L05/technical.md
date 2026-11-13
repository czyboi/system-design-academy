# M04-L05 technical and provenance review

Round 0 reviewed the lesson, companion and evidence at draft commit `a01124b` on 2026-11-13.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M04-L05-T1 | major | open | Companion lines 18, 62 and 68, EX-1 and Plan and semantics rubric. | Only the baseline's average of two emitted rows per loop is stated. The candidate probes a smaller and potentially different population, the 20 newest invoices. Its average can differ, so the expected 40 rows cannot be inferred from the supplied trace. Give the candidate its own hypothetical average or report the candidate output conditionally. Keep the exercise and rubric consistent. Explain that node outputs and loop counts quantify parts of the plan and need other observations to establish work or latency. | [PostgreSQL 18 Using EXPLAIN, actual values and loops](https://www.postgresql.org/docs/18/using-explain.html#USING-EXPLAIN-ANALYZE) |
| M04-L05-T2 | minor | open | Lesson lines 25–27, Walk two plans under one workload. | Make the equivalence conditions reproducible. State that the baseline also preserves zero-line orders. Show how the rewritten outer query retains zero counts, for example by using a left join and counting a non-null line ID. State that the final query specifies the same outer ordering, since the initial ordered limit alone does not order the enriched output. | [PostgreSQL 18 joined tables](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-JOIN), [aggregate functions](https://www.postgresql.org/docs/18/functions-aggregate.html), [sorting rows](https://www.postgresql.org/docs/18/queries-order.html) |

The PostgreSQL 18 distinction between cost units, actual time, average rows per loop and client-observed latency is supported. The suggested B-tree can satisfy the matching order and limit, subject to the chosen plan. The PostgreSQL type, constraint and pruning claims stay version-scoped, and the bulk load example is limited to a new isolated table. The assessment uses the 1,000 original requests for each variant and correctly obtains 97% and 98.5%, both below 99%. The candidate's extra WAL remains part of the decision. The evidence distinguishes an unnecessary read path from a genuine owner-level write or capacity limit. [PostgreSQL 18 using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html), [B-tree ordering](https://www.postgresql.org/docs/18/indexes-ordering.html), [table partitioning](https://www.postgresql.org/docs/18/ddl-partitioning.html), [populating a database](https://www.postgresql.org/docs/18/populate.html).

## Provenance

The MySQL 5.7.44 implementation documents the result-set cache and invalidation by table. MySQL 8.0 documents removal of the cache and its tuning settings. PostgreSQL references identify the major version used throughout. The stated plans and load figures are illustrative. The package contains original examples and imports no third-party code or assets. [MySQL 5.7.44 query cache source](https://github.com/mysql/mysql-server/blob/mysql-5.7.44/sql/sql_cache.cc), [MySQL 8.0 removals](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals).

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the lesson and companion at draft commit `6d5ed71` on 2026-11-13.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M04-L05-T1 | resolved | EX-1 specifies independent averages of two rows per loop across 3,000 baseline lookups and three across 20 candidate lookups. The sample and rubric correctly use 6,000 and 60 emitted rows. The teaching example independently uses 4,000 × 3 and 25 × 4. Both distinguish these outputs from total work or elapsed time. | [PostgreSQL 18 Using EXPLAIN, actual rows and loops](https://www.postgresql.org/docs/18/using-explain.html#USING-EXPLAIN-ANALYZE) |
| M04-L05-T2 | resolved | Both teaching plans preserve zero-line headers using a left join and a count of non-null child IDs. The revised explanation requires the same deterministic ordering in the limiting query and the final enriched output, and the companion checks the equivalent behavior for adjustments. | [PostgreSQL 18 joined tables](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-JOIN), [aggregate functions](https://www.postgresql.org/docs/18/functions-aggregate.html), [sorting rows](https://www.postgresql.org/docs/18/queries-order.html) |

The comparison still measures the same 1,000-request cohort per variant and counts all 15 candidate misses against the 99% target. The revision preserves the separate write-WAL measurement and introduces no external assets.

### Verdict

`ready-for-human-review`
