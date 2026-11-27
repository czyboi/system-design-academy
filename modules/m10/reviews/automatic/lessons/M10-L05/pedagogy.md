# M10-L05 independent pedagogy and curriculum coverage review

Reviewed 2026-11-27 after scoped draft handoff `922eddd`: `modules/m10/lessons/M10-L05.md` was read before the companion answer and rubric, followed by `modules/m10/assessments/M10-L05.md`, evidence, canonical task spec/state/worklog and approved M10-L05 outline and topic matrix. The audience is experienced system-design engineers. I independently inspected the assigned [Primer social-graph case](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/social_graph/README.md) and [graph snippets](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/social_graph/social_graph_snippets.py) at pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`; reviewed the source's scope, BFS, server/lookup, snippet state and optimization bullets, not author self-review as evidence.

## Findings

| ID | Severity | Status | Location | Evidence, learner impact and precise fix |
| --- | --- | --- | --- | --- |
| M10-L05-PED-01 | major | open | `modules/m10/lessons/M10-L05.md`, “Bidirectional search changes the shape of work”; `modules/m10/assessments/M10-L05.md`, EX-1 deliverable and reference solution | The lesson says to expand coherent BFS layers and establish a minimal meeting distance and a sound lower bound, but gives no usable lower-bound calculation or termination rule. Its example stops at a meeting without showing the relevant completed frontier depths and why an unexplored alternative cannot be shorter. EX-1 explicitly asks for the termination bound; the answer just repeats that a lower-bound condition must hold. A learner cannot reconstruct the criterion to decide when to stop from the lesson, although proving bidirectional shortest-path termination is central to LO1 and its grading. Teach one correct, fully specified stopping policy (with its assumptions) by tracing the two frontier depths, best candidate path and lower bound for unseen candidates in the worked graph; show what incomplete/asynchronous layer responses do to that proof. Bring EX-1's solution/rubric into agreement; accept other correctly justified policies. Evidence: approved `curriculum/revision-1/CURRICULUM_MASTER.md`, M10-L05 teaching sequence 2 and LO1; lesson-first rule in `.agents/skills/pedagogical-review/SKILL.md`. |
| M10-L05-PED-02 | major | open | `modules/m10/lessons/M10-L05.md`, final “Choose a contract before calling the service reliable” SLO paragraph; `modules/m10/assessments/M10-L05.md`, EX-1 and rubric | The stated 99% success SLO counts a correctly justified `incomplete` as success, but the accompanying complete-layer coverage fraction has no required target. A service that returns justified incomplete responses for every request within 800 ms can meet the only numerical target; merely reporting zero coverage does not establish an acceptable usefulness threshold. Moreover the exercise and rubric give no original cohort, outcome counts or grading of a separate completion/usefulness target at all. Define a bounded original-request objective and a separate completion/usable-answer target, specify mutually understandable categories and numerator/denominator, and supply a synthetic cohort with enough outcomes to evaluate both under a stated window/start/end/deadline. Require the comparison in the rubric separately from admitted-only latency and retain failed/timed-out/wrong results; preserve `incomplete` vs proven no-path distinction. Evidence: `.agents/skills/module-quality-review/SKILL.md` publication-readiness bar requires user-visible success/error denominators and says a rubric that passes through excessive shedding is not ready; approved M10-L05 LO2 demands choices against resource budgets and failure criteria. |
| M10-L05-PED-03 | minor | open | `modules/m10/assessments/M10-L05.md`, front-matter outcome_map | LO1 names only the worked-trace heading though Q2's per-request isolation is taught under “Start with BFS and reconstruct the path” and EX-1's bidirectional proof is under “Bidirectional search changes the shape of work.” LO2 names only the visibility/caching section though directed reverse traversal in Q6 is taught in the bidirectional section and resource limits in EX-1 under directory/fetches and reliability. Expand front-matter `taught_in` to actual relevant teaching headings; retain item IDs and align the narrative map, including bidirectional for LO2/Q6. Evidence: `docs/authoring-format-contract-v1.md` outcome-map requirement and actual lesson/assessment. |

## Source-topic coverage

`L` = lesson, `A` = separate companion. IDs and physical line locators come from approved `curriculum/revision-1/coverage.csv`. All topics below are assigned to M10-L05; statuses assess the presence of explanation, while PED-01 identifies material missing depth in the bidirectional proof. The source's separate snippet exposes a boolean BFS and object-held `visited_ids`; the lesson correctly distinguishes reachability, path reconstruction and per-request isolation rather than reproducing that shared-state sketch.

| Source ID and locator | Disposition, actual instruction and assessment |
| --- | --- |
| PR-SOCIAL_GRAPH-H002 `README.md#L5` | taught: L “Define the graph and the answer” sets path/privacy contract; A EX-1. |
| PR-SOCIAL_GRAPH-H003 `#L13` | taught: L defines valid path query and visibility; A Q1, EX-1. |
| PR-SOCIAL_GRAPH-H004 `#L15` | taught: L defines unweighted shortest relationship path, rather than reachability alone; A Q1 and EX-1. |
| PR-SOCIAL_GRAPH-H005 `#L20` | taught: L declares snapshot, unweighted graph, size, degree and deadline assumptions; A EX-1. |
| PR-SOCIAL_GRAPH-H006 `#L22` | taught: L synthetic 100m vertices, 2bn edges and peak query envelope; A EX-1 applies partition and budget assumptions. |
| PR-SOCIAL_GRAPH-H007 `#L34` | taught: L derives four billion endpoint adjacency references, 32 GB decimal before overhead and mean degree ~40; A EX-1 assesses application, not the exact storage arithmetic. |
| PR-SOCIAL_GRAPH-H008 `#L49` | taught: L three-server ownership directory, adjacency RPC batching and cache/placement decisions; A Q3, EX-1. |
| PR-SOCIAL_GRAPH-H009 `#L55` | taught: L explicit BFS queue/visited/parent model and partitioned expansion; A Q1–Q3, EX-1. |
| PR-SOCIAL_GRAPH-H010 `#L59` | taught: L derives layers, predecessor chain and four-hop route; A Q1 and EX-1. |
| PR-SOCIAL_GRAPH-H011 `#L249` | taught: L batching, skew, caching, sharding and approximation/privacy constraints; A Q3–Q6 and EX-1. |
| PR-CODE-R1-GRAPH-BFS `social_graph_snippets.py#L11` | taught: L explains FIFO frontier, enqueued visited, reachability versus reconstructed shortest path; A Q1–Q2. |
| PR-CODE-R1-GRAPH-PERSON `#L31` | taught: L IDs and adjacency edge sets mapped to three person servers; A Q1/Q3, EX-1. |
| PR-CODE-R1-GRAPH-LOOKUP `#L39` | taught: L directory maps vertex ownership with stale-routing risks; A Q3, EX-1. |
| PR-CODE-R1-GRAPH-SERVER `#L49` | taught: L groups b,c and d,e into owner batches; A Q3, EX-1. |
| PR-CODE-R1-GRAPH-DISTRIBUTED `#L62` | taught: L contrasts per-query visited/parent with a shared global visited bit and prevents cross-viewer leakage; A Q2, EX-1. |
| PR-BODY-R1-GRAPH-CACHE `README.md#L278` | taught: L scoped cache, final authorization/revision and limited offline precomputation; A Q5, EX-1. |
| PR-BODY-R1-GRAPH-PLACE `#L280` | taught: L owner batching and locality-aware versus hash placement, churn and skew costs; A Q3, EX-1. |
| PR-BODY-R1-GRAPH-BIDIRECTIONAL `#L282` | taught with **material depth gap PED-01**: L shows two frontiers and intersection but leaves shortest-termination criterion unspecified; A EX-1 asks for it. |
| PR-BODY-R1-GRAPH-LIMIT `#L283` | taught: L separates hop/edge/deadline budget and incomplete from graph-wide no path, and explains high-degree pruning can change proof; A Q4, EX-1. |
| PR-BODY-R1-GRAPH-ALTERNATIVES `#L285` | taught: L distinguishes GraphQL API from traversal and Gremlin/Cypher/graph engine options; A Q6, EX-1. |

