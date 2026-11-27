# M10-L07 — independent pedagogy and curriculum coverage review

Initial Stage A; scoped draft handed off at `922eddd`. Audience: middle/senior engineers, English. Reviewed task spec/state/worklog, approved `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L07 and assigned `coverage.csv`/source inventory rows, lesson before companion, assessment and evidence. Pinned source: [Primer sales rank case](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/sales_rank/README.md) and [sales_rank_mapreduce.py](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/sales_rank/sales_rank_mapreduce.py), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. Inspected actual case, nested bullets and two source code stages, not only row names. M08-L02 is an accepted prerequisite input, not re-audited.

## Coverage matrix

Lesson sections below are in `modules/m10/lessons/M10-L07.md`; Q and EX items refer to its separate assessment. Grouped IDs each receive the stated disposition.

| Assigned source topic / locator | Outcome and instructional evidence | Status; assessment and gap/rationale |
| --- | --- | --- |
| H002, H003, H004, H006, H007, H008: weekly ranking scope, assumptions and usage, README L5–68 | LO1/LO2; State ranking contract gives half-open week, hourly refresh, product/category counts, read volume and late correction | taught; EX-1. Synthetic assumptions replace dated source numbers. |
| H009: high-level design, README L69–74 | LO1; Start reproducible snapshot, Trace two jobs, Publish and Invalidate readers give the end-to-end materialization/serve path | merged; EX-1. |
| H010, H011 and CODE-RANK-FILTER: filter and aggregation, README L75–200, code L6 | LO1; Start and Trace: canonical revision dedup, UTC window, taxonomy membership, mapper keys, partition/shuffle and per-product sum | taught; Q1–Q2, EX-1; multi-category sample distinguishes 21 category-units from 16 unique product-units. |
| CODE-RANK-SORT: composite sort and identity reducer, README L120–200, code L39 | LO1; Trace two jobs: category, descending units and product tie-break, category/range partition and warning about hash-local order | taught; Q3, EX-1. Direction and stable ties are made explicit rather than inheriting source's ascending code. |
| H012: serve materialized ranking, README L201–237 | LO1/LO2; Publish and Invalidate readers: complete revision, pointer, pinned pagination and version-keyed read cache | taught; Q4–Q5, EX-1. |
| H013: scaling/cache and read-heavy workload, README L238 onward | LO2; Invalidate and Resolve: materialized top-100, cache generation, skew and batch vs incremental; original extra talking points map elsewhere | merged; Q5–Q6, EX-1. Hot-key resolution requires P-2 correction. Timestamp, replay and multi-category cases are explained. |

The approved outline additionally requires changing taxonomy and event time/replay/hot-category decisions, which extend the source's simpler fixed-category assumptions. Lesson addresses these; see P-2 for a specific hot-key causal gap. No other material assigned source-topic omission identified.

## Lesson-first reasoning and outcome alignment

Before inspecting companion answers, the sample can be reconstructed from canonical unique input → event-time filter and frozen taxonomy → mapping to category/product → exact sums → category composite sort and deterministic tie-break → complete staged result and manifest → generation-pinned cache. Initial pA=7, pB=5, pC=4; return s6 revises pA to 4, Kitchen to 9 and places pB ahead. A late old batch must not replace the corrected result. Batch is preferred while hourly freshness holds; incremental state and reconciliation trade complexity for timeliness. The explanation of salting is the exception identified in P-2: it loses the instructional path back to product-level output for the stated skew case.

| Outcome action | Lesson instruction | Companion evidence |
| --- | --- | --- |
| LO1 trace/model filter, grouping, two stages and materialized serving | State; Start; Trace; Publish; Invalidate | Q1–Q3 and EX-1 require duplicate handling, two stages, rankings and manifest. |
| LO2 choose/defend batch/incremental, membership, skew and freshness | State; Resolve; Publish; Invalidate; Make measurable | Q4–Q6 and EX-1 address correction, taxonomy, cache, policy and batch choice. P-1 leaves taught SLO decision ungraded; P-2 affects hot-key reconstruction. |

Six checks with explanations and separate practical exercise/rubric are present. Equivalent SQL is accepted with explicit equivalent contract. No diagram or length quota used.

## Initial findings — round 0 history

P-1 — **major, open** — `modules/m10/assessments/M10-L07.md`, EX-1 Task, Reference solution 5 and rubric “Evidence and SLO”. The lesson's “Make the result measurable and falsifiable” requires 99% of all original valid reads in a five-minute ingress cohort to receive the authorized, correct advertised published revision at the client within 300 ms, counting wrong, rejected, failed and late requests. EX-1 only asks for an original-read metric; its reference omits the specific window, endpoint, target and deadline, and its rubric asks only for a denominator. No observed outcomes or pass/fail decision are required, so the taught success criterion can be bypassed by a fast admission-only metric and the design decision is not actually assessed against it.

**Fix:** Add exclusive counts for a five-minute cohort of unique original reads, including timely correct/authorized results, wrong/stale results, late responses, rejected and failed/unknown requests. Require and score the success calculation and decision against 99%, using client receipt within 300 ms of first ingress and the correct advertised revision. Count retries once and keep shedding and other failures in the denominator; separately measure scheduled hourly publication success. Basis: approved M10-L07 LO2 and batch/freshness trade-off in `curriculum/revision-1/CURRICULUM_MASTER.md`; lesson “Make the result measurable and falsifiable”.

P-2 — **major, open** — `modules/m10/lessons/M10-L07.md`, “Resolve hot categories, boundaries and replays”; companion EX-1 reference item 4. Job 1 earlier partitions on the full `(window, category, product)` aggregation key, but this paragraph says all Kitchen events share a key and recommends salting `Kitchen` and a final reduce per logical category before ranking. A learner following that transition can merge pA and pB to a category total and lose the individual product totals required for the product leaderboard; alternatively, a hot category's many distinct product keys may already be distributed in Job 1, while the category-grouped Job 2 sort remains hot. The text therefore does not show how its stated hot-key improvement preserves the central product ranking, and the reference repeats the unspecified category-level merge.

**Fix:** distinguish a hot `(window,category,product)` aggregation key from a hot category in the ordered top-K stage. For aggregation, salt while preserving full product key, then remove the salt by exact final reduce on the original full key; for the category sort, show how range partitions or bounded local top-K merge preserve deterministic global product order/ties. Align EX-1 reference with the chosen approach and its cost. Evidence: approved sequence items 2 and 4 in `curriculum/revision-1/CURRICULUM_MASTER.md` and pinned source [filter and sort code](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/sales_rank/sales_rank_mapreduce.py#L6), which retains `(category, product)` through aggregation.

## Initial verdict — round 0 history

**revise** — P-1 and P-2 were open at the initial review. This is pedagogical and assigned-topic coverage review, not technical or source-rights approval, human approval, or publication authorization.


## Targeted round 1 re-review — 2026-11-27

Scope: P-1, P-2, their changed lesson and assessment dependencies, and nearby regressions. Reused the initial assigned-topic inventory and source inspection above; this is not a new whole-source audit. Reviewed the changed lesson before the companion solution. The approved `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L07 outline requires filtering and category/product aggregation, distributed sorting, ranking publication/cache, handling hot categories and batch versus incremental freshness decisions.

