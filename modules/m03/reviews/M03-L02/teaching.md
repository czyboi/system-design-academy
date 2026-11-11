# M03-L02 actual coverage and pedagogy review

## Scope and sources

Reviewed the English draft and companion for middle and senior engineers against the approved SDA-v1 outline, approved inventory and coverage matrix. Inspected the [main Primer communications sections](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1455-L1544) and all eight Communications locators below at revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. Each solution's source section gives the same composition prompts for public HTTP/REST, internal RPC and service discovery. The Academy lesson explains the common mechanism once, then applies it to original examples for the eight settings. The table names the shared explanatory sections where related topics merge.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
| --- | --- | --- | --- |
| PR-H150 | RPC path and interface choices | taught | README.md#L1455. Operation, arguments, generated stubs, transport, dispatch and observable remote errors are distinguished. LO1 Q2 and EX-1 require the round trip. |
| PR-H151 | RPC path and interface choices | taught | README.md#L1497. Explains schema and release coupling, per-operation contracts, protocol-aware debugging and explicit response caching. LO2 Q6 and EX-1 apply the trade-offs. |
| PR-H152 | Resource interfaces and REST constraints | taught | README.md#L1504. States client/server, stateless/cache, layered and uniform-interface constraints with optional code on demand, then distinguishes resource and representation. Q1 and Q4 use the status-link example and the uniform interface. |
| PR-H153 | RPC path and interface choices | taught | README.md#L1526. Explains multi-request nesting, old-client payload growth, composite and cursor alternatives, and a collection filtered by update cursor versus an event-oriented operation. LO2 Q6 tests the cost. |
| PR-H154 | Worked example | taught | README.md#L1533. The same export workload exposes a public creation/status resource and an internal StartExport operation with different contracts. EX-1 transfers both shapes. |
| PR-PASTEBIN-H020 | Applying the decision to other workloads | merged | solutions/system_design/pastebin/README.md#L314. The shared composition trace applies to snippet creation by public resource URI and a storage call by stable snippet ID. The stable ID supports resolving an ambiguous result. |
| PR-TWITTER-H020 | Applying the decision to other workloads | merged | solutions/system_design/twitter/README.md#L315. The activity-feed sketch uses a paged public collection and a bounded internal timeline read with a deadline. Endpoint ownership and failure policy come from the shared composition trace. |
| PR-WEB_CRAWLER-H021 | Applying the decision to other workloads | merged | solutions/system_design/web_crawler/README.md#L335. The sketch separates a crawl-job progress resource from job-ID scheduling and explains why discovery can replace a stopped worker. |
| PR-MINT-H020 | Applying the decision to other workloads | merged | solutions/system_design/mint/README.md#L423. The sketch exposes timestamp and currency on a public summary, with an authorized account scope and explicit partial failures for internal aggregation. The shared trace supplies the endpoint decision. |
| PR-SOCIAL_GRAPH-H017 | Applying the decision to other workloads | merged | solutions/system_design/social_graph/README.md#L331. The sketch separates a public connections collection from a bounded GetConnections operation and explains the need to avoid an unbounded traversal response. The shared trace supplies the endpoint decision. |
| PR-QUERY_CACHE-H020 | Applying the decision to other workloads | merged | solutions/system_design/query_cache/README.md#L288. The sketch shows the public query/filter identity and the tenant-scoped Lookup key, which protects caller isolation. The shared trace supplies the endpoint decision. |
| PR-SALES_RANK-H018 | Applying the decision to other workloads | merged | solutions/system_design/sales_rank/README.md#L320. The reporting window is visible on the public ranking resource and carried in the internal operation to avoid mixing periods. The shared trace supplies the endpoint decision. |
| PR-SCALING_AWS-H043 | Applying the decision to other workloads | merged | solutions/system_design/scaling_aws/README.md#L385. Shows why the public catalogue resource remains stable when inventory deployment changes, while internal discovery ownership and timeout behavior must be made explicit. |
| PR-BODY-R1-RPC-PATH | RPC path and interface choices | taught | README.md#L1468. Traces client marshal, transport, server unmarshal and dispatch, and result or error in reverse. LO1 Q2 and EX-1 directly assess the steps. |
| PR-BODY-R1-RPC-SDK | RPC path and interface choices | taught | README.md#L1488. Relates SDK choice to known client platforms and packaging of serialization, authentication and errors, with compatibility and release costs. |
| PR-BODY-R1-REST-IDENTITY | Resource interfaces and REST constraints | taught | README.md#L1510. Explains a stable URI and multiple representations, including representing state and requesting a change. The export scenario gives one resource path and status representation. |
| PR-BODY-R1-REST-SELF | Resource interfaces and REST constraints | taught | README.md#L1512. Explains why method, media type and headers matter in addition to status and applies the distinction in Q4. |
| PR-BODY-R1-REST-HYPERMEDIA | Resource interfaces and REST constraints | taught | README.md#L1513. The representation advertises a status transition and later a download link. The browser shortcut is replaced with the actual interaction constraint. LO1 Q1 and LO2 Q4 assess it. |
| PR-BODY-R1-REST-COSTS | RPC path and interface choices | taught | README.md#L1530. Nested report/section/attachment requests illustrate round trips, and composite representations introduce extra bytes and cache/contract costs. LO2 Q6 transfers this to an older client. |

Pagination with snapshot semantics, optional-field and field-number compatibility, total deadlines, and atomic operation-key recording add the Academy scope. The failed worker A and successful worker B trace in the worked example has the same order and time budget as the linked M03-L03 section. The preview is self-contained, the lesson's declared prerequisites stay unchanged, and the deeper comparison belongs to module synthesis per plan finding N1.

## Pedagogy and language

LO1 proceeds from the public create/status path to stub-level dispatch and then a stale endpoint and an unknown response. LO2 uses the resource/operation comparison, versioning and retry contract, and returns to specific decision criteria in the final section. The small applied cases add concrete contract decisions without requiring later domain modules. The companion has six explained checks and a readable secondary map to exact teaching sections.

EX-1 changes an export into a constrained reservation with old mobile clients, independently replaced inventory instances and a large history listing. Learners design public and internal contracts, trace a response, and address deadlines, unknown results and compatibility with their own assumptions. The rubric covers the transfer even though Q1–Q3 rehearse the lesson's exact example. English prose is appropriate for the audience.

## Findings

- **M03-L02-P1 (minor).** EX-1 requires at most one reservation effect per request. The reference answer explicitly scopes its durable key contract to the documented retention window and asks for stated assumptions, while the lesson already teaches that expiry behavior must be part of the contract. Giving an example of rejecting an expired replay or retaining a permanent operation identity would make the scope easier to grade.
- **M03-L02-P2 (note).** The related discovery trace is self-contained and the link resolves. Labeling it explicitly as a preview in **Worked example** would make the sequencing intent from N1 clearer.

Verdict **ready-for-human-review**.