No assigned topic is absent or merely a heading/assessment; PED-01 blocks sufficient depth for an assigned core mechanism.

## Lesson-first comprehension and assessment alignment

One-sided BFS is reconstructible: initial queue and visited, mark on enqueue, complete FIFO layers, parent links, a→b→d→f→g and alternative a→c→e→f→g. The sample maps each frontier to responsible partitions, and a timeout invalidates an unqualified shortest/no-path claim. The lesson explains graph revision, visible-edge checks, per-request visited isolation and high-degree/deadline limits. Its first missing link is the concrete *bidirectional termination proof* at PED-01; “meet at d or e” and a warning about arbitrary intersections do not tell learners how to calculate the bound they are later required to apply. Lesson/assessment remain separate, with six answered checks and one exercise.

| Outcome | Teaching | Graded evidence |
| --- | --- | --- |
| M10-L05-LO1 | “Start with BFS,” “Trace a shortest path across three person servers,” and “Bidirectional search” teach core trace, subject to PED-01. | Q1–Q3 and EX-1 check shortest path, query-local visited and batched/timeout behavior; the latter's proof requirement has PED-01. |
| M10-L05-LO2 | “Make the directory and fetches pay,” “Treat visibility,” “Bidirectional search” and “Choose a contract” teach alternatives, privacy, directed reverse edges and bounds, subject to PED-02. | Q4–Q6 and EX-1 assess pruning/approximation, cache privacy, GraphQL and reverse edges; numerical objective/completion measurement is not yet graded (PED-02). |

