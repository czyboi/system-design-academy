# M07 independent pedagogy and coverage synthesis

Reviewed the integrated draft at `526ddd2` against the approved M07 lesson and integration Stories in `delivery/backlog.json`, `curriculum/revision-1/CURRICULUM_MASTER.md`, the integrated brief, solution/rubric, decision summary, taught-coverage and outcome portfolio. The individual lesson reviews are reused: M07-L01, M07-L02 and M07-L03 each ended `ready-for-human-review` within pedagogy/coverage scope. This is a module-wide synthesis, not a repeat of their individual audits.

## Synthesis and coverage

The approved sequence builds durable queue execution in L01, bounded work and retries in L02, then independent log progress and replay in L03. M07-EX1 correctly limits M07-S1 to L01-LO1 and L02-LO2; L03 replay remains assessed in its own companion rather than being claimed by the integration exercise. The portfolio maps all six lesson outcomes to their lesson companions, and the taught-coverage inventory retains the assigned Primer rows, including PR-H141 and PR-ARCH-KAFKA. The decision summary distinguishes synchronous work, broker delivery, task execution and independent log replay. No module-wide missing source row or prerequisite inversion was identified.

The integrated fault drill defines the population as 400 original valid submissions in a five-second burst, measures each from first arrival through the full three-second deadline to client-visible usable output, and counts each original once. The solution scores 384/400 = 96% against 98%, including rejection, unfinished and terminal failures. Capacity calculations separately identify waiting and nonterminal limits and do not use admitted-only latency to pass the user target. The acceptance trace requires commitment before responding to a matching retry, preserving the original durable identity and deadline.

## Findings

**M07-P1 — Major, open — the integration grades a recovery mechanism not taught as an actionable trace.** Location: `modules/m07/integrated/brief.md`, M07-EX1 item 3; `modules/m07/integrated/solution-rubric.md`, “Reserve work and persist the handoff” and “Effect and recovery” rubric; M07-L01 “Trace the crash around acknowledgement.” The brief asks learners to trace an accepted job whose delivery no longer exists. The solution introduces an aged-pending scan, absence of a live claim, a recovery generation and an atomic replacement outbox intent; full credit requires tracing missing-delivery recovery and fencing stale attempts. L01 tells learners to reconcile aged pending jobs even without a DLQ entry, but does not teach a concrete path from detecting the missing delivery to restoring runnable intent or closing the job, and its worked race uses guarded terminal transitions rather than the solution's expiring claim and attempt-token protocol. The synthesis decision summary also does not explain that recovery. A learner cannot reproduce the expected trace from the teaching path without reading the reference solution. Teach one concise end-to-end recovery mechanism and the guard that makes an old delivery or worker harmless in the relevant learner-facing teaching path, or narrow the exercise and rubric to mechanisms explicitly taught; accept equivalent designs that preserve the job's identity, deadline and durable intent. If a previously accepted lesson changes materially, the parent should follow the targeted Stage A re-review workflow.

## Verdict

**revise** — M07-P1 is an open major finding. This synthesis is not technical, source-rights, human, or publication approval.

## Targeted revision 1 re-review — `6fc6c5b`

**M07-P1 — Major, resolved.** The learner-facing `modules/m07/integrated/decision-summary.md`, “Work a deferred completion decision,” now traces an independent reconciler detecting a due pending job or expired claim, fencing the token, atomically reserving a waiting slot and retry intent, and retaining identity and deadline. It explains the full-cap terminal-overload alternative, recovery-generation cooldown and continued physical permit while a stale worker runs. `brief.md` item 3 now explicitly asks for both available and full waiting capacity, and the solution and effect-and-recovery rubric trace those cases and accept equivalent guarded workflows. The earlier gap between merely naming reconciliation and an actionable recovery trace is closed.

**M07-P2 — Major, open — the newly graded admission-to-execution transfer is not taught in the learner-facing synthesis.** Location: `modules/m07/integrated/solution-rubric.md`, “Pending → running” and “Queue and retry budgets” criterion; `modules/m07/integrated/decision-summary.md`, “Work a deferred completion decision.” Full credit newly requires “atomic waiting-slot transfers”; the solution specifies that a worker atomically removes the job from its waiting slot when it claims execution. The learner-facing summary teaches reserving a slot for recovery and keeping a physical permit until execution stops, but does not explain when an ordinary pending job stops consuming a waiting slot or how that transfer relates to the execution claim. The brief asks for states and separate caps, yet it does not supply that transition. A learner could use the taught capacity counts and recovery guard without inferring this specific graded atomicity. Add the pending-to-running transition to the synthesis teaching, connecting the waiting-slot release to the guarded execution claim and separately acquired physical permit; or grade an equivalent demonstrably bounded transfer rather than a specific untaught atomic operation.

## Latest verdict

**revise** — M07-P1 is resolved; M07-P2 is an open major finding. This synthesis is not technical, source-rights, human, or publication approval.

## Targeted revision 2 re-review — `ffd5f31`

- **M07-P2 — Major, resolved.** `modules/m07/integrated/decision-summary.md`, “Work a deferred completion decision,” now explicitly teaches acquiring a separate physical permit and dispatch allowance, atomically releasing the waiting slot while establishing the guarded running claim, and retaining the nonterminal reservation. The “Pending → running” solution uses that same transition, and the queue-and-retry criterion assesses it.
- **M07-P1 — Major, remains resolved.** The decision summary retains the independent reconciler, guarded recovery generation and due time, reuse of existing pending slots, eligibility checks, expired-claim fencing, full-cap terminal overload and the stale execution's physical permit. The integrated solution traces the corresponding paths, and the brief requests both full and available waiting capacity.

## Latest verdict

**ready-for-human-review** — M07-P1 and M07-P2 are resolved within the assigned module pedagogy and coverage scope. This synthesis is not technical, source-rights, human, or publication approval.

## M07-L03 pilot targeted synthesis — `02eb870`

This check is limited to the changed lesson's module connections and reuses the ready Stage A lesson cycle and the previous synthesis findings. The L02 prerequisite still supplies bounded work and retry control, and L03 applies that prerequisite when bounding replay traffic in “Replay into a new index.” The L03 explanation now teaches its own assignment fencing and cutover contract, so following the L02-to-L03 sequence does not require readers to infer fencing from L02.

The integrated decision summary's broker and retained-log rows still distinguish individual job delivery from independent group progress and replay, consistent with the lesson's “Choose the delivery and ordering unit.” Its preview-versus-projection paragraph preserves the boundary between completing a preview job and rebuilding a separate projection. The `PR-ARCH-KAFKA` entry in `modules/m07/integrated/taught-coverage.csv` still points to the lesson's extant “Choose the delivery and ordering unit” section. Both L03 outcome entries in `modules/m07/integrated/outcome-portfolio.json` point to extant teaching sections and the L03 companion.

The integrated `brief.md` assesses M07-S1 through the preview job lifecycle and overload policy. Its outcome-portfolio entry uses L01-LO1 and L02-LO2, while the L03 portfolio entries direct replay assessment to the L03 companion. This remains consistent with the approved M07 integration scope in `curriculum/revision-1/CURRICULUM_MASTER.md`. The earlier M07-P1 and M07-P2 resolutions are unaffected by the L03-only change. No new material sequencing, coverage, or integration finding was identified in this scope.

## Latest pilot synthesis verdict

**ready-for-human-review** — the affected M07 teaching and coverage connections remain consistent.
