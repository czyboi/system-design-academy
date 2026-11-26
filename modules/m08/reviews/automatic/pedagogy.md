# M08 module synthesis pedagogy and coverage review

**Verdict:** ready-for-human-review  
**Round:** 0  
**Scope:** M08 integrated brief, reference solution and rubric, decision summary, evidence, taught coverage and outcome portfolio at handoff `6ea945f`. The review covers integration, progression, coverage reconciliation and assessment. It reuses the three accepted lesson review cycles and does not repeat their detailed audits.

## Coverage and progression

All three per-lesson cycles have status `ready`. Their teaching reviews record five taught source rows for M08-L01, three for M08-L02 and one for M08-L03. `modules/m08/integrated/taught-coverage.csv` contains those nine assigned rows and maps each to a teaching heading. The pinned Primer revision is `ae9bbd7b02d90b9866215de185217d33f39ab733`. The module sequence moves from distributed batch and retries to windowed updates and then indexed search. M08-L02 uses the batch prerequisite explicitly, while M08-L03 composes its own search path and the declared M07-L03 repair prerequisite.

`modules/m08/integrated/outcome-portfolio.json` records all six lesson outcomes against their lesson sections and companion items. Its M08-S1 entry names exactly the approved M08-L01-LO1, M08-L02-LO2 and M08-L03-LO2. The integration evidence identifies their use in exercise tasks 1, 2 and 3 respectively, matching `curriculum/revision-1/CURRICULUM_MASTER.md`, “M08 integrated package plan.”

The decision summary's two sections teach M08-S1 using the exercise's record totals, late correction, slow shard, freshness and full-versus-partial decision. Its option rows expose the requested trigger, mechanism, benefit, cost, signal, avoidance condition and lesson link. The exercise then asks the learner to reconstruct and defend those choices.

## Findings

| ID | Severity | State | Location and learner impact | Suggested change |
| --- | --- | --- | --- | --- |
| M08-P1 | minor | open | `modules/m08/integrated/brief.md`, “Inputs,” describes an export requiring a complete answer and separately limits every search to two matches. The solution correctly discusses the global top two. The word “export” can invite the reader to assume every matching record must be exported, even though the exercise specifies a top-two response. | Name the export contract explicitly as a complete global top-two response in the brief. |

## Synthesis assessment

The exercise computes Tea 9, Mugs 8 and Filters 4, then updates Mugs to 11 after a unique late sale while ignoring the duplicate. Its solution traces the two jobs, retry boundary and hot-key decision. It distinguishes source retention and correction revisions from the live update. The supplied shard times yield an 80 ms cutoff, a partial browse head `[a11, b21]`, and an ideal global head `[c31, a11]`. The solution separately explains generation freshness, missing-shard coverage and export failure.

The drill counts all 1,000 original valid export requests once from first ingress through each 100 ms deadline. Only the 968 correct, complete, fresh on-time responses qualify, producing 96.8% against 98%. Partial, stale, rejected and failed or late requests remain in the denominator. The rubric grades this success ratio separately from result correctness and does not credit a partial export as complete. The prompt, solution and rubric are aligned for the declared top-two exercise, subject to the local wording clarification M08-P1.

No blocker or major teaching, progression or reconciliation gap was identified. M08-L01's accepted lesson report retains its open minor P-1 about RDD lineage explanation. This synthesis verdict covers pedagogy and integration coverage only. Technical and source-rights decisions are recorded independently.

## Independent Stage B review — 2026-11-26

**Provenance of preceding text:** The preceding round-0 report was recovered from an untracked local checkout, not from the GitHub branch or a recorded module cycle. Its historical verdict is not used as an accepted module gate. The review below is this reviewer's independent assessment of the GitHub handoff `f921f8c`; it preserves the recovered finding ID. Scope is the M08 integration package and cross-lesson coverage, progression and assessment only. It reuses the accepted Stage A reports for the three unchanged lessons, whose cycles are ready, rather than repeating their full audits. Audience: middle/senior engineers. Approved scope: `curriculum/revision-1/CURRICULUM_MASTER.md`, “M08 integrated package plan”; approved mapping: `curriculum/revision-1/coverage.csv`. Source map: [System Design Primer, pinned README](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

### Module coverage reconciliation

The integrated topic map has exactly the nine rows assigned to M08 in the approved matrix (five L01, three L02, one L03). The table groups the independently verified exact Primer locator lines and uses the accepted Stage A reports for instructional depth and per-lesson assessment; it does not imply the integrated exercise assesses every lesson outcome.