Product/source behavior and publisher version claims require the independent technical reviewer; no executable traversal or load test was run in this review. Human approval remains separate.

## Verdict

`revise`

## Round 1 targeted re-review — 2026-11-27

Reviewed correction handoff `e763f03`, reading the changed bidirectional and success-contract teaching before the revised companion answer and rubric. This re-review covers the findings and nearby dependent examples, not a fresh audit of unchanged topics.

| ID | Status | Verification and evidence |
| --- | --- | --- |
| M10-L05-PED-01 | resolved | “Bidirectional search changes the shape of work” now defines complete authorized forward/backward BFS balls, distance labels, minimum intersection sum `μ`, and a sufficient condition `μ ≤ r_s + r_t` for fixed-revision unweighted search. It explains that all required adjacency batches/pages for smaller depths must be complete, then proves why any shorter path would intersect both balls and contradict the minimum candidate. The original graph's radius-2 balls meet at d/e with sum four; a separate delayed-shorter-candidate trace changes an early length-four result to length three when q's batch arrives, and a timeout prevents certification. EX-1 asks for these radii, labels and certificate; its answer, accepted alternative proofs and rubric match the teaching. The learner can reconstruct the rule and worked proof before reading the answer key. Evidence: approved M10-L05 sequence and LO1 in `curriculum/revision-1/CURRICULUM_MASTER.md`. |
| M10-L05-PED-02 | resolved | “Choose a contract before calling the service reliable” now sets separate 99% responsiveness and 98% useful exact-completion objectives over all valid originals in a five-minute ingress cohort through 800 ms client receipt. The EX-1 categories are mutually exclusive and total 1,000: 930 on-time authorized exact paths, 30 justified within-four-hop negatives, 20 truthful incompletes, ten rejected/failed and ten late. The answer correctly computes 980/1,000 = 98% responsiveness, missing 99%, and 960/1,000 = 96% useful completion, missing 98%; the rubric requires both comparisons, the boundaries, all categories and admitted-only latency distinction. A service returning only incompletes has zero useful completion, and a bounded negative remains scoped to four hops. Evidence: `.agents/skills/module-quality-review/SKILL.md` publication-readiness bar and approved M10-L05 LO2. |
| M10-L05-PED-03 | resolved | Both front-matter outcome maps now include the relevant actual BFS, bidirectional, partition-fetch, visibility and reliability headings; LO2 narrative mapping adds bidirectional for Q6. Existing item IDs are preserved. Evidence: `docs/authoring-format-contract-v1.md` outcome-map requirements. |

The modified lesson and assessment retain snapshot/viewer visibility, per-request visited state, batching and incomplete-vs-no-path distinctions. No new teaching or assessment regression was identified in the changed scope. The separate technical reviewer determines the mathematical and source-claim correctness; no traversal or load test was executed here.

**Verdict:** `ready-for-human-review`. Human publication approval remains separate.
