# M10-L03 independent pedagogy and curriculum coverage review

Reviewed 2026-11-27: canonical task spec/state/worklog, approved M10-L03 outline and `curriculum/revision-1/{coverage.csv,source-inventory.json}`, then lesson and companion/evidence. The lesson was read before assessment answers and rubric. Audience: middle/senior engineers. I independently opened the pinned Primer [crawler case](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/README.md), [crawler skeleton](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/web_crawler_snippets.py) and [unique-only reducer](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/web_crawler_mapreduce.py) at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`, inspecting scope, use cases, loop, queues, recrawl, search and scaling leaves. M08-L03 and M10-L02 are prerequisites; no full audit of those accepted lessons was repeated. Same-author self-review is not independent evidence.

## Findings

| ID | Severity | Status | Location | Impact, evidence and bounded correction |
| --- | --- | --- | --- | --- |
| M10-L03-PED-01 | major | open | `modules/m10/lessons/M10-L03.md`, “Scope crawl input, output and cost” and “Choose recrawl budget and query freshness together”; assessment EX-1 budget/rubric | The approved first teaching item explicitly requires deriving **frontier, page-storage and index sizes**; item 5 includes **bandwidth budgets**. The lesson calculates only raw fetched-page bytes and average request rate, then says to estimate URL/edge/index storage separately and mentions bandwidth without a worked derivation. No given frontier cardinality/record size, posting count/bytes or bandwidth calculation allows the reader to reproduce those required planning decisions; EX-1 grades only raw page-storage calculation. Add clearly synthetic assumptions and an explicit, unit-checked worked derivation for frontier records, index/postings size and average payload bandwidth, distinguishing ingress/egress, peak/host limits, compression/replication and unmeasured overhead; update EX-1 inputs and rubric to measure those operations. Avoid invented real-system benchmarks. Evidence: approved `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L03 teaching sequence 1 and 5, and approved mapping `PR-BODY-R1-CRAWL-BANDWIDTH` in `curriculum/revision-1/coverage.csv`. |
| M10-L03-PED-02 | major | open | `modules/m10/assessments/M10-L03.md`, EX-1 Task, worked solution and “Contracts and falsification” rubric | The exercise asks for client-facing export and persisted-change-to-index SLIs, but its rubric awards full credit for naming the two populations and a test. Neither objective has a stated measurement window, complete numerator/denominator and target, a given exclusive original-operation outcome cohort, or a required computation and target comparison; export client deadline is unspecified. A learner can produce a fail-fast/mostly stale design and still receive full contract credit by identifying denominators alone. Provide separate synthetic original-query and successfully-persisted-change cohorts with appropriate, explicitly distinct endpoints/windows/deadlines and targets; require the learner to classify late/missing/failed/rejected or stale outcomes, compute each result and compare to its own target, while reporting not-yet-fetched coverage and admitted-only latency separately. This extends rather than changes the lesson's taught SLI populations. Evidence: `.agents/skills/module-quality-review/SKILL.md` publication-readiness bar; approved M10-L03 LO2 decision/failure criteria. |
| M10-L03-PED-03 | minor | open | `modules/m10/assessments/M10-L03.md`, outcome_map front matter and LO2 narrative map | LO1 names only the index walkthrough although Q2's unique-only versus distinct filtering is taught in “Store versions and deduplicate without deleting meaning.” LO2 names only recrawl though Q4 needs “Make the frontier recoverable and polite” (robots/transport) and Q5 needs “Store versions and deduplicate without deleting meaning” (similarity). Add the actual teaching headings to both front matter and narrative LO2 map; keep existing item IDs. Evidence: `docs/authoring-format-contract-v1.md` assessment outcome mapping and the companion/lesson. |
| M10-L03-COV-01 | minor | open | `modules/m10/lessons/M10-L03.md`, “Make the frontier recoverable and polite”; source mapping PR-CODE-R1-CRAWL-LOOP | The source skeleton explicitly reduces priority on detecting a duplicate; the lesson explains priority, normalized URL state, cycle control and future recrawl but does not explain how a repeated discovery merges or updates an already queued URL's priority/due time. Define one bounded deterministic duplicate-discovery merge policy that preserves a single scheduled URL, host fairness and later recrawl, and show its effect on the loop example. Evidence: approved source-map row `PR-CODE-R1-CRAWL-LOOP` and [pinned skeleton](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/web_crawler_snippets.py). |

