# M04-L02 pedagogy and curriculum coverage review

Reviewed the canonical lesson, assessment and evidence at draft handoff `3668bc3` for middle and senior engineers. The scope is the [approved M04-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l02), the five assigned rows in [coverage.csv](../../../../../../curriculum/revision-1/coverage.csv), and the [pinned Primer replication section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L829-L876), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`.

## Coverage

| Topic | Disposition | Teaching and assessment evidence |
| --- | --- | --- |
| PR-H085, single-leader replication | taught | **Follow the log to a reader** distinguishes leader execution, standby receipt, durability, replay and eligible read routing. Q1 and EX-1 use the receipt/replay distinction. |
| PR-H086, single-leader disadvantages | taught | **Promote one writer and account for lost history** traces lost acknowledged positions and fencing before promotion. Q2, Q4 and EX-1 assess the consequences. |
| PR-H087, multi-writer replication | taught | **Reconcile concurrent writers** traces two profile edits, their version vectors and a merge that retains independent field intent. Q3 and EX-1 assess causal branches and merging. |
| PR-H088, multi-writer disadvantages | taught | **Reconcile concurrent writers** covers conflicting same-field edits, potentially lost updates, coordinated uniqueness and the availability or latency cost of coordination. Q6 and EX-1 apply the uniqueness decision. |
| PR-H089, replication disadvantages | taught | **Follow the log to a reader** and **Choose by workload and failure contract** explain lag, replay capacity, network and storage cost, leader write work and synchronous wait. Q5 and EX-1 apply these limitations. |

## Pedagogy and assessment

The lesson motivates the authority and freshness decisions with profile edits, then gives a log-position failover trace and an independent concurrent-edit trace. Its session watermark explanation specifies a matching history, applied position, fresh snapshot and unavailable response. EX-1 asks for a safer acknowledgement and promotion contract, link-failure behavior and conflict policy under distinct field semantics. Its worked score uses 93 successful original requests out of 100, counts all seven misses and identifies the 95% target over the 15-minute drill. The sample answer treats a new measurement as necessary to establish whether a revised design meets the target.

LO1 is taught in the first three sections and assessed by Q1–Q3 and EX-1. LO2 is taught across all four sections and assessed by Q4–Q6 and EX-1. The companion has six explained checks and a scenario with a point-bearing rubric that accepts equivalent architectures. The relevant prerequisite topics and separation of teaching and assessment remain clear.

## Findings

No open pedagogical or assigned-topic coverage findings.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned curriculum coverage.

## Round 1 targeted re-review

Reviewed the revised lesson and companion at `0ce6602`. The revised **Promote one writer and account for lost history** section teaches the fixed designated standby, the claim and operation ID transaction, the distinction between pre-admission rejection and an unknown admitted result, and the flush proof needed before a retry or status response reports success. It traces recovery on the designated standby and explains why new confirmations remain unavailable while cross-region protection is absent. The [approved outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m04-l02) assigns acknowledgement, promotion and recovery decisions to this lesson.

The revised EX-1 sample solution and write/failover rubric assess those taught decisions and continue to accept equivalent architectures that satisfy the exercise contract. The original 93/100 score, 15-minute measurement window, 400 ms threshold and accounting for rejected, stale and late requests remain intact. Both outcome maps still point to the sections and assessment items that teach and measure their outcomes. No new pedagogical or coverage finding arose in the revised material.

**Current verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and assigned-topic coverage re-review.
