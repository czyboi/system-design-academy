# M07-L03 independent coverage and pedagogy review

Reviewed lesson-mode combined assignment at `88eb08d` for English-speaking middle/senior engineers. Inputs: SD-M07-L03 spec, approved curriculum and coverage inventory, canonical lesson, assessment and evidence. The topic map is [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733) at `ae9bbd7b02d90b9866215de185217d33f39ab733`; the accepted global inventory is reused for this lesson's assigned row.

## Coverage matrix

| Source topic and locator | Lesson / outcomes and actual instruction | Status | Assessment and disposition |
| --- | --- | --- | --- |
| PR-ARCH-KAFKA, Kafka architecture mechanism, README L1715 | M07-L03 LO1/LO2: “Choose the delivery and ordering unit” explains historical partition reads and offsets, independent groups, current Kafka assignment and durability choices; “Replay into a new index” and “Repair an incomplete history” apply replay and retention | taught | Q1–Q6 and EX-1 assess positions, replay, ordering and retention. No assigned source-row gap; P1 concerns the depth of the Academy-added repair procedure. |

The approved additions—transactional outbox, duplicate-safe effects, source revisions and reconciliation—appear in the lesson. LO1 is assessed through Q1–Q3 and EX-1; LO2 through Q4–Q6 and EX-1. The illustrative scenario makes no SLO claim.

## Findings

**M07-L03-P1 — Major, open — repairing the missing history names a boundary but does not teach how to establish one.** Location: lesson “Repair an incomplete history,” last paragraph; assessment EX-1 and “Repair and cutover” rubric. The lesson says to take “a newer snapshot with its corresponding source and log boundary” or reconcile while “capturing overlapping changes,” then resume after “proving coverage.” It does not show how a snapshot's represented source changes are related to replay positions when changes and outbox publication continue, nor how overlap and removals are resolved. A learner cannot reproduce a safe repair from the instruction or know what evidence demonstrates coverage; EX-1 nevertheless requires recovery after its saved cursor is lost and full credit requires state paired with its continuation. Add one concrete recovery protocol with its consistency and concurrency assumptions: show how a state snapshot and a safe replay boundary are obtained, how intervening changes and deletions are covered, and what observable evidence permits cutover. Align the sample and rubric with equivalent valid repair approaches.

**M07-L03-P2 — Minor, open — the assessment's record semantics are ambiguous.** Location: assessment EX-1, P0:14 and P1:8. The prompt labels P0:12 a “full update” but says P0:14 “changes” M and P1:8 “updates” K. The taught highest-revision guard works for complete replacement records, while the lesson expressly says deltas require ordered, gap-detecting processing. Without specifying those two records' form, a learner cannot tell whether to use the sample solution's revision guard or design a delta replay. State that all non-delete events in EX-1 are complete searchable replacements, or explicitly provide the delta ordering assumptions and accept an appropriate trace.

## Pedagogical assessment and sequence

The outage motivates independent consumer groups and replay. The trace shows positions per partition, duplicate application after a checkpoint failure, a deletion marker and a separate generation. The separate companion contains six explained checks, an exercise, a points rubric and outcome map; its main replay and messaging-choice criteria follow taught content, while repair remains under-specified as described in P1. Prerequisite M07-L02 is declared and replay traffic is bounded by reference to that lesson. The retained log versus work queue comparison and hot-key limitation support LO2 without elementary filler. No embedded quiz or material assigned-source omission was found.

## Verdict

**revise** — M07-L03-P1 is an open major finding and P2 an open minor finding. This review is not technical, source-rights, human, or publication approval.

## Targeted revision 1 re-review — `96b2258`

- **M07-L03-P1 — Major, resolved.** “Repair an incomplete history” now records and protects consumer-readable partition ends before taking a consistent authority snapshot with deletion revision markers, replays overlap from that earlier vector under revision guards, and validates against a fenced cutover barrier. It states committed-only publication, retention and full-value assumptions. Q6 and EX-1's sample and repair criterion use that protocol while the rubric accepts equivalent proven coverage.
- **M07-L03-P2 — Minor, resolved.** EX-1 now says all non-delete events are complete searchable replacements, including M and K, so the taught highest-revision guard applies.
- The assigned PR-ARCH-KAFKA coverage and outcome map remain intact. The revised worked trace gives the generation its own stored positions and specifies restart and fencing, making the crash trace reproducible under its stated assumptions.

**M07-L03-P3 — Major, open — a new full-credit comparison is absent from EX-1's request.** Location: assessment EX-1 and “Messaging choice” rubric. EX-1 declares a delete-only topic and an out-of-order relay, then asks learners to defend a log or queue and describe hot-key parallelism. The rubric additionally requires explaining “delete-only retention versus unsafe out-of-order compaction,” although the prompt never asks to evaluate a compacted topic. A correct log-versus-queue and hot-key answer can satisfy the stated task yet lose credit for this additional comparison. Ask explicitly whether a compacted topic is safe under the stated ordering and why, or remove that comparison from the full-credit criterion while retaining the independently taught concept.

## Latest verdict

**revise** — P1 and P2 are resolved; P3 is an open major assessment-fairness finding. This review is not technical, source-rights, human, or publication approval.

