---
id: M08-EX1
status: draft
outcomes: [M08-S1]
---

# Publish category rankings and query a sharded index

A shop publishes hourly category totals by units sold and lets shoppers search its catalogue. The sales snapshot and the catalogue index have separate source streams. The ranking can be revised for late sales. Search has separate contracts for browsing and for an export that demands a complete answer.

## Inputs

The closed batch input for the provisional `[10:00, 11:00)` UTC window contains these rows. Each ID identifies one sale. The trusted durable intake commits a duplicate delivery of `s4` at 11:01:30 and then a distinct sale `s7` of 3 Mugs (event time 10:58) at 11:02. The duplicate uses `s4`'s original ID and payload and contributes no new units. Another distinct sale, `s8` for 2 Filters (event time 10:57), is first durably admitted to the archive at 11:07, after the live close barrier.

| Split | Sales in the provisional input |
| --- | --- |
| A | `s1 Tea 6`, `s2 Mugs 3`, `s3 Tea 1` |
| B | `s4 Mugs 5`, `s5 Filters 4`, `s6 Tea 2` |

Publish the initial provisional ranking by 11:01, then a higher provisional revision for each distinct live-eligible sale. For this exercise a source progress estimate at event-time 11:05 **only prompts** closing; it neither proves completeness nor classifies an arrival. The hour-specific, trusted durable intake serializes each first admission with a **close marker committed at 11:05:00 UTC, after the duplicate `s4` delivery and `s7`**. First admissions ordered before that marker are live-eligible; admissions at or after the marker are correction-only. Persist each event ID, payload and original live/correction classification with its intake sequence, then preserve those decisions across restart. The final live publication must first drain all live events before the marker and durably commit counts, seen IDs, progress and a terminal publication intent (atomically or through a recoverable equivalent).

This exercise uses the explicit policy **provisional → acknowledged final live → correction**. The serving sink accepts a full final live replacement only after the drain and durably acknowledges it. Hold archive corrections until that final is visible; a delayed correction must not overtake final publication in this particular design. Retire live state only after the final intent is durable and its matching final write is acknowledged. This is an exercise policy, not an engine default; [M08-L02](../lessons/M08-L02.md) also teaches a valid design where a complete correction can supersede a delayed final.

The authoritative archive admits corrections for this hour until **12:00:00 UTC exclusive**. An arrival first admitted at or after that archive cutoff is outside this exercise's automatic correction policy: reject/escalate it for explicit reconciliation rather than silently changing a closed hour. Retain the single ordered history as complete, immutable nested cuts, each including every live record through the close marker, beyond intake closure as necessary for safe retries and repair. Assign each eligible complete cut a stable, increasing correction revision **before** computation; deduplicate IDs over its entire prefix and conditionally publish the full result only after final acknowledgement. Do not purge required cuts until admitted corrections have been reconciled or explicitly failed and retry obligations are satisfied. The source never promises that all late sales arrive before these cutoffs. Sort totals descending with category name ascending to break ties.

For the catalogue, the index lowercases and splits on spaces. Query `steel filter` requires both terms. Search uses disjoint document-ID shards and the same ranking formula on each shard, ordering by descending score and then ascending ID. The following values are the locally ranked matches in a tested common readable index generation `g17`. No other document in the generation matches this query. Shard replies, including transit, arrive at the coordinator at the listed times relative to request ingress.

| Shard | Local candidates `(ID, score)` | Reply at |
| --- | --- | --- |
| A | `(a11, 12)`, `(a12, 6)` | 34 ms |
| B | `(b21, 10)`, `(b22, 7)` | 73 ms |
| C | `(c31, 15)`, `(c32, 8)` | 104 ms |

Return at most two matches. The client deadline is 100 ms from first ingress. Reserve 20 ms after the shard cutoff for merge, response and transit to the client. Browsing accepts an explicitly incomplete result. Export demands a complete, fresh result. For this exercise, freshness requires a verified generation whose manifest proves it includes every catalogue change through a source cut no more than three minutes older than first request ingress. Until that proof is available, freshness is unknown. For the listed query `g17` has a verified two-minute-old cut.

An hourly fault drill attempts 1,000 original valid export requests. Observe each from first ingress through its own 100 ms deadline, retaining first-ingress time across retries. The target is 98% correct, complete, fresh responses received on time. The bins are exclusive. 968 were correct, complete, fresh and on time, 20 returned only partial results on time, four returned complete but stale results on time, three were rejected and five failed or missed the deadline. Partial results in the export drill are contract violations and are counted as failures.

## M08-EX1

1. Trace both jobs from mapper output through partition, shuffle and reduce to ranked output. Show where a retry can replace an attempt without replacing the logical input split. Identify which job is sensitive to a hot category and what measurements would justify an extra aggregation stage.
2. Trace the ranking from the initial provisional publication through duplicate `s4`, live-admitted `s7`, the durable close/final acknowledgement and archive-only `s8`. Give each phase's whole-result totals and publication identity. Specify the deduplication, terminal intent, archive-cut and replay rules. Defend scheduled batch, continuous aggregation or both under the stated freshness and correction requirements.
3. Sketch the postings and request path for the two-term query. Compute the ideal full top two and the on-time browse result. Specify the cutoff, coverage, freshness, and export behavior including a retry. Score the drill and name the data required to distinguish slow shards from stale index generations.
