# M09 independent technical and provenance synthesis

Stage B initial review, 2026-11-26. Reviewed the integrated brief, solution/rubric, decision summary, evidence, taught-topic map and outcome portfolio on `codex/drafts-sda-ms05`, after successful integration handoff and accepted Stage A reports for all three M09 lessons (latest report handoff before this review: `942b7a8`). This review uses the accepted lesson decisions and examines only integration contracts and cross-lesson effects. It does not repeat their complete factual or assessment audits. No prior official M09 module verdict or correction round is assumed.

## Open finding

| ID | Severity | Status | Exact location and impact | Required correction and primary evidence |
| --- | --- | --- | --- | --- |
| M09-SYN-T1 | major | open | `modules/m09/integrated/solution-rubric.md:17–18,26,52`, worker→result-store and API→result-store paths; related brief §Trust boundaries and decision-summary queue boundary. The answer names only “protected access”/a requester recheck for these new network links, while it explicitly specifies TLS and principals for database/queue links. Tenant reports and access credentials can therefore traverse an unspecified channel or reach an unverified result endpoint despite a correct object check. The rubric enumerates queue/worker/DB protection but does not require result-store transport or workload admission. This leaves a confidentiality and origin boundary incomplete in the reference design. | Specify encrypted channels with intended result-store peer verification for **both** clients, authenticate their service identities, scope worker writes and API reads to the intended tenant/job result, and stop transfer on failed transport, identity or permission checks. Preserve fresh end-user authorization at release. Carry the same contract into prompt, diagram, ledger, evidence and grading. Equivalent locally enforced stores may state an explicit non-network boundary. [OWASP TLS, Use TLS For All Pages/API-only endpoints](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-tls-for-all-pages), [Correct Domain Names](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-correct-domain-names), [Authorization, per-request checks](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request). |

This is a bounded integration correction. The accepted lessons need no material edit to resolve it. It does not require a new vendor choice, workflow stage or whole-module regeneration.

## External correction and cross-lesson checks

