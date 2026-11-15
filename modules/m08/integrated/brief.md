---
id: M08-EX1
status: draft
outcomes: [M08-S1]
---

# Publish category rankings and query a sharded index

A shop publishes hourly category totals by units sold and lets shoppers search its catalogue. The sales snapshot and the catalogue index have separate source streams. The ranking can be revised for late sales. Search has separate contracts for browsing and for an export that demands a complete answer.

## Inputs

The closed batch input for the provisional `[10:00, 11:00)` UTC window contains these rows. Each ID identifies one sale. The retained event archive also receives a duplicate of `s4` at 11:01:30 and a new sale `s7` for 3 Mugs with event time 10:58, arriving at 11:02. Both arrive before the window's correction cutoff.

| Split | Sales in the provisional input |
| --- | --- |
| A | `s1 Tea 6`, `s2 Mugs 3`, `s3 Tea 1` |
| B | `s4 Mugs 5`, `s5 Filters 4`, `s6 Tea 2` |

Publish provisional totals by 11:01. A source progress estimate at event-time 11:05 permits the normal pipeline to record a close marker in the durable intake order. Close only after applying all earlier live inputs. The source does not guarantee that every late event will arrive before closure. The archive retains a single ordered history of the sales and corrections, with immutable complete prefixes, until the correction period ends. During that period, a missing sale discovered after closure may be reconciled into a newer published revision without reopening live state. Sort totals descending with category name ascending to break ties.

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
2. Show the published ranking before and after the two late deliveries. Define the state and identity needed to make that update safe. Defend scheduled batch, continuous aggregation or both under the stated freshness and correction requirements. Explain how an archived correction changes the reader-visible result.
3. Sketch the postings and request path for the two-term query. Compute the ideal full top two and the on-time browse result. Specify the cutoff, coverage, freshness, and export behavior including a retry. Score the drill and name the data required to distinguish slow shards from stale index generations.
