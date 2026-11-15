# M06-L02 independent coverage and pedagogy review

Lesson-mode combined review of `SD-M06-L02` at `349c588`, for English-speaking middle/senior engineers. Inputs: canonical task specification, approved curriculum and accepted coverage inventory/review, lesson, companion assessment, evidence, task worklog and repository governance. Source map: [System Design Primer at ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), README caching update sections L1199–L1312. Inventory dispositions below concern instruction, not technical or rights approval.

## Coverage matrix

All rows are assigned to M06-L02 and its LO1/LO2. Section abbreviations: O = Order the cache-aside update; F = Fence a late fill; T = Trace write-through, write-behind and refresh-ahead; C = Choose by the promises clients need. Assessment items refer to the separate companion.

| Source row and locator | Teaching evidence and depth | Status | Assessment and disposition |
| --- | --- | --- | --- |
| PR-H127, when to update, README L1199 | O/T/C compare read and write paths and promises | taught | EX-1 policy choice |
| PR-H128, cache-aside, L1203 | O describes miss, fill, store-first deletion and races | taught | Q1, EX-1 |
| PR-H129, cache-aside disadvantages, L1233 | O: extra miss lookup, stale-fill and failed deletion | taught | Q1, EX-1 |
| PR-H130, write-through, L1239 | T: store commit, cache publish, reply and partial failure | taught | EX-1 cache publication failure |
| PR-H131, write-through disadvantages, L1269 | T/C: store latency, cold keys and unused eager entries | taught | Q4, EX-1 |
| PR-H132, write-behind, L1274 | T: dirty acceptance, later flush and ordering | taught | Q3, EX-1 |
| PR-H133, write-behind disadvantages, L1287 | T: loss before flush and durable replay | taught | Q3, EX-1 |
| PR-H134, refresh-ahead, L1292 | T: near-expiry refresh racing a write, guarded fill | taught | Q5 assesses only capacity; see P1 |
| PR-H135, refresh-ahead disadvantages, L1304 | T/C: failed or unused refresh and origin budget | taught | Q5 wording problem; see P2 |
| PR-H136, cache disadvantages, L1308 | O/F/T/C: stale state, origin fallback, recovery work and latency costs across policies | merged | EX-1 assesses recovery; integration of generic cache costs into policy examples is appropriate for this audience. |

Academy-added read-through is explained in O as ownership of the miss loader and bypass/recovery choice. F presents a concrete authority-checked revision scheme and distinguishes overlapping readers from checks started after commit. No scenario SLO is asserted. The lesson traces overlapping operation and cache failure for the four named policy designs, although the assessment does not measure all of that declared capability (P1).

## Findings

**M06-L02-P1 — Major, open — LO1 is broader than its assessment.** Location: lesson outcomes and assessment Q1–Q3 and EX-1. LO1 promises a trace of both an overlapping read/write and a cache failure under *each* policy. The companion assesses the cache-aside race, a read-through definition, write-behind loss, and write-through publication failure, but asks for neither a write-through overlap nor the refresh-ahead overlap or crash path. A learner can receive full credit without demonstrating the stated capability across policies. Add targeted trace prompts and matching rubric criteria for the missing paths, or explicitly narrow the outcome through the approved curriculum process; preserve the practical scenario and permit equivalent correct traces.

**M06-L02-P2 — Minor, open — refresh check conflates two failure cases.** Location: assessment Q5. The question asks why a *failed* refresh is a capacity concern; its answer explains origin work on a refreshed value that is *never used*. Failure and misprediction can both waste work, but the current explanation does not establish how a failed refresh leads to unused refresh results, so a correct explanation of retry or subsequent demand is not clearly credited. Ask about an unused refresh, or explain the origin work and retry/miss pressure of a failed refresh, accepting both valid causal answers as appropriate.

## Pedagogical assessment and sequence

The lesson follows the venue problem through an explicit stale-fill schedule, a revision-fence example and comparable write-policy traces. It explains trade-offs and repair, assumes the declared M06-L01 prerequisite, and labels implementation assumptions rather than presenting absolute freshness. The companion is separate and has six explained checks, a practical exercise, an outcome map and rubric; EX-1 allows equivalent policies. P1 limits outcome assessment and P2 makes one explanation ambiguous. No material introductory filler or prerequisite gap was identified.

## Verdict

**revise** — M06-L02-P1 is an open major finding and M06-L02-P2 an open minor finding. This is not technical, source-rights, human, or publication approval.

## Targeted re-review at 1de42fe

The initial findings and verdict above are retained as history. The following findings and verdict supersede them.

- **M06-L02-P1 — Major, resolved.** EX-1 now explicitly asks for overlapping reads and recovery after cache loss for cache-aside, write-through, write-behind and refresh-ahead. Its sample solution traces each, including write-through between store commit and cache publication, write-behind pending and replay states, and a refresh surviving a restart. The race/fence and crash-outcome rubric criteria explicitly require these paths. Q2 additionally assesses a read-through loader across a restart.
- **M06-L02-P2 — Minor, resolved.** Q5 now asks about a predicted read that never arrives, and its explanation connects the unnecessary origin work to that exact case.

The affected lesson explains the revision-fenced paths, replay and source-observation deadline used in the revised assessment. EX-1 states the display age limit, requests unavailable behavior and preserves the authoritative reservation path. The lesson provides those decision criteria and fallback, and the rubric accepts alternatives meeting the constraints. The affected coverage remains intact; no material teaching or assessment regression was identified.

**Latest verdict: ready-for-human-review.** This is not technical, source-rights, human, or publication approval.
