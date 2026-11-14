# M06-L01 independent coverage and pedagogy review

Reviewed draft at Git revision `eeb7933`, lesson-mode combined assignment, for English-speaking middle/senior engineers. Inputs: task spec SD-M06-L01, approved curriculum and accepted source inventory/review, lesson, assessment, evidence, governance, task history. Source map: [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), pinned revision `ae9bbd7b02d90b9866215de185217d33f39ab733`; exact sections and assigned inventory rows below. N1 in `curriculum/revision-1/review.md` requires the later policy traces to be presented as a preview, not an undeclared prerequisite.

## Original coverage matrix at eeb7933

All rows map to M06-L01 LO1/LO2. Teaching section abbreviations: B = Put reuse at the right boundary; U = Pick the unit of reuse; S = Size the catalogue and trace a miss; C = Combine granularity and update policy. Assessment: `modules/m06/assessments/M06-L01.md`.

| Source topic and pinned locator | Actual instruction and depth | Status | Assessment / gap |
| --- | --- | --- | --- |
| PR-H119 Cache, README L1132 | B, S: reusable work and capacity | taught | Q1–Q3, EX-1 |
| PR-H120 Client, L1144 | B: browser reuse and privacy | taught | EX-1 contrasts shared/private boundaries |
| PR-H121 CDN, L1148 | B: backend avoidance and variants | taught | EX-1 |
| PR-H122 Web server, L1152 | B: rendering avoidance and authorization | taught | EX-1 |
| PR-H123 Database, L1156 | B: buffers versus finished results | taught | Q1 |
| PR-H124 Application, L1160 | B: query/object reuse and permissions | taught | EX-1 |
| PR-H125 Query level, L1178 | U: canonical key and dependencies | taught | Q5, EX-1 |
| PR-H126 Object level, L1185 | U, C: assembly and invalidation | taught | Q4 |
| PR-BODY-R1-CACHE-ROW, L1171 | U: row reuse and changes | taught | EX-1 alternatives |
| PR-BODY-R1-CACHE-QUERY, L1172 | U: result IDs/ranks, keys and invalidation | taught | Q5, EX-1 |
| PR-BODY-R1-CACHE-OBJECT, L1173 | U: assembled card and source changes | taught | Q4 |
| PR-BODY-R1-CACHE-HTML, L1174 | U: rendering savings and variants | taught | EX-1 alternatives |
| PR-BODY-R1-CACHE-FILE, L1176 | S: clone state, disposable warm-up or shared cache | taught | Q3, EX-1 |
| PR-BODY-R1-CACHE-QUERY-DEPS, L1180 | U: hash tuple and dependency domain/new membership | taught | Q5, EX-1 |
| PR-BODY-R1-CACHE-OBJECT-ASM, L1187 | U: card assembly and underlying changes | taught | Q4 |
| PR-BODY-R1-CACHE-EXAMPLES, L1194 | U/C: card, rendered page, activity and adjacency objects | merged | Session-object example is absent; see P2. |
| PR-PASTEBIN-H018, pastebin README L290 | C: public paste at edge, expiry and deletion | taught | EX-1 transfers boundary choice |
| PR-TWITTER-H018, twitter README L291 | C: activity scoped to authorized viewer | merged | EX-1 transfers authorization |
| PR-WEB_CRAWLER-H019, web crawler README L311 | C: URL metadata, normalized keys | taught | EX-1 transfers key design |
| PR-MINT-H018, mint README L399 | C: account summaries and authoritative balance | taught | EX-1 transfers access boundary |
| PR-SOCIAL_GRAPH-H015, social graph README L307 | C: adjacency objects and visibility invalidation | merged | EX-1 transfers access boundary |
| PR-QUERY_CACHE-H018, query cache README L264 | U/C: query keys, invalidation and cache-aside | taught | Q5, EX-1; policy comparison gap P1 |
| PR-SALES_RANK-H016, sales rank README L296 | C: ranked result keyed by reporting generation | taught | EX-1 transfers key/generation |
| PR-SCALING_AWS-H041, scaling AWS README L361 | S/C: disposable local state and shared reuse across replicas | taught | Q3, EX-1 |

