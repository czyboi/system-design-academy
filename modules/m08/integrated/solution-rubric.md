---
id: M08-EX1-solution
status: draft
---

# Reference design and rubric

## Aggregate once per logical input, then sort

Job 1 maps each sale to `(category, quantity)`. Use one logical contribution per record in the input snapshot. For illustration send Tea and Filters to reducer X and Mugs to Y. A replacement attempt for split A writes attempt-scoped intermediate output. The coordinator's accepted output for A supplies all reducer buckets for that logical split, without consuming both attempts' outputs as separate contributions. A reducer publishes only one completed result per logical output partition. This handles execution retry while the input snapshot or a deduplication step handles duplicate source events. [M08-L01](../lessons/M08-L01.md).

| Reducer | Grouped values | Totals |
| --- | --- | --- |
| X | `Tea [6, 1, 2]`, `Filters [4]` | `Tea 9`, `Filters 4` |
| Y | `Mugs [3, 5]` | `Mugs 8` |

Job 2 emits ordered keys `(-9, Tea)`, `(-4, Filters)` and `(-8, Mugs)` from the completed totals. One reducer sorts this small result and emits `[Tea 9, Mugs 8, Filters 4]`. At larger category counts, range-partition the same composite key and read partition files in range order. Sorting within independently hashed partitions would leave an unordered set of files. If Tea dominates shuffle bytes and one reducer's execution time, combine local sums and inspect the resulting per-reducer bytes and task duration. If the imbalance remains, divide the hot key into stable salt buckets, sum each, and reduce the bucket sums back to one Tea total before ranking. Extra shuffle and recovery work need a measured benefit.

## Keep provisional totals revisable

An event's event time selects `[10:00, 11:00)`. Initialize exact category sums and deduplication identities from the same provisional snapshot, then apply the retained continuation from its input cut. A retry of `s4` leaves `Mugs 8` unchanged. On the first valid `s7`, add 3 to Mugs and publish `[Mugs 11, Tea 9, Filters 4]` as a higher revision. Commit the event ID, state delta, progress and publication intent together or make them recoverable from the same durable progress. A restart drains inputs durably ordered before the close marker using the original intake classification. Use whole-result conditional writes at the serving boundary so replaying a publication cannot double increment a reader's totals.

Use a scheduled batch for reproducible reconciliation, plus an incremental view for the provisional deadline and late updates if repeated scans cannot meet the freshness requirement under representative loads. Require the sink to order provisional results by durable intake sequence and prevent them from superseding final results. This exercise enables correction publication after the final live result is durably visible, so a retry cannot regress the final state. During archive retention, a repair groups a complete archive prefix by sale ID before aggregating. Before computation, bind each immutable prefix to its stable revision in coverage order. Require that the prefix includes the closed live cut and replace the whole result only with greater verified coverage. A delayed repair from a smaller prefix loses even if it finishes last. Record both the source cut and the serving revision. Exact totals make sense for this small category dimension. A bounded approximate display is defensible only with a product contract that communicates uncertainty, especially if candidate counts are close. [M08-L02](../lessons/M08-L02.md).

## Preserve the difference between fast and complete

Each shard uses its term-to-document postings and intersects the postings for `steel` and `filter`. The coordinator sends the query and generation `g17` to all three shards and requests local top two. Under one score order and disjoint document IDs, a candidate dropped below its shard's top two already has at least two global candidates ahead of it. This means the merged head contains the complete global top two if all shards successfully reply from `g17`.

The full order starts `[c31, a11]`; C's reply at 104 ms misses the 80 ms shard cutoff. Browsing can return `[a11, b21]`, marked `complete=false`, `responded_shards=2/3`, `missing=[C]`, `generation=g17` and a verified freshness cut. It cannot say that `a11` is best across all documents. Export returns an explicit incomplete-search failure, not a short or empty list under a complete label. Late replies must not mutate the answer. A retry within the same original request must retain the 100 ms client deadline and combine only compatible results of the same generation; a replica hedge is useful only when spare capacity and the remaining deadline allow it. Charge the extra attempt against the request's load budget. [M08-L03](../lessons/M08-L03.md).

Only 968 of 1,000 original requests qualified, so user-visible success was **96.8%**, below 98%. Record per-shard reachability and timeout histograms, fan-out deadline and coverage, plus the served generation and verified source cut. Compare client-received status and time against those observations. A full reply from an older generation can still fail freshness. Separate successful-response latency from the whole cohort's success ratio.

## Rubric

| Points | Evidence for full credit |
| --- | --- |
| 4 | Group all six sales correctly, show the two job boundaries, preserve one output per logical task, and justify a skew mitigation with relevant signals. |
| 3 | Hold duplicate `s4` constant, incorporate `s7` in the correct event-time window, and explain the provisional/final state and versioned replay correction without duplicate effects. |
| 3 | Derive both top-two lists and the 80 ms cutoff. Preserve completeness and freshness independently in the browse and export contracts. |
| 2 | Count 968/1,000, diagnose a miss against the 98% target, and name measurement fields that separate slow or missing shards from stale generations. |

Use equivalent algorithms or placement if they preserve the stated boundary and workload. A partial export, unqualified global result, duplicated input or exclusion of failed originals earns no credit for the affected criterion.
