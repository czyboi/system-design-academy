# M03-L02 pedagogy and curriculum coverage review

Reviewed the canonical lesson, companion and evidence in lesson mode after draft handoff at `7459b0a`. The audience is middle and senior engineers. Scope is the [approved M03-L02 outline](../../../../../../curriculum/revision-1/CURRICULUM_MASTER.md#m03-l02) and its 19 rows in the [SDA-v1 coverage map](../../../../../../curriculum/revision-1/coverage.csv). The Primer revision is `ae9bbd7b02d90b9866215de185217d33f39ab733`. The prior archived review provided context for the revised cursor, retention and preview wording. The exact eight case-source sections and the [main communications section](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L1455-L1544) were inspected for assigned topic scope.

## Coverage

| Topic and source locator | Status | Teaching evidence and assessment |
| --- | --- | --- |
| PR-H150, RPC, README.md#L1455 | taught | **RPC path and interface choices** traces operation, stubs, transport, dispatch and return. Q2 and EX-1 trace that path. |
| PR-H151, RPC disadvantages, README.md#L1497 | taught | The same section explains client libraries, version coupling, debugging and explicit cache design. LO2 and EX-1 compare the interface costs. |
| PR-H152, REST, README.md#L1504 | taught | **Resource interfaces and REST constraints** explains resource identity, representations, client/server, stateless, cache, layered and uniform-interface constraints. Q1 and Q4 assess the interaction and constraints. |
| PR-H153, REST disadvantages, README.md#L1526 | taught | **RPC path and interface choices** compares nested-resource trips, composite payloads and narrower requests. Q6 applies these costs to an older client. |
| PR-H154, RPC and REST comparison, README.md#L1533 | taught | **Worked example** combines a public export resource with internal `StartExport` and discovery. EX-1 transfers both contracts to reservation. |
| PR-PASTEBIN-H020, pastebin Communications, solutions/system_design/pastebin/README.md#L314 | merged | **Applying the decision to other workloads** uses a public snippet resource and stable internal storage identity. The shared export trace supplies the interface and endpoint-failure mechanism. |
| PR-TWITTER-H020, twitter Communications, solutions/system_design/twitter/README.md#L315 | merged | The activity-feed sketch uses a public paged collection and internal bounded timeline operation, building on the shared trace. |
| PR-WEB_CRAWLER-H021, crawler Communications, solutions/system_design/web_crawler/README.md#L335 | merged | The crawl-job sketch pairs a public progress resource with internal scheduling and replacement through discovery. |
| PR-MINT-H020, mint Communications, solutions/system_design/mint/README.md#L423 | merged | The financial summary sketch identifies timestamp and currency and scopes the internal aggregation to an authorized account. |
| PR-SOCIAL_GRAPH-H017, social graph Communications, solutions/system_design/social_graph/README.md#L331 | merged | The connections example pairs a public collection with a bounded internal operation and explains the response-size constraint. |
| PR-QUERY_CACHE-H020, query cache Communications, solutions/system_design/query_cache/README.md#L288 | merged | The example gives a public query identity and an internal cache identity containing tenant and query. |
| PR-SALES_RANK-H018, sales rank Communications, solutions/system_design/sales_rank/README.md#L320 | merged | The public ranking and internal operation carry the reporting window to avoid mixing periods. |
| PR-SCALING_AWS-H043, scaling Communications, solutions/system_design/scaling_aws/README.md#L385 | merged | The public catalogue remains stable while the internal inventory boundary changes discovery ownership and timeout policy. |
| PR-BODY-R1-RPC-PATH, RPC request and return, README.md#L1468 | taught | **RPC path and interface choices** explains client marshalling, transport, server dispatch and reverse response. Q2 and EX-1 assess the sequence. |
| PR-BODY-R1-RPC-SDK, SDK selection, README.md#L1488 | taught | The same section relates SDK packaging to known platforms, authentication, compatibility, releases and debugging. |
| PR-BODY-R1-REST-IDENTITY, resource identity, README.md#L1510 | taught | **Resource interfaces and REST constraints** distinguishes URI identity, representation and change through representations. The export example supplies a resource path. |
| PR-BODY-R1-REST-SELF, self-descriptive messages, README.md#L1512 | taught | The same section names method, media type and relevant headers alongside status. Q4 tests why JSON and a status alone are insufficient. |
| PR-BODY-R1-REST-HYPERMEDIA, hypermedia constraint, README.md#L1513 | taught | The same section explains links and controls for transitions. The export representation supplies status and later download links, assessed in Q1 and Q4. |
| PR-BODY-R1-REST-COSTS, round trips and payload, README.md#L1530 | taught | **RPC path and interface choices** compares nested requests with composite representations, pagination and extra client payload. Q6 applies the trade-off. |

The eight case sections repeat the same public HTTP, internal RPC and discovery prompts in the pinned Primer. Their Academy examples merge that shared mechanism with distinct workload constraints. The source-to-section mapping records teaching locations. This review evaluated the actual explanations for depth.

## Pedagogy and assessment

The reporting workload motivates stable public identity, internal operation contracts and endpoint selection. The lesson moves from the REST constraints through the complete RPC path and compatibility choices, then traces a request, timeout and stale endpoint. Its preview is self-contained and explicitly points to the archived M03-L03 trace. The milestone integration must reconcile that reference against the canonical M03-L03 draft when it is available.

LO1 is taught in the resource, RPC, retry and worked-example sections and assessed by Q1–Q3, Q5 and EX-1. LO2 uses those sections and the trade-off and decision sections, assessed by Q4–Q6 and EX-1. The companion's front matter and narrative map identify those same sections and items. Six questions have answers and explanations. The separate reservation exercise asks for public and internal contracts, discovery, deadlines, duplicate handling, pagination and compatibility. Its sample solution states the durability and retained-identity assumptions for the at-most-once effect, and its ten-point rubric covers each major deliverable.

## Findings

No open pedagogy or assigned-coverage findings. The documented M03-L03 preview dependency remains to be reconciled during the milestone integration.

**Verdict: ready-for-human-review.** This verdict covers pedagogy and the assigned curriculum topics.
