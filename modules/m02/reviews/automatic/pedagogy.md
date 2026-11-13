# M02 module synthesis pedagogy and coverage review

Round 0, 2026-11-12. Reviewed the integrated brief, solution, decision summary and module evidence against the [approved M02 synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan), [coverage matrix](../../../../curriculum/revision-1/coverage.csv), and the accepted per-lesson pedagogy and coverage reports for M02-L01–L04. The review checks synthesis, sequencing and the module maps. It reuses the completed lesson reviews for detailed topic and assessment judgments.

## Finding

| ID | Severity | Status | Location and impact | Targeted correction |
| --- | --- | --- | --- | --- |
| M02-P1 | major | open | `modules/m02/integrated/outcome-portfolio.json`, M02-S1 `teaching`, points to `M02-S1` in `modules/m02/integrated/brief.md`. That section restates the outcome and links to the four lessons, but it does not itself teach the linked DNS-to-origin trace or the proxy/CDN decisions. A reader following the portfolio cannot find the synthesis instruction at the recorded location. | Add a concise explanatory connection under the recorded `M02-S1` heading, showing how DNS selection, edge hit/miss, origin ingress and the L4/L7 and CDN choices compose. Cite the existing lesson sections for their mechanisms. Preserve the exercise's scenario-specific calculations and decisions, and retain the exact S1 assessment subset. Alternatively, update the portfolio to point to actual instructional sections that jointly teach this connection. [Approved M02 synthesis outline](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan) |

## Synthesis and assessment

The image-catalogue brief asks learners to apply DNS cache expiry, protocol and TLS boundaries, path-based routing, cache variants, privacy, and origin-failure behavior. The reference solution traces a hit and miss through the request path, provides numerical warm and cold origin-demand estimates, and specifies conditions behind request coalescing. The rubric awards separate credit for DNS, request path, capacity/freshness and verification, and accepts other designs that meet the constraints. The assessment explicitly measures M02-S1 using the approved M02-L01-LO1, M02-L03-LO2 and M02-L04-LO2 subset.

The decision table states trigger, option, mechanism, benefit, cost, failure signal, when to avoid and a lesson reference. The lessons progress from DNS through transport and ingress to CDN cache control. The integrated private response and stale-public-response choices follow the accepted lesson boundaries.

## Coverage and outcome reconciliation

The module coverage file contains the 39 assigned M02 topic IDs, each with a canonical lesson path and an existing instructional heading. The accepted lesson reports cover their actual explanations. The outcome portfolio records all eight lesson outcomes and M02-S1. The lesson entries match the current companion teaching-heading lists and assessment item IDs, including the corrected M02-L02-LO2 UDP teaching section. The coverage rows locate teaching; their `mapped` values are not a depth verdict.

M02-P1 concerns the accuracy of the separate synthesis teaching locator. The solution demonstrates a useful complete example, but the portfolio currently identifies the brief's outcome-only section as the teaching evidence.

**Verdict: revise.** M02-P1 requires a targeted synthesis or locator correction before this review can be clear.

## Round 1 targeted re-review

Reviewed the integration correction at `82df90a`. The M02-S1 portfolio entry now names the reference solution's `DNS, connections and routing` and `Cache behavior and origin capacity` sections. Those sections walk through the complete request path and explain the proxy, cache, freshness and failure choices using the accepted lesson mechanisms. The entry continues to identify M02-EX1 and the approved M02-L01-LO1, M02-L03-LO2 and M02-L04-LO2 synthesis subset.

The brief now explicitly states that uncoalesced viewer-edge misses reach the origin directly, with no intermediate cache hits, extra retries or other origin traffic. The solution connects this condition to the origin-demand calculation and identifies upstream cache hits and retries as reasons to measure the real origin boundary. This makes the exercise's quantitative assumptions visible to learners.

| Finding | Status | Supporting curriculum evidence |
| --- | --- | --- |
| M02-P1 | resolved | curriculum/revision-1/CURRICULUM_MASTER.md |

