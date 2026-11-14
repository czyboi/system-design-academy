---
id: M05-EX1-solution
status: draft
---

# Reference design and rubric

## Match the query to the invariant

| Path and recommendation | Mechanism, trade-off and failure response | Two product evidence questions |
| --- | --- | --- |
| Session key in a durable store | Use a hash-derived token key. Commit revocation at the authority and then acknowledge. A later authoritative check reads inactive and denies even if a cache returns active. An earlier overlapping check follows the specified timing contract. Fail closed if the authority is unavailable. A relational key lookup is also viable if that deployment meets the read and write contract. A cache can accelerate hints while it remains outside the authorization decision. | For the selected deployment, can the exact API and read endpoint observe a previously acknowledged revocation? Which failure or failover modes can make the authority unavailable or weaker, and how does the caller recognize those modes? |
| Indexed product document | Store price and bounded labels in one aggregate and update them together. Query an index with category and state equality followed by price range. A price of 84 eventually removes a former 72 listing from the under-80 result. Keep a canonical compatible price while fixed old readers and writers deploy out. After old writers are gone, update both representations in one document operation, backfill and verify before retiring the old field. A relational transaction and indexed join offer another option, with join and deployment cost to measure. | What is the atomicity scope of the update under the selected configuration? Which actual index and read route supports the browse query while meeting its 15-second freshness target? |
| Wide-column telemetry | Use a key ordered by stable bucket, device, date, time and event ID. Derive the bucket from the immutable ID. Two events with one timestamp are distinct rows, while a correction targets the same event row with a distinct supported cell timestamp. Query one half-open range per bucket and merge by event time and event ID. Keep a retention policy that preserves the original and all required corrections through 30 days after the original event, plus explicit audit and latest-only read filters. A time-partitioned relational table can also work if measurements meet its load and retention targets. | How do encoded bounds, partitions and key distribution affect a cross-midnight read and hot device? Which timestamp granularity, version limits and garbage-collection policy preserve the audit history, and which filters govern its visibility? |
| Graph adjacency with a bound | Find the seed by ID, traverse two directed hops, exclude seed and direct neighbors, and deduplicate. When a required remote expansion misses the budget, return a marked partial result. An asynchronous endpoint can offer exhaustive enumeration. A relational adjacency table or derived neighborhood view fits a fixed traversal if its fan-out and freshness can be measured. | Does the selected execution plan use the seed index and where does remote adjacency work occur? How does the chosen API report timeouts or truncation, and can it distinguish partial from complete results? |

Prefer one operating stack when it meets all four contracts with manageable cost. Add a specialized store where a measured query or scaling requirement warrants the additional migration, restore, monitoring and repair work. Validate read paths under the same traffic and failure assumptions before comparing costs. The store model does not resolve the authority contract.

## Score the drills and test repair

Browse timely freshness is 196/200 = 98%, below 99%. The two late and two unavailable commits remain in the original commit cohort. Trace an atomic price edit and measure when its revision or a newer valid state is visible through the actual browse path. Use controlled probes and an isolated fixture where a newer revision's membership is known. Test a delayed and failed index/read path and verify the compatibility query against both shapes.

Relationship completion is 91/100 = 91%, below 95%. A correctly labeled partial reply satisfies the truthfulness requirement and misses the completeness objective. Late full replies and timeouts also miss. Keep the original trace identity across retries. Report latency for complete successful replies separately from completeness. Compare normal seeds with remote high-degree seeds under the same budget.

Inject revocation while the cache has an active entry, start another check after acknowledgement, and verify denial or fail-closed behavior when the authority is unavailable. For time series, force two same-timestamp events into one bucket, replay a correction, test interval endpoints across midnight, and verify audit versions and latest-only results after retention and compaction. Exercise restore or rebuild for each derived path while its authoritative data remains available.

## Rubric

| Criterion | Points | Full credit |
| --- | ---: | --- |
| Access paths and alternatives | 3 | Compares viable models for all four operations using keys, queries, failure behavior and ownership. |
| Guarantees and failure traces | 3 | Preserves late revocation semantics, atomic product fields and rollout compatibility, event identity and audit history, and honest relationship completeness. |
| Cohorts and repair | 2 | Computes 98% and 91% with the stated denominators and deadlines, and identifies concrete failure and repair tests. |
| Product evidence and cost | 2 | Gives two scoped verification questions per operation and justifies the operational cost of the proposed split. |

Accept alternative models and fewer stores when their access paths and verified guarantees meet the same requirements.
