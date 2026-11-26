# M09-L02 technical and provenance review

> Recovery provenance (2026-11-26): the historical sections below were recovered verbatim from a prior untracked local artifact. They were absent from the GitHub branch and are retained as historical claims, not accepted QA evidence. The new independent verification at the end is the operative decision.

Round 0 reviewed the lesson, companion and evidence at draft commit `0335dc8` on 2026-11-15.

## Technical findings

| ID | Severity | Status | Location | Finding and suggested fix | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M09-L02-T1 | major | open | `modules/m09/lessons/M09-L02.md:21–23,27,37`, success endpoint, outcome reconciliation and timeline. `modules/m09/assessments/M09-L02.md:18,64,72`, EX-1 prompt, sample and rubric. | The success contract ends when the caller receives the correct report, while the implementation reconciles terminal outcomes at the edge. An edge can record a completed response after the caller times out or when the response never arrives. Teach one observable contract. To keep the existing user outcome, assume instrumented clients or the controlled load harness, join validated client receipt to the first edge arrival by the stable original ID, state the clock or uncertainty rule for the cross-boundary deadline, and explicitly count missing receipt evidence as unsuccessful or unknown under a stipulated policy that retains all eligible originals. Distinguish the edge span from the client receipt and include a server-completed/client-failed path. Apply the same classification to EX-1 and provide or require its measurement evidence. The numerical totals can remain as illustrative client-reconciled counts. | [Google SRE, Service Level Objectives, Indicators in Practice](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice), [Google SRE Workbook, Implementing SLOs, Moving from SLI Specification to SLI Implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation) |
| M09-L02-T2 | minor | open | `modules/m09/lessons/M09-L02.md:55–57,59`, recovery objectives and drill. `modules/m09/assessments/M09-L02.md:22,58–60,68,74`, EX-1 and Q6. | The examples use 12:00 both as the point before which data must be recoverable and as the declaration that starts the scenario's restoration timer. The drill states only the declaration time and EX-1 grammatically attaches declaration-to-validation measurement to both objectives. State the disruption or defined data-loss cutoff and the declaration separately. They can coincide at 12:00 in the drills, or differ when detection lags. Calculate RPO from cutoff to the contiguous recoverable committed point and RTO, under the stated scenario convention, from declaration to validated service. Record the distinct events in the answer and rubric. The gap is a recovery window rather than the volume or count of lost commits. | [NIST SP 800-34 Rev. 1 §3.2.1, RPO and RTO](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=31) |

