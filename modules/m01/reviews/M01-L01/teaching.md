# M01-L01 actual coverage and pedagogy review

## Scope and sources

Lesson mode for middle/senior engineers. Reviewed the approved SDA-v1 outline, lesson, companion and evidence. The source map is Donne Martin's The System Design Primer, revision ae9bbd7b02d90b9866215de185217d33f39ab733. The listed locators were inspected in the pinned source. The course review's N1 concerns M03-L02 and M06-L01 and does not affect this lesson.

## Actual coverage

| Topic ID | Exact teaching heading | Disposition | Source locator and instructional evidence |
|---|---|---|---|
| PR-H016 | Core concepts and mechanisms | taught | README.md#L270. Converts activity by window and estimates peak, copies, bandwidth and distinct working set. |
| PR-H158 | Latency and the request path | taught | README.md#L1577. Explains scales and derives the dependent request path. |
| PR-H159 | Core concepts and mechanisms | taught | README.md#L1581. Explains binary versus decimal prefixes and bit/byte conversion. |
| PR-H161 | Latency and the request path | taught | README.md#L1600. Uses an explicitly assumed scale, access-pattern distinctions and measurement. |
| PR-H162 | Latency and the request path | taught | README.md#L1637. Original scale presents relative illustrative timings. |
| PR-PASTEBIN-H022 | Latency and the request path | merged | solutions/system_design/pastebin/README.md#L325. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-TWITTER-H022 | Latency and the request path | merged | solutions/system_design/twitter/README.md#L326. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-WEB_CRAWLER-H023 | Latency and the request path | merged | solutions/system_design/web_crawler/README.md#L346. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-MINT-H022 | Latency and the request path | merged | solutions/system_design/mint/README.md#L434. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-SOCIAL_GRAPH-H019 | Latency and the request path | merged | solutions/system_design/social_graph/README.md#L342. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-QUERY_CACHE-H022 | Latency and the request path | merged | solutions/system_design/query_cache/README.md#L299. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-SALES_RANK-H020 | Latency and the request path | merged | solutions/system_design/sales_rank/README.md#L331. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |
| PR-SCALING_AWS-H045 | Latency and the request path | merged | solutions/system_design/scaling_aws/README.md#L396. The source subsection points back to the common latency appendix. The shared section explains timing scales, dependent round trips and measurement. |

The merged appendix references lead to the same latency material, so the common explanatory treatment covers their assigned scope.

## Pedagogy and assessment

The audience can apply the formulas to a feed, then compare a path change and measurement. The assumed scale is labeled and separates present measurement from historical intuition.

The companion has a distinct exercise, six checks with explanations and a ten-point rubric. LO1 Q1–Q3 and EX-1 calculate workload. LO2 Q4–Q6 and EX-1 compare margin, critical path and measurement. EX-1 changes rates and payloads, although two results coincide.

## Findings

**P01 — minor.** LO1 maps to Worked example, which covers traffic, storage, egress and working set. Its latency component is taught in Latency and the request path. The one-heading map does not identify that second section. Include a cross-reference from the mapped section or otherwise make the full teaching location explicit.

**P02 — minor.** Assessment EX-1 changes inputs, but its retained-storage and working-set numeric results equal the worked example. Other calculations differ. Distinct outputs would make independent checking clearer.

Verdict: **ready-for-human-review**.