## Source-topic coverage

`L` is `modules/m10/lessons/M10-L03.md`; `A` is the separate companion. Locators are approved physical source anchors; source rendering can have different line numbers. Coverage means explanatory instruction, not just heading, citation or assessment. The 24 rows below represent all source topics assigned to M10-L03.

| Topic ID and source locator | Disposition, teaching evidence and assessment |
| --- | --- |
| PR-WEB_CRAWLER-H002 `README.md#L5` | taught: L “Scope crawl input, output and cost” states source/search scope and boundaries; A EX-1. |
| PR-WEB_CRAWLER-H003 `#L13` | taught: L defines crawl and query uses with freshness/completeness; A Q3/Q6, EX-1. |
| PR-WEB_CRAWLER-H004 `#L15` | taught: L traces URL discovery, indexing and search output; A EX-1. |
| PR-WEB_CRAWLER-H006 `#L31` | taught: L states permitted hosts, storage/retention, queries and host-resource assumptions; A EX-1. |
| PR-WEB_CRAWLER-H007 `#L33` | taught: L synthetic 2m fetches/day, 50 KiB and 30 days plus query rate and per-host caps; A EX-1. |
| PR-WEB_CRAWLER-H008 `#L51` | partly taught: L derives raw body storage and rates but not required frontier/index sizing or bandwidth arithmetic; A EX-1 assesses raw size only; PED-01. |
| PR-WEB_CRAWLER-H009 `#L68` | taught: L frontier→fetch→page store→index→query architecture; A EX-1. |
| PR-WEB_CRAWLER-H010 `#L74` | taught: L frontier/lifecycle, URL and content identity, version/index queues; A Q1–Q3, EX-1. |
| PR-WEB_CRAWLER-H011 `#L78` | taught: L host-partitioned durable frontier with leases, recoverable fetch and link extraction; A EX-1. |
| PR-WEB_CRAWLER-H012 `#L179` | taught: L separates duplicate URLs, exact content and near-duplicate signatures, and correct distinct vs unique-only output; A Q1/Q2/Q5. |
| PR-WEB_CRAWLER-H013 `#L204` | taught: L adaptive bounded next_due_at, validators, robots and durable version/index propagation; A Q3/Q4, EX-1. |
| PR-WEB_CRAWLER-H014 `#L212` | taught: L “Walk a duplicate and a changed page to the index” connects postings, title/snippet and one-generation query results; A Q3/Q6, EX-1. |
| PR-WEB_CRAWLER-H015 `#L255` | taught with bandwidth depth gap: L distributes host fetch/index partitions, versioned caches, DNS/pooling and critiques raw UDP; capacity arithmetic needs PED-01. A Q4, EX-1. |
| PR-PROMPT-02 `README.md#L1655` | taught: L composes crawl source cuts with prerequisite inverted-index scatter/gather, search title/snippet and freshness; A Q6, EX-1. |
| PR-PROMPT-03 `README.md#L1656` | taught: L frontier, host gate, fetch, dedup, recrawl and source-to-index flow; A Q1–Q3, EX-1. |
| PR-CODE-R1-CRAWL-FRONTIER `web_crawler_snippets.py#L4` | taught: L durable per-URL key, priority, host gating, lease and known URL/recrawl lifecycle; A EX-1. |
| PR-CODE-R1-CRAWL-PAGE `#L35` | taught: L URL identity, immutable page version, links and body digest with source provenance; A Q1/Q3. |
| PR-CODE-R1-CRAWL-LOOP `#L48` | partly taught: L explains URL states, loop handling and index events, but repeated-discovery priority merge needs COV-01. A EX-1. |
| PR-CODE-R1-CRAWL-REDUCE `web_crawler_mapreduce.py#L6` | taught: L explains `count == 1` emits no u1 for duplicate input, unlike one output per distinct URL; A Q2/EX-1. |
| PR-BODY-R1-CRAWL-SIMILAR `README.md#L202` | taught: L gives exact digest verification and Jaccard/cosine representations with non-equivalence caveat; A Q1/Q5. |
| PR-BODY-R1-CRAWL-ROBOTS `#L210` | taught: L robots rules versus authentication/index exclusion and host budgets; A Q4/EX-1. |
| PR-BODY-R1-CRAWL-DNS `#L286` | taught: L resolver TTL and revalidation/security checks; A EX-1 applies host safety. |
| PR-BODY-R1-CRAWL-POOL `#L287` | taught: L pooling and HTTP/3 QUIC versus arbitrary UDP substitution; A Q4. |
| PR-BODY-R1-CRAWL-BANDWIDTH `#L289` | partly taught: L names ingress/egress and response-size limits but lacks an actual bandwidth budget; PED-01. |

