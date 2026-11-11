# M01 integrated design revision 1 technical and provenance recheck

Checked 2026-11-11. The verdict binds the brief, solution and rubric, revised decision summary, evidence, pinned curriculum inputs, and revised M01-L02 lesson.

## Technical findings

- **MI-T1 · minor · Solution rubric, Operation histories, fallback lag.** The exercise assumes a conservative lag bound and refuses fallback when the bound is unknown. For an implementation, an authoritative timestamp through which the local projection applied every write could supply evidence for the bound. Include clock uncertainty when judging the proof's age after disconnection. A local applied offset alone does not establish time freshness. [Google SRE Workbook, A Worked Example, freshness and quality indicators](https://sre.google/workbook/implementing-slos/#a-worked-example).

The only decision-summary change is the M01-L02 reference destination. The link resolves to the separately reviewed revision, and its SHA-256 matches the corresponding value in the lesson's accepted technical recheck. That lesson supports the unchanged recommendation to add serving capacity when workers are the bottleneck and verify surviving capacity, balanced routing, and shared dependency headroom. The brief and solution retain the same assumed workload, arithmetic, freshness policy and availability model. Their hashes and the unchanged evidence and curriculum hashes match the first review. [Microsoft Azure Architecture Center, Application design considerations](https://learn.microsoft.com/en-us/azure/architecture/best-practices/auto-scaling#application-design-considerations) · [AWS Well-Architected Framework, REL11-BP05](https://docs.aws.amazon.com/wellarchitected/2022-03-31/framework/rel_withstand_component_failures_static_stability.html).

## Provenance findings

The revised reference points to an original Academy lesson within the repository. Its source citations, attribution and evidence were checked in the lesson's own revision review. The link update introduces no third-party assets or additional claims.

Verdict: **ready-for-human-review**.
