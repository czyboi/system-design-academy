# Evidence for M08-EX1

Verified against the SDA-v1 M08 integration plan. The sales and search datasets, deadlines and drill counts are original scenario inputs. No throughput or product latency is implied.

| Integrated claim | Supporting evidence and applicability |
| --- | --- |
| Map, partition and reduce the snapshot, then range-sort the completed totals. Use attempt-scoped outputs. | [M08-L01 evidence](../evidence/M08-L01.md), C1–C3. Original MapReduce, §§2–4 and §5.3. The reducers, salt proposal and totals belong to this exercise. |
| Event-time membership, late corrections and deduplication depend on window and sink policy. | [M08-L02 evidence](../evidence/M08-L02.md), C1–C3. The archive cutoff and version contract are assumptions, not an engine's default. |
| Disjoint shards and comparable scores permit a top-k merge. A timeout can require an explicit partial result or a failure, while a source cut describes freshness separately. | [M08-L03 evidence](../evidence/M08-L03.md), C1–C4. Cutoff math and the merge order are derived from the original scenario. Manifest freshness is an application-level proof requirement. |

The assessment consumes M08-L01-LO1 in task 1, M08-L02-LO2 in task 2 and M08-L03-LO2 in task 3. All companion outcomes remain in their own assessments. The M08-L03 [retrieval handoff](../evidence/M08-L03.md#retrieval-handoff-to-sda-ms06) identifies the exact MS06 input paths and consumers.
