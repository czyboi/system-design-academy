# M10-L02 — independent pedagogy and curriculum coverage review

Initial Stage A. Scope: M10-L02 only; middle/senior engineers; English. Reviewed canonical lesson, assessment, evidence, task spec/state/worklog, approved `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L02, assigned `coverage.csv` rows and source inventory. Source: [System Design Primer Twitter timeline and search](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/twitter/README.md) at pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`; inspected actual sections, nested design bullets and API/data examples. The case directory has no separate executable code file. Also inspected [Primer root prompts](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1664). Shared additional talking points H017–H023 are assigned to other lessons by the approved coverage map, outside this lesson review.

## Coverage matrix

Teaching locations are in `modules/m10/lessons/M10-L02.md`; checks and EX-1 are in `modules/m10/assessments/M10-L02.md`. IDs in a grouped row each receive the stated disposition.

| Assigned source topics and locator | Outcome and actual instructional evidence | Disposition; assessment and rationale |
| --- | --- | --- |
| H002, H003, H004, H006, H007, H008: scope, use cases, assumptions and usage, Twitter README L7–91 | LO1/LO2; State product and workload defines author/home timelines, media, 100k daily posts, 20M entries/day, 231/s and tail skew | taught; Q4 and EX-1. Synthetic numbers replace dated source assumptions; feed and publish contracts make intended outcome observable. |
| H009, H010, H011: architecture and publication, L92–155 | LO1; Begin with durable author posts and Compose: authenticated canonical write and durable outbox, graph lookup, async inbox, object media, downstream notifications | taught; Q1–Q3 and EX-1. Concrete durability boundary and retry identity replace source's illustrative API payload. |
| H012: home timeline, L156–190 | LO1/LO2; Compose and Cache/search: push/pull merge, eligibility and batched post/author/media hydration | taught; Q3, Q5 and EX-1. ID-based materialization and hydration are explained. |
| H013: author timeline, L191–198 | LO1; Begin and Walk two authors: indexed author read is independent of follower inbox delivery | taught; Q2 and EX-1. |
| H014: keyword search, L199–221 | LO1/LO2; Cache/search: independent event-fed projection and source cut, indexing lag; mechanics delegated to M08-L03 | merged; EX-1. Explicit approved ownership avoids duplicating tokenization, scatter/gather and ranking. |
| H015: scaling, L222–281 | LO1/LO2; Compose, Walk, Make ordering and Failures: celebrity pull, ordinary push, reply ordering, current visibility, bounded inbox, inactive rebuild, stable cursors, hydration and measured trade-offs | taught; Q4–Q6 and EX-1. Time-window retention and rebuild decisions replace source's example-specific limits. |
| PR-PROMPT-11, PR-PROMPT-12: feed and timeline prompts, root README L1664–65 | LO1/LO2; State, Compose and Walk explain distinct products and two-viewer trace | merged; Q2, Q4–Q5, EX-1. Source is a design prompt, not an independent vendor implementation requirement. |

No material assigned source-topic omission identified. Lesson coverage is explanatory rather than inferred from headings, references or companion answers.

## Lesson-first comprehension and outcome alignment

Before reading the companion answers, the lesson supports: authenticate and commit canonical post plus durable dispatch intent → choose ordinary push or celebrity pull according to follower skew and capacity → merge bounded inbox and followed-author candidates → hydrate in batches and apply current visibility/order → recover duplicate or delayed delivery while preserving canonical author timeline. Ada/Zee and Ben/Cara show how delay changes the home view while the author view remains available. Reply parent relation, snapshot cursor, privacy changes and inactive rebuild have explicit failure conditions. The text explains search as a separate lagging projection, with retrieval mechanics owned by M08-L03. No central causal gap identified in this teaching path.

| Outcome action | Teaching evidence | Assessment evidence |
| --- | --- | --- |
| LO1 trace/model publication, author and home paths, delivery, media/hydration and recovery | Begin; Compose; Walk; Cache/search | Q1–Q3 and EX-1 ask for commit/outbox, fan-out, reads, merge and hydration. |
| LO2 choose and defend fan-out strategy against workload, freshness, privacy, ordering and budgets | State; Compose; Make ordering; Failures | Q4–Q6 and EX-1 ask for estimates, skew, threshold, eligibility and ordering; P-1 grading weakness resolved in round 1. |

