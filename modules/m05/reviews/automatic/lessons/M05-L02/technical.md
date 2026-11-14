# M05-L02 technical and provenance review

Round 0 reviewed the lesson, companion and evidence at draft commit `adc6c52` on 2026-11-13.

## Technical findings

| ID | Severity | Status | Location | Finding and correction | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M05-L02-T1 | major | open | Lesson line 23, wide-row ranges. Companion lines 20, 32–34 and 62–69, EX-1, Q2 and Wide-column route. | With `bucket#device#day#time` and chronological encoding, one device's rows remain contiguous across midnight within each bucket. Eight day-scoped subranges can implement the request, but they are not required by the Bigtable key. Correct the answer to four cross-midnight ranges or explicitly stipulate one subrange per bucket/day in the scenario. Show the actual lower-inclusive and upper-exclusive bounds for one bucket, and distinguish this from a Cassandra model where day is part of the partition key. | [Bigtable row-key design and range reads](https://docs.cloud.google.com/bigtable/docs/schema-design#row-keys), [Bigtable Data API RowRange](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2#rowrange), [Cassandra CQL primary keys](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html) |
| M05-L02-T2 | major | open | Lesson lines 21–27, example cell and row identity. Companion lines 18–20 and 62–69, event and correction model. | Two independent readings for one meter can share the encoded time and even the same bucket. The proposed row key would combine those readings in one row and the same qualifier, where they can look like versions of one event. Add an immutable event ID as a tie-breaker and derive the bucket from that stable identity so corrections reuse the original row. Scope the shown version timestamps as illustrative or show valid distinct timestamps at the table's granularity. State what the audit read requests, how retention protects the required history, and why the latest-value path deliberately selects one version. | [Bigtable schema design, unique row key and timestamped cells](https://docs.cloud.google.com/bigtable/docs/schema-design), [Bigtable Data API Cell and SetCell](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2), [Bigtable garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection) |
| M05-L02-T3 | minor | open | Lesson lines 21 and 27–29, evidence rows Wide rows and versions and HBase and Cassandra. | Use the Bigtable paper's data-model section instead of its landing page. Link HBase family retention and Get/Scan controls as well as the data-model section. Capture the cited Cassandra documentation's version or living-document scope. Cassandra's per-column timestamp claim applies to ordinary reconciliation, and equal timestamps need additional tie behavior if the example discusses them. | [Chang et al., Bigtable §2](https://www.usenix.org/legacy/event/osdi06/tech/chang/chang.pdf#page=2), [HBase data model and versions](https://hbase.apache.org/book.html#datamodel), [Cassandra data versioning](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html#data-versioning) |

The HBase and Cassandra descriptions distinguish queryable cell versions from ordinary timestamp-based conflict reconciliation. The graph walk correctly yields D and E after removing A and duplicate D. The seed index does not bound edge expansion, and the remote supernode trace treats placement and incomplete responses as application decisions. [HBase Reference Guide](https://hbase.apache.org/book.html#datamodel), [Cassandra Dynamo architecture](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html), [Neo4j performance indexes](https://neo4j.com/docs/cypher-manual/current/indexes/performance-indexes/using-indexes/), [variable-length paths](https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/).

## Provenance

The vendor documents substantiate the product mechanisms. The Primer is identified as a topic map. The sample readings, key layout and graph are original. The distributed traversal example is scoped as a design scenario, with no copied figures or other assets.

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the lesson, companion and evidence at draft commit `c06c5e6` on 2026-11-14.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M05-L02-T1 | resolved | The example fixes the bucket and device prefix and defines one closed-start, open-end range per bucket. Keys for all events at 23:45 follow the lower bound. Keys for all events at 00:15 follow the upper bound and are excluded. The chronological day fields keep the midnight crossing in the same range. The revised sample, Q2 and rubric agree on four Bigtable ranges. The Cassandra example addresses both day partitions for each bucket. | [Bigtable row-key order](https://docs.cloud.google.com/bigtable/docs/schema-design#row-keys), [Data API RowRange](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2#rowrange), [Cassandra CQL primary keys](https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html) |
| M05-L02-T2 | resolved | The full immutable event ID distinguishes two measurements in the same second even when their buckets match. Corrections keep the original row and qualifier. The two illustrative microsecond timestamps are distinct and divisible by 1,000, as required for millisecond granularity. The audit and latest-value reads have separate version selection, with retention sized for the audit interval and correction volume. | [Bigtable schema design](https://docs.cloud.google.com/bigtable/docs/schema-design), [Bigtable Data API Cell and SetCell](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc/google.bigtable.v2), [garbage collection](https://docs.cloud.google.com/bigtable/docs/garbage-collection) |
| M05-L02-T3 | resolved | The revision cites the Bigtable paper's data-model discussion directly, adds the HBase version and read-control section and scopes the Cassandra references to the project's living documentation. The Cassandra claim concerns ordinary per-column reconciliation. | [Chang et al., Bigtable §2](https://www.usenix.org/legacy/event/osdi06/tech/chang/chang.pdf#page=2), [HBase version controls](https://hbase.apache.org/book.html#versions), [Cassandra data versioning](https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html#data-versioning) |

The unchanged graph example still returns D and E and distinguishes bounded adjacency work from result completeness. The revision introduced no imported assets.

### Verdict

`ready-for-human-review`
