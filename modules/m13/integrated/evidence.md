# M13 integration — primary-source evidence and rights

Reviewed 2026-11-16. The case workload/SLI are original synthetic. Primary historical architecture sources are referenced by URL and year, not copied as diagrams or source code.

| Claim | Primary source / date | Applicability limit |
| --- | --- | --- |
| MapReduce key/value map, shuffle/reduce and recoverable distributed work | Dean and Ghemawat, OSDI 2004, [Google Research](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) | Mechanism and historical cluster workload, not present-day capacity guarantee |
| GFS large-file/append-heavy chunk design | Ghemawat et al., SOSP 2003, [Google Research](https://research.google/pubs/the-google-file-system/) | Paper-specific environment, not mandatory design for existing object storage |
| Spark RDD partition lineage and recomputation | Zaharia et al., NSDI 2012, [USENIX](https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia) | Depends on reuse and resource limits, not universal winner |
| Bigtable sorted key structure | Chang et al., OSDI 2006, [Google Research](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) | Historical behavior, not HBase/Cassandra current API |
| Dynamo historical availability/versions | DeCandia et al., SOSP 2007, [Amazon Science](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store) | Not DynamoDB current API or a transaction guarantee |
| Spanner clock uncertainty/coordinated global transactions | Corbett et al., OSDI 2012, [Google Research](https://research.google/pubs/spanner-googles-globally-distributed-database/) | Historical system, not timestamps alone |
| Coordination versus observability | Hunt et al., 2010, [ZooKeeper USENIX](https://www.usenix.org/conference/usenix-atc-10/zookeeper-wait-free-coordination-internet-scale-systems); [Dapper Google Research](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) | A trace is not a fencing/lock authority |

Source ledger is expanded in [M13-L01 evidence](../evidence/M13-L01.md); contemporary MongoDB/Cassandra/DynamoDB/Kafka/Redis/Storm product claims require current version/edition docs if selected in an implementation. No copied graphics or implementation code. No Python tests, actual benchmarking, independent Stage A/B review, source-rights clearance or human approval has occurred.
