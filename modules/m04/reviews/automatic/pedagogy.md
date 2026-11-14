# M04 module synthesis pedagogy and coverage review

Reviewed the integrated package at `1147892` against the [approved M04 synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-integrated-package-plan), the canonical integration spec and the accepted per-lesson Stage A pedagogy reports. The review covers cross-lesson sequencing, topic and outcome reconciliation, the integrated exercise and its rubric.

## Finding

| ID | Severity | Status | Location and learner impact | Suggested correction |
| --- | --- | --- | --- | --- |
| M04-SYN-P1 | major | open | [Brief, M04-EX1 item 4](../../integrated/brief.md#m04-ex1) requires checkout timely success for **all original eligible checkouts**, a 15-minute drill, a 750 ms deadline and a 98% target, including late, rejected, failed, timed-out and unresolved operations as misses. [Rubric, Durability and status](../../integrated/solution-rubric.md#rubric) awards full credit for calculating status success and keeping checkout and status outcomes distinct, without requiring the checkout cohort, deadline, threshold or miss accounting. A design that sheds nearly all checkouts can satisfy the stated full-credit rubric while leaving the checkout success target unmeasured. The [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-integrated-package-plan) requires an evaluated benchmark plan and invariants. | Require the checkout success numerator and denominator, 15-minute arrival window, 750 ms deadline, 98% target and all named miss categories in the sample measurement plan and full-credit rubric. Keep confirmed-order loss and status success as separately scored outcomes. |

## Integration and coverage

The sequence builds from M04-L01 transaction ownership through M04-L02 acknowledgement and M04-L03 routing, then uses the M04-L04 derived view and M04-L05 plan analysis as scaling options. The integrated scenario exercises query work, replica recovery, capacity placement, routing and fenced movement. The stated placement totals 236, 185, 160 and 59 checkouts/s across four modeled 250/s shards, and the reference identifies merchant-wide fan-out. The status calculation is 980/1,000 = 98% against a 99% target, including late, stale, timeout and unavailable responses.

The topic ledger maps the assigned M04 source topics to the accepted teaching sections, including the four historical SQL scaling patterns in M04-L05. The outcome portfolio retains each lesson's two separate companion outcomes and maps M04-S1 only to M04-L02-LO2, M04-L03-LO2 and M04-L05-LO1, as specified in the approved synthesis plan. The decision summary contains trigger, option, mechanism, benefit, cost, failure signal, avoidance condition and lesson reference for each planned option.

The model's baseline and candidate per-loop inputs are distinct, yielding 12,000 and 50 emitted rows. The reference also distinguishes remote durability proof on retries from a recovered operation record. M04-SYN-P1 concerns the scoring of the user-visible checkout outcome.

**Verdict: revise.** This verdict covers module synthesis pedagogy and coverage.

## Round 1 targeted synthesis re-review

Reviewed the revised brief and reference/rubric at `4bfd404`. The checkout cohort now contains 576,000 original eligible requests over 15 minutes at the stated uniform arrival rate. With confirmations paused for 30 seconds and a 750 ms deadline, the reference counts at least 640 × 29.25 = 18,720 misses and computes an upper bound of 96.75% timely success. It explicitly concludes that this proposed policy misses the 98% target. The rubric requires the cohort, deadline, target, miss categories, calculation and separate confirmed-ID recovery reconciliation. Status success remains a distinct 980/1,000 = 98% measure against 99%.

| Finding | Status | Evidence |
| --- | --- | --- |
| M04-SYN-P1 | resolved | [Revised brief, M04-EX1 item 4](../../integrated/brief.md#m04-ex1) and [reference design and rubric](../../integrated/solution-rubric.md#rubric). The [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-integrated-package-plan) requires an assessed benchmark plan. |

The revised reference also traces a stable operation receipt and logical order revision across a location move and rollback, and tests immediate loss after the new writer becomes active. The brief asks for this trace and the rubric grades its durability barriers and recovery. Capacity placement is correctly treated as provisional until the synchronous path is measured. These additions connect the accepted replication and sharding lessons to the integrated task. Topic and outcome reconciliation and the original status cohort remain intact.

**Current verdict: ready-for-human-review.** This verdict covers targeted module synthesis pedagogy and coverage.

## PR #77 targeted synthesis re-review

Reviewed the changed decision summary and outcome portfolio at `49210a1`, using accepted lesson-review evidence. **Work a bottleneck-to-ownership decision** transfers query-plan diagnosis to a support-ticket workload, then connects a hot workspace to project-local routing, fan-out, migration and separate success and loss measurements. Its query rewrite states the eligibility and ordering conditions, and its throughput figures are labeled hypothetical.

The M04-S1 portfolio names the new worked section together with the decision table. Its lesson outcome subset remains M04-L02-LO2, M04-L03-LO2 and M04-L05-LO1. The M04-L05-LO1 portfolio entry includes **Read a concrete SQL plan**, consistent with its companion's front matter and narrative map. This progression supports transfer into the order-database exercise defined in the [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-integrated-package-plan).

No new pedagogical or assigned-topic coverage finding arose in the changed scope.

**Current verdict: ready-for-human-review.** This verdict covers the PR #77 targeted module synthesis pedagogy re-review.