## Targeted revision 2 re-review — `526ddd2`

**M07-L03-P3 — Major, resolved.** EX-1 now explicitly asks learners to “compare delete-only retention with compaction under the stated out-of-order relay.” The messaging-choice criterion assesses that comparison along with independent progress and ordering or hot-key cost. “Repair an incomplete history” teaches the relevant delayed older revision after a deletion and the resulting compaction risk; the sample solution applies it to the exercise. The affected PR-ARCH-KAFKA retention and replay coverage remains taught, and the separate outcome map remains coherent.

## Latest verdict

**ready-for-human-review** — P3 is resolved; P1 and P2 were resolved in revision 1. This review is not technical, source-rights, human, or publication approval.

## Learner-first pilot re-review — `317a303`

The lesson-first pass used the current lesson and declared prerequisite M07-L02, including its M07-L01 prerequisite, before consulting the companion. The assigned source row remains **taught** in “Choose the delivery and ordering unit” and the replay and repair sections. The approved `PR-ARCH-KAFKA` mapping is `curriculum/revision-1/coverage.csv` at README.md L1715 in the pinned [System Design Primer revision](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1715). The curriculum's Academy additions remain taught through the outbox publication and retained-continuation repair examples. No assigned coverage regression was found.

Compared with `main` at `dc80848`, the pilot makes the search-versus-notifications motivation and independent progress explicit, introduces the snapshot-and-position replay contract before production details, places lost-cursor repair before the compaction caveat, and closes with decision criteria. The offset trace and repair assumptions remain present. The learner can follow why a saved position and durable effect belong together and why a missing continuation requires a fresh baseline. The following required dependency still interrupts the recovery reasoning.

**M07-L03-P4 — Major, open — the fencing required for a safe replay and cutover is not explained.** Location: lesson “Replay into a new index,” paragraph starting “A saved index snapshot,” then the “For cutover” paragraph. The first paragraph instructs the reader to “fence workers that lose assignment” without explaining what fencing prevents or how a stale worker is denied effect and checkpoint writes after reassignment. The later cutover instruction likewise requires permanently fencing old index writers without teaching how to establish that previously active writers can no longer publish or why merely capturing an end vector while they can still publish is insufficient. Neither M07-L02 nor M07-L01 supplies this dependency. A reader can reproduce the happy-path offset arithmetic but cannot independently reconstruct the stated ownership and cutover safety contract in LO1 or defend its operational cost in LO2. Explain the stale-owner race and a concrete enforcement contract, including rejection of stale owners at the relevant effect and checkpoint boundaries and settlement of in-flight writes before the served-effect barrier. Distinguish the required guarantee from any implementation-specific mechanism, and cite evidence for material technical details. The approved scope and outcomes appear in `curriculum/revision-1/CURRICULUM_MASTER.md` under M07-L03.

**M07-L03-P5 — Minor, open — the partition model is introduced through Kafka terminology before it is named as an ordered part of a log.** Location: lesson “Choose the delivery and ordering unit,” second paragraph. A short explanation that each partition is an independently ordered sequence would connect per-partition assignment and next positions to the P0/P1 trace more directly. The subsequent paragraph states append order within a partition, so the trace remains followable.

After the lesson-first pass, the unchanged companion was checked for compatibility. Its six explained checks and exercise still map to both outcomes, and EX-1 requires the same fenced cutover condition. The assessment's sample uses fencing as an instruction and therefore does not supply the missing lesson mechanism in P4. Earlier findings P1, P2 and P3 remain resolved by the existing changes.

## Pilot verdict

**revise** — P4 is an open major pedagogical finding. P5 is a local clarity improvement. This verdict does not assert technical, rights, human, or publication approval.

## Pilot targeted revision 1 re-review — `a600734`

- **M07-L03-P4 — Major, resolved.** In “Replay into a new index,” the lesson now shows a delayed old-owner write arriving after reassignment, then explains an application-owned epoch contract that closes the old epoch at both index and checkpoint stores, settles admitted writes, and rejects later stale requests before the new owner proceeds. The cutover paragraph separately explains closing the served generation and settling admitted effects before capturing the barrier, including the late-visible-effect failure. These explanations allow the learner to reconstruct the role of fencing in the existing replay and cutover trace. The Chubby sequencer reference identifies a related resource-side mechanism without making it the only implementation. [Chubby §2.4](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf#page=5).
- **M07-L03-P5 — Minor, resolved.** “Choose the delivery and ordering unit” now defines a partition as an independently ordered sequence before explaining group assignment and next positions.

The correction to the repair introduction supplies a concrete missing-update example and places protection of the continuation before the source snapshot, matching the worked repair. The revised position-20 wording identifies where the example contains a record and remains consistent with the subsequent discussion of offset holes. The lesson-first pass found no new missing causal dependency in the touched passages. The unchanged assessment's EX-1 and rubric still follow the taught trace and cutover contract. Assigned Kafka, replay, retention, ordering and outbox coverage remains present, and P1–P3 remain resolved. The pilot's progressive explanation supports the same two approved outcomes.

## Latest pilot verdict

**ready-for-human-review** — P4 and P5 are resolved and no open blocker or major pedagogy or assigned-coverage finding remains. This verdict concerns teaching and coverage.
