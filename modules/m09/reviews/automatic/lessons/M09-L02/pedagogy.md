# M09-L02 independent pedagogy and coverage review

**Historical record notice (2026-11-26):** The original report below was recovered from an untracked local checkout, not from the GitHub branch; its claimed historical review and acceptance are not independently verified. The new independent review is the separately dated section appended at the end.

Verdict: **ready-for-human-review**

## Scope

Round 0 reviews the lesson and companion for middle and senior engineers against the approved M09-L02 outline and `curriculum/revision-1/coverage.csv`. The lesson was read before the assessment solution. The source topic map is the [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. Its eight case-specific ongoing-work headings are explicitly combined in the approved coverage map. The RPO, RTO and restore drill are Academy additions.

## Coverage matrix

L refers to `modules/m09/lessons/M09-L02.md` and A to `modules/m09/assessments/M09-L02.md`. All rows are assigned to M09-L02 and support its diagnostic outcomes.

| Topic ID and locator | Disposition and teaching evidence | Assessment |
| --- | --- | --- |
| PR-ARCH-DAPPER, `README.md#L1714` | Taught. L, “Follow a request through waiting and work” explains spans, trace context, propagation, sampling, absent telemetry and cost in a timed request. | A, Q1–Q3, Q5, EX-1 |
| PR-PASTEBIN-H023, `solutions/system_design/pastebin/README.md#L329` | Merged. L, “Test a bottleneck hypothesis” covers the shared ongoing-work assignment with profiling, controlled load and repeat measurements. | A, Q5, EX-1 |
| PR-TWITTER-H023, `solutions/system_design/twitter/README.md#L330` | Merged. The approved map places this repeated ongoing-work topic in the same diagnostic sequence. | A, Q5, EX-1 |
| PR-WEB_CRAWLER-H024, `solutions/system_design/web_crawler/README.md#L350` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |
| PR-MINT-H023, `solutions/system_design/mint/README.md#L438` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |
| PR-SOCIAL_GRAPH-H020, `solutions/system_design/social_graph/README.md#L346` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |
| PR-QUERY_CACHE-H023, `solutions/system_design/query_cache/README.md#L303` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |
| PR-SALES_RANK-H021, `solutions/system_design/sales_rank/README.md#L335` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |
| PR-SCALING_AWS-H046, `solutions/system_design/scaling_aws/README.md#L400` | Merged. The shared sequence teaches profile, load-test and iterative diagnosis. | A, Q5, EX-1 |

The merged case rows have the explicit shared-topic rationale in the approved map, and the diagnostic sequence supplies a concrete workload and mechanism. L, “Check recovery against objectives” teaches the added recovery objectives with a contiguous recovery-point and validated-service timeline. No assigned topic is mention-only or assessment-only.

## Pedagogical assessment

The lesson starts with a user-visible objective over all original valid requests in an arrival window. It includes retries, rejected, failed, timed-out and late work in the denominator and follows arrivals through their deadlines. The worked trace partitions edge, API, queue, worker and database time into non-overlapping intervals, then uses queue wait to motivate a falsifiable worker hypothesis. It compares resource evidence and a controlled intervention before testing restore and recovery boundaries. The prior M01-L04 recovery concepts and M09-L01 sensitive-data constraints are applied at appropriate points.

| Outcome | Teaching evidence | Assessment evidence |
| --- | --- | --- |
| M09-L02-LO1 | L, “Measure the original request” and “Follow a request through waiting and work” establish the measurement population and locate the 760 ms queue wait within the 1,200 ms trace. | A, Q1–Q3 and EX-1 test overlapping spans, wait location, missing telemetry and trace interpretation. |
| M09-L02-LO2 | L, “Test a bottleneck hypothesis” compares metrics, profiling and controlled tests. “Check recovery against objectives” tests the contiguous point and usable-service time. | A, Q4–Q6 and EX-1 test the original-request objective, falsifiable diagnosis and both recovery objectives. |

The companion has six answered checks and a separate practical exercise with a sample, ten-point rubric and explicit outcome map. The exercise gives its arrival population, time window, failure categories and complete follow-through to each deadline. It asks for an alternative supported by refuting evidence and accepts interventions supported by the observed workload. The lesson contains the reasoning needed for the assessment, including the distinction between an enclosing span and exclusive intervals. No material sequence or audience issue was identified.

## Findings

No open blocker, major or minor findings. No required changes. Technical/source review and human publication approval are separate decisions.

## Round 1 targeted re-review

Verdict: **ready-for-human-review**. Round 0 contained no open pedagogy or coverage findings. The correction prompted by the independent technical review preserves the topic and outcome coverage above.

In L, “Measure the original request” now states the managed cohort, stable retry identity, first edge ingress and client-validated receipt. It explains the join and bounded-clock deadline decision and treats missing or inconclusive receipts as unsuccessful. The edge send is explicitly a diagnostic proxy. The revised timeline reaches client validation and remains non-overlapping. This lets the learner reproduce the 93% calculation and distinguish the user outcome from server-side telemetry.

L, “Check recovery against objectives” distinguishes the disruption cutoff used for the contiguous RPO gap from the declaration used for the RTO timer. Its example teaches both calculations and the validation boundary. A, EX-1 specifies both anchors, asks the learner to classify a sent-but-unreceived result, and grades the stable identity, client receipt, original-request denominator and distinct recovery anchors in the rubric. Q6 remains answerable from the lesson. The revised material introduces no pedagogical or coverage regression and no new finding is open.

## Independent targeted re-review — 2026-11-26

**Scope and method.** Reviewed the current teaching lesson before the assessment answer key, then checked the M09-L02 client-receipt and recovery corrections and their companion effects against the approved M09-L02 outline in `curriculum/revision-1/CURRICULUM_MASTER.md`. This independent re-review does not certify the provenance of the recovered history above. The exact subject is the original first-edge-arrival → validated-client-receipt boundary and the separately defined RPO/RTO clocks, with adjacent reasoning and rubric regressions.

**Outcome and coverage verification.** `modules/m09/lessons/M09-L02.md` “Measure the original request” explains stable caller-scoped IDs, all valid original arrivals, the five-minute arrival window, the two-second deadline, missing/inconclusive receipts, and why an edge send cannot prove a client outcome. The learner can reconstruct 930/1,000 and distinguish admitted latency from on-time user success. “Follow a request through waiting and work” shows exclusive intervals, a 760 ms queue wait and a client-validation endpoint; its total remains 1,200 ms. “Check recovery against objectives” makes the cutoff and declaration separate even when coincident, traces the four-minute contiguous recovery gap and the 17-minute validation time, and uses 24 minutes as a failing alternative. These changes preserve the taught tracing/diagnosis sequence and the Academy-added recovery outline; the assessment's EX-1 and Q4–Q6 use the same taught boundaries. EX-1 grades the full original population, stable identity, receipt and separate recovery anchors; its supplied 920/1,000, seven-minute gap and 18-minute restoration interval are consistent. The conceptual lesson does not depend on its answer key.

| ID | Severity | Status | Location | Evidence and disposition |
| --- | --- | --- | --- | --- |
| M09-L02-PED-R1-01 | note | resolved | Lesson “Measure the original request” and “Check recovery against objectives”; assessment EX-1 and Q6 | Targeted correction and companion impact verified as described above; no new pedagogical or coverage gap found. Approved outline: `curriculum/revision-1/CURRICULUM_MASTER.md`, M09-L02. |

**Verdict:** `ready-for-human-review`. This is a pedagogy/coverage determination for the targeted correction; factual and provenance QA and human approval remain separate.

## Round 2 targeted re-review — 2026-11-26

Reviewed correction commit `c21e9f8`: the lesson's Dapper passage retains the explanation of trace propagation, sampled and missing spans, and telemetry cost; the change adds a second full-text route and publication record. The neighboring paragraph still distinguishes job correlation, metrics and logs. No assessment item or learning outcome changed, and Q3/EX-1 remain answerable from the lesson. The adjusted evidence ledger supports access to the existing explanation without changing the teaching sequence.

| ID | Status | Verification and evidence |
| --- | --- | --- |
| M09-L02-PED-R1-01 | resolved | The original-receipt and recovery corrections remain intact; the source-route update does not alter them. `curriculum/revision-1/CURRICULUM_MASTER.md` M09-L02, teaching sequence items 2–4. |

Verdict: `ready-for-human-review`. This is targeted pedagogy/coverage only; independently verifying source availability and factual claims remains the technical reviewer's responsibility.
