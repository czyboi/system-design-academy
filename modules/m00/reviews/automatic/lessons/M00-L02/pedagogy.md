# M00-L02 pedagogy and curriculum coverage review

Round 0 reviews the lesson, assessment and evidence for middle/senior backend engineers against the approved [M00-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l02--from-requirements-to-a-defensible-design) and [coverage matrix](../../../../../../curriculum/revision-1/coverage.csv). The assigned topic map is Donne Martin's System Design Primer at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`, [README lines 218–269](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L218-L269). The pinned local source was inspected. No relevant prevention reminders were supplied. Prior review and task feedback were considered.

## Coverage

| Assigned topic and source location | Disposition and actual teaching | Assessment evidence |
|---|---|---|
| PR-H011, approach to a design interview, README L218 | **Taught**, [Time-bounded design review](../../../../lessons/M00-L02.md#time-bounded-design-review). The learner sequences scope, paths, a risky decision, alternatives, costs and evidence in a timebox. | Q6 asks what the review communicates. |
| PR-H012, use cases, constraints and assumptions, L226 | **Taught**, [Frame the design](../../../../lessons/M00-L02.md#frame-the-design). Actors and operations are tied to a revocation constraint, traffic assumption and non-goals. | Q1 and EX-1 apply framing. |
| PR-H013, high-level design, L239 | **Taught**, [Draw the paths and choose a deep dive](../../../../lessons/M00-L02.md#draw-the-paths-and-choose-a-deep-dive). Client, service and store participate in create, read and revoke paths. | Q3 and EX-1 trace roles and flows. |
| PR-H014, core components, L246 | **Taught**, Draw the paths and choose a deep dive. The revocation constraint selects a status-store deep dive and the stated status contract explains the decision for a later read. The source's URL-shortener algorithms and data structures are examples, while the approved scope calls for a targeted core-component deep dive. | Q2 and EX-1 use the order of revoke and read. |
| PR-H015, scale design, L259 | **Taught**, [Estimate, measure, and revise](../../../../lessons/M00-L02.md#estimate-measure-and-revise) and [Worked example](../../../../lessons/M00-L02.md#worked-example). A workload drives measurement, profiling and a conditional pool change followed by a repeat test. The two-host alternative exposes host failure and shared dependencies. | Q5 and EX-1 require a test and revision decision. |

The source's example technologies are used as an open set of possible bottleneck responses. This lesson teaches the approved decision method and defers detailed implementations to their assigned later lessons. No assigned topic is omitted or assessment-only.

## Learning and assessment

The lesson begins with a revocation condition, identifies the relevant client, service and store interactions, and shows why an authoritative status check must observe the completed revocation. It uses the host-failure requirement to compare the original candidate with two application hosts, then shows the evidence needed before selecting the latter. The assumed store contract, host-failure limits and costs are present in the lesson, allowing the learner to reconstruct both outcomes without the answer key. The test example connects a signal to profiling and a conditional change while preserving the uncertainty of the diagnosis.

LO1 is taught through the framing and path sections and assessed by Q1–Q3. LO2 is taught through the worked comparison, test process and review communication, and assessed by Q4–Q6 and EX-1. The separate assessment has six explained checks, one exercise, a sample response and a five-point rubric accepting other justified designs. The exercise additionally assesses the LO1 operation paths.

## Findings

- **M00-L02-P1 · minor · open · outcome traceability** — The [companion front matter](../../../../assessments/M00-L02.md) maps LO2 only to Worked example, although Q6 is taught in Time-bounded design review. EX-1 also asks for create/read/revoke paths and its rubric awards a point for them, but the LO1 item list stops at Q1–Q3. The items remain answerable, so this does not prevent learning. Add the relevant lesson heading to the LO2 trace and EX-1 to LO1, keeping the front matter, narrative mapping if present, and module portfolio aligned. Evidence is the [approved outcome and assessment plan](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l02--from-requirements-to-a-defensible-design).

No blocker or major coverage, sequencing, assessment or language gap was found. The assessment calls for a representative load-test plan and criteria, and does not claim numerical service-level objectives that would require a fixed request denominator or window.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and assigned-topic coverage.

## Round 1 targeted re-review

| Finding | Status | Evidence |
|---|---|---|
| M00-L02-P1 | **Resolved in lesson package** | [Companion front matter and outcome map](../../../../assessments/M00-L02.md#outcome-map) now associate EX-1 with LO1 and identify both the measurement and time-bounded review teaching sections for LO2. These references match the exercise and Q6. The approved [M00-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m00-l02--from-requirements-to-a-defensible-design) defines the outcomes. The module outcome portfolio is pending its separately assigned integration reconciliation. |

The revised [worked example](../../../../lessons/M00-L02.md#worked-example) shows how a host-loss target uses a ten-minute window, all original valid client requests as its denominator, a full-body deadline and explicit failed, rejected, timed-out and late outcomes. The example distinguishes successful-read latency and survivor capacity from that success target and excludes revoked-link probes from the valid-read population. The [exercise and rubric](../../../../assessments/M00-L02.md#practical-exercise) ask for and evaluate those taught decisions, accepting justified targets. The revised status-check and cache path includes the order of revocation and a concrete follow-up request. No new material pedagogy or coverage gap was found in the changed passages.

**Round 1 verdict: ready-for-human-review.** This verdict covers the targeted pedagogy and coverage re-review.
