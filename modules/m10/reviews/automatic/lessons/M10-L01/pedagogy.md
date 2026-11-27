# M10-L01 independent pedagogy and curriculum coverage review

Reviewed 2026-11-27 at draft handoff `922eddd`, using approved `curriculum/revision-1/CURRICULUM_MASTER.md` M10-L01 and `curriculum/revision-1/coverage.csv`, `.academy/specs/SD-M10-L01.json`, task state/worklog, lesson, companion assessment and evidence. Audience: middle/senior engineers. The lesson was read before the assessment solution and rubric. The original case and its topic rows were independently opened at pinned Primer commit [ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/pastebin/README.md), together with the [separate mapper/reducer file](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/pastebin/pastebin.py). Its headings, meaningful use-case bullets, algorithm examples and scaling discussion were checked against the assigned outline; source snippets and answer keys are not teaching evidence.

## Findings

| ID | Severity | Status | Location | Impact, evidence and smallest correction |
| --- | --- | --- | --- | --- |
| M10-L01-PED-01 | major | open | `modules/m10/assessments/M10-L01.md`, EX-1 Deliverables and “Measurable success and recovery” rubric | EX-1 asks the learner to define a client-visible SLI, but the rubric awards full credit for an original-operation denominator with failures and interleavings alone. It does not require a measurement window, start/end events, deadline, target, correct-vs-error classification, or observed original-request outcome and a conclusion about meeting the target. The exercise can therefore pass a design that rejects most active-content reads while omitting evidence of whether its objective is met; the sample answer's more complete SLI does not repair the grading requirement. Add a stated or learner-selected bounded original-request objective, explicit synthetic outcomes sufficient to evaluate it, and rubric criteria for computing and judging that result, with failed/rejected/timed-out/late originals counted and admitted-only latency separate. The lesson's “Verify success on original operations” already teaches these boundaries. Evidence: `.agents/skills/module-quality-review/SKILL.md` publication-readiness bar; approved M10-L01 LO2 and decision/failure criteria in `curriculum/revision-1/CURRICULUM_MASTER.md`. |
| M10-L01-PED-02 | minor | open | `modules/m10/assessments/M10-L01.md` front matter `outcome_map` | LO1 front matter names only “Make the first version correct before adding an object store,” although Q3 tests monthly analytics taught under “Derive the short-link case and the analytics path.” LO2 names only “Trace expiration through caches and cleanup,” although Q4 and Q6 require “Assign an identifier without confusing representation and safety.” Expand the front matter to include the actual lesson sections already correctly listed in its narrative map, and keep item IDs. Evidence: `docs/authoring-format-contract-v1.md`, required assessment outcome mapping. |
| M10-L01-PED-03 | minor | open | `modules/m10/lessons/M10-L01.md`, “Make the first version correct before adding an object store”, last paragraph | A learner-facing paragraph describes an unmerged MS05 branch and publication dependency. That transient workflow detail interrupts the explanation of private authorization and will become stale independently of the lesson; the prerequisite link already provides the instructional context. Remove the branch/QA-status sentence while keeping the prerequisite link and authorization explanation. Evidence: approved M10-L01 outline and the lesson's declared M09-L01 prerequisite. |

No source-mapped topic was missing from the teaching lesson; the major assessment finding prevents a ready verdict.

## Coverage matrix

`L` = `modules/m10/lessons/M10-L01.md`, `A` = `modules/m10/assessments/M10-L01.md`. Source locators below are the physical line anchors in the approved matrix; the web extraction renders Markdown with different line offsets. Status means actual instructional coverage, not a judgment of factual correctness. The rows describe the source's scope and mechanisms and Academy's explicit original adaptation, including authentication/private links beyond the source's anonymous-only baseline.

| Assigned source topic and locator | Teaching disposition and assessed evidence |
| --- | --- |
| PR-PASTEBIN-H002 `README.md#L7` | taught: L “Start with a small workload and a precise contract” frames scope and workload; A EX-1. |
| PR-PASTEBIN-H003 `#L15` | taught: L defines create/read/delete/redirect use cases and visibility boundaries; A EX-1. |
| PR-PASTEBIN-H004 `#L17` | taught: L explicitly scopes original requests, public/private content, expiry and retrieval; A EX-1. |
| PR-PASTEBIN-H006 `#L39` | taught: L states workload, retention, visibility and design assumptions; A EX-1. |
| PR-PASTEBIN-H007 `#L41` | taught: L states quantitative and privacy assumptions plus peak as a design input; A EX-1. |
| PR-PASTEBIN-H008 `#L52` | taught: L derives retained payload, mean rates and example peak; A EX-1. |
| PR-PASTEBIN-H009 `#L78` | taught: L API contract and transaction/object-store progression give high-level design; A EX-1. |
| PR-PASTEBIN-H010 `#L84` | taught: L “Assign an identifier”, “Make the first version correct” and “Trace expiration” explain create/read/storage components; A Q1–Q2, Q4–Q6 and EX-1. |
| PR-PASTEBIN-H011 `#L88` | taught: L unique insertion, collision handling and idempotent create/object activation; A Q1–Q2 and EX-1. |
| PR-PASTEBIN-H012 `#L166` | taught: L authoritative metadata lookup then bound object version, authorization and expiry; A Q2, Q5 and EX-1. |
| PR-PASTEBIN-H013 `#L191` | taught: L “Derive the short-link case and the analytics path” defines admitted-hit events and month/code grouping; A Q3 and EX-1. |
| PR-PASTEBIN-H014 `#L230` | taught: L “Trace expiration through caches and cleanup” gives indexed scan, tombstone, conditional deletion and late-fill prevention; A Q5 and EX-1. |
| PR-PASTEBIN-H015 `#L234` | taught: L “Scale only when observations justify it” compares caching, replicas, object storage, allocator bottlenecks and async warehouse; A EX-1. |
| PR-PROMPT-08 `README.md#L1661` | taught: L derives code-to-target mapping and 3xx/abuse policy from paste storage, with distinct lifetime; A EX-1. |
| PR-CODE-R1-HITS `pastebin.py#L6` | taught: L explicitly emits month/code key + one, groups, reduces, illustrates Jan/Feb and deduplicates h2. Source file's extraction stubs and mapper/reducer were inspected; no source code is reused. A Q3 and EX-1. |
| PR-BODY-R1-PASTE-HASH `pastebin/README.md#L123` | taught: L critiques deterministic content hashing/truncation, collision, leakage and source-era MD5 advice, and explains unique insert/random alternative; A Q6 and EX-1. |
| PR-BODY-R1-PASTE-ENCODE `#L127` | taught: L contrasts positional Base62, standard Base64 and base64url characters, no entropy from encoding; A Q4. |
| PR-BODY-R1-PASTE-ANALYTICS `#L198` | taught: L traces distinct events through UTC month/code map/group/reduce; A Q3 and EX-1. |
| PR-BODY-R1-PASTE-WAREHOUSE `#L263` | taught: L separates immutable content object storage from analytics log/warehouse and explains when to split; A EX-1. |

