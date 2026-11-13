# M03 module synthesis pedagogy and coverage review

Reviewed integration handoff HEAD `9c8a3f9cf80808cd8edc818de5b46a44e40182be`, the approved [M03 curriculum and synthesis outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l03), integration specification and canonical brief, solution, decision table, coverage and outcome portfolio. Scope is module synthesis and cross-lesson connections for middle/senior engineers, reusing accepted Stage A reports rather than rescoring unchanged lessons. All three recorded lesson cycles are ready.

## Coverage, sequence and integration

The 24 topic rows in `integrated/taught-coverage.csv` have existing lesson headings as locators; their substantive dispositions are supported by the accepted Stage A coverage reports (three M03-L01, 19 M03-L02, two M03-L03). The seven portfolio records include six lesson outcomes and M03-S1. The lesson records identify actual teaching headings and assessment items consistently with the accepted individual outcome maps. The M03-S1 subset is exactly M03-L01-LO2, M03-L02-LO1 and M03-L03-LO2, and M03-EX1 is the separate synthesis assessment. Its teaching evidence needs the correction below.

The learning sequence proceeds from boundaries and ownership, through interface contracts, to discovery and bounded retries before the catalogue synthesis. The M03-L02 preview now links to the canonical M03-L03 worked example; its 40 ms failure, 20 ms backoff and 120 ms completion match the later trace. The decision table supplies all eight planned fields for each row and links to the relevant lessons. The exercise asks learners to compare boundary alternatives, trace public and internal contracts, and choose discovery and failure policies in the same workload; the reference accepts a justified modular alternative.

## Findings

- **P-M03-S1-01 — Major, open — `modules/m03/integrated/outcome-portfolio.json`, M03-S1 teaching:** The record identifies only `solution-rubric.md` as teaching. Those sections are the answer and rubric for M03-EX1, not the prior instructional evidence on which the synthesis can rely. The [approved synthesis outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l03) identifies the three lesson outcomes as its taught subset; the portfolio should trace each constituent skill to the actual applicable lesson teaching sections, including the worked examples, while keeping M03-EX1 and its solution in the assessment evidence. Use the existing canonical portfolio representation or a precise supported representation that identifies those separate lesson paths and sections; do not claim all six lesson outcomes for the synthesis.
- **P-M03-S1-02 — Major, open — `modules/m03/integrated/solution-rubric.md`, Self-evaluation / Failure policy and Verification:** Brief item 3 requires a bounded concurrency policy and behavior during discovery unavailability, but full-credit failure-policy criteria name only time, ownership and operation identity. Verification mentions testing maximum endpoint age and an in-flight cap without explicitly grading the policy and fallback themselves. A response can therefore earn full credit without specifying the required outage behavior or an actual bound. The [approved integration Story](../../../../.academy/specs/SD-M03-INTEGRATION.json) requires discovery lifecycle and timeout/retry sequence, and the exercise explicitly makes these deliverables. Add them to a scored criterion with clear full-credit evidence and retain the existing alternatives and scoring scale.

**Verdict: revise.** The above are synthesis and portfolio findings; this is not technical, human or publication approval.

## Round 1 targeted re-review

Reviewed the corrections handed off at `7049534a56600c4cc5560e3e2a4ebac38a1eba36`. The earlier verdict records the initial review; this section records the current result.

| Finding | Status | Curriculum basis |
| --- | --- | --- |
| P-M03-S1-01 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |
| P-M03-S1-02 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |

The M03-S1 teaching record now points to the instructional synthesis in `decision-summary.md`, which explains the three constituent skills and links directly to the respective lesson worked examples and discovery mechanism. Its `uses_lesson_outcomes` retains exactly the approved three IDs, each resolving to the corresponding lesson teaching record; the brief and solution remain assessment evidence. The failure-policy rubric now requires an in-flight cap and where saturated work waits, a bounded cache age and the defer/resume/expiry policy during discovery failure. The reference supplies an example and retains the two-point criterion scale and alternative designs.

**Current verdict: ready-for-human-review.** This verdict covers module pedagogy and assigned coverage, not technical or human approval.