| Approved topic IDs and source locator | Lesson and instructional evidence | Companion assessment / disposition |
| --- | --- | --- |
| PR-B006 `README.md#L1804`; PR-ARCH-MAPREDUCE `#L1697` | L01, “Trace a category from input to ranked output”; accepted L01 pedagogy report traces map, shuffle, reduce and sorting. | L01 Q1–Q3, Q5, EX-1; taught. |
| PR-ARCH-SPARK `#L1698` | L01, “Choose a processing model”; accepted L01 report describes reuse and recomputation trade-offs. | L01 Q6, EX-1 part 4; taught. The accepted lesson report retains a localized minor P-1 on explaining lineage. |
| PR-ARCH-GOOGLE-FILE-SYSTEM `#L1710`; PR-ARCH-HADOOP-FILE-SYSTEM `#L1711` | L01, “Store inputs as replicated blocks”; accepted report records metadata and data-node roles and availability. | L01 Q6 and EX-1 part 3; taught. |
| PR-PROMPT-16 `#L1669` | L02, “Measure popularity and change separately”; accepted L02 report compares current counts with baseline and limits. | L02 Q5, EX-1 part 4; taught. |
| PR-PROMPT-18 `#L1671` | L02, “Rank exact counts or bound the memory”; accepted L02 report includes windows, deduplication and bounded ranking. | L02 Q1–Q4, EX-1 parts 1–3; taught. |
| PR-ARCH-STORM `#L1699` | L02, “Match recovery to the processing system”; accepted report traces spouts, bolts and replay. | L02 Q6, EX-1 part 5; taught. |
| PR-B008 `#L1806` | L03, “Trace a search across three shards”; accepted report records postings, fan-out, ranked merge and missing-shard boundary. | L03 Q1, Q2, Q4, Q5, EX-1 parts 1–3; taught. |

I fetched the pinned README and checked each of these nine **physical source lines** directly: the first two are the additional-problem prompts, the next five are architecture-reference entries, and the last two are under-development topic entries. Those lines identify the mapped subjects; the approved outline supplies required instructional depth. This supports the author's rejection of `MS05-COV-01` **for the nine M08 locators**. It does not independently decide the separate M09 locators or verify every external-review allegation because the original external report is not in the checkout. No source-topic omission was found within this scoped M08 reconciliation.

The portfolio includes both outcomes for each of L01, L02 and L03, mapped to the corresponding lesson sections and companion items, plus M08-S1 using precisely L01-LO1, L02-LO2 and L03-LO2. The decision summary's record trace and comparisons teach this synthesis; M08-EX1 parts 1–3 measure the trace, late-result choice and freshness/completeness policy. Batch → streaming → scatter/gather follows the approved prerequisites, with the index-repair prerequisite assigned to M07-L03; the synthesis uses rather than retells the individual exercises. No module-wide sequence or duplication blocker is identified.

### Findings and historical corrections

| ID | Severity | State | Evidence, learner impact and specific fix |
| --- | --- | --- | --- |
| M08-P1 | minor | open | Recovered historical finding independently confirmed in `modules/m08/integrated/brief.md`, “Inputs”: export requires a “complete answer” while the same paragraph caps responses at two. The task and solution consistently compute global top two, but a reader can construe “export” as every matching document. State “complete global top-two result” explicitly, while retaining the separate coverage and freshness conditions. Approved target: `curriculum/revision-1/CURRICULUM_MASTER.md`, M08 integrated package plan's partial-result and merge rules. |
| M08-P2 | minor | open | `modules/m08/integrated/brief.md`, M08-EX1 part 3 asks learners to sketch postings, but the inputs list only documents that match **both** terms. The individual postings can also contain unknown single-term documents, so exact postings are underdetermined. A valid generic diagram remains possible, and this does not prevent the top-two decision; clarify that the sketch is conceptual or provide individual term-to-document sets and specify whether those sets are exhaustive. The approved M08-L03 sequence item 1 requires an intelligible index/boolean mechanism. |
| MS05-M08-SYN-01 | major (external) | resolved in reviewed scope | Current `brief.md` “Inputs” explicitly orders duplicate s4, live s7, the 11:05 close and final acknowledgement, then archive-only s8; `solution-rubric.md` “Keep provisional totals revisable” traces `[Tea 9, Mugs 8, Filters 4]` → `[Mugs 11, Tea 9, Filters 4]` → final same → `[Mugs 11, Tea 9, Filters 6]`. The rubric's three-point criterion checks the same ordered classifications and totals. The selected final-before-correction policy is explicitly distinguished from L02's separately taught correction-first alternative. The externally recorded issue is closed for pedagogical alignment of the current artifacts; protocol/source correctness is for the technical review. Evidence: approved M08-L02 sequence item 2 and M08 integrated package plan in `curriculum/revision-1/CURRICULUM_MASTER.md`. |

