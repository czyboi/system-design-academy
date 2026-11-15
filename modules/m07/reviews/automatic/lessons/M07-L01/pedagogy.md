# M07-L01 independent coverage and pedagogy review

Reviewed lesson-mode combined assignment at draft revision `1cc293d` for English-speaking middle/senior engineers. Inputs: SD-M07-L01 spec and task history, approved curriculum and coverage inventory, lesson, assessment, evidence, and governance. The assigned topic map is the [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733) at `ae9bbd7b02d90b9866215de185217d33f39ab733`. The accepted global inventory is reused for this lesson's assigned rows. Section abbreviations: A = Separate acceptance, delivery and completion; C = Trace the crash around acknowledgement; B = Compare broker and executor contracts; D = Decide which work waits. Assessment items refer to `modules/m07/assessments/M07-L01.md`.

## Coverage matrix

All rows map to M07-L01 LO1/LO2. The repeated case headings are merged with the shared mechanism; the plan assigns detailed ownership and overload mechanisms to M03-L01 and M07-L02.

| Assigned source topic and pinned locator | Actual teaching and depth | Status | Assessment and disposition |
| --- | --- | --- | --- |
| PR-H138 Asynchronism, README L1324 | A/C/D: durable acceptance, later execution/status, crash and latency choice | taught | Q1–Q3, Q6, EX-1; retry acceptance detail needs P1. |
| PR-H139 Message queues, README L1334 | A/C/B: broker routing, delivery, acknowledgement and redelivery | taught | Q1–Q4, EX-1. |
| PR-H140 Task queues, README L1349 | A/B: executor maps job types to code and manages concurrency/retry; Celery case | taught | EX-1 applies worker responsibility. |
| PR-H142 Asynchronism disadvantages, README L1359 | C/D: duplicate effects, terminal failure, lag, bounded admission and synchronous alternatives | taught | Q2–Q3, Q5–Q6, EX-1. |
| PR-PASTEBIN-H019, pastebin README L307 | D: durable save versus deferred indexing; A explains owned result and handoff | merged | EX-1 applies the same boundary to document save; scope rationale acceptable. |
| PR-TWITTER-H019, twitter README L308 | D: record owned post before fan-out and notification; A/C provide handoff and failure mechanisms | merged | EX-1 transfers boundary choice; scope rationale acceptable. |
| PR-WEB_CRAWLER-H020, web crawler README L328 | D: bound and deduplicate URL work; A/C provide handoff and retries | merged | EX-1 transfers bounded worker reasoning; scope rationale acceptable. |
| PR-MINT-H019, mint README L416 | D: defer reconciliation while preserving authoritative transfer invariant; A supplies ownership | merged | EX-1 tests durable-input boundary; scope rationale acceptable. |
| PR-SOCIAL_GRAPH-H016, social graph README L324 | D: background snapshot when consumers tolerate lag, combined with A/C/D handoff and failure trade-offs | merged | EX-1 transfers deferred-work choice; scope rationale acceptable. |
| PR-QUERY_CACHE-H019, query cache README L281 | D: defer warm-up when consumers tolerate lag, combined with A/C/D | merged | EX-1 transfers deferred-work choice; scope rationale acceptable. |
| PR-SALES_RANK-H017, sales rank README L313 | D: recompute in background when consumers tolerate lag, combined with A/C/D | merged | EX-1 transfers deferred-work choice; scope rationale acceptable. |
| PR-SCALING_AWS-H042, scaling AWS README L378 | D: add workers only with dependency and execution headroom; otherwise limit admission | merged | EX-1 tests bounded capacity; scope rationale acceptable. |

The Academy-added outbox, request identity, duplicate-safe publication, poison-job handling and product-scoped cases appear in A–D. The worked trace makes both sides of the worker commit visible; Q1–Q3 and EX-1 exercise LO1. D compares synchronous and deferred choices, while Q4–Q6 and EX-1 exercise aspects of LO2. The lesson has no scenario SLO.

## Findings

**M07-L01-P1 — Major, open — a retry's acceptance proof is implicit at the key race.** Location: lesson A, first paragraph (“A retry with the same key and same input returns the same job ID” and “returns acceptance only after commit”); assessment EX-1 and sample solution. The lesson does not explicitly connect the two rules when the retry encounters an original request still in flight or an uncertain commit: finding or claiming an identity alone is not proof that its job and runnable intent committed. A learner tracing a lost response needs to know that the retry waits for or verifies the same durable transaction before returning acceptance, and must not report acceptance based on an uncommitted claim. The practical exercise asks how a retry finds the same operation, so the omission leaves the failure trace underspecified. Add that verification/wait and outcome for an aborted original transaction to A, with the same durable acceptance contract on retry as on the original response; reflect it in the sample solution or rubric.