Academy additions: S teaches working-set sizing, hit-rate arithmetic, expiry, eviction, cold starts and coalescing; C names Redis OSS 7.4 lists, sorted sets, persistence and eviction, and scopes M06-L02's detailed traces as a preview. The policy decision itself needs the repair in P1. No SLO is asserted in this scenario.

## Original findings at eeb7933

**M06-L01-P1 — Major, open — policy choice is under-taught for LO2.** Location: lesson, “Combine granularity and update policy”; assessment, EX-1 and policy trade-off criterion. The write-through sentence says the write waits for the backing store but does not explain what happens to the cache on a write, while write-behind and refresh-ahead lack enough transition detail to compare the alternatives with cache-aside. The lesson asks learners to defend an update policy and EX-1 grades this choice, yet a learner cannot reconstruct the alternatives' cache/store paths and failure criteria from the instruction. Add a concise policy comparison describing each policy's cache/store update timing and one decision-relevant cost or failure for each, keeping detailed concurrent traces in M06-L02 as the approved preview; align the rubric with valid choices under stated assumptions.

**M06-L01-P2 — Minor, open — one mapped example lacks disposition.** Location: source inventory PR-BODY-R1-CACHE-EXAMPLES, README L1194; lesson “Pick the unit of reuse” and workload table. Activity, graph and rendered-page examples are combined with meaningful instruction, but the mapped session-object example is absent. Learners miss an example of session reuse and its user-specific boundary. Add a short scoped session example with the relevant sharing/invalidation decision, or obtain an explicit curriculum scope decision. This is an illustrative gap rather than a missing core caching mechanism.

## Original pedagogical assessment at eeb7933

The museum scenario motivates reused query work; the capacity example states units and the hit-to-origin assumptions. Q1–Q6 and the separate practical exercise cover the declared outcomes, with explanations and a points rubric. EX-1 admits audience-scoped staff caching or bypass, and its baseline origin and memory arithmetic are supported by the lesson. The policy criterion is not fully fair until P1 is repaired. No embedded assessment bank appears in the lesson. No material prerequisite or excessive introductory exposition was identified; the preview of M06-L02 preserves the intended sequence.

## Original verdict at eeb7933

**revise** — M06-L01-P1 is an open major finding; P2 is an open minor coverage finding. This review is not technical, source-rights, human, or publication approval.

## Targeted re-review at d98bb98

The correction is independently reviewed against the lesson and assessment at `d98bb98`. The prior matrix and findings above preserve the original evidence and verdict; the following statuses and verdict supersede them.

- **M06-L01-P1 — Major, resolved.** In lesson “Combine granularity and update policy,” the new policy table explicitly describes the cache and store paths for cache-aside, write-through, write-behind and refresh-ahead, with a decision-relevant benefit and failure or cost for each. The paragraph immediately following labels M06-L02 as the detailed failure-window preview. Assessment EX-1's policy criterion now accepts other defensible choices based on scenario assumptions and failure costs. These changes give learners the mechanism and criteria needed for the assessed comparison. The previously identified policy gap in PR-QUERY_CACHE-H018 is closed.
- **M06-L01-P2 — Minor, resolved.** The lesson workload table now includes a user-session object scoped to its authenticated session, with logout or revocation invalidation and an authoritative authorization check. This completes the session example within the merged PR-BODY-R1-CACHE-EXAMPLES row; the remaining mapped examples retain their instruction.

The revised shared-cache scale-out explanation and EX-1 solution distinguish a warm shared entry from shared expiry, define rate and concurrency controls, and explain excess request behavior. The assessment now states its effective hit-ratio population including staff bypasses; its solution and rubric use that assumption consistently. The more detailed generation example explains its ordering and delayed advancement, and does not displace the mapped query-key and invalidation instruction. No affected teaching or coverage regression was identified.

## Current verdict

**ready-for-human-review** — P1 and P2 are resolved; no open major or blocker finding remains in the reviewed scope. This is not technical, source-rights, human, or publication approval.

## Round 2 targeted re-review at 1347538

The change since `d98bb98` replaces the AWS Cache Validity URL in the lesson and evidence; the lesson instruction, policy table, session example and assessment are unchanged. **M06-L01-P1 remains resolved; M06-L01-P2 remains resolved.** The previously reviewed mapped coverage remains intact.

**Latest verdict: ready-for-human-review.** This is a pedagogy and coverage verdict, not technical, source-rights, human, or publication approval.
