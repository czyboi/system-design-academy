# M03 module synthesis pedagogy and coverage review

Reviewed integration handoff HEAD `9c8a3f9cf80808cd8edc818de5b46a44e40182be`, the approved [M03 curriculum and synthesis outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l03), integration specification and canonical brief, solution, decision table, coverage and outcome portfolio. Scope is module synthesis and cross-lesson connections for middle/senior engineers, reusing accepted Stage A reports rather than rescoring unchanged lessons. All three recorded lesson cycles are ready.

## Coverage, sequence and integration

The 24 topic rows in `integrated/taught-coverage.csv` have existing lesson headings as locators; their substantive dispositions are supported by the accepted Stage A coverage reports (three M03-L01, 19 M03-L02, two M03-L03). The seven portfolio records include six lesson outcomes and M03-S1. The lesson records identify actual teaching headings and assessment items consistently with the accepted individual outcome maps. The M03-S1 subset is exactly M03-L01-LO2, M03-L02-LO1 and M03-L03-LO2, and M03-EX1 is the separate synthesis assessment. Its teaching evidence needs the correction below.

The learning sequence proceeds from boundaries and ownership, through interface contracts, to discovery and bounded retries before the catalogue synthesis. The M03-L02 preview now links to the canonical M03-L03 worked example; its 40 ms failure, 20 ms backoff and 120 ms completion match the later trace. The decision table supplies all eight planned fields for each row and links to the relevant lessons. The exercise asks learners to compare boundary alternatives, trace public and internal contracts, and choose discovery and failure policies in the same workload; the reference accepts a justified modular alternative.

## Findings

- **P-M03-S1-01 — Major, open — `modules/m03/integrated/outcome-portfolio.json`, M03-S1 teaching:** The record identifies only `solution-rubric.md` as teaching. Those sections are the answer and rubric for M03-EX1, not the prior instructional evidence on which the synthesis can rely. The [approved synthesis outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-integrated-package-plan) identifies the three lesson outcomes as its taught subset; the portfolio should trace each constituent skill to the actual applicable lesson teaching sections, including the worked examples, while keeping M03-EX1 and its solution in the assessment evidence. Use the existing canonical portfolio representation or a precise supported representation that identifies those separate lesson paths and sections; do not claim all six lesson outcomes for the synthesis.
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

## Human-feedback scoped re-review — 2026-11-13

Reviewed integration changes from `e805261` through `31b2eb0` after issue #64 feedback, preserving the previous coverage, sequence and finding history. Brief item 4 now explicitly asks for peak-load failure-drill pass criteria and concurrency tests in multiple publication, edit and revocation orders. The rubric states design requirements for publication eligibility, duplicate logical work and bounded load separately from the verification evidence required for full credit. Its verification criterion names observable performance, queue, retry and limit checks, reply-loss and race tests, and accepts equivalent tests that establish the same constraints. The 2/1/0 criteria remain independent; the prior synthesis outcome subset and portfolio links remain unchanged.

No new open findings in this scoped review. **Verdict: ready-for-human-review.** This is a pedagogy and assigned-coverage verdict, not human or technical approval.

## Verification wording follow-up

Reviewed the subsequent working-tree change to the Verification row of `modules/m03/integrated/solution-rubric.md`. Specifying the drill duration and tracking every preview accepted during the drill through its two-minute deadline, including expired, failed and late jobs as misses, makes the assessed cohort and outcome measurable. The existing equivalent-tests allowance remains. No new pedagogy finding; **verdict remains ready-for-human-review**.

## PR #66 publication-readiness synthesis — 2026-11-13

Reviewed the integration at `0dcef2a`, with the accepted M03-L02 correction at `a78f38c`, the [approved M03 synthesis](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-integrated-package-plan), [integration specification](../../../../.academy/specs/SD-M03-INTEGRATION.json), portfolio, coverage ledger, decision summary and accepted Stage A reports. This is a module synthesis for middle/senior learners, not a repeat of lesson audits. No matched prevention reminders were supplied.

### Coverage and sequence

