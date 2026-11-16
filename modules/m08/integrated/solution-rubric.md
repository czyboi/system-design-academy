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

Event time places `s1`–`s8` in `[10:00, 11:00)`; the serialized **durable first-admission order**, not the progress estimate, determines which distinct IDs may enter live state. Initialize exact sums and deduplication IDs from the snapshot: the ranking published by 11:01 is `[Tea 9, Mugs 8, Filters 4]` (provisional). The duplicate `s4`, admitted at 11:01:30 with the same payload, leaves it unchanged. First admission of `s7` at 11:02 raises Mugs by 3 and publishes the newer *provisional* whole result `[Mugs 11, Tea 9, Filters 4]`. An input retry must reuse its recorded identity, sequence and classification; it cannot increment a live or archive total twice.

The durable **11:05 close marker follows `s7`**. Its event-time progress trigger is not evidence of a complete source. Drain every intake sequence before that marker, then persist the terminal intent, progress, deduplication state and counts atomically or through a recoverable equivalent. The sink publishes the same `[Mugs 11, Tea 9, Filters 4]` as a **final live** whole result and durably acknowledges it. A delayed provisional intent cannot overwrite this final. This exercise intentionally requires final live acknowledgement **before** permitting any correction write; a failure to publish final delays correction rather than reclassifying `s7` or bypassing the phase order. Retire live state only after terminal intent and acknowledged final are durable. The broader [M08-L02](../lessons/M08-L02.md) allows a distinct, properly fenced policy where a complete correction wins before a delayed final, but that is not the selected contract here.

The new `s8` is first admitted at 11:07 and belongs to **archive-only correction** despite its 10:57 event time. For a complete immutable archive cut covering the closed live prefix through `s8`, deduplicate all event IDs, then compute `[Mugs 11, Tea 9, Filters 6]`. Durably assign that cut a stable higher correction revision before computing and publish a full replacement **after** final acknowledgement. The sink accepts only increasing verified-coverage revisions; an older repair finishing later loses, and retrying the same cut with the same revision/payload has no effect. A conflicting payload is rejected. An archive admission at or after 12:00 is escalated instead of silently counted, and all accepted immutable cuts remain recoverable until reconciliation and retry obligations finish. Record source cut, phase and serving revision so readers can distinguish a corrected result from final live.

Use scheduled batch for reproducible reconciliation plus an incremental provisional view if repeated scans cannot satisfy the observed freshness deadline. Exact totals suit the small category dimension. Approximate top-k is defensible only with a product contract that communicates uncertainty, especially for close candidates. [M08-L02](../lessons/M08-L02.md).

## Preserve the difference between fast and complete

Each shard uses its term-to-document postings and intersects the postings for `steel` and `filter`. The coordinator sends the query and generation `g17` to all three shards and requests local top two. Under one score order and disjoint document IDs, a candidate dropped below its shard's top two already has at least two global candidates ahead of it. This means the merged head contains the complete global top two if all shards successfully reply from `g17`.

The full order starts `[c31, a11]`; C's reply at 104 ms misses the 80 ms shard cutoff. Browsing can return `[a11, b21]`, marked `complete=false`, `responded_shards=2/3`, `missing=[C]`, `generation=g17` and a verified freshness cut. It cannot say that `a11` is best across all documents. Export returns an explicit incomplete-search failure, not a short or empty list under a complete label. Late replies must not mutate the answer. A retry within the same original request must retain the 100 ms client deadline and combine only compatible results of the same generation; a replica hedge is useful only when spare capacity and the remaining deadline allow it. Charge the extra attempt against the request's load budget. [M08-L03](../lessons/M08-L03.md).

Only 968 of 1,000 original requests qualified, so user-visible success was **96.8%**, below 98%. Record per-shard reachability and timeout histograms, fan-out deadline and coverage, plus the served generation and verified source cut. Compare client-received status and time against those observations. A full reply from an older generation can still fail freshness. Separate successful-response latency from the whole cohort's success ratio.

## Rubric

| Points | Evidence for full credit |
| --- | --- |
| 4 | Group all six sales correctly, show the two job boundaries, preserve one output per logical task, and justify a skew mitigation with relevant signals. |
| 3 | Keep duplicate `s4` constant; classify `s7` before the durable close and `s8` after it; show the provisional → acknowledged final → full archive correction totals, identities and retry/retirement safety. |
| 3 | Derive both top-two lists and the 80 ms cutoff. Preserve completeness and freshness independently in the browse and export contracts. |
| 2 | Count 968/1,000, diagnose a miss against the 98% target, and name measurement fields that separate slow or missing shards from stale generations. |

Use equivalent algorithms or placement if they preserve the stated boundary and workload. A partial export, unqualified global result, duplicated input or exclusion of failed originals earns no credit for the affected criterion.