**M07-L01-P2 — Major, open — the exercise adds admission requirements without teaching or grading their concurrency implications.** Location: lesson D, first paragraph; assessment EX-1, sample solution and “Failure reporting and admission” rubric. D says to bound accepted pending work and reject before acceptance, but does not explain how concurrent new requests avoid oversubscribing the bound or how a retry of already accepted work is treated at a full limit. The sample solution introduces an atomic capacity reservation and returning the existing job when admission is full, yet the two-point criterion merely says “Bounds new work and retries,” with no stated expectation for either behavior or equivalent valid designs. Learners cannot reliably infer the expected admission trace or assess their answers. Teach a brief identity-before-new-admission decision and an atomic or equivalently coordinated reservation tied to durable acceptance, and make the rubric accept equivalent designs while identifying the full-budget retry and concurrency expectations.

## Pedagogical assessment and sequence

The motivating render case connects acceptance, execution, duplicate-safe effects and durable status. The companion is separate, supplies six explained checks and a scored practical exercise, and offers a worked trace with permanent and transient failure. The exercise supports multiple implementation choices only if the revised rubric makes required observable properties clear (P2). Prerequisite M03-L03 is declared, and the pointers to M03-L01 and M07-L02 distinguish further ownership and overload detail; no material filler or embedded quiz was found. The concise case examples use the shared mechanism rather than duplicating full case studies. There is no identified core source-topic omission; the material gaps above affect the application and assessment of the taught contract.

## Verdict

**revise** — M07-L01-P1 and M07-L01-P2 are open major findings. This review is not technical, source-rights, human, or publication approval.

## Targeted revision 1 re-review — `9a74022`

The revised lesson and assessment retain the assigned source coverage dispositions above. PR-H138's retry qualification is now taught, and PR-H142's admission decision now includes the concurrency and full-budget retry behavior. Findings P1 and P2 are resolved:

- **M07-L01-P1 — Major, resolved.** Lesson A now says a retry must “wait for or verify that its job and outbox committed before returning acceptance” when the original transaction is in flight or uncertain, and may attempt a new claim if it aborted. EX-1's sample solution and durable-acceptance criterion require the same commit verification and aborted-original handling. This supplies the same durable acceptance proof for retry and original.
- **M07-L01-P2 — Major, resolved.** Lesson A teaches coordinated new reservations, rollback at capacity, and matching retries returning the committed job without a second slot; D repeats the full-budget distinction. The sample solution traces those cases, and the admission criterion accepts equivalent designs that prevent oversubscription and return an existing committed job at capacity.

**M07-L01-P3 — Major, open — the revised exercise grades transport-specific details without choosing a transport.** Location: assessment EX-1 prompt, sample solution, and durable-acceptance and worker-trace rubric criteria. The prompt describes an abstract document service and asks for a publish and worker retry; it does not choose a broker or transport. Yet full credit requires handling “misrouting” and redelivery “using the current receipt handle,” while the lesson explicitly scopes receipt handles to its SQS Standard example and mandatory returns to a RabbitMQ 4.2 single-route example. A valid design using one of these transports or another taught contract cannot infer that it must satisfy both products' specific mechanics. State the intended transport and applicable routing assumptions in EX-1 and align the rubric with that contract, or grade equivalent transport-specific handoff and acknowledgement evidence according to the learner's declared choice; preserve the separately taught RabbitMQ and SQS checks.

## Latest verdict

**revise** — P1 and P2 are resolved; P3 is an open major assessment-fairness finding. This review is not technical, source-rights, human, or publication approval.

## Targeted revision 2 re-review — `349c588`

- **M07-L01-P3 — Major, resolved.** EX-1 now declares an SQS Standard queue and configured queue URL. Its sample solution sends the stable job ID to that queue, retains failed or uncertain sends for retry, and deletes redeliveries with the current receipt. The durable-acceptance and worker-trace rubric criteria now match that declared contract; RabbitMQ mandatory-return reasoning remains separately scoped to Q4. Lesson A teaches confirmed handoff and uncertain retries, and the SQS crash trace teaches the current receipt handle.
- **M07-L01-P1 — Major, remains resolved.** Lesson A still requires waiting for or verifying the job and outbox commit before retry acceptance and permits a new claim after abort; EX-1's sample solution and durable-acceptance rubric retain these expectations.
- **M07-L01-P2 — Major, remains resolved.** Lesson A still coordinates concurrent reservations and returns a committed matching retry without another slot at capacity; EX-1's sample solution and admission criterion preserve these requirements and accept equivalent designs.

## Latest verdict

**ready-for-human-review** — P1, P2 and P3 are resolved within the assigned targeted pedagogy and coverage scope. This review is not technical, source-rights, human, or publication approval.