**Round 1 verdict: ready-for-human-review.** The updated synthesis teaching locator and exercise assumptions address the findings.

## Human-feedback scoped re-review — 2026-11-13

Reviewed the integration changes from `e805261` through `31b2eb0` after issue #64 feedback, using the prior coverage and sequence findings. Brief item 3 now solicits the no-collapse, ideal and four-domain comparisons and asks about upstream caches, nonoverlap and retries. The solution's modeled rates are 200 warm, 2,160 cold, 240 ideal and 480 split-domain fetches/s: 160 warm misses plus 80 cold fetches in the ideal case or 320 across four independent domains. The capacity assumptions are explicit. Item 4 asks for a peak cold-start test at the origin limit and reporting of shed traffic; the verification criterion scores that evidence. The separate capacity criterion and 2/1/0 scale permit partial credit, while the freshness and privacy criterion remains independently assessed. The approved synthesis scope and portfolio assessment subset remain unchanged.

No new open findings in this scoped review. **Verdict: ready-for-human-review.** This is a pedagogy and assigned-coverage verdict, not human or technical approval.

## Publication-readiness synthesis review at `0dcef2a`, 2026-11-13

Reviewed the current integrated brief, reference solution/rubric, decision summary, coverage ledger and outcome portfolio against the [approved M02 synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan), integration Story and task specification. Reused the accepted M02-L01–L04 pedagogy/coverage reports and their ready lesson cycles, including the targeted L02 `954dba2` and L04 `54b7566` re-reviews; did not repeat their lesson audits. Audience: self-studying middle/senior engineers. Matched reminders supplied: explicit SLO cohorts/windows, teach and assess each action, and capacity/trade-off/verification.

### Coverage and connections

The accepted lesson ledgers cover the assigned pinned Primer DNS, load-balancing/proxy, transport and CDN rows at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. The synthesis uses those accepted dispositions, not an independent second audit. The portfolio retains all eight lesson outcomes in separate companions and identifies the approved M02-S1 subset (L01-LO1, L03-LO2, L04-LO2) and M02-EX1. The reference path connects resolver caching, edge hit/miss, origin ingress and L4/L7 routing; the decision table links all four lessons and includes the planned decision fields. Prior M02-P1 remains resolved at the portfolio's reference-solution teaching locator. No new module-wide coverage or sequence gap is identified.

### Pedagogy and assessment findings

