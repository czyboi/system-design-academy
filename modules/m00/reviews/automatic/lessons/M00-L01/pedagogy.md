# M00-L01 pedagogy and curriculum coverage review

Round 0 reviews the lesson, companion and evidence for middle/senior backend engineers against the approved [M00-L01 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l01--how-to-learn-and-check-readiness) and [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv). The source topic map is Donne Martin's System Design Primer at `ae9bbd7b02d90b9866215de185217d33f39ab733`, README sections [Study guide](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L182) and [System design topics: start here](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L372-L409). The pinned local source was inspected. No relevant prevention reminders were supplied.

## Coverage

| Topic and source locator | Lesson evidence and disposition | Assessment and gap |
|---|---|---|
| PR-H010, Study guide, README L182 | **Taught** in [Choose a study route](../../../../lessons/M00-L01.md#choose-a-study-route). The table adapts breadth, depth and practice to time and readiness. | Q4–Q5 and EX-1 apply a route and its cost. |
| PR-H028, System design topics: start here, README L372 | **Merged** into the same section. The first pass maps requests, state and failure boundaries and identifies a constraint for later study. | Q5 and EX-1 apply the route. Merging orientation with route selection is consistent with the outline. |
| PR-H029, Step 1: Review the scalability video lecture, README L378 | **Taught** in Choose a study route. The learner actively sketches a flow, constraint and failure while using the linked lecture. | Q5 addresses the route. |
| PR-H030, Step 2: Review the scalability article, README L390 | **Planned-not-taught.** Choose a study route recommends a written architecture case and revisiting components, but supplies no corresponding first-pass reading or guided comparison of the source's article topics, including clones, databases, caches and asynchronism. See P-1. | Q5 and EX-1 test general practice, leaving the article-reading step without instructional or assessment evidence. |
| PR-H031, Next steps, README L400 | **Merged** into Choose a study route and [Worked example and historical architecture](../../../../lessons/M00-L01.md#worked-example-and-historical-architecture). Learners revisit decision-driving components, change workload or failure, and inspect evidence before transferring a design. | Q6 and EX-1 apply evidence-based evaluation. Detailed performance, availability and consistency trade-offs are assigned to later M01 lessons. |

## Findings

- **P-1 · major · open · coverage** — [Choose a study route](../../../../lessons/M00-L01.md#choose-a-study-route), paragraph 1, and the historical [teaching review](../../../M00-L01/teaching.md). The assigned PR-H030 is the scalability **article** at README L390, while the historical report identifies it as a historical architecture case. The current lesson's written architecture example teaches evidence evaluation but does not show the learner how to use the distinct introductory article step to compare the basic scaling mechanisms. The approved matrix assigns this source heading to this lesson's first-pass route. Add a concise guided first-pass article-reading step that makes the intended component comparison and follow-up action clear, and align the coverage evidence and any relevant assessment mapping. Source: [pinned PR-H030](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L390-L398), [approved coverage matrix](../../../../../../curriculum/revision-1/coverage.csv).
- **P-2 · minor · open · pedagogy** — [Companion front matter](../../../../assessments/M00-L01.md) maps LO2 only to Choose a study route. Q6 and EX-1 also require the historical-architecture evidence criterion taught under Worked example and historical architecture. Add that heading to the outcome map so learners and maintainers can trace the complete assessed route to its teaching. The questions themselves are answerable from the lesson. Source: [approved LO2 and assessment plan](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l01--how-to-learn-and-check-readiness).

## Lesson comprehension and assessment

The initial request trace identifies the unknown after a lost response, distinguishes transaction atomicity from the application rule across attempts, and connects a crash before acknowledgement to repeated consumer work. These explanations and the declared backend/SQL prerequisites allow the learner to reconstruct LO1 without the answer key. The transaction-gap worked example then selects a repair and changes the failure ordering, and the route table states breadth, depth, practice and time costs for LO2. The six checks have explanations, and EX-1 has a sample answer and a four-point rubric that accepts justified alternatives. No material sequence or audience-level issue was found beyond P-1.

The assessment maps LO1 to Q1–Q3 and LO2 to Q4–Q6 and EX-1. Q6 and EX-1 need the additional lesson heading identified in P-2. The companion is separate from teaching.

**Verdict: revise.** P-1 remains a material assigned-topic coverage gap.

## Round 1 targeted re-review

Reviewed the corrected lesson, companion and evidence after the scoped handoff at `bae5308`. The preceding table and findings record round 0 observations.

| Finding | Status | Resolution and evidence |
|---|---|---|
| P-1 | resolved | [Choose a study route](../../../../lessons/M00-L01.md#choose-a-study-route) now guides a first pass through the introductory scalability article topics and explains how clones, a database, a cache and asynchronous work affect the request path. It uses a slow-database example to connect an observation to the next study or profiling step. [Q7](../../../../assessments/M00-L01.md#q7) assesses that comparison. The source heading and its topic list are identified in the [pinned Primer](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L390-L398). PR-H030 is now taught. The evidence notes that the archived article pages could not be verified on recheck. |
| P-2 | resolved | The [companion front matter and outcome map](../../../../assessments/M00-L01.md#outcome-map) now name both Choose a study route and Worked example and historical architecture for LO2, and map Q6 and EX-1 to the outcome. This matches the [approved outcome and assessment plan](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l01--how-to-learn-and-check-readiness). |

The added comparison is understandable from the teaching text, and Q7's decision and explanation follow the example. The updated companion has seven checks, a practical exercise, a sample answer and a rubric. The changes to the request, transaction and queue traces preserve the lesson's causal sequence for its declared audience. The historical article's accessibility remains a source-verification limitation recorded in the lesson evidence.

**Round 1 verdict: ready-for-human-review.** No open blocker or major pedagogy or coverage finding remains.