Six explained checks and a separate practical exercise are present. The lesson suits the declared audience and does not rely on answer-key rescue. M07-L03 supports the queue boundary; M08-L03 is the approved search owner, and its accepted draft is a read-only input. No length or diagram quota applied.

## Findings

P-1 — **major, resolved in round 1** (initial finding) — `modules/m10/assessments/M10-L02.md`, EX-1 Task, Reference design item 6 and rubric “Search/ops and user SLO”. The lesson's “Failures, choices and observable success” specifies at least 99% of all valid original five-minute ingress opens must reach the managed client within 800 ms with an authorized correct page and eligible routine posts committed at least ten seconds before ingress in rank range. EX-1 asks learners to define an SLI, while the reference omits the 99% threshold and the rubric requires only an original-operation denominator. No cohort outcome counts or decision are required. Thus an answer can receive full credit without evaluating the taught target, or by presenting fast admission-only latency alongside a denominator without grading whether useful pages were delivered. This leaves the central LO2 decision insufficiently assessed.

**Fix:** Supply a five-minute cohort of unique original opens with exclusive counts for timely correct/fresh pages, stale or wrong pages, late responses and rejected/failed/unknown opens; require the success fraction and pass/fail decision against 99%. In reference and rubric require all originals once, first ingress through confirmed managed-client delivery, 800 ms deadline, ten-second eligible routine-post freshness and authorization/correctness, with fast shedding excluded from success. Keep admitted-only latency separate and accept multiple viable fan-out architectures. Approved basis: `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L02 LO2 and trade-offs, and lesson “Failures, choices and observable success”.

P-2 — **minor, resolved in round 1** (initial finding) — `modules/m10/assessments/M10-L02.md`, EX-1 Scenario and Reference design item 3. The scenario says “A user” unfollows Ada, but the reference asserts Ben did so. Since Cara also follows Ada, the learner cannot determine whose subsequent page must filter Ada without adopting an unstated assumption; the core eligibility mechanism remains answerable. Specify Ben in the scenario or accept either viewer explicitly with corresponding feed consequences. Evidence: approved worked example traces two distinct viewers in `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L02.

## Initial verdict

**revise** — P-1 was open and P-2 required clarification at initial review.


## Round 1 targeted re-review

Reviewed correction handoff `99b0514`: changed lesson passages first, then Q3, Q5–Q6 and EX-1 and their immediate dependencies; not a new full lesson audit. The teaching text explains that a bounded immutable candidate view pins inbox membership, celebrity source cuts, follow/ranking versions, last exclusive key and expiry. Ben's late `a10` is outside the 10:00:03 view; a continuation cannot add it, a fresh session may, and expiry requires restart. Stable pagination and the separate ten-second freshness requirement remain distinguishable. Per-page admission after hydration is serialized with follow and post-policy updates: an earlier unfollow suppresses entries, earlier admission can finish, and authority failure closes access. Protected media follows the same rule with explicit limits for issued capabilities and already released bytes. Q3/Q5/Q6 and EX-1 exercise these taught mechanisms without relying on the reference to supply a missing causal step. The hypothetical later candidates are explicitly before applying the new follow policy; the actual response still uses current admission.

| Finding | Status | Correction verified |
| --- | --- | --- |
| P-1 | resolved | `modules/m10/assessments/M10-L02.md`, EX-1 scenario, task, reference 6 and rubric: exclusive counts 970 timely authorized correct fresh, 10 stale, 8 late, 7 rejected, 5 failed/unknown among 1,000 original valid opens in a five-minute cohort; retries preserve first ingress. Required and scored 970/1,000 = 97%, below 99%, with client receipt within 800 ms and ten-second eligible routine-post freshness; admitted-only latency remains separate. The lesson's “Failures, choices and observable success” teaches the same boundaries. Approved evidence: `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L02 LO2 and trade-offs. |
| P-2 | resolved | `modules/m10/assessments/M10-L02.md`, EX-1 scenario names Ben as the unfollowing user, matching reference 3 and its page-admission trace. Approved evidence: `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L02 worked-example plan. |

No new pedagogical blocker or major regression found in the changed passages. Both original findings are resolved. **Verdict: ready-for-human-review.** No technical, source-rights, human or publication approval is asserted.