| ID | Severity | Status | Location, evidence and learner impact | Targeted correction |
| --- | --- | --- | --- | --- |
| M02-P2 | major | open | [Brief, M02-EX1 items 3–4](../../integrated/brief.md#m02-ex1) asks the learner to defend a capacity policy and design an SLO test, but does not explicitly ask them to reason whether their proposed policy can meet the 9,900/10,000 individual deadlines or to identify and mitigate a failure when it cannot. [Self-evaluation, Origin capacity](../../integrated/solution-rubric.md#self-evaluation) demands a policy “without violating” the success budget, while the only partial-credit instruction is the generic 2/1/0 scale. The [reference capacity discussion](../../integrated/solution-rubric.md#cache-behavior-and-origin-capacity) correctly says the 240/480 fetch estimates do not establish latency, but gives no conditional end-to-end outcome or scored failure example. A learner cannot reliably distinguish credit for a sound diagnosis of an infeasible or unproven design from credit for an unsupported claim that a cap and coalescing meet the objective. | Ask explicitly for a conditional viewer-success argument or identified failure and mitigation under stated realistic timing/collapse assumptions. Add a small worked passing/failing or unproven comparison that counts original requests through their own deadlines, including a late-window arrival and the 100-request failure budget, separately from the per-second origin-attempt cap. Calibrate the rubric's full and partial credit for a justified alternative, an honest failure diagnosis with mitigation, and a cap-only or unsupported success claim; do not imply the supplied fetch counts prove latency. The [approved synthesis scope](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan) and [integration specification](../../../../.academy/specs/SD-M02-INTEGRATION.json) require an assessable reference/self-evaluation and realistic user-success constraints. |

The brief correctly defines the first-second cohort, the per-request two-second deadline and failure accounting; the solution explicitly follows late-window arrivals and separates origin fetches from viewer outcomes. Its 9,900 threshold and four-domain count are useful. The finding concerns making the requested design judgment and grading of conditional outcomes reproducible, not a demand for an invented latency guarantee. Freshness/privacy, DNS, path and verification have separate rubric criteria, and alternative designs are accepted subject to the stated requirements.

**Verdict: revise.** M02-P2 remains open. This is a pedagogy and assigned-coverage synthesis verdict, not technical approval, human approval or publication authorization.

## Correction re-review at `25dc3b7`, 2026-11-13

Reviewed `0dcef2a..25dc3b7` for M02 integration, concentrating on M02-P2 and the adjacent scenario, reference and rubric. Reused the accepted lesson-cycle and coverage evidence above; this is not a second lesson audit.

| ID | Severity | Status | Re-review evidence |
| --- | --- | --- | --- |
| M02-P2 | major | resolved | [M02-EX1 items 3–4](../../integrated/brief.md#m02-ex1) now request an explicit conditional judgment on both limits, a diagnosis and mitigation when a result fails or is unproven, and a test joining retries to original requests and following each deadline. [Conditional capacity and viewer outcomes](../../integrated/solution-rubric.md#conditional-capacity-and-viewer-outcomes) models at most 520 origin-entry attempts across replay and drain, then separately assumes end-to-end timing for a passing viewer result; it traces a +0.999 s arrival to its +2.999 s deadline. Its immediate-shed contrast reaches only 8,840/10,000 despite meeting the attempt cap and identifies mitigation. The reference labels assumptions and requires measurement, and distinguishes the 100- and 101-failure cases. [Self-evaluation](../../integrated/solution-rubric.md#self-evaluation) scores origin capacity and viewer success independently, awards partial credit for a sound failure or uncertainty diagnosis with mitigation, denies viewer-success credit for unsupported or cap-only claims, and accepts justified alternatives. The [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan) and [integration specification](../../../../.academy/specs/SD-M02-INTEGRATION.json) establish the exercise and user-success assessment scope. |

The revised brief defines the cohort and measurement at the client and sets the origin-entry boundary for every rolling second through drain. Retry, validation, modeled prefill and background attempts count at that boundary; pre-boundary failures are separately reported. The example's 520 total is a conservative rolling-window bound, not a latency proof. The prompt, reference and scoring now support independent reasoning about both constraints and follow late-window arrivals. No new material pedagogy or module-coverage finding was identified in the changed scope. M02-P1 remains resolved.

**Verdict: ready-for-human-review.** This is a targeted pedagogy and assigned-coverage synthesis verdict, not technical approval, human approval or publication authorization.

## Round 2 targeted re-review at `b14257a`, 2026-11-13

Reviewed the M02 integration change in `25dc3b7..b14257a` and the adjacent example and self-evaluation. The [conditional capacity example](../../integrated/solution-rubric.md#conditional-capacity-and-viewer-outcomes) now bounds the 40 additional retry or validation attempts across the entire replay and drain, making the stated maximum of 520 total origin-entry attempts explicit for that whole period. Its separately assumed viewer timing, late-arrival trace, failing shed example and measurement requirement remain intact. The independent capacity and viewer-success criteria, partial-credit rule and acceptance of justified alternatives remain unchanged.

| ID | Severity | Status | Evidence |
| --- | --- | --- | --- |
| M02-P2 | major | resolved | The corrected [conditional example](../../integrated/solution-rubric.md#conditional-capacity-and-viewer-outcomes) and unchanged [self-evaluation](../../integrated/solution-rubric.md#self-evaluation) retain the assessment required by the [approved synthesis plan](../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m02-integrated-package-plan) and [integration specification](../../../../.academy/specs/SD-M02-INTEGRATION.json). No new pedagogy regression is identified in the changed scope. |

**Verdict: ready-for-human-review.** This is a targeted pedagogy and assigned-coverage synthesis verdict, not technical approval, human approval or publication authorization.
