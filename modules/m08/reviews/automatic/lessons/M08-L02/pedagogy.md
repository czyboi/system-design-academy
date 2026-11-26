# M08-L02 pedagogy and curriculum coverage review

**Verdict:** ready-for-human-review  
**Round:** 2 targeted re-review  
**Scope:** Lesson-mode review of M08-L02 for middle and senior engineers. The lesson was read before its companion solution. Reviewed materials include the approved SDA-v1 outline, task specification, the lesson and companion. The draft handoff commit is `dce189b`.

## Coverage

The pinned System Design Primer revision is `ae9bbd7b02d90b9866215de185217d33f39ab733`. The assigned source entries are README.md lines 1669 and 1671 for the trend and top-k design prompts, and line 1699 for the Storm architecture reference. The Primer entries name scenarios and link to resources. The approved scope in `curriculum/revision-1/coverage.csv` and `curriculum/revision-1/CURRICULUM_MASTER.md` defines the mechanisms expected here.

| Assigned topic and source locator | Outcome | Actual teaching and assessment evidence | Disposition |
| --- | --- | --- | --- |
| PR-PROMPT-16, README.md#L1669, trending topics | LO1, LO2 | “Measure popularity and change separately” compares current volume and baseline ratios, including minimum volume and zero baseline. Q5 and EX-1 part 4 assess the comparison. | taught |
| PR-PROMPT-18, README.md#L1671, top-k in an interval | LO1, LO2 | “Update an hourly result” defines a window, late events and deduplication. “Rank exact counts or bound the memory” traces Space-Saving counter replacement and uncertainty. Q1–Q4 and EX-1 parts 1–3 assess these mechanisms. | taught |
| PR-ARCH-STORM, README.md#L1699, Storm architecture mechanism | LO2 | “Match recovery to the processing system” explains spout and bolt roles, anchoring, acknowledgements and replay through e4, and contrasts Spark recovery. Q6 and EX-1 part 5 assess the recovery contract. | taught |

The Academy-added window, correction, state-retention and ranking comparisons have explicit examples. No assigned topic is omitted.

## Findings

| ID | Severity | State | Location, evidence and learner impact | Required change |
| --- | --- | --- | --- | --- |
| P-1 | major | resolved | Round 0 identified unexplained spout, bolt and anchoring roles in `modules/m08/lessons/M08-L02.md`, “Match recovery to the processing system,” blocking LO2's recovery comparison. | Round 1 explains each role and traces e4 from root through an anchored child to acknowledgment or failure, including re-emission and external-effect risk. The lesson supports Q6 and EX-1 part 5. The teaching scope is in `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L02 sequence item 4. The named Storm behavior is documented in [Storm Core 2.8.1, Guaranteeing Message Processing](https://storm.apache.org/releases/2.8.1/Guaranteeing-message-processing.html). |
| P-2 | major | resolved | Round 0 identified that `modules/m08/lessons/M08-L02.md`, “Update an hourly result,” assigned increasing revisions without tying them to snapshot coverage. A later-numbered older snapshot could defeat the intended correction order. | Round 1 defines complete immutable nested archive cuts, binds a stable increasing revision to each cut before computation, and traces cut B publishing before A and A's rejection. It also explains same-cut retry and precedence over delayed live writes. EX-1 part 2, its model answer and recovery rubric assess the same contract. This scenario-specific design addresses the late-event and recomputation scope in `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L02 sequence item 2. [The Dataflow Model, §§2–3](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf#page=2) provides the event-time and correction context. |

## Outcomes and assessment

LO1 is taught through the timed event trace, durable-intake cutoff, correction path and bounded-counter example. Q1–Q3 and EX-1 parts 1–3 assess the trace. LO2 is addressed by retention, exact-versus-approximate ranking, trend thresholds and engine-recovery comparisons. Q4–Q6 and EX-1 parts 2–5 assess these decisions.

The six checks have answers and explanations. EX-1 gives a concrete event sequence, durable-intake boundary, crash and correction tasks, model answer and point-based rubric, and accepts either engine when justified. The earlier batch prerequisite provides the initial freshness comparison.

Round 2 rechecked `modules/m08/lessons/M08-L02.md`, “Update an hourly result,” and the changed EX-1 part 2, reference solution and recovery rubric. The lesson states the ordered provisional, final and correction phases, traces correction A arriving before the stalled live drain, and shows why both the older provisional and eventual final intent are rejected. It also explains that live state can retire only after drain, a durable terminal intent, and authoritative confirmation of the matching final or a correction whose complete cut covers that final. The companion asks for and grades this separate correction-first trace and retirement condition. P-1 and P-2 remain resolved. These guarantees are explicit scenario contracts under the M08-L02 late-event and recovery scope in `curriculum/revision-1/CURRICULUM_MASTER.md`; the event-time context is [The Dataflow Model, §§2–3](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf#page=2).

No new major pedagogy or coverage issue was identified in the corrected passages and linked assessment. This report assesses instruction and assigned-topic coverage. Technical and source-rights review are separate.