The accepted Stage A ledgers dispose of the 24 assigned pinned-Primer rows (revision `ae9bbd7b02d90b9866215de185217d33f39ab733`); the integration ledger maps them to the same three lessons. No cross-lesson coverage regression was identified. The portfolio maps M03-S1 to exactly the three approved constituent outcomes and to M03-EX1; the decision summary connects their worked mechanisms. The sequence and reference trace are coherent with the accepted lessons, including the accepted M03-L02 pending identity and recovery contract. The exercise compares deployment and discovery alternatives, and the publication-race invariant is an explicit separate design requirement rather than merely a performance result. The previous P-M03-S1-01 and P-M03-S1-02 resolutions remain supported.

### Findings

- **P-PR66-M03-1 — major, open — `integrated/brief.md`, M03-EX1 item 4; `integrated/solution-rubric.md`, Verification:** The scenario and reference require durable acceptance within one second for 99% of original valid previews, but the learner deliverable asks for preview completion without explicitly asking for an acceptance criterion. The single 2/1/0 Verification row then groups metadata success, successful-response p99, preview acceptance, preview completion and race tests; it does not say which missing or failed individual objectives prevent full credit. A learner may omit acceptance or one metadata objective yet receive a plausible partial score without a clear independent gate. Explicitly elicit preview acceptance and score each of the four user-visible objectives independently, with original-submission denominators and the successful-response p99 population; make clear that a missed threshold cannot be offset by another passing metric. Preserve the distinct publication eligibility invariant gate. Basis: [integration acceptance criterion ac-publication-readiness](../../../../.academy/specs/SD-M03-INTEGRATION.json).
- **P-PR66-M03-2 — major, open — `integrated/brief.md`, scenario and item 4; `integrated/solution-rubric.md`, Verification:** The 60-second drill identifies the submission cohort and deadlines, but neither asks the learner to define event-time boundaries and follow that cohort after the drill through the one-second and two-minute deadlines. Stopping observation at 60 seconds can omit the slow tail and inflate results or mark in-flight work prematurely. Specify arrivals during the drill as the cohort, measure each outcome from first submission, continue observation through the last member's applicable deadline, and classify unresolved or late work as misses; retain the separate stable-version load and deliberate cancellation correctness cohorts. Basis: [integration acceptance criterion ac-publication-readiness](../../../../.academy/specs/SD-M03-INTEGRATION.json).
- **P-PR66-M03-3 — major, open — `integrated/brief.md`, item 4; `integrated/solution-rubric.md`, Verification:** The modeled peak and failure drill say what to measure but do not elicit or grade an executable model/test plan: arrival pattern and capacity/service assumptions, when and for how long the worker and discovery failures occur, and how outcomes are observed. Consequently a response can repeat thresholds without demonstrating that either the modular alternative or separate renderer has been tested under comparable demand and failure. Require a reproducible modeled or actual test with stated workload and capacity assumptions, failure timing, cohort tracking and observed results or explicitly labeled projected results; grade those elements while accepting equivalent alternative designs and tests. Basis: [approved integration Story](../../../../delivery/backlog.json) and [integration specification](../../../../.academy/specs/SD-M03-INTEGRATION.json).

**Current verdict: revise.** This is a module pedagogy and assigned-coverage judgment, not technical or human publication approval.

## Targeted correction re-review at `0f2f337` — 2026-11-13

Reviewed the changed [brief](../../integrated/brief.md), [reference and rubric](../../integrated/solution-rubric.md), and adjacent decision summary against the [approved synthesis outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-integrated-package-plan) and [integration specification](../../../../.academy/specs/SD-M03-INTEGRATION.json). Stage A evidence remains accepted; this is a targeted synthesis review.