No topic is wholly absent, but the required sizing and loop-update depth gaps are recorded above rather than counted as full coverage.

## Lesson-first comprehension and assessment alignment

The lesson causally separates raw URL, normalized fetch key and versioned document identity; a durable host frontier and recoverable lease prevent cycles while allowing recrawl. It distinguishes exact body sharing with separate URL provenance from similarity thresholds, then traces u1:v1→v2, a crashed index worker, idempotent replay, title/snippet/postings change and g17→g18 query visibility. The reader can follow how a fresh source is still absent in an older complete index before consulting the assessment. Politeness, robots and protocol/SSRF boundaries, freshness/latency trade-offs and current-generation query composition are explicitly taught. Sizing of frontier/index/bandwidth is the first substantial missing planning step (PED-01), not a request for a fixed length or diagram.

| Outcome | Teaching | Assessment |
| --- | --- | --- |
| M10-L03-LO1 | Frontier/politeness, distinct/signature handling and u1/u2 changed-page indexing trace. | Q1–Q3 and EX-1 test URL identity, distinct reduction, durable event and index publication; PED-03 fixes mapping. |
| M10-L03-LO2 | Scope/retention (with PED-01 gap), recrawl and query freshness, safety/protocol, and separate persisted-change/query measurement. | Q4–Q6 and EX-1 test robots/UDP, similarity and stale index; PED-02 is an assessment gap for success measurement and PED-03 fixes mapping. |

The assessment is separate and contains six explained checks and one practical exercise with a 12-point rubric. The lesson's two SLI populations do not pretend to count unfetched source changes as already-persisted changes. Numeric example assumptions are explicitly synthetic; no live crawl, bandwidth or index test was executed by this reviewer. Technical/provenance QA and human release approval are separate.

## Verdict

`revise`

## Round 1 targeted re-review — 2026-11-27

Reviewed correction handoff `e55ed03`, reading the changed lesson before the assessment solution and rubric. This is a targeted review of the four findings and nearby changed content, not a repeat audit of unchanged topics.

