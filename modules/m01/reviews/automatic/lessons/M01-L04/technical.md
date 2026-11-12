# M01-L04 targeted technical and provenance review

Reviewed the lesson, companion and evidence changes from `e2158e2` through `434dc63` on 2026-11-12. Scope follows the owner's [PR #55 feedback](https://github.com/czyboi/system-design-academy/pull/55#issuecomment-6820605428). The earlier [module review](../../technical.md) records the historical broader review.

## Findings

| ID | Severity | Status | Location | Evidence and result |
| --- | --- | --- | --- | --- |
| PR55-1 | major | resolved | `modules/m01/lessons/M01-L04.md:27–52`, `modules/m01/assessments/M01-L04.md:16–38,71–75`, `modules/m01/evidence/M01-L04.md:13` | The timeline labels the recovered prefix and the primary's final acknowledgment as facts of the worked model. The assumed eligibility check at 40 s is explicit. A controller with a prior lag sample and the standby's applied state has no basis for certifying the ten-second bound without evidence of the primary's acknowledged history or a conservative bound. The strict operation returns unavailable when proof is absent. A separately authorized read with a weaker contract follows its own eligibility rules. The answer to Q4 applies these checks and keeps writes disabled when fencing is unverified. [PostgreSQL 18, §27.2.4](https://www.postgresql.org/docs/18/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW) · [PostgreSQL 18, §26.3](https://www.postgresql.org/docs/18/warm-standby-failover.html) |
| PR55-2 | minor | resolved | `modules/m01/assessments/M01-L04.md:5–11,89–96` | Each `taught_in` string names the same existing headings, in the same order, as the corresponding table row. LO1 includes both the failover trace and the time-budget calculation. EX-1 continues to measure both outcomes. [SDA-v1 M01-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04) |

The lesson arithmetic holds with the stipulated history and verified eligibility. The recovered point is 7 s behind the final acknowledgment, within the 10 s read bound and 2 s beyond the 5 s RPO. The first successful read after 60 s misses the 45 s RTO by 15 s. In EX-1 the corresponding results are an 8 s gap, within the 12 s read bound and 2 s beyond the 6 s RPO, and a 70 s interruption within the 80 s RTO. The 30-day time budget leaves `259.2 − 70 = 189.2 s` after the incident. [AWS, Define recovery objectives](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html) · [Google SRE, Availability table](https://sre.google/sre-book/availability-table/)

## Provenance

PostgreSQL 18 §27.2.4 describes reported lag as timing for recent WAL and distinguishes reported replay timing from other notions of lag. The read eligibility rule is an inference from the lesson's modeled contract. The revised diagram, timestamps and exercise are original. PostgreSQL and AWS supply factual references. The fencing policy also agrees with the external isolation mechanism described in [Red Hat Enterprise Linux 10, Chapter 9](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/configuring_and_managing_high_availability_clusters/index).

No open findings in the reviewed changes. Verdict **ready-for-human-review**.

## Round 1 targeted re-review

Reviewed `68d36a4` against `434dc63` on 2026-11-12. Scope is the LO2 mapping correction raised in the companion pedagogy review.

| Finding | Status | Supporting evidence |
| --- | --- | --- |
| L04-P1 | resolved | [M01-L04, Trace a two-region recovery](../../../../lessons/M01-L04.md#trace-a-two-region-recovery) · [SDA-v1 M01-L04 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m01-l04) |

Q4 applies the section's requirement for evidence of acknowledged history to the earlier lag sample. The companion's `taught_in` string, narrative outcome map and integrated portfolio now all include `Trace a two-region recovery` for M01-L04-LO2 and keep Q4–Q6 and EX-1. The question, answer, teaching text and evidence are unchanged from the earlier technical review. No technical or provenance regression was found. [M01-L04 assessment](../../../../assessments/M01-L04.md#outcome-map) · [M01 outcome portfolio](../../../../integrated/outcome-portfolio.json)

Current verdict **ready-for-human-review**.
