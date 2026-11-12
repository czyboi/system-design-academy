# M01-L04 targeted pedagogy and coverage review

Reviewed 2026-11-12 at `434dc63`, in lesson mode for the edits responding to [PR #55 feedback](https://github.com/czyboi/system-design-academy/pull/55#issuecomment-6820605428). The audience is middle and senior engineers. The previous [module review](../../pedagogy.md) supplies the prior M01-L04 coverage assessment. This review examines the changed lesson, companion and affected outcome-portfolio entries against the [approved M01-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04).

## Finding

| ID | Severity | Status | Location and learner impact | Evidence and correction |
| --- | --- | --- | --- | --- |
| L04-P1 | major | open | `modules/m01/assessments/M01-L04.md`, LO2 front matter and Outcome map, and `modules/m01/integrated/outcome-portfolio.json`, M01-L04-LO2 | Q4 now asks the learner to explain why a pre-partition lag measurement cannot establish the strict read's freshness. The causal explanation is in `Trace a two-region recovery`, under “At failover.” LO2's `taught_in`, narrative map and portfolio list three other headings but omit this necessary teaching section. A consumer following the LO2 mapping will miss the explanation needed for Q4. Add `Trace a two-region recovery` to all three LO2 teaching-section lists and keep the current Q4–Q6 and EX-1 mapping. [Approved M01-L04 outcome and assessment plan](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04) · [Authoring contract, required metadata](../../../../../../docs/authoring-format-contract-v1.md#required-metadata) |

## Findings addressed in the changed material

- The lesson's worked history distinguishes the supplied retrospective facts from the controller's evidence at failover. Its 60-second successful-read timeline explicitly assumes the eligibility check succeeds. The explanation also provides a response for an unprovable strict freshness contract. [M01-L04, Trace a two-region recovery](../../../../lessons/M01-L04.md#trace-a-two-region-recovery)
- Q4 applies the new distinction to a specific lost-heartbeat scenario. EX-1 stipulates independent verification in its successful-read timeline, and its sample solution addresses missing evidence separately. The checks and exercise remain separate from teaching. [M01-L04 assessment, EX-1 and Q4](../../../../assessments/M01-L04.md)
- LO1 metadata, narrative outcome map and portfolio agree on the three teaching headings and Q1–Q3 plus EX-1. Those items retain the recovery-time, recovery-point, dependency and availability-budget assessments. [M01-L04 outcome map](../../../../assessments/M01-L04.md#outcome-map) · [M01 outcome portfolio](../../../../integrated/outcome-portfolio.json)

## Coverage and verdict

The changed recovery explanation continues to teach the failover mechanism and decision assigned to PR-H047 and supports the approved failure-policy outcome. The prior module review's other M01-L04 source-topic judgments remain historical context for this targeted re-review.

**Verdict: revise.** L04-P1 is open and requires the three LO2 mapping entries to be synchronized. This verdict covers pedagogy and the affected curriculum mapping.

## Round 1 targeted re-review

Reviewed the correction at `68d36a4`. The following status supersedes the earlier finding and verdict.

| Finding | Status | Supporting curriculum |
| --- | --- | --- |
| L04-P1 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |

The M01-L04 LO2 front matter, narrative outcome table and integrated outcome portfolio now all include `Trace a two-region recovery`. The section's “At failover” explanation supplies the reasoning used in Q4. Q4–Q6 and EX-1 remain mapped to LO2. The previously reviewed LO1 mapping is unchanged.

**Round 1 verdict: ready-for-human-review.** This verdict covers the affected pedagogy and curriculum mapping.