The lesson's exclusive intervals add to 1,200 ms and the EX-1 intervals add to 1,100 ms. Queue waits are respectively 760 and 700 ms. The 80 and 100 ms database calls include network time and neither diagnoses database execution independently. The declared synchronized timestamps bound the worked subtraction. Both original-denominator arithmetic examples are correct given their input classifications. The controlled workload holds offered traffic, mix, dataset and starting state fixed and compares evidence before and after one intervention. Worker saturation and an individual trace support a hypothesis about the cause. The Dapper and W3C text correctly distinguishes historical trace trees, propagated HTTP context and sampled span retention. [Google SRE, Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), [Brendan Gregg, Linux USE metrics](https://www.brendangregg.com/USEmethod/use-linux.html), [Dapper §§2.1–2.4, authors' report](https://zhjwpku.com/assets/201810/dapper.pdf#page=3), [W3C Trace Context §3.2.2.5.1](https://www.w3.org/TR/trace-context/#sampled-flag).

## Provenance findings

| ID | Severity | Status | Location | Finding and suggested fix | Primary evidence |
| --- | --- | --- | --- | --- | --- |
| M09-L02-P1 | minor | open | `modules/m09/lessons/M09-L02.md:43,59`, Dapper and drill citations. `modules/m09/evidence/M09-L02.md:8,11`, C2 and C5. | The Dapper archive PDF redirected to an inaccessible address during this review. The authors' report was independently verified from the accessible mirror, and Google Research's official bibliography confirms its identity. Retain the bibliographic reference and give readers a working full-text route. Correct the NIST drill citation to §3.5.1 for testing and §4.4 for reconstitution and validation. §3.6 covers plan maintenance. | [Google Research, Dapper publication record](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/), [Dapper §§2.1–2.4, authors' report](https://zhjwpku.com/assets/201810/dapper.pdf#page=3), [NIST SP 800-34 Rev. 1 §3.5.1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=41) |

## Source and asset ledger

| Material | Role and use |
| --- | --- |
| Donne Martin, System Design Primer at `ae9bbd7` | Topic map for the ongoing diagnosis examples and Dapper. The lesson supplies an original report service, timeline, outcome counts and recovery drill. [Pinned topic map](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Google SRE, USE method, Google technical report, W3C Recommendation and NIST SP 800-34 Rev. 1 | Factual references for diagnostics, trace propagation and recovery planning. The exercise uses assumed data and makes no measured benchmark, regulatory or current product guarantee. The package imports no third-party assets. |

## Verdict

`revise`

## Round 1 targeted re-review

Reviewed the corrected lesson, companion and evidence at draft commit `6ea945f` on 2026-11-15.

| ID | Status | Verification | Primary evidence |
| --- | --- | --- | --- |
| M09-L02-T1 | resolved | The managed test cohort retains every valid original first observed at the edge in each five-minute window. Client validation is joined by the stable caller-scoped original ID across retries. The deadline uses a common clock or a bounded elapsed-time upper bound. An absent or inconclusive receipt stays in the denominator and cannot count as success. EX-1 grades the joined events and a timeout despite edge send. Evidence C6 scopes these rules to the scenario. Locations are lesson lines 21–29 and 39–40, assessment lines 18–22, 64 and 72, and evidence line 12. | [Google SRE, Service Level Objectives, Indicators in Practice](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice), [Google SRE Workbook, SLI specification to implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation) |
| M09-L02-T2 | resolved | The disruption cutoff and outage declaration are separate events. The lesson compares the contiguous recovery point to the disruption cutoff and explicitly allows declaration to occur later. Its example records a four-minute recovery gap and 17 minutes to usable validation. The exercise reports a seven-minute gap and 18 minutes from declaration, with distinct anchors in the prompt, answer and rubric. Q6 expects a four-minute gap and 24 minutes to validated service. Locations are lesson lines 58–62, assessment lines 22, 58–60, 68 and 74, and evidence line 11. | [NIST SP 800-34 Rev. 1 §3.2.1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=31) |
| M09-L02-P1 | resolved | The replacement MIT-hosted PDF returned HTTPS `200` with content type `application/pdf`. Its original report text supports the trace-tree, common-library context and sampling claims in §§2.1–2.4. The NIST references now point to §3.5.1 for recovery testing and §4.4 for reconstitution and validation. Locations are lesson lines 46 and 62 and evidence lines 8 and 11. | [Dapper, MIT-hosted original report](https://people.csail.mit.edu/matei/courses/2015/6.S897/readings/dapper.pdf), [NIST §3.5.1, Testing](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=41), [NIST §4.4, Reconstitution Phase](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf#page=55) |

The added receipt intervals preserve the full 1,200 ms lesson and 1,100 ms exercise traces. Queue waits remain 760 and 700 ms, and original on-time proportions remain 93% and 92%. Sampled spans remain diagnostic and the controlled-load comparison retains the original request metrics. The scoped changes introduce no third-party assets.

### Verdict

`ready-for-human-review`


## 2026-11-26 independent continuation of reserved round 1

Reviewed the current lesson, companion and evidence after successful scoped draft handoff `f921f8c`. This reviewer did not author their corrections. Only T1, T2, P1 and their nearby effects were rechecked; recovered claims of earlier successful HTTP responses were not adopted as evidence.

| ID | Current status | Fresh verification and location | Exact evidence |
| --- | --- | --- | --- |
| M09-L02-T1 | resolved | Lesson “Measure the original request”, lines 21–25, defines the managed cohort, original ID, client receipt, uncertainty upper bound and missing-receipt policy. The EX-1 prompt, sample and rubric preserve the client-failed/server-sent case and all original requests. The edge is explicitly a proxy. | [Google SRE, Indicators in Practice](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice); [SRE Workbook, SLI specification and implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation) |
| M09-L02-T2 | resolved | Lesson lines 58–62 and companion Q6/EX-1 separately name disruption cutoff, declaration, contiguous recovered point and validated usability. The scenario-specific declaration timer is explicit. Four minutes/17 minutes, seven minutes/18 minutes and four minutes/24 minutes follow the stated clocks. | [NIST SP 800-34 Rev. 1, §§3.2.1, 3.5.1 and 4.4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) |
| M09-L02-P1 | open — minor, narrower remaining source-route issue | NIST section references are corrected. The MIT full-text URL in lesson line 46 and evidence C2 could not be opened by this review tool; this does **not** establish an HTTP 404 or that the paper is unavailable everywhere. Its historical `200` claim cannot be freshly verified. The original report was independently read through the alternative below, and its identity confirmed at Google Research. Supply the verified full-text alternative beside the official bibliography, retaining exact §§2.1–2.4 and identifying the mirror. No teaching rewrite is needed. | [Official Google Research publication record](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/); [original Dapper report, accessible mirror, §§2.1–2.4](https://zhjwpku.com/assets/201810/dapper.pdf#page=3) |

The original report verifies the scoped historical trace-tree, shared-library propagation and sampling discussion. The W3C [Trace Context §§3.2.2 and 4](https://www.w3.org/TR/trace-context/#traceparent-header) separately supports HTTP context and sampled flags; it does not promise retained spans. The exclusive trace intervals still total 1,200 ms and 1,100 ms, with queue waits of 760 ms and 700 ms. The original-request proportions remain 93% and 92%. No executable code, load test or recovery drill was run by this reviewer; numerical data remain synthetic. No new factual, rights or asset issue was found in the changed material. Original examples and the prior source ledger remain applicable.

### Current verdict

`revise` — only the minor P1 source-route correction remains open. T1 and T2 are independently resolved. This is not human publication approval.


## Round 2 targeted independent re-review — 2026-11-26

Reviewed the correction at pushed draft `c21e9f8`, limited to P1 and its lesson/evidence links and nearby companion effects. Earlier recovered history is retained above; this is the current decision.

| ID | Status | Verified correction | Exact evidence |
| --- | --- | --- | --- |
| M09-L02-P1 | resolved | Lesson line 46 and evidence C2 now supply the identified original-report mirror and official bibliography. Both were independently reopened. The MIT route is retained as historical; its earlier HTTP-success assertion is not required for the present verdict. Corrected NIST section references remain intact. | [Dapper original report mirror, §§2.1–2.4](https://zhjwpku.com/assets/201810/dapper.pdf#page=3); [Google Research bibliography](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/); [NIST §§3.5.1 and 4.4](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) |
| M09-L02-T1 | resolved, preserved | The source-link correction does not change the original-operation receipt join, clock-bound deadline or failure classification. | [Google SRE SLI implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation) |
| M09-L02-T2 | resolved, preserved | The disruption cutoff, declaration, contiguous recovery point and validated-usability boundaries are unchanged. | [NIST §3.2.1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf) |

The companion and trace arithmetic are unchanged; no source or technical regression was found in the correction. No code, drill or load test was executed. No open finding remains.

### Final verdict

`ready-for-human-review`