| Finding | Severity | State | Evidence and action |
| --- | --- | --- | --- |
| P-PR66-M03-1 | major | open | Brief item 4 now elicits admission, and separate rubric rows score each objective with no offset; however, the revised latency population excludes successful responses after one second, a material regression described in P-PR66-M03-4. Restore the full successful-response population while retaining independent scoring. |
| P-PR66-M03-2 | major | resolved | The brief fixes the original cohort at first submissions in [0, 60 s), follows each to its own deadline, and separates stable versions from deliberate correctness cases; the illustrative drill follows the final preview to approximately 180 s. Basis: [integration specification](../../../../.academy/specs/SD-M03-INTEGRATION.json). |
| P-PR66-M03-3 | major | resolved | Item 4 and Test plan row require reproducible arrivals, capacity/service assumptions, timed faults and results for alternatives on the same schedule. The illustrative procedure specifies arrival rates, worker and queue assumptions, worker loss and discovery outage timings, distinguishes operational from correctness cases, and labels projections and unverified results. Basis: [integration Story](../../../../delivery/backlog.json). |

- **P-PR66-M03-4 — major, open — `integrated/brief.md`, second target; `integrated/solution-rubric.md`, Metadata latency:** Both now restrict p99 to successes arriving within one second. This drops successful late responses from the original successful-response latency population; a design can pass that latency check while its omitted successful tail is slow. The separate 99% within-one-second success objective does not make the populations equivalent. Define p99 over all successful responses from the original cohort, including late successes observed in a stated bounded observation window, and separately count those late responses as misses for the one-second success target. Define treatment of unresolved responses at the observation cutoff and grade the two metrics independently. Basis: [integration specification, ac-publication-readiness](../../../../.academy/specs/SD-M03-INTEGRATION.json) and the preceding `0dcef2a` brief's successful-response target.
- **P-PR66-M03-5 — major, open — `integrated/solution-rubric.md`, Interface trace:** The correction replaced the old explicit resource/operation and stub-path full-credit requirements with identity, recovery and compatibility checks. Brief item 2 still asks for both contracts and the request/reply trace, and the [approved M03-S1 outcome](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-integrated-package-plan) expressly requires tracing the contract. A response can now receive full credit on this row without tracing the interface. Restore explicit full-credit evidence for public resource and internal operation semantics and the request/return path through the stubs, while keeping the new durability and compatibility criteria. The 2/1/0 scheme otherwise gives incomplete evidence partial credit, and the safety invariant remains a separate gate.

**Current verdict: revise.** Pedagogy and assigned module coverage only; this is not technical or human publication approval.

## Round 2 targeted re-review at `dd96223` — 2026-11-13

Reviewed the `0f2f337..dd96223` integration changes and adjacent brief, reference, test procedure and rubric against the [approved M03 integrated package plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-integrated-package-plan) and [integration specification](../../../../.academy/specs/SD-M03-INTEGRATION.json).

| Finding | Severity | State | Verified correction |
| --- | --- | --- | --- |
| P-PR66-M03-1 | major | resolved | The brief elicits durable admission and all four targets; separate rubric rows independently score each, and a passing target cannot compensate for another failure. |
| P-PR66-M03-2 | major | resolved | The original [0, 60 s) cohort, separate stable-version and correctness cases, and per-original deadline follow-up remain intact; metadata now also has an explicit observation horizon. |
| P-PR66-M03-3 | major | resolved | The comparable alternative test schedule, arrival and capacity assumptions, fault timing and distinction between measured and projected evidence remain. The test row now names caller, handler and active-render limits. |
| P-PR66-M03-4 | major | resolved | Brief, drill and latency row include successes through two seconds after each original submission, including those after one second; those late successes separately miss the one-second success objective. The rubric reports sample size and unresolved operations and treats an empty sample as unverified. |
| P-PR66-M03-5 | major | resolved | Interface trace full credit again requires public resource and internal operation semantics and request/reply through both caller and server stubs, alongside identity, recovery and compatibility. |

The adjacent corrections add authorization, current-version admission, runnable durable acceptance and receiver-limit evidence to the reference and assessment. The independent safety gate still requires publication/edit and publication/revocation orders, and the 2/1/0 scoring retains partial credit for incomplete evidence. No new pedagogical or assigned-coverage regression was identified in the changed scope.

**Current verdict: ready-for-human-review.** This is a pedagogy and assigned module coverage judgment only, not technical or human publication approval.