The brief defines the hourly original-valid-export cohort, first-ingress start, per-request 100 ms deadline, correct/complete/fresh success threshold and exclusive failure bins. The worked solution uses 968/1,000 = 96.8% versus 98%; the rubric separately credits this cohort result and does not let shedding or partial export count as success. The browse and export choices distinguish coverage from freshness and preserve retries under the original deadline. This checks the module-quality-review publication-readiness measurement criterion, rather than relying on a successful-request latency distribution.

**Verdict: `ready-for-human-review`.** No open blocker or major finding in this pedagogy/coverage scope. M08-P1 and M08-P2 are localized minor improvements; the Stage A L01 minor is retained in its own accepted report. This is neither technical/source approval nor human publication approval.

## Round 2 targeted independent re-review — 2026-11-26

Reviewed the corrected integration at draft handoff `d91844f`; scope covers the originally open M08-P1/P2, the changed receipt/snapshot and freshness teaching, assessment and rubric, and adjacent cross-lesson consistency. Earlier recovered history and the independent coverage matrix above remain preserved. Unchanged lesson reviews and outcome mappings were reused rather than re-audited.

| Finding ID | State | Evidence and verification |
| --- | --- | --- |
| M08-P1 | resolved | `modules/m08/integrated/brief.md`, introduction and “Inputs,” now explicitly require a complete **global top-two** export. M08-EX1 part 3 and `solution-rubric.md`, “Preserve the difference between fast and complete,” compute the same global top two and fail an incomplete export. The learner no longer needs to guess whether all matching records are requested. This implements the complete/partial merge distinction in `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L03 sequence item 3 and M08 integrated package plan. |
| M08-P2 | resolved | `modules/m08/integrated/brief.md`, M08-EX1 part 3, now requests a conceptual postings sketch and states that the table supplies conjunctive matches rather than exhaustive single-term postings. `solution-rubric.md`, “Preserve the difference between fast and complete,” makes the same limitation explicit while teaching intersection. This is answerable from the approved M08-L03 index/boolean mechanism in `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L03 sequence item 1. |
| MS05-M08-SYN-01 | remains resolved | The corrected `brief.md` and `solution-rubric.md`, “Keep provisional totals revisable,” continue to distinguish s4 duplicate, s7 live event, final and s8 correction, with the same totals and phase order. The three-point rubric still measures the phase transitions. Evidence: `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L02 sequence item 2 and M08 integrated package plan. |

The integration's decision summary now explains the complete immutable prefix and bound exclusive continuation: the state, seen IDs and publication intent retain `p6`, and an event admitted during startup remains readable instead of being skipped. The exercise states that assumption and explicitly asks for the continuation; its solution traces a duplicate after capture and a possible new admission, while the rubric requires the bound continuation. This composes the approved M08-L01 retry and M08-L02 late-event/recomputation outcomes with the explained capture-order prerequisite in `modules/m07/lessons/M07-L03.md`, “Recover when the snapshot's cursor is gone.” The current scenario's supplied prefix is an assumption rather than a claim that an arbitrary database snapshot intrinsically has such a cursor.

The decision summary explains that the durable final receipt survives correction replacement, why the recovering writer can query that receipt after losing the response, and why it cannot overwrite the newer phase. The brief asks for this lost-acknowledgement, correction and restart trace; the reference answer walks the ordering and idempotent retry, and the rubric grades the receipt and retirement boundary. It is a named scenario policy and is clearly distinguished from the correction-first policy in `modules/m08/lessons/M08-L02.md`, “Update an hourly result.” No new lesson-first causal gap was found in that composition.

For freshness, the decision summary now identifies source-cut relay publication, durable application and eligible-reader query visibility, plus generation/shard/read-view binding; the reference answer explains the missed-deletion and stale-reader failure paths. The brief asks what happens when all shards answer on time but proof is stale or missing, and the rubric requires failing export in that case. These obligations follow the distinction taught in `modules/m08/lessons/M08-L03.md`, “Keep the index current and repairable,” and the approved M08-L03 freshness and partial-failure sequence. The original 968/1,000 cohort calculation and failure denominator remain consistent. No new major pedagogy, module coverage, sequence or assessment regression was found.

**Round 2 verdict: `ready-for-human-review`.** M08-P1 and M08-P2 are resolved for this module synthesis. The separate accepted L01 lesson report's historical minor P-1 remains as recorded there. This is a pedagogy/coverage verdict and does not substitute for technical review or human publication approval.
