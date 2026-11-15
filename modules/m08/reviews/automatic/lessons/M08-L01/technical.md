# M08-L01 technical and provenance review

Round 0 reviewed the lesson, companion assessment and claim evidence at draft commit `e6775ee` against the approved SDA-v1 scope for `SD-M08-L01`.

| ID | Severity | Status | Location | Finding and suggested correction | Evidence |
| --- | --- | --- | --- | --- | --- |
| M08-L01-T1 | minor | open | `modules/m08/lessons/M08-L01.md` line 34, “Make retry outputs safe”, and `modules/m08/assessments/M08-L01.md` lines 18 and 35–37 | The example's rule to discard an invalidated contribution is safe. Its claim that a reducer “must discard or replace” after producer loss can sound like a general correctness requirement. A reducer that has already fetched a complete verified deterministic partition can keep it and must avoid appending the replacement for that split. A reducer without a complete fetch can abandon the incomplete attempt and use the replacement. Clarify the two branches or explicitly identify the example as using the stricter discard policy. | [Dean and Ghemawat, MapReduce, §3.3 Worker Failure and Semantics in the Presence of Failures](https://www.usenix.org/legacy/publications/library/proceedings/osdi04/tech/full_papers/dean/dean_html/) |
| M08-L01-T2 | note | open | `modules/m08/lessons/M08-L01.md` line 42, “Place work near data and address skew”, and `modules/m08/assessments/M08-L01.md` lines 53–55 and 69 | To make the performance condition reproducible, the salted subkeys must distribute records reasonably evenly and reach different reducers. For the two-bucket example, derive the bucket from stable sale IDs and show how the partitioner separates those buckets. Two keys can share a hash partition. The second aggregation shown already preserves the total. | [Dean and Ghemawat, MapReduce, §4.1 Partitioning Function](https://www.usenix.org/legacy/publications/library/proceedings/osdi04/tech/full_papers/dean/dean_html/) |

## Technical checks

- The two-job trace and EX-1 preserve quantity under retry. The composite key sorts descending quantities with an ascending category tie-break, and the stated boundary places each example key in the shown range. Reading files in range order produces the stated rankings. The same invariants support Q1–Q5. The lesson explicitly scopes duplicate source rows and external effects outside per-task output selection. [Dean and Ghemawat, MapReduce, §§3.1, 3.3–3.4, 4.1, 4.3, 4.5 and 5.3](https://www.usenix.org/legacy/publications/library/proceedings/osdi04/tech/full_papers/dean/dean_html/)
- GFS master/chunkserver and HDFS NameNode/DataNode responsibilities match the original paper and pinned Hadoop documentation. The lesson and Q6 preserve the separate requirement for an available metadata path. The Spark comparison identifies persistence, lineage recomputation and wide dependencies without assuming memory-only execution or inherited performance figures. [GFS, §§2.3–2.6 and 4.3](https://web.mit.edu/6.1800/www/readings/papers/gfs.pdf#page=2), [HDFS 3.4.2, NameNode and DataNodes and Robustness](https://hadoop.apache.org/docs/r3.4.2/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html#NameNode_and_DataNodes), [Resilient Distributed Datasets, §§2.1, 3.1 and 4.3](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)

## Provenance and asset scope

The claim ledger links the original MapReduce, GFS and RDD research and versioned Apache HDFS documentation. The curriculum's Primer mappings establish scope. The sale records, worked partitions, retry contract and assessment are original examples. The reviewed package contains no embedded third-party figures, code or extended quotations. No material provenance findings.

## Verdict

`ready-for-human-review`
