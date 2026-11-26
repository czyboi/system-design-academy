# M08-L03 pedagogy and curriculum coverage review

**Verdict:** ready-for-human-review  
**Round:** 1 targeted re-review  
**Scope:** Lesson-mode review of M08-L03 for middle and senior engineers, using the approved SDA-v1 outline, task specification, teaching lesson and companion assessment. The lesson was read before the assessment solution. The reviewed draft was handed off in commit `26d1afa`.

## Coverage

The pinned System Design Primer revision is `ae9bbd7b02d90b9866215de185217d33f39ab733`. The sole source row assigned to this lesson is the under-development topic at README.md line 1806. `curriculum/revision-1/coverage.csv` and `curriculum/revision-1/CURRICULUM_MASTER.md` define its approved instructional scope.

| Source topic and locator | Outcome | Actual teaching depth | Companion evidence | Status |
| --- | --- | --- | --- | --- |
| PR-B008, README.md#L1806, scatter gather | LO1, LO2 | “Trace a search across three shards” analyzes a query, intersects postings, sends it to three shards and merges ranked matches. It shows the missing top candidate on a timeout. “Choose the work and failure boundary” explains partitioning, deadlines, hedging, completeness and costs. | Q1, Q2, Q4, Q5 and EX-1 parts 1–3 | taught |

The Academy-added index analysis and boolean lookup appear in “Find candidates from terms.” “Keep the index current and repairable” links freshness and the repair contract to the declared M07-L03 prerequisite. Those are taught, with a concrete three-shard scoring trace and explicit assumptions.

## Findings

| ID | Severity | State | Location, evidence and learner impact | Required change |
| --- | --- | --- | --- | --- |
| P-1 | major | resolved | Round 0 found that `modules/m08/assessments/M08-L03.md`, EX-1 part 3, requested every matching record while the scenario and answer returned only top two. | Round 1 scopes both the prompt and sample answer to the correct complete global top two, with the missing-shard failure decision taught in `modules/m08/lessons/M08-L03.md`, “Trace a search across three shards” and “Choose the work and failure boundary.” The approved completeness decision is in `curriculum/revision-1/CURRICULUM_MASTER.md`, M08-L03 teaching sequence item 3. |
| P-2 | minor | resolved | Round 0 found that the companion front matter omitted teaching sections used by Q1, Q3 and Q6. | Round 1's `outcome_map` includes “Find candidates from terms” and “Keep the index current and repairable” for LO1, and “Keep the index current and repairable” for LO2. The mapping agrees with the narrative coverage and actual teaching. The required mapping contract is `docs/authoring-format-contract-v1.md`, Required metadata. |

## Outcomes, assessment and sequence

LO1 is taught in the postings, analysis, shard-ranking and index-update sections, and measured by Q1–Q3 and EX-1. LO2 is taught through partitioning, deadline, failure and repair decisions, and measured by Q4–Q6 and EX-1. The companion provides six explained checks, a practical scenario and a point-based rubric.

The one-hour success measure states the original valid-search population, arrival-to-client-response interval, 200 ms deadline and 99% target. It counts rejected, failed, timed-out, late and partial responses against complete on-time success, with partial-result rate and successful-response latency reported separately. EX-1 applies the same denominator and computes 960/1,000 = 96%.

The corrected “Keep the index current and repairable” uses a visible deletion at offset 42 to explain why durable index application alone cannot establish search visibility at cutover. It distinguishes that guarantee from a committed deletion still pending in the outbox, then states the additional source-cut and relay-publication boundary. EX-1 part 4, its sample answer and rubric assess the same distinction. The cited engine behavior is scoped to [Elasticsearch 8.19 near-real-time search](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/near-real-time.html) and the outbox context to [AWS transactional outbox issues and considerations](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html#issues-and-considerations). The application-level cutover contract remains clearly stated as a scenario design.

The worked trace explains a query before introducing partial response policies and the explicitly linked M07-L03 rebuild contract. The corrected passages and linked assessment introduce no new major pedagogy or coverage finding. This report covers instruction and assigned-topic coverage. Technical and source-rights review are separate.
