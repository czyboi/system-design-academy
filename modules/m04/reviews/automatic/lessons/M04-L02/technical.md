# M04-L02 technical and provenance review

Round 0 reviewed the lesson, companion and evidence at draft commit `3668bc3` on 2026-11-13.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M04-L02-T1 | major | open | Lesson lines 33–35, Promote one writer and account for lost history. Companion lines 66–74, sample and Write and failover rubric. | The sample asks for a candidate that can recover the acknowledged history and a retry at the authoritative writer. It gives no observable evidence that the candidate has that history and no remote durability check before returning a deduplicated success. During a link break, a timed-out PostgreSQL transaction can already be committed locally. A retry that finds the ID locally and returns success can therefore confirm a claim absent from the surviving region. Teach and grade a concrete two-region rule. Require the particular remote standby to flush every claim's commit and atomic operation record before any success, including retry or status responses. Keep the policy in force and recover that standby's durable WAL after verified fencing. Distinguish definite pre-admission rejection from an admitted request with unknown outcome. If only one region remains, allow eligible reads after replay and keep new claim confirmations unavailable until the required durability can be restored. | [PostgreSQL 18 synchronous replication, planning for high availability](https://www.postgresql.org/docs/18/warm-standby.html#SYNCHRONOUS-REPLICATION), [PostgreSQL 18 synchronous-commit modes](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT), [PostgreSQL 18 replication wait implementation, SyncRepWaitForLSN](https://raw.githubusercontent.com/postgres/postgres/REL_18_STABLE/src/backend/replication/syncrep.c#L274-L310), [PostgreSQL 18 failover](https://www.postgresql.org/docs/18/warm-standby-failover.html) |
| M04-L02-T2 | minor | open | Lesson lines 21–29, Follow the log to a reader. Evidence rows REPL-1–2. | The linked commit-mode source supports WAL acknowledgement but does not document timeline ancestry. Cite the hot standby and timeline sections for new-snapshot visibility and divergent histories. The session token and router should remain explicitly application design. | [PostgreSQL 18 hot standby](https://www.postgresql.org/docs/18/hot-standby.html), [PostgreSQL 18 timelines](https://www.postgresql.org/docs/18/continuous-archiving.html#BACKUP-TIMELINES) |

The asynchronous example separates durable receipt, replay and acknowledgement. The lost tail is a known premise of the drill, and the lesson correctly limits what can be inferred from lag during a live incident. The original-request read score is 93%, with stale, late and unavailable results counted as misses. The concurrent vectors and componentwise merge context agree with the original Dynamo causal example. The field-level policy is scoped to independent edits with retained intent. [PostgreSQL 18 log-shipping standby servers](https://www.postgresql.org/docs/18/warm-standby.html), [Dynamo §4.4](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf#page=6).

## Provenance

PostgreSQL 18 documentation supports the replication and failover claims. The original Dynamo paper supports causal branch detection. The profile example and traces use original illustrative data. The pinned Primer is identified as the topic map. The package includes no imported figures, diagrams or code. [Pinned System Design Primer, replication](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L829-L876).

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the lesson, companion and evidence at draft commit `0ce6602` on 2026-11-13.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M04-L02-T1 | resolved | The lesson's promotion section and the companion's sample and rubric tie every claim confirmation to durable flush at the fixed other-region standby. The operation ID and claim share one transaction. A retry or status lookup that finds the record locally must still prove a WAL position at or beyond that commit is durable on the designated standby and history. The pre-admission and unknown outcomes are distinguished. Failover verifies fencing and recovers the designated standby's WAL, so the acknowledgement policy identifies the recoverable history without an externally guessed final acknowledgement. A recovered record can establish presence while new confirmations wait for restored other-region protection. | [PostgreSQL 18 synchronous commit](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT), [replication wait implementation](https://raw.githubusercontent.com/postgres/postgres/REL_18_STABLE/src/backend/replication/syncrep.c#L274-L310), [WAL positions](https://www.postgresql.org/docs/18/functions-admin.html), [WAL receiver flush and timeline statistics](https://www.postgresql.org/docs/18/monitoring-stats.html#MONITORING-PG-STAT-WAL-RECEIVER-VIEW), [failover](https://www.postgresql.org/docs/18/warm-standby-failover.html) |
| M04-L02-T2 | resolved | The lesson and evidence cite hot standby for visibility to fresh snapshots and timeline history for branch ancestry. The watermark token and routing policy are described as application design. | [PostgreSQL 18 hot standby](https://www.postgresql.org/docs/18/hot-standby.html), [recovery timelines](https://www.postgresql.org/docs/18/continuous-archiving.html#BACKUP-TIMELINES) |

The strict-read denominator and the concurrent profile-edit trace remain consistent with the original scenario. The revised mechanism preserves the distinction between durable WAL and replay, and the revision uses the PostgreSQL source as a reference without importing source code.

### Verdict

`ready-for-human-review`
