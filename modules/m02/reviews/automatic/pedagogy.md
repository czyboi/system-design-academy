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
