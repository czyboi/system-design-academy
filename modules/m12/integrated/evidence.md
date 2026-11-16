# M12 integration source evidence and rights

Checked 2026-11-16. M12-S1 is the approved parking extension in [curriculum/revision-1/CURRICULUM_MASTER.md](../../../curriculum/revision-1/CURRICULUM_MASTER.md). The example rows, vehicle IDs, three-spot truck rule, races, probabilities and outcome cohort are original exercise assumptions, **not** claims about a real facility.

| Mechanism | Evidence and applicability |
| --- | --- |
| Parking allocation's compatibility, contiguous bus and release invariant | [M12-L03](../lessons/M12-L03.md) and [evidence](../evidence/M12-L03.md). Database transactions or one local owner lock can implement a coherent transition; no real platform executed. |
| Conditional state transitions and identity-bound retries | [PostgreSQL 17 isolation](https://www.postgresql.org/docs/17/transaction-iso.html), [AWS idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). These describe architectural mechanisms, not an assertion that an actual parking system runs PostgreSQL. |
| Neighboring object designs | M12-L01 [evidence](../evidence/M12-L01.md), L02 [evidence](../evidence/M12-L02.md), L04 [evidence](../evidence/M12-L04.md), L05 [evidence](../evidence/M12-L05.md), L06 [evidence](../evidence/M12-L06.md). Individual companion exercises grade their own outcomes. |

No third-party code or art copied. No executable scenario, concurrent allocation test, scoped Python checker, official independent per-lesson review, Stage B or human approval occurred here. Claims and topic mapping still require independent QA.
