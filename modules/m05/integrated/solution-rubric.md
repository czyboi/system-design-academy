---
id: M05-EX1-solution
status: draft
---

# Reference design and rubric

## Match the query to the invariant

| Path and recommendation | Mechanism, trade-off and failure response | Two product evidence questions |
| --- | --- | --- |
| Session key in a durable store | Use a hash-derived token key and commit revocation in a single-Region DynamoDB base table before acknowledging it. A same-Region `GetItem` with `ConsistentRead=true` begun after acknowledgement reads revoked and denies despite a stale positive cache. If the read cannot verify state, fail closed and report authority unavailable. An earlier overlapping check follows the specified timing contract. A relational key lookup is also viable if its deployment meets the read and write contract. | Can the exact endpoint observe a previously acknowledged revocation? Which failure or failover modes make the authority unavailable or weaker, and how does the caller recognize them? |
| Indexed product document | Store price and bounded labels in one aggregate and update them together. Query an index with category and state equality followed by price range. A price of 84 eventually removes a former 72 listing from the under-80 result. Keep a canonical compatible price while fixed old readers and writers deploy out. After old writers are gone, update both representations in one document operation, backfill and verify before retiring the old field. A relational transaction and indexed join offer another option, with join and deployment cost to measure. | What is the atomicity scope of the update under the selected configuration? Which actual index and read route supports the browse query while meeting its 15-second freshness target? |
| Wide-column telemetry | Use a key ordered by stable bucket, device, date, time, event ID and correction ID. Derive the bucket from immutable event ID. Store the original and each accepted correction as a separately keyed immutable record. A durable authority binds each correction ID and its inputs to one monotonically allocated per-event revision. A retry after an ambiguous reply reuses that mapping and key. The dashboard selects the greatest committed revision, while audit reads return all accepted records. Query one half-open range per bucket and merge by event time and event ID. A time-partitioned relational table can also work if measurements meet its load and retention targets. | How do encoded bounds, partitions and key distribution affect a cross-midnight read and hot device? How are correction identity, revision allocation, cleanup timing and latest-selection consistency implemented and tested? |
| Graph adjacency with a bound | Find the seed by ID, traverse two directed hops, exclude seed and direct neighbors, and deduplicate. When a required remote expansion misses the budget, return a marked partial result. An asynchronous endpoint can offer exhaustive enumeration. A relational adjacency table or derived neighborhood view fits a fixed traversal if its fan-out and freshness can be measured. | Does the selected execution plan use the seed index and where does remote adjacency work occur? How does the chosen API report timeouts or truncation, and can it distinguish partial from complete results? |

Prefer one operating stack when it meets all four contracts with manageable cost. Add a specialized store where a measured query or scaling requirement warrants the additional migration, restore, monitoring and repair work. Validate read paths under the same traffic and failure assumptions before comparing costs. The store model does not resolve the authority contract.

## Score the drills and test repair

Browse timely freshness is 196/200 = 98%, below 99%. The two late and two unavailable commits remain in the original commit cohort. For each isolated fixture, poll from commit through 15 seconds inclusive at one-second intervals. The actual browse index and route must return the entire ordered A, C result, while same-snapshot instrumentation verifies target B's canonical committed revision. Before the edit, A, B, C is the known result. The fixture fits one page. If pagination is introduced, every page must share the snapshot and be present. An empty or partial result, an older target revision or a separate point read from another snapshot cannot prove exclusion. Freeze later edits for this drill. If a variant permits a newer revision, establish its expected membership and revision in that same snapshot before crediting it. Test delayed and failed index/read paths and verify compatibility against both shapes. [MongoDB 8.0 snapshot read concern](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/).

Relationship completion is 91/100 = 91%, below 95%. A correctly labeled partial reply satisfies the truthfulness requirement and misses the completeness objective. Late full replies and timeouts also miss. Keep the original trace identity across retries. Report latency for complete successful replies separately from completeness. Compare normal seeds with remote high-degree seeds under the same budget.

Inject revocation while the cache has an active entry. Start a same-Region strongly consistent base-table check after acknowledgement and verify a revoked-state denial. Separately make the authoritative route unavailable and verify fail-closed behavior.

For telemetry, use immutable correction records rather than overloading a cell timestamp. The revision authority atomically binds a unique correction ID and immutable inputs to a per-event revision before publishing. Concurrent corrections get distinct ordered revisions. A retry after a lost reply looks up the same binding and republishes the same immutable key and value. A reused ID with different inputs is rejected. Latest means the highest committed revision whose record is available, with pending or unavailable returned if the authority cannot establish that the view is complete.

Retain the original and all accepted corrections until at least original event time plus 30 days. Configure no count-based trimming and no automatic age-based deletion that could remove these records early. A cleanup process deletes only after a trusted clock proves the deadline has passed, accounting for its maximum configured clock error. Corrections received after the audit deadline follow an explicit reject or separately retained policy. Test duplicate and concurrent corrections, an ambiguous retry, two same-timestamp events in one bucket, cross-midnight endpoints, and audit reads immediately before and at the 30-day boundary under maximum clock error. Exercise restore or rebuild for each derived path while its authoritative data remains available. [Bigtable garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection), [Bigtable Data API](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2).

## Rubric

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Access paths and alternatives | 3 | Compares viable models for all four operations using keys, queries, failure behavior and ownership. |
| Guarantees and failure traces | 3 | Preserves the post-acknowledgement revocation check boundary, distinguishes revoked denial from unavailable fail-closed, preserves atomic product fields and rollout compatibility, and specifies stable correction identity, latest selection and 30-day event-relative audit retention. |
| Cohorts and repair | 2 | Computes 98% and 91% with the stated denominators and deadlines. Defines the complete same-snapshot browse fixture probe and tests ambiguous retries, concurrent corrections, retention boundaries and partial traversal. |
| Product evidence and cost | 2 | Gives two scoped verification questions per operation and justifies the operational cost of the proposed split. |

Accept alternative models and fewer stores when their access paths and verified guarantees meet the same requirements.