| Reviewed assertion | Independent disposition and evidence |
| --- | --- |
| `MS05-M09-SYN-01`, queued-report authority and worker database path | Original identified gap **resolved in the present text**: brief lines 14/25, solution lines 24–26 and the queue decision row bind trusted requester/tenant/action, restrict producer and consumer, require current execution/retrieval authorization, tenant-constrained reads and worker-specific DB TLS/account. Membership failure is fail closed; enqueue approval is not permanent authority. [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request), [Database Security, transport/authentication/permissions](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html#implementing-transport-layer-protection) were opened independently. T1 is the remaining adjacent result-store boundary, not a rejection of that completed worker correction. |
| User versus workload identities | Bo's issuer-scoped subject remains separate from proxy/API/worker credentials. Tenant C membership cannot authorize D's record; lookup failure is not permission. These assumptions match accepted M09-L01. The proxy treatment agrees with [RFC 9700 §4.13](https://www.rfc-editor.org/rfc/rfc9700.html#section-4.13). No general JWT-profile or database-product guarantee was inferred. |
| Report diagnostic and user-success contracts | The exclusive intervals sum to 1,200 ms and queue wait is 760 ms; the enclosing parent is not added again. The five-minute original cohort totals 1,000 and has 930 on-time correct client receipts, so 93% misses 99%. Retry IDs, first ingress, receipt validation, deadline follow-through and failed/late originals agree with accepted M09-L02. Its bounded-clock prerequisite remains applicable. The competing worker/database hypotheses require cohort and controlled-intervention evidence. [Google SRE SLOs](https://sre.google/sre-book/service-level-objectives/#indicators-in-practice), [SLI implementation](https://sre.google/workbook/implementing-slos/#moving-from-sli-specification-to-sli-implementation). |
| Storage fence, quorum and recovery | The solution requires confirmed durable fence 42 before W2 writes, serialization with tenant mutations, rejection of delayed 41 after the fence, explicit pre-fence exposure and refusal after unknown installation. B+C authority is conditional on the stated quorum and resource availability. Shared dependencies and restoration are not equated with an election. These connections preserve accepted M09-L03 and M09-L02; [Chubby §2.4](https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows_html/) independently supports the delayed external-request problem. |

## Pinned-source locator dispute

The author disposition `MS05-COV-01` was independently checked for the **26 M09 rows only**, using GitHub's raw UTF-8 file contents at Primer commit `ae9bbd7b02d90b9866215de185217d33f39ab733`. Counting physical lines gives 1,840 README lines. The web tool's extracted text had fewer lines; those extraction labels are not repository `#L` anchors. All M09 locators resolve to the assigned source topic. No approved curriculum mutation is warranted by the line-number dispute.

| Pinned file | Verified physical locators in M09 |
| --- | --- |
| [README](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md) | Security at 1560; body topics at 1566–1569; Spanner 1706; Chubby 1713; Dapper 1714; ZooKeeper 1716. The shared topic row also uses 1566. |
| [pastebin](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/pastebin/README.md) | Security/Ongoing: 321/329 |
| [twitter](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/twitter/README.md) | 322/330 |
| [web_crawler](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/web_crawler/README.md) | 342/350 |
| [mint](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/mint/README.md) | 430/438 |
| [social_graph](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/social_graph/README.md) | 338/346 |
| [query_cache](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/query_cache/README.md) | 295/303 |
| [sales_rank](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/sales_rank/README.md) | 327/335 |
| [scaling_aws](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/solutions/system_design/scaling_aws/README.md) | 392/400 |

This is source-location verification, not a second lesson-depth audit. Teaching/outcome coverage decisions rely on accepted Stage A and the separate synthesis pedagogy report. The portfolio preserves six lesson outcomes and M09-S1; its M09-L03-LO2 teaching-section list should be reconciled with the newly expanded companion map during integration correction, without changing outcome scope.

## Provenance and limits

Donne Martin's *System Design Primer* is the [pinned topic map](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). OWASP, IETF, Google SRE and research papers provide factual references. The merchant data, text flow, request counts and failure scenario are original synthetic material; no imported third-party figure/code, private data, benchmark, endorsement or certification was identified. The integrated evidence reuses accepted lesson source packs and explicitly treats queue/gateway enforcement as application design choices. No source-rights blocker was identified.

No runtime, load, restore or failure-injection test was executed by this reviewer; the proposed drills remain plans. An attempted NIST SP 800-207 fetch timed out and was not used as evidence. Self-review and author-side correction records were not counted as independent verdicts.

## Verdict

`revise` — resolve open major M09-SYN-T1, then targeted independent re-review of the changed integration and companion effects. This is not human approval to publish or merge.


## Round 1 targeted independent synthesis re-review — 2026-11-26

Reviewed pushed integration correction `785bfca`. Scope is M09-SYN-T1, the changed security/rubric/evidence passages, two portfolio section additions and nearby interactions. Accepted unchanged Stage A content was reused; no full lesson re-audit occurred. The initial finding and verdict above remain historical.

| ID | Current status | Exact resolution evidence | Independently reopened primary sources |
| --- | --- | --- | --- |
| M09-SYN-T1 | resolved | Brief lines 14/25 now requires both result-store links and their failure policy. Solution diagram lines 17–19 separates worker upload, API retrieval and end-user release; paragraph 27 requires TLS, intended-store identity verification, distinct authenticated worker-write/API-read principals scoped to the tenant/job, and no transfer after failed checks. It explicitly preserves fresh end-user authorization. The decision summary's boundary paragraph and queue row, new integrated evidence row and security rubric line 51 carry the same contract. | [OWASP TLS, API endpoints](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-tls-for-all-pages); [intended domain names](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html#use-correct-domain-names); [OWASP per-request authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html#validate-the-permissions-on-every-request) |

The fix remains an explicit application contract, without promising automatic queue/store-vendor enforcement. It preserves the original queued-job correction's producer/consumer restriction, current worker authorization, tenant-constrained DB reads and separate DB identity. Workload permission is not treated as end-user authorization. No adjacent security contradiction was found.

The revised diagnostic answer and rubric line 52 now explicitly grade the five-minute first-ingress cohort, two-second client-validation endpoint, all original failure/late groups and **930/1,000 = 93% versus 99%**. The eight exclusive intervals still total 1,200 ms, with queue wait 760 ms. These are consistent with the accepted M09-L02 measurement contract, not claimed benchmark results.

The portfolio adds “Measure the original request” for M09-L02-LO2 and “Chubby and ZooKeeper solve coordination, not arbitrary storage fencing” for M09-L03-LO2. Both are existing accepted teaching sections already used by their companions. No new outcome or product claim was introduced. The fence/quorum/recovery passages and source locator map are unchanged by this correction; their initial synthesis conclusions remain applicable.

No new factual, source-rights or companion regression was identified. No runtime, load, restore or fault-injection test was executed. The current review has **no open technical/provenance blocker, major or minor finding**.

### Final verdict

`ready-for-human-review`

This clears the bounded independent synthesis review only; human merge/publication approval remains separate.