| ID | Status | Verification and evidence |
| --- | --- | --- |
| M10-L03-PED-01 | resolved | “Scope crawl input, output and cost” now derives raw 30-day payload `3.072 TB ≈ 2.794 TiB`, 10m × 256 B frontier = 2.56 GB ≈ 2.38 GiB and independently 5m unique live documents × 200 postings × 12 B = 12 GB ≈ 11.18 GiB. It distinguishes 2m successful fetches/day (~23.15/s) from 2.5m attempts/day (~28.94/s), and derives average ~9.48 Mbit/s from successful retained body volume and a 100-body/s burst of 40.96 Mbit/s. The example labels cardinalities independent and overhead, replication, other wire traffic and host limits separately. EX-1 gives the inputs and requires those derivations in its task, solution and rubric. Evidence: approved M10-L03 sequence 1 and 5, `curriculum/revision-1/CURRICULUM_MASTER.md`. |
| M10-L03-PED-02 | resolved | The lesson separately defines a five-minute original-valid export cohort with 99% target, 800 ms first-ingress-to-client receipt and source-cut age ≤ five minutes at ingress; and a one-hour cohort of persisted eligible changes with 99% target and five-minute commit-to-visibility deadline on every required eligible reader. EX-1 supplies exclusive 970+10+8+7+5 = 1,000 export outcomes and 960+15+10+10+5 = 1,000 change outcomes; the solution computes 97% and 96%, both below target, and the rubric requires both comparisons, populations, endpoints, cut-age distinction, failure categories and separate admitted latency/unfetched coverage. Evidence: `.agents/skills/module-quality-review/SKILL.md` publication-readiness bar and approved M10-L03 LO2. |
| M10-L03-PED-03 | partly resolved; minor open | Front matter now names the specific deduplication section for Q2 and frontier/robots and deduplication/similarity sections for Q4/Q5; LO2 narrative map has both. However, LO1 front matter still omits “Make the frontier recoverable and polite,” which teaches the frontier/lifecycle action in EX-1 and is present in its narrative map; LO2 front matter still omits “Scope crawl input, output and cost” and “Test the composed system, not just isolated stages,” which teach EX-1's budget and two-SLI/falsification actions and are in the LO2 narrative map. Add these three headings to the respective front-matter entries. Evidence: `docs/authoring-format-contract-v1.md` outcome-map requirements and the current companion's EX-1 and narrative map. |
| M10-L03-COV-01 | resolved | The frontier section now explains bounded max-priority/earliest-existing-due merging in a single URL record, no parallel lease when already leased, a pending priority merged into future recrawl, and generation/conditional protection against a stale worker erasing that update. It walks A→B→A and preserves host fairness; EX-1 solution/rubric require the bounded merge. Evidence: approved PR-CODE-R1-CRAWL-LOOP in `curriculum/revision-1/coverage.csv` and [pinned source skeleton](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/web_crawler_snippets.py). |

The updated lesson separates fragment-free HTTP fetch keys from raw discovered fragment provenance and an optional bounded hash-route rendering key. The same distinction appears in EX-1's solution, and the URL identity/dedup explanation remains followable. The changed index explanation distinguishes durable apply/relay from query-visible confirmation on every eligible reader and ties each persisted change to its own freshness deadline. No new major pedagogical or coverage regression was identified in the changed scope; technical claims remain with the technical reviewer.

**Verdict:** `revise` for the remaining minor mapping inconsistency in PED-03. Human publication approval remains separate.

## Round 2 targeted re-review — 2026-11-27

Reviewed handoff `d469ca9`, limited to the changed assessment front matter and its adjacent narrative outcome map. No lesson, exercise, numerical example or evidence text changed in this correction.

| ID | Status | Verification and evidence |
| --- | --- | --- |
| M10-L03-PED-03 | resolved | LO1 front matter now includes “Make the frontier recoverable and polite” for EX-1's frontier/lifecycle action. LO2 front matter now includes “Scope crawl input, output and cost” for EX-1's capacity derivations and “Test the composed system, not just isolated stages” for its SLI and failure-test actions. The previously added deduplication and robots headings remain; all eight named teaching headings across the two entries exist in the lesson and both front-matter entries now match the narrative map. Q1–Q6 and EX-1 item IDs are unchanged. Evidence: current `modules/m10/assessments/M10-L03.md` front matter and outcome table; current `modules/m10/lessons/M10-L03.md` headings; `docs/authoring-format-contract-v1.md` assessment outcome-map contract. |

M10-L03-PED-01, PED-02 and COV-01 remain resolved as independently verified in the preceding targeted re-review. No new pedagogical or mapping regression was identified in this metadata-only change.

**Verdict:** `ready-for-human-review`. Technical/provenance QA and human publication approval remain separate.
