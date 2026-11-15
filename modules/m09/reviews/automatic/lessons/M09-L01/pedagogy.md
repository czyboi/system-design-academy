# M09-L01 independent pedagogy and coverage review

Verdict: **ready-for-human-review**

## Scope and method

Round 0 covers the lesson and companion assessment for middle and senior engineers. I read the lesson before the assessment solution and checked the approved M09-L01 outline and `curriculum/revision-1/coverage.csv`. The source topic map is the [System Design Primer](https://github.com/donnemartin/system-design-primer/tree/ae9bbd7b02d90b9866215de185217d33f39ab733), revision `ae9bbd7b02d90b9866215de185217d33f39ab733`. I inspected its `README.md` security section and the assigned mappings. The repeated case-security headings are intentionally combined into the owning security lesson in the approved matrix. The Academy's authorization and CSRF material extends the source map.

## Coverage evidence

All rows below map to M09-L01 and its two outcomes. `L` means `modules/m09/lessons/M09-L01.md` and `A` means `modules/m09/assessments/M09-L01.md`. Section titles identify instructional evidence, and assessment items provide a separate check.

| Topic ID and source locator | Status and actual teaching evidence | Assessment |
| --- | --- | --- |
| PR-H156, `README.md#L1560` | Taught. L, “Make the access decision at the record boundary”, “Protect each hop and stored copy” and “Keep input as data and output in its context” apply the controls to a financial record. | Q1–Q6, EX-1 |
| PR-B005, `README.md#L1566` | Taught. L, “Protect each hop and stored copy” and “Keep input as data and output in its context” explain encryption, SQL injection and XSS. “Make the access decision at the record boundary” covers least privilege. | Q1–Q6, EX-1 |
| PR-BODY-R1-SEC-ENCRYPT, `README.md#L1566` | Taught. L, “Protect each hop and stored copy” distinguishes transport, storage and key-access boundaries. | Q2, Q4, EX-1 |
| PR-BODY-R1-SEC-INPUT, `README.md#L1567` | Taught. L, “Keep input as data and output in its context” connects input validation and output-context encoding to injection and browser execution. | Q3, Q5, EX-1 |
| PR-BODY-R1-SEC-QUERY, `README.md#L1568` | Taught. L, “Keep input as data and output in its context” traces bound values through a tenant-constrained query. | Q3, EX-1 |
| PR-BODY-R1-SEC-LEAST, `README.md#L1569` | Taught. L, “Make the access decision at the record boundary” describes separate caller, service and administrative authority and network limits. | Q1, Q6, EX-1 |
| PR-PASTEBIN-H021, `solutions/system_design/pastebin/README.md#L321` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-TWITTER-H021, `solutions/system_design/twitter/README.md#L322` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-WEB_CRAWLER-H022, `solutions/system_design/web_crawler/README.md#L342` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-MINT-H021, `solutions/system_design/mint/README.md#L430` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-SOCIAL_GRAPH-H018, `solutions/system_design/social_graph/README.md#L338` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-QUERY_CACHE-H021, `solutions/system_design/query_cache/README.md#L295` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-SALES_RANK-H019, `solutions/system_design/sales_rank/README.md#L327` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |
| PR-SCALING_AWS-H044, `solutions/system_design/scaling_aws/README.md#L392` | Merged. The approved map assigns the shared case-security topic to the financial-record trace and control explanations in L. | EX-1 |

The Academy additions are taught in L. “Make the access decision at the record boundary” distinguishes identity from object authorization and follows a denied cross-tenant request through the bound query. “Keep input as data and output in its context” explains a session-bound CSRF defense and its relationship to XSS. No assigned topic is mention-only or assessment-only.

## Pedagogy and outcome alignment

The motivating cross-tenant request leads to the access decision, a concrete denied query, transport and storage protections, input/output defenses and a control comparison with costs. The instruction explains the failure that motivates each layer and identifies where the layer's protection ends. Its API and proxy prerequisites match the approved outline. The sequence and scope suit experienced engineers without requiring a separate worked answer to reconstruct the main decision.

| Outcome | Teaching evidence | Assessment evidence |
| --- | --- | --- |
| M09-L01-LO1 | L, the record boundary trace, “Protect each hop and stored copy”, and “Keep input as data and output in its context” model identity, authorization, encryption and input/output controls. | A, Q1–Q3 and EX-1 require the reader to trace those controls. |
| M09-L01-LO2 | L, “Select controls for the threat” gives threat-specific benefits, costs and boundaries, supported by the preceding explanations. | A, Q4–Q6 and EX-1 require choices and trade-offs. |

The assessment is separate and has six answered checks plus a practical exercise, sample solution, ten-point rubric and outcome map. The exercise supplies the membership, tenant and token assumptions needed to answer it, includes policy failure, and accepts equivalent defenses that meet the specified boundary. The lesson contains no assessment answer key.

## Findings and required changes

No open blocker, major or minor findings. No required changes. The merged case rows follow the explicit shared-topic assignment in the approved coverage matrix.

This verdict covers teaching and assigned topic coverage. Technical/source review and the human publication decision are separate.

## Round 1 targeted re-review

Verdict: **ready-for-human-review**. Round 0 had no pedagogy or coverage findings to resolve. The correction prompted by the independent technical review preserves the coverage and outcome evidence above.

The revised L, “Make the access decision at the record boundary”, traces browser-to-proxy, proxy-to-service and service-to-database connections. It states the assumed user-delegated token profile, distinguishes the token's user subject from the forwarding proxy workload, and explains the database server verification, separate service principal and failed-connection behavior before the query. The “Protect each hop and stored copy” section explains the alternative proxy-authenticated assertion before Q2 uses that variant. A learner can therefore reconstruct both variants from the lesson.

The revised A, Q2 asks about the taught proxy-authentication variant and its answer retains the record-authorization step. EX-1 specifies the token profile and identity assumptions, and the sample traces the three connections and denied cross-tenant read. Its rubric checks the user/workload distinction, database boundary, policy failure and controls while allowing equivalent defenses. The coverage rows and LO1/LO2 assessment mapping remain supported. No new open pedagogy or coverage findings were identified.