| ID | Current state | Resolution evidence and instructional judgment |
| --- | --- | --- |
| P-1 | resolved | Lesson “Publish a whole result revision” defines the exclusive two-hour admission cutoff, hourly complete prefix, 15-minute publication deadline and the s6 11:00/12:00 distinction. “Make the result measurable and falsifiable” defines the five-minute original-read population, client receipt within 300 ms, authorized correct revision, 99% threshold and failure denominator; it separately defines the hourly publication objective and 3/4 example. Assessment EX-1 scenario supplies mutually exclusive outcomes totaling 1,000 and four scheduled cases; Task requires both calculations and decisions; reference 5 and “Evidence and SLO” rubric grade 970/1,000 = 97% versus 99% and 3/4 = 75% versus 100%. Retries remain one original and shedding remains in the denominator. This closes the assessed decision gap. |
| P-2 | resolved | Lesson “Resolve hot categories, boundaries and replays” distinguishes the hot full `(week, category, product)` Job-1 key from the Job-2 category ordering group. It preserves that full key through salted partial sums and recombines on it, then explains exact disjoint local top-K using the common `(-units, product_id)` ordering, including why a discarded item cannot enter global top K and the alternative of ordered ranges. EX-1 reference 4 and “Policy and performance trade-offs” rubric require the same product-preserving recombination and shared-order merge. This restores the path from skew mitigation to per-product ranking. |

The lesson-first reconstruction also remains coherent for changed revision and publication contracts: select the highest authoritative line revision or tombstone, give a return a separate identity, and emit +2 for the +3→+2 replacement; bind a manifest to immutable inputs, then admit only currently authorized taxonomy/policy with nonregressing complete source coverage. The two incomparable-job examples show why a newer taxonomy or a newer cut alone cannot decide admission. Q1, Q5 and EX-1 reinforce these transitions, and the rubric requires the relevant revision and eligibility decisions. No new material teaching or assigned-topic coverage regression was identified in the changed passages; the initial coverage matrix remains applicable, with its P-2 caveat now resolved. Six explained checks, the separate exercise and the outcome mappings remain present.

## Current verdict

**ready-for-human-review** — P-1 and P-2 are resolved; no open blocker or major finding in this targeted pedagogy and assigned-topic coverage re-review. This is not technical or source-rights approval, human approval, publication authorization, or a claim of execution.

