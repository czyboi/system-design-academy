# M08-L01 pedagogy and curriculum coverage review

**Verdict:** ready-for-human-review  
**Round:** 0  
**Scope:** Lesson-mode review of M08-L01 for middle and senior engineers, using the approved SDA-v1 outline, task specification, teaching lesson, and companion assessment. The lesson was read before the assessment solution. The reviewed draft is in commit `e6775ee`.

## Coverage

The pinned System Design Primer revision is `ae9bbd7b02d90b9866215de185217d33f39ab733`. Its assigned source entries are the under-development item at README.md line 1804 and architecture-reference entries at lines 1697–1698 and 1710–1711. The approved coverage rows are in `curriculum/revision-1/coverage.csv`. The source entries name topics and reference external materials, and the Academy outline defines the instructional depth reviewed here.

| Assigned topic and locator | Outcome | Teaching evidence and depth | Companion evidence | Status |
| --- | --- | --- | --- | --- |
| PR-B006, README.md#L1804, distributed computing with MapReduce | LO1, LO2 | `M08-L01.md`, “Trace a category from input to ranked output,” follows mapper pairs through partition, shuffle, group and reduce, then sorts totals in a second job. “Make retry outputs safe” adds a failure trace. | Q1–Q3, Q5 and EX-1 | taught |
| PR-ARCH-MAPREDUCE, README.md#L1697, MapReduce architecture | LO1, LO2 | The same worked trace and “Place work near data and address skew” explain distributed roles, locality, a hot key, the extra aggregation and its cost. | Q1–Q5 and EX-1 | taught |
| PR-ARCH-SPARK, README.md#L1698, Spark architecture | LO2 | “Choose a processing model” explains persisted intermediate partitions, reuse, loss recovery and the memory, shuffle and recomputation trade-offs for the approved comparison. See P-1 for a local clarity improvement. | Q6 and EX-1 part 4 | taught |
| PR-ARCH-GOOGLE-FILE-SYSTEM, README.md#L1710, GFS architecture | LO1, LO2 | “Store inputs as replicated blocks” explains historical master metadata, chunkservers, direct data reads and replica availability. | EX-1 part 3 | taught |
| PR-ARCH-HADOOP-FILE-SYSTEM, README.md#L1711, HDFS architecture | LO1, LO2 | The same section explains NameNode metadata, DataNode blocks, reporting and re-replication, and the metadata availability boundary. | Q6 and EX-1 part 3 | taught |

All five assigned source rows have instructional evidence in the lesson. The Academy-added retry, ordering, locality and skew outcomes appear in the worked trace and decision sections. There are no blocking coverage gaps.

## Pedagogical findings

| ID | Severity | State | Location and learner impact | Suggested change |
| --- | --- | --- | --- | --- |
| P-1 | minor | open | `modules/m08/lessons/M08-L01.md`, “Choose a processing model,” line 54 introduces reconstruction from transformation lineage without naming what lineage records or how recovery uses it. The surrounding discussion supplies enough to make the reuse and recomputation decision, but the recovery cause is less explicit for a learner new to RDDs. | Briefly explain that the lineage records the transformations and dependencies needed to recompute a missing partition from available input or upstream partitions. Preserve the version scope and existing trade-offs. |

## Outcomes and assessment

LO1 is taught through the two-job record trace, retry contract, and storage path, then measured by Q1–Q3 and EX-1 parts 1–3. LO2 is taught through the locality, skew, metadata and processing-choice comparisons, then measured by Q4–Q6 and EX-1 parts 3–4. The companion contains six answered checks and a scenario with a worked solution and a point-based rubric. Its accepted global-order choices include range partitions and a single reducer. Its closed-snapshot and retry assumptions match the lesson, and its decision rubric accepts justified workload-based choices.

The prerequisite M07-L03 is used for the optional external-side-effect connection. The main batch trace is explained within the lesson. No sequencing, duplication or audience-level blocker was found. This report records teaching and assigned-topic coverage, with technical and source-rights review handled separately.
