# M09-L03 independent pedagogy and curriculum coverage review

Reviewed 2026-11-26: `modules/m09/lessons/M09-L03.md`, separate assessment `modules/m09/assessments/M09-L03.md`, task spec `.academy/specs/SD-M09-L03.json`, approved `curriculum/revision-1/CURRICULUM_MASTER.md` M09-L03 and `curriculum/revision-1/coverage.csv`. Audience: middle/senior engineers. The lesson was read before its companion answer key. This is an independent Stage A lesson review, not technical or publication approval.

## Findings

| ID | Severity | Status | Location | Learner impact, evidence, and suggested fix |
| --- | --- | --- | --- | --- |
| M09-L03-PED-01 | major | open | `modules/m09/assessments/M09-L03.md:46-48,55,65-68`, EX-1 task and rubric | The exercise requests a user-visible SLI but only demands a denominator that includes failures; the rubric's full-credit SLO row likewise requires only the original-request denominator and failure/late categories. A response can get all SLO points while omitting a window, success endpoint/deadline, success target, and observed successful numerator; it can even shed nearly all requests without a graded decision that the user-facing objective fails. The reference answer names a detailed example, but it is not made a grading requirement or tied to provided observations. Define an explicit illustrative original-operation objective, supply or request evidence adequate to evaluate it in the exercise window (including rejected, failed, late and timely-correct counts), and require calculation/assessment of success against that objective independently of admitted-only latency. Include window, start/end event and deadline in the evidence for full credit; accept equivalent metrics with explicit boundaries. The lesson already teaches these distinctions in “Define success on original operations”; approved curriculum M09-L03 LO2 requires a defended choice using availability and failure criteria, and `.agents/skills/module-quality-review/SKILL.md` requires user-visible success to be checked separately from admitted latency and excessive shedding. |
| M09-L03-PED-02 | minor | open | `modules/m09/assessments/M09-L03.md:9-11,36-42,74-75` | LO2 front matter identifies only the quorum section even though Q5 depends on the Chubby/ZooKeeper section and Q6 depends on the Spanner section. The narrative map at line 75 identifies Spanner but omits the Chubby/ZooKeeper section for Q5. Add those actual teaching headings to both LO2 mappings, preserving the existing item IDs. Source: `docs/authoring-format-contract-v1.md` and approved M09-L03 sequence. |

No unresolved coverage blocker found. The assessment gap above prevents a ready verdict. The existing lesson itself supports the proposed SLI fix; do not relocate teaching into the answer key.

## Source coverage

The pinned Primer revision is [ae9bbd7b02d90b9866215de185217d33f39ab733](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md). Its system-architectures table names Spanner (physical source line 1706), Chubby (1713) and ZooKeeper (1716), each with its own reference; those rows do not supply a nested in-repository mechanism inventory. The approved matrix assigns the three IDs to this lesson, and the approved outline specifies the depth. I opened the pinned source table and compared each assignment with actual explanation, not just headings or assessment text.

| Assigned source topic / locator | Disposition and teaching evidence | Assessment |
| --- | --- | --- |
| PR-ARCH-SPANNER, `README.md#L1706` | **taught** — “Why Spanner is a different choice” explains replicated database transactions, clock-uncertainty API, timestamps and commit-wait, contrasts a worker lease, and scopes the trade-off. | Q6; EX-1 assesses the related choice of safety/availability but does not require Spanner. |
| PR-ARCH-CHUBBY, `README.md#L1713` | **taught** — “Chubby and ZooKeeper solve coordination, not arbitrary storage fencing” explains coarse lock/configuration use, sequencer validation at a consuming server and lock delay's limitation, connected to the paused-owner trace. | Q1–Q3 and EX-1 assess the application-level delayed-owner mechanism; none requires recalling a Chubby API. |
| PR-ARCH-ZOOKEEPER, `README.md#L1716` | **taught** — the same section describes ordered ephemeral sequential nodes, predecessor watches, expiry and the absent external-store fence; it states the sequence-reuse and uncertain-creation boundaries. | Q5; EX-1 tests the analogous protected resource decision. |

