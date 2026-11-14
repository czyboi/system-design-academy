# M05 integrated technical and provenance review

Round 0 reviewed the integrated brief, solution, decision summary and evidence at draft commit `7f8154b` on 2026-11-14. The review reused the accepted Stage A reports and checked how the four operation contracts are observed in one workload.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Evidence |
| --- | --- | --- | --- | --- |
| M05-SYN-T1 | major | open | Integrated brief line 18, product drill. Solution lines 13, 21 and 33, product browse, scoring and repair rubric. | The endpoint can show a revision while a product matches the filter, but it cannot show a per-product revision when a price change removes that product. An empty or partial response, a stale response that never contained the product, or a separate authoritative point read could be mis-scored as evidence that the browse path incorporated the edit. Define the observed production-path probe and how it proves both revision and complete membership for inclusion and exclusion. Use a controlled fixture with known initial and expected membership and either a browse-serving applied watermark from the same snapshot or a same-snapshot diagnostic comparison of product revision and browse membership. Set the probe deadline and score unproven or incomplete results as misses. If a newer revision qualifies, verify the corresponding expected state before crediting it. | [MongoDB 8.0 snapshot read concern](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/), [MongoDB 8.0 read preference](https://www.mongodb.com/docs/v8.0/core/read-preference/), [M05-L01 technical round 1](lessons/M05-L01/technical.md) |
| M05-SYN-T2 | major | open | Integrated brief line 15, telemetry audit invariant. Solution lines 14 and 25, telemetry recommendation and test. | Bigtable age-based garbage collection applies to cell timestamps, and a low version cap can discard the original before 30 days if corrections accumulate. Two writes to the same column using one supported timestamp cannot be stored as two distinct cell versions. Choose an explicit policy covering the event-relative audit deadline, initial version timing, correction volume and version precision. Define how distinct corrections receive distinct ordered versions and how a retry reuses the same write identity and version. A count cap needs a defensible correction bound. Another valid design uses immutable separately keyed correction records and an explicit latest selector. Test duplicate and concurrent corrections and the oldest required version near the audit boundary. | [Bigtable garbage collection by age and version count](https://docs.cloud.google.com/bigtable/docs/garbage-collection), [Bigtable Data API Cell and SetCell](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2), [M05-L02 technical round 1](lessons/M05-L02/technical.md) |
| M05-SYN-T3 | minor | open | Solution lines 12 and 25, session recommendation and test. | The evidence identifies a tested contract for the example store, while the sample only says durable keyed authority. Name the same-Region DynamoDB base-table `GetItem` with `ConsistentRead=true`, or another explicit eligible route. Trace separately the expected revoked-state denial and fail-closed behavior when that route cannot verify state. In the rubric, replace “late revocation semantics” with the precise post-acknowledgement check boundary. | [DynamoDB GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html), [strongly consistent reads](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html), [M05-L01 technical round 1](lessons/M05-L01/technical.md) |

The initial sample correctly separates the revocation rule from an overlapping check. The four-bucket telemetry model preserves distinct event identity and a contiguous range per bucket. Graph completeness is 91/100 for the fixed-edge cohort. Partial, timed-out and late replies stay in the denominator. The browse calculation is 196/200 = 98% on the supplied labels and misses 99%. Finding T1 concerns how a future test produces those labels. The decision summary ties the storage choices to access and authority.

## Provenance

The package distinguishes DynamoDB operations, MongoDB version scope, Bigtable APIs and Neo4j query mechanisms. Workload inputs are labeled illustrative and the graph placement is an application scenario. No imported examples, executable samples or third-party assets were identified.

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the revised integrated brief, solution and evidence at draft commit `b188d79` on 2026-11-14.

| ID | Status | Verification and next action | Primary evidence |
| --- | --- | --- | --- |
| M05-SYN-T1 | resolved | The fixed fixture starts at A, B, C and expects exactly A, C in the price-and-ID order after B's edit. The production browse route and index must produce the complete result, and instrumentation checks B's committed revision in the same snapshot. Earlier revisions, partial or empty responses, and independent cross-route reads do not qualify. The finite probe schedule, deadline and inclusion of unobserved outcomes are defined. | [MongoDB 8.0 snapshot read concern and atClusterTime](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/#read-concern-and-atclustertime), [read preference](https://www.mongodb.com/docs/v8.0/core/read-preference/) |
| M05-SYN-T2 | open | Independent event and correction keys, durable allocation, duplicate identity and the 30-day event-relative cleanup threshold now address timestamp collision and premature version-count eviction. The durability boundary between the allocator and separately stored Bigtable record remains unspecified. If revision 7 gets a durable binding but its publisher fails before the Bigtable record is written, a scan containing revision 8 cannot establish whether a missing 7 is pending, rejected or an accepted correction lost from the view. Put the immutable payload, revision binding and publication intent in one authoritative transaction, and state whether that commit is acceptance. Let an idempotent publisher repair from retained source without a client retry. Drive latest selection and audit completeness from authoritative committed revisions rather than the maximum row observed. Coordinate cleanup with the same authority to close intake and fence or drain admitted publications, so delayed retries do not recreate expired records. Another design that commits data and accepted identity atomically at one owner can meet the same contract. | [AWS relational outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html#using-an-outbox-table-with-a-relational-database), [Bigtable write atomicity and conditional writes](https://docs.cloud.google.com/bigtable/docs/writes), [Bigtable garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection) |
| M05-SYN-T3 | resolved | The revised sample names a strongly consistent `GetItem` on the same single-Region DynamoDB base table and separates revoked-state denial from an authority outage. The rubric now checks the exact post-acknowledgement boundary and preserves the operation-overlap behavior. | [DynamoDB GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html), [strongly consistent reads](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) |

The 98% browse score and 91% relationship result remain correct. The revision introduced no assets.

### Verdict

`revise`

## Round 2 targeted re-review

Reviewed the revised integration at draft commit `55afdc4` on 2026-11-14. The review checked the telemetry acceptance and cleanup races and the earlier product and session corrections.

| ID | Severity | Status | Location | Verification and primary evidence |
| --- | --- | --- | --- | --- |
| M05-SYN-T2 | major | resolved | Brief lines 15 and 27–28. Solution lines 14 and 27–31, 38–39. Evidence line 9. | The conditional row mutation checks open lifecycle and the observed revision before it commits the next revision, payload and input-bound receipt together. Concurrent corrections observing the same revision serialize at that mutation. A matching retry reads the saved outcome, and a losing or ambiguous attempt rereads before making another guarded write. The audit and latest paths require the complete row from the same authority. Google documents row-atomic reads, and same-cluster read-your-writes with an app profile eligible for and configured to allow single-row transactions. The bound of 100 corrections at up to 2 KiB each bounds the correction payload, with row size and read cost checked separately. The conservative clock check keeps the fence beyond the event-relative retention deadline. A correction that wins before the fence is included in the row, while a mutation arriving after close cannot match the open state. Deletion follows durable closure, and the retained marker prevents a delayed create or retry from reopening the identity. The solution keeps strict reads unavailable if recovery lacks proof of the complete authoritative row. [Bigtable CheckAndMutateRowRequest](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2#checkandmutaterowrequest), [atomic row reads](https://docs.cloud.google.com/bigtable/docs/reads#overview), [routing and single-row transactions](https://docs.cloud.google.com/bigtable/docs/routing#single-row-transactions), [app profile settings](https://docs.cloud.google.com/bigtable/docs/app-profiles#standard-app-profiles), [row sizing](https://docs.cloud.google.com/bigtable/docs/schema-design#rows), [garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection) |
| M05-SYN-T1 | major | resolved | Brief lines 18–20. Solution line 21. | The complete A, C result through the actual browse route and B's committed revision remain jointly required from one database snapshot. The 15-second deadline, 196/200 score and miss classification remain intact. [MongoDB 8.0 snapshot read concern and atClusterTime](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/#read-concern-and-atclustertime) |
| M05-SYN-T3 | minor | resolved | Solution lines 12, 25 and 38. | The same-Region DynamoDB base-table check still uses `ConsistentRead=true` after revocation acknowledgement and distinguishes revoked denial from an unavailable authority. [DynamoDB GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html), [strongly consistent reads](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) |

The new Bigtable mechanism is supported by Google Cloud documentation. The retention fence and retry contract are application design rules. The revision adds no third-party assets or executable examples.

### Verdict

`ready-for-human-review`

## Owner-authorized rubric follow-up

Reviewed the single integrated content change at draft commit `0583ebb` on 2026-11-14. The full-credit criterion at `integrated/solution-rubric.md` line 38 now allows any implementation that demonstrates the required operational guarantees.

| ID | Severity | Status | Location and verification |
| --- | --- | --- | --- |
| M05-SYN-T2 | major | resolved | Solution line 38 requires an atomic and durable acceptance outcome bound to the payload, input identity and revision, with no duplicate effect on a retry. It still requires proof of complete audit and latest reads or an unavailable result, retention from the original event time and protection against recreation during or after cleanup. The concrete Bigtable mechanism and failure tests remain at lines 27–31 and 39. [Bigtable conditional writes](https://docs.cloud.google.com/bigtable/docs/writes#conditional-writes), [atomic row reads](https://docs.cloud.google.com/bigtable/docs/reads#overview), [garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection) |
| M05-SYN-T1 | major | resolved | Solution lines 21 and 39 still require the complete browse membership and revision proof from the same snapshot. Line 38 still requires atomic product changes and rollout compatibility. [MongoDB 8.0 snapshot read concern](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/) |
| M05-SYN-T3 | minor | resolved | Line 38 preserves the post-acknowledgement boundary and distinguishes revoked denial from unavailable fail-closed. The same-Region base-table `GetItem` with `ConsistentRead=true` remains at lines 12 and 25. [DynamoDB GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) |

### Verdict

`ready-for-human-review`

## PR #77 targeted technical follow-up

Reviewed the integrated decision summary, brief, solution and evidence at draft commit `49210a1` on 2026-11-14.

| ID | Severity | Status | Location and verification |
| --- | --- | --- | --- |
| M05-SYN-T1 | major | resolved | Brief lines 18–20, solution lines 21–23 and 41, evidence line 8. Success still requires the complete ordered A, C response and B's applicable committed revision on the actual serving path, both observed by 15 seconds. A newer revision qualifies only with the same known expected fixture membership. The database example uses one snapshot for canonical revision and browse membership. The separate-index example correlates B's committed revision and durable event ID with the searchable generation actually used, including each required shard. A revision-bearing indexed record, removal receipt or gap-free applied position must describe that serving view, which also spans every page. Broker publication, a canonical point read or a different replica's progress supplies insufficient evidence. Outbox documentation supports the atomic publication intent. The response-to-generation proof is application instrumentation. [MongoDB 8.0 snapshot read concern and atClusterTime](https://www.mongodb.com/docs/v8.0/reference/read-concern-snapshot/#read-concern-and-atclustertime), [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html#using-an-outbox-table-with-a-relational-database) |

The parcel worked decision at `integrated/decision-summary.md` lines 8–12 separates keyed current state, ordered event history and code redemption. The `(parcel_id, event_time, event_id)` ordering provides a stable tie-breaker. The redemption authority commits the one-use claim and input-bound operation receipt atomically. A timed-out admitted request remains unknown until the authority resolves the same operation ID, and independent confirmation is forbidden during a partition. The linked M05 lesson scopes remain applicable. The example's durable receipt is an application contract. DynamoDB's `ClientRequestToken` alone provides only a ten-minute retry window. [PostgreSQL 18 transactions](https://www.postgresql.org/docs/18/tutorial-transactions.html), [DynamoDB transaction actions and scope](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html#transaction-apis-txwriteitems), [DynamoDB TransactWriteItems token](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_TransactWriteItems.html#DDB-TransactWriteItems-request-ClientRequestToken).

The original browse denominator and 98% result remain intact. M05-SYN-T2 and M05-SYN-T3 remain resolved. The revision introduces no third-party assets or new vendor guarantees.

### Verdict

`ready-for-human-review`
