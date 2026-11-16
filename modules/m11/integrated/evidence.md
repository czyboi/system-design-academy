# Source evidence — M11 integration

Checked 2026-11-16 against the approved SDA-v1 outline, all nine canonical M11 lesson/evidence/assessment packages on the branch, and the bounded primary references below. All work rates, thresholds, key labels, two-region failure timing and scores are **synthetic exercise parameters**, not measured throughput or published SLOs.

| Decision | Evidence and applicability |
| --- | --- |
| ID range non-reuse and stale issuer protection | [M11-L05 lesson](../lessons/M11-L05.md), [M11-L05 evidence](../evidence/M11-L05.md), [M09-L03 storage-side fencing](../../m09/lessons/M09-L03.md) (upstream in unmerged MS05 PR #100). Treat external fencing and range burn as design mechanisms, not proven installed software. |
| Global rolling quota and original-operation receipt | [M11-L06 lesson](../lessons/M11-L06.md), [M11-L06 evidence](../evidence/M11-L06.md), [Redis rate-limit techniques](https://redis.io/docs/latest/develop/use-cases/rate-limiter/), [RFC 6585 §4, 429](https://www.rfc-editor.org/rfc/rfc6585.html#section-4). A fixed window or per-gateway counter does not establish the synthetic strict rolling claim. |
| Durable acceptance and scope of idempotent retry | [AWS Builders' Library, Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), [M03-L02](../../m03/lessons/M03-L02.md). Stable input-bound receipt and canonical original identity are deliberate application requirements. |
| Other specialised domains and non-overlapping decisions | Refer to individual [M11-L01](../evidence/M11-L01.md), [L02](../evidence/M11-L02.md), [L03](../evidence/M11-L03.md), [L04](../evidence/M11-L04.md), [L07](../evidence/M11-L07.md), [L08](../evidence/M11-L08.md), [L09](../evidence/M11-L09.md) evidence matrices. Each companion retains assessment of its two LOs; the integration is intentionally restricted to M11-S1. |

## Rights and remaining independent checks

All scenario text, diagrams, numeric examples, decision table and rubric are original. No copied vendor implementation, third-party asset, or unsupported legal license claim. Independent Sol/Terra per-lesson Stage A and module Stage B gates **pending**; the nine lesson source claims and the integration have not been independently certified. No Python format/content/coverage/regression validator or repository draft-handoff command executed here. Upstream MS05/MS06 references remain unmerged and may change; Codex must reconcile them before QA clearance.