Academy-added membership, election, leases, epochs/fencing, quorum placement, correlated failures and workload-dependent coordination choices appear in the approved teaching sequence and explanatory lesson sections. No mapped topic is mention-only or assessment-only. A reference link is a topic map rather than proof of product semantics; product correctness and source rights are outside this review.

## Lesson-first comprehension and outcome assessment

The lesson begins with operator-confirmed single ownership, explains why automated failover needs coordination, then traces the old writer's pause and lease expiry, fence installation at the resource, new write, and rejection of the delayed old write. It explicitly limits protection before installation and distinguishes fencing from same-epoch idempotency and authorization. The three-voter example then connects majority loss and common-cause risk to availability, latency and the difference between coordinator and database recovery. The Spanner comparison explains why a worker lease does not provide cross-record transactions. The main invariant and safety decision can be reconstructed from the lesson and declared prerequisites without consulting EX-1.

| Outcome | Teaching evidence | Assessment evidence |
| --- | --- | --- |
| M09-L03-LO1 | “Start with the invariant”, “Follow the paused owner”, and the Chubby/ZooKeeper section teach membership, expiry and resource-side fencing with trace and failure limits. | Q1–Q3 and EX-1 assess delayed writes, installation/acknowledgment ordering and duplicate current-owner work; EX-1 also checks ownership and quorum. |
| M09-L03-LO2 | “Place the quorum”, Chubby/ZooKeeper, “Why Spanner is a different choice” and “Define success on original operations” compare placement, tool limits, transaction alternative and user-visible costs. | Q4–Q6 and EX-1 address quorum, tool boundaries and a coordination decision; EX-1's SLI grading requires PED-01 correction. |

Six questions have answers and explanations; the separate exercise provides a scenario, reference answer, and ten-point rubric that admits alternative architectures. Apart from PED-01 and the mapping defect PED-02, no additional material sequencing, coverage or audience gap was identified.

## Verdict

`revise`

## Round 1 targeted re-review — 2026-11-26

Reviewed correction commit `c21e9f8` against the lesson, revised EX-1 and both outcome maps, and checked nearby questions and explanations for regressions. The linked ZooKeeper reference was version-pinned without changing the teaching explanation or Q5's expected reasoning.

| Finding | Status | Exact verification and evidence |
| --- | --- | --- |
| M09-L03-PED-01 | resolved | The synthetic drill in `modules/m09/assessments/M09-L03.md`, EX-1 supplies 1,000 distinct originals in a ten-minute first-ingress window, the five-second first-ingress-to-client-validated success boundary and a 99% objective. The exclusive categories total 1,000: 970 on-time-correct, ten late, ten rejected, five timed out and five stale-generation responses. The answer correctly gives 970/1,000 = 97%, below 99%; rubric now requires the window, endpoints, deadline, all failure categories, comparison with the objective and the distinction from admitted-success latency. A shedding-heavy result can no longer pass this SLO criterion on a denominator alone. The lesson's “Define success on original operations” already teaches these boundaries, and prerequisite M09-L02 “Measure the original request” explains joining receipts and treating failed evidence. Approved teaching and outcome scope: `curriculum/revision-1/CURRICULUM_MASTER.md`, M09-L03 LO2; evidence for rubric calibration: `.agents/skills/module-quality-review/SKILL.md`, publication-readiness bar. |
| M09-L03-PED-02 | resolved | LO2 front matter and narrative map now both identify the Chubby/ZooKeeper section used for Q5 and the Spanner section used for Q6, alongside quorum and success sections. Existing item IDs are unchanged. The headings exist in the companion lesson. Evidence: `docs/authoring-format-contract-v1.md`, assessment outcome-map requirements, and approved M09-L03 teaching sequence. |

The revised question is answerable from the lesson and its stated prerequisite; the sample and rubric agree with the supplied counts. The authority, fencing, retry and falsification parts of EX-1 remain intact. No new pedagogical or assigned-coverage gap was identified in the changed scope.

**Verdict:** `ready-for-human-review`. Technical/provenance review and human publication approval remain separate.
