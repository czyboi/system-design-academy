# M09-L03 independent technical and provenance review

Initial Stage A review, 2026-11-26, after scoped draft handoff `f921f8c`. Scope: canonical lesson, assessment and evidence, task SD-M09-L03, approved SDA-v1 M09-L03 outline and its three assigned architecture topics. Audience: middle/senior engineers. This reviewer is independent of the author and pedagogy reviewer; self-review was not accepted as QA evidence.

## Findings

| ID | Severity | Status | Location and finding | Evidence and required correction |
| --- | --- | --- | --- | --- |
| M09-L03-P1 | minor | open | Lesson line 61 and evidence C2 cite `https://zookeeper.apache.org/doc/current/recipes.html`, which returned 404 on both independent opens. The factual recipe is supported by the versioned Apache page, but the learner cannot follow the cited route and the evidence calls it verified/current. | Replace with [ZooKeeper 3.9.4 Recipes, Locks and Recoverable Errors](https://zookeeper.apache.org/doc/r3.9.4/recipes.html#sc_recipes_Locks), checked during this review. State the pinned documentation version, not a floating current path. The session claim can additionally cite [3.9.4 Programmer's Guide, Sessions](https://zookeeper.apache.org/doc/r3.9.4/zookeeperProgrammers.html#ch_zkSessions). |

No open technical blocker or major was identified. P1 is a source-route defect, not evidence that the ZooKeeper mechanism is false.

## Independently checked mechanisms and boundaries

- The five-step 41→42 takeover establishes its barrier at protected storage before the replacement writer mutates state. Durable `max_epoch`, serialization of installation with mutations, writer authorization, non-reused epochs, relevant-partition coverage and same-epoch duplicate/version checks are explicit. The lesson admits the pre-installation stale-write window and refuses replacement writes after unknown installation. These are scenario contracts, not a claim that a coordination product automatically fences another store. [Chubby, §2.4 Locks and sequencers](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/) provides the primary delayed-request rationale. The diagram and Q1–Q3/EX-1 agree with that boundary.
- The verified [ZooKeeper 3.9.4 lock recipe](https://zookeeper.apache.org/doc/r3.9.4/recipes.html#sc_recipes_Locks) supports ephemeral sequential contenders, predecessor watches and GUID recovery after uncertain creation. [Sessions](https://zookeeper.apache.org/doc/r3.9.4/zookeeperProgrammers.html#ch_zkSessions) supports ephemeral removal on expiry. The lesson correctly treats external fencing and sequence reuse after namespace restoration as separate application obligations.
- Three-voter two-of-three arithmetic is consistent with the assumed configuration. Minority refusal, election interruption and majority-loss write unavailability match [etcd v3.6 Failure modes, Leader failure / Majority failure / Network partition](https://etcd.io/docs/v3.6/op-guide/failures/). Shared-failure warnings and no TTL-only failover promise appropriately limit the availability inference. Coordinator recovery is not equated with database restoration.
- [Spanner's publisher record](https://research.google/pubs/spanner-googles-globally-distributed-database-2/) and [publisher-hosted paper, TrueTime and timestamp assignment](https://storage.googleapis.com/gweb-research2023-media/pubtools/1974.pdf) support synchronous replication, bounded clock uncertainty and commit wait. The latter publisher download is the expanded TOCS 2013 paper; its §§3 and 4.1.2 describe the relevant mechanism. [Current Cloud documentation, External consistency](https://docs.cloud.google.com/spanner/docs/true-time-external-consistency#external_consistency) confirms the serializable isolation boundary. No worker lease is represented as a cross-record transaction system.
- Lesson lines 84–88 and EX-1 specify original valid requests, ingress window, five-second deadline and rejected/failed/late/stale failures. A managed cohort and [M09-L02's explicit client-receipt join](../../../../lessons/M09-L02.md) supply the prerequisite measurement contract. The 99% target and time bounds are declared synthetic. [Google SRE SLOs](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice) supports user-oriented measurement, not those invented thresholds.

The textual trace and conditional-update suggestion are illustrative and untested. No database code, product integration, clock-fault experiment, region drill or benchmark was executed. Readiness cannot be inferred from those absent experiments; the package does not claim otherwise.

## Source and asset ledger

| Material | Role and rights disposition |
| --- | --- |
| Donne Martin, *System Design Primer*, pinned `ae9bbd7b02d90b9866215de185217d33f39ab733` | Licensed topic map for PR-ARCH-SPANNER, PR-ARCH-CHUBBY and PR-ARCH-ZOOKEEPER, mapped by approved `curriculum/revision-1/coverage.csv`. [Source](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The package uses original tenant data, prose and trace, with no detected close adaptation or imported asset. |
| Burrows/USENIX, Apache ZooKeeper, etcd project, Google Spanner papers/docs and Google SRE | Factual references only. Version/historical scope is explicit except for the floating broken ZooKeeper route in P1. No large quotation, third-party figure or implementation code is imported. |
| Tenant identifiers, epochs, timeline, text diagram and exercise | Original synthetic Academy material. No private learner data, claimed benchmark, affiliation, certification or permission is asserted. |

## Verdict

`revise` — correct the minor P1 citation route and version scope. No unresolved technical blocker/major or asset-rights ambiguity was found. This verdict is not publication approval.


## Round 1 targeted independent re-review — 2026-11-26

Reviewed pushed correction `c21e9f8`: the P1 citation change, added measurement scenario, outcome map and their immediate lesson/assessment dependencies. The accepted unchanged coordination/Spanner explanations were not re-audited.

| ID | Status | Verified correction | Exact evidence |
| --- | --- | --- | --- |
| M09-L03-P1 | resolved | Lesson line 61 now pins Apache's 3.9.4 recipe. Evidence C2 pins the same version and links its session contract. Both primary pages were independently reopened and support the limited recipe/session claims already reviewed. | [ZooKeeper 3.9.4 Locks](https://zookeeper.apache.org/doc/r3.9.4/recipes.html#sc_recipes_Locks); [ZooKeeper 3.9.4 Sessions](https://zookeeper.apache.org/doc/r3.9.4/zookeeperProgrammers.html#ch_zkSessions) |

The revised EX-1 gives mutually exclusive outcomes totaling 1,000: 970 on time, 10 late, 10 rejected, five timed out and five stale. Its sample correctly computes 97%, below 99%, and retains every original in the denominator. The ten-minute ingress cohort, first-ingress start, client-validated durable/current result endpoint and five-second deadline are consistent across prompt, answer and rubric. Admitted-only latency cannot certify this objective. M09-L02's declared prerequisite supplies the bounded-clock/receipt reconciliation contract; these values remain scenario assumptions, not vendor performance guarantees. See [Google SRE, Indicators in Practice](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice) and [SLI implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation).

The expanded outcome map changes no product claim. The takeover still requires a durable fence before new writes and preserves pre-fence and unknown-installation limitations. No new source, arithmetic, companion or rights regression was found. No runtime test or failure drill was executed. No open technical/provenance finding remains.

### Final verdict

`ready-for-human-review`
