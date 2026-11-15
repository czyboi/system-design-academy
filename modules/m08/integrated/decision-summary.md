---
id: M08-decisions
status: draft
---

# Choose processing and search contracts

## Trace the ranking and search decisions

One provisional sales snapshot supports a reproducible count. Map five units of Mugs on one split and three on the other to the same grouping key. Shuffle that key to one logical reducer, then put the completed total of eight into the sales-ordering job. Accept one published result per logical unit of work even if a worker retries. Keep the sales event identity through the lateness window so a replayed five units cannot raise the Mugs total to thirteen. The first new three-unit sale raises it to eleven. Publish a whole revision to make retry and repair observable to readers. [M08-L01](../lessons/M08-L01.md) and [M08-L02](../lessons/M08-L02.md).

Search has a different wait boundary. Before the deadline, the coordinator can compare only the scores from responding shards using the requested index generation. A missing shard makes the list provisional even when that generation is fresh. A complete list can still be too old for export. Choose coverage and freshness contracts for the caller, and record a complete, correct response received on time separately from the latency distribution of responses that succeeded. [M08-L03](../lessons/M08-L03.md).

## Compare processing and retrieval options

| Trigger | Option | Mechanism | Benefit | Cost | Failure signal | When to avoid | Lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Closed replayable sales and a scheduled reporting deadline | Distributed batch | Group and reduce per logical input, then sort completed totals | Reproducible window result | Scan, shuffle and skew delay | Slow reducer grows with one key or retries shift publication past the deadline | A database scan already meets the workload and deadline | [M08-L01](../lessons/M08-L01.md) |
| Consumers need a timely provisional ranking plus late updates | Exact stream and periodic reconciliation | Keep windowed sums and IDs, publish higher revisions and replay retained history for repair | Fresh view with inspectable corrections | State, source retention and revision coordination | Old revision reappears, duplicate inflates count, retained replay unavailable | Batch alone meets freshness or lateness/state budget has no defensible bound | [M08-L02](../lessons/M08-L02.md) |
| Large key cardinality and tolerance for rank uncertainty | Bounded approximate summary | Keep a limited counter set and expose estimate boundaries | Bounds tracking memory | Near ties and missing candidates require interpretation | Overlapping estimates at the publication cutoff | Money settlement or precise rank requires exact totals | [M08-L02](../lessons/M08-L02.md) |
| Interactive browse accepts qualified results | Deadline-bounded partial search | Merge same-generation hits from responding shards and disclose missing shards | Keeps usable results when a shard is slow | Lower recall and possible loss of the best document | Rising missing-shard ratio or contradictory absence claims | An incomplete list cannot safely drive the user's next action | [M08-L03](../lessons/M08-L03.md) |
| Export requires complete, fresh search | Complete-or-fail search | Require all shard replies from the verified generation by cutoff | Preserve global ranking and freshness contract | A single unavailable or slow shard can fail the request | Complete-fresh-on-time cohort success misses target | Caller explicitly accepts coverage loss to meet its own deadline | [M08-L03](../lessons/M08-L03.md) |
