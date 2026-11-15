# M07-L02 independent coverage and pedagogy review

Reviewed the lesson-mode combined assignment at `564f4e0` for English-speaking middle/senior engineers. Inputs: SD-M07-L02 spec, approved curriculum and coverage inventory, canonical lesson, assessment and evidence. Source topic map: [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The accepted global inventory is reused for the assigned lesson row.

## Coverage matrix

| Source topic and locator | Lesson / outcome and instruction | Status | Assessment and disposition |
| --- | --- | --- | --- |
| PR-H141 Back pressure, README L1355 | M07-L02 LO1/LO2; “Trace one burst and its recovery” quantifies a cap and rejection; “Put back pressure where it can work” distinguishes producer pacing, rate limits, admission rejection, priority shedding and concurrency | taught | Q2–Q4 and EX-1 apply queue and capacity decisions. The Primer topic is covered; the Academy-added retry feedback loop needs P1. |

Academy additions include boundary-consistent Little's law, a finite burst, user-visible completion cohort and retry control. The instruction identifies the full burst cohort, initial-arrival clock, full deadline observation, failures/rejections/late originals and target, so admitted-only latency is not confused with user success. LO1 is taught and assessed by Q1–Q3 and EX-1; LO2 is taught and assessed by Q4–Q6 and EX-1, subject to P1 and P2. The illustrative 95% target is tied to its cohort and deadline rather than presented as an operational measurement over an unspecified population.

## Findings

**M07-L02-P1 — Major, open — overload feedback is named without tracing its causal loop.** Location: lesson “Keep retries inside the budget,” especially “A retry consumes the same worker and downstream budgets as fresh work” and “On overload, lower retry and admission pressure quickly.” The approved outline explicitly requires overload feedback, but the lesson jumps from retry costs to a control instruction without showing how overloaded service delays or failures provoke retries, those retries add demand to the same constrained capacity, and the added demand further delays original work. Learners can repeat a mitigation without understanding when it interrupts the feedback. Add a concise causal trace in the burst context, identifying the shared bottleneck, the retry trigger and why bounded, deadline-aware retries and reduced admission break or limit the loop.

**M07-L02-P2 — Major, open — EX-1's full-credit retry requirement is not requested.** Location: assessment EX-1 and “Capacity and retry decision” rubric. The prompt asks learners to defend an admission or capacity change and explain why jitter alone cannot meet the target; full credit additionally requires bounding retries by rate and deadline. An answer that explains jitter spreads load without adding capacity can satisfy the stated request without proposing either bound, yet lose points for an unstated task. Ask explicitly for a retry policy with rate and deadline constraints, or adjust the criterion to assess the explanation actually requested. Preserve acceptance of equivalent feasible designs.

## Pedagogical assessment and sequence

The fixed-rate worked scenario connects wait budget, queue cap, rejection, drain and the original-job outcome; the companion varies the rates and asks for a defensible change. Six checks include explanations, the assessment is separate and contains a points rubric and outcome map, and no quiz is embedded in the lesson. The lesson declares the earlier queue and capacity prerequisites and sends queue ownership back to M07-L01. The fluid model is appropriately qualified and contrasts mean wait with deadline guarantees. No material introductory filler or missing assigned Primer topic was found. P1 concerns the planned Academy-added causal mechanism; P2 concerns fair grading of the practical exercise.

## Verdict

**revise** — M07-L02-P1 and M07-L02-P2 are open major findings. This review is not technical, source-rights, human, or publication approval.

## Targeted revision 1 re-review — `adfb8ea`

- **M07-L02-P1 — Major, resolved.** “Keep retries inside the budget” now traces overload lengthening queue waits, client timeouts producing retries, and those retries adding demand to the same bottleneck and extending waits further. It identifies bounded admission and deadline-aware retry budgets as controls and describes jitter's distinct role in spreading remaining attempts. The adjacent instruction preserves the original identity and deadline when acceptance is uncertain.
- **M07-L02-P2 — Major, resolved.** EX-1 now explicitly asks for a retry policy with rate and deadline constraints as well as the jitter explanation; its capacity-and-retry criterion assesses those requested decisions. The lesson teaches separate retry and dispatch limits, estimated end-to-end time and the unchanged deadline. Equivalent feasible alternatives and partial credit remain expressly accepted.

The revised numerical example and EX-1 specify busy service slots, no retries or accepted execution failures for the trace, one outcome per original and a full deadline observation. The lesson distinguishes a retry after definite rejection from resolving uncertain acceptance; the companion's example and rubric retain that distinction. The mapped outcomes, separate assessment and M07-L01/M01-L02 prerequisite sequence remain coherent in the targeted scope. The assigned PR-H141 back-pressure coverage remains taught.

## Latest verdict

**ready-for-human-review** — P1 and P2 are resolved in the assigned pedagogy and coverage scope. This review is not technical, source-rights, human, or publication approval.