## Lesson-first comprehension and outcome alignment

The lesson establishes a manageable transaction-first paste service and concrete traffic/retention inputs, then explains why namespace uniqueness, idempotency and authorization differ. Its split-store progression identifies the pending → object → verified → active sequence and the lost-response/pending-object cases. The reader can follow strict expiry versus asynchronous object cleanup and a late cache fill before seeing the assessment. The link-shortener section derives redirect and month/code aggregation with a duplicate and explicit counting semantics; scale choices are tied to observed load and policies. This supports the approved sequence for the intended audience without reliance on the assessment answer. The lesson and assessment are separate; six answered checks and a practical exercise exist.

| Outcome | Teaching evidence | Assessment evidence |
| --- | --- | --- |
| M10-L01-LO1 | Workload/API contract; transaction-to-object-store progression; short-link analytics trace. | Q1–Q3 and EX-1 cover create/retry, object publication, and month grouping; EX-1 also checks estimates and expiry. Front-matter teaching links need PED-02. |
| M10-L01-LO2 | Identifier/encoding/hash trade-offs; expiry/tombstone and cache boundaries; scale/observed success choices. | Q4–Q6 and EX-1 assess identifier/privacy and expiry, plus architecture selection; the SLI grading gap is PED-01 and front matter needs PED-02. |

The user-visible SLO is described in the lesson, including original population, five-minute window, 500 ms client deadline and class-specific correctness. The current assessment's grading does not require learners to demonstrate that the SLO is actually met; see PED-01. This is a pedagogy/coverage review, not independent technical/source-rights approval or a human release decision.

## Verdict

`revise`

## Round 1 targeted re-review — 2026-11-27

Reviewed the changed lesson before the revised answer/rubric at correction handoff `ae0e035`, then checked Q5, EX-1, outcome metadata and adjacent consistency. This is a targeted pedagogical and coverage assessment of the changed scope; no other lesson topics were re-audited.

| Finding | Status | Verified correction and supporting evidence |
| --- | --- | --- |
| M10-L01-PED-01 | resolved | EX-1 now defines the five-minute ingress cohort of 1,000 valid originals, first-ingress to client-received 500 ms deadline and 99% target. A controlled oracle classifies 980 originals as requiring active content and 20 as requiring an unavailable result. Within the active group, 970 correct-on-time plus five late, three rejected and two timed out = 980; within unavailable, 15 correct-on-time plus one rejected, one timeout and three incorrect-content = 20. Therefore 985/1,000 = 98.5%, below target. The answer and rubric explicitly grade both response classes, original denominator/failure categories, deadline, target comparison and admitted-only limitation. The 12-point rubric is retained. The lesson's “Verify success on original operations” teaches those classifications and measurement boundaries before the assessment. Evidence: approved M10-L01 LO2 in `curriculum/revision-1/CURRICULUM_MASTER.md` and the user-visible success requirement in `.agents/skills/module-quality-review/SKILL.md`. |
| M10-L01-PED-02 | resolved | The assessment's LO1 front matter now names the workload, create and analytics sections for Q1–Q3; LO2 names identifier, expiry and scale sections for Q4–Q6 and EX-1. The headings exist in the lesson, match the narrative outcome map, and the item IDs remain unchanged. Evidence: `docs/authoring-format-contract-v1.md`, assessment `outcome_map` requirements. |
| M10-L01-PED-03 | resolved | The transient unmerged-branch/publication sentence has been removed from the private-paste paragraph. The lesson keeps the relevant M09-L01 prerequisite link and the presigned-URL authorization and expiry boundary. Evidence: approved M10-L01 prerequisites in `curriculum/revision-1/CURRICULUM_MASTER.md`. |

The changed lesson now causally explains why an earlier metadata check can lose a race with a slow object fetch; after fetch or cache hit, a gate checks current generation, permission and expiry with a bounded UTC clock and serializes release admission against deletion. Its trace covers expiry-first and both read/delete orders, and it explicitly limits the promise to admission rather than recall of already delivered data. Q5 and EX-1 ask for those taught distinctions, the reference answer and rubric require the same post-fetch gate and in-flight limitation, and their correct-response classifications use that admission boundary. The lesson-first chain is reconstructible without relying on the sample answer. The scope-specific MD5 wording change does not disrupt the identifier explanation or Q6. No new pedagogical or coverage finding was identified in the corrected scope.

**Verdict:** `ready-for-human-review`. This verdict does not substitute for independent technical/provenance review or human publication approval.
