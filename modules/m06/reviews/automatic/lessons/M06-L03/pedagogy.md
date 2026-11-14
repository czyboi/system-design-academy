# M06-L03 independent coverage and pedagogy review

Lesson-mode combined review of `SD-M06-L03` at `570412f`, for middle/senior engineers reading English. Inputs: canonical task specification, approved curriculum, accepted inventory and course coverage review, lesson, assessment and evidence. Source: [System Design Primer, revision ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733). The three assigned inventory rows and exact locators are below. The plan adds local LRU and query-cache operation, layout, failure and hot-key decisions; these are checked in actual instruction.

## Coverage matrix

| Source topic and locator | Assigned lesson/outcome and actual instructional evidence | Status | Assessment / disposition |
| --- | --- | --- | --- |
| PR-ARCH-MEMCACHED, README L1707 | M06-L03 LO1/LO2, “Route to the cache and lose an owner”: client or proxy routes keys; baseline servers do not replicate among themselves. The layout table explains failure and memory implications. | taught | EX-1 layout/failure; appropriate baseline scope. |
| PR-ARCH-REDIS, README L1708 | M06-L03 LO1/LO2, same section: Cluster hash slots, asynchronous replica failover, possible missing recent fill, approximate eviction; compares routing and recovery questions. | taught | Q6 and EX-1; version/deployment scope explicitly stated. |
| PR-CODE-R1-QUERY-NODE, `solutions/system_design/query_cache/query_cache_snippets.py` L25 | M06-L03 LO1/LO2, “Maintain a map and a recency list”: key/value/link node, bidirectional list and map correspondence, update and eviction invariants, capacity-three trace. | taught | Q1, Q2 and EX-1 local operations. |

The query API, miss/fill, changing query/content/rank, placement and failure costs specified by the Academy outline are taught in the query and routing sections. The capacity-three sequence is reproducible, including existing-key update. The clockwise ring gives explicit positions and shows exactly which old key moves when N2 is removed. EX-1 correctly distinguishes its supplied old Q position from the new composite key: the latter's actual hash is not supplied, so its new owner cannot be numerically determined; the sample makes that limitation explicit rather than inventing an owner. No SLO is claimed.

## Findings

**M06-L03-P1 — Major, open — eviction-policy decision is not assessed.** Location: lesson outcome LO2 and assessment Q4–Q6, EX-1 and rubric. LO2 promises that learners can defend an eviction policy as well as a layout using reuse, stale-data risk, failover load and memory. The lesson explains scan pollution and the condition for considering frequency-based admission or eviction; Q1/Q2 and EX-1 trace LRU mechanics, while Q4–Q6 and EX-1 assess freshness, routing and layout, with no prompt or credit criterion asking the learner to select or defend an eviction policy using observed reuse. A learner can earn full marks without demonstrating that part of LO2. Add a workload observation and an explicit LRU-versus-alternative decision with a rubric accepting defensible choices, or obtain an approved outcome-scope change.

## Pedagogy and sequence

The motivating parts directory connects scan pollution to cache choice, then teaches a map/list invariant before a concrete local trace, query flow, and node-loss example. The separate companion has six explained checks, a practical exercise, an outcome map and an alternatives/partial-credit instruction. LO1 is substantively assessed across local, query-coherence and failure traces. The curriculum prerequisites are declared and the scenario stays within their scope. No material excessive introductory filler or missing prerequisite was found. P1 prevents complete LO2 assessment.

## Verdict

**revise** — M06-L03-P1 is an open major finding. No source-topic omission was identified in the assigned three-row scope. This verdict is not technical, source-rights, human or publication approval.

## Targeted re-review at ce55d07

The initial finding and verdict above are retained as history and superseded by this re-review.

**M06-L03-P1 — Major, resolved.** EX-1 now states that measured one-off scans repeatedly evict reusable searches and asks learners to recommend an eviction or admission policy using that observation. Its sample solution compares frequency-based protection and metadata cost with conditional LRU suitability, and the layout/recovery rubric explicitly awards credit for a defensible policy based on observed reuse. The lesson's scan-pollution explanation supports this choice, and the rubric accepts defensible alternatives.

The revised lesson explains the generation/ranking mismatch, complete-key rerouting, shared deadlines and separate check/fill budgets that the changed EX-1 and Q4 assess. It also distinguishes successful Redis replica promotion from a failed promotion before Q6 asks for that distinction. The original capacity-three and ring traces remain reproducible; assessment and teaching retain their scoped boundaries. No material affected coverage or teaching regression was identified.

**Latest verdict: ready-for-human-review.** This is not technical, source-rights, human or publication approval.
