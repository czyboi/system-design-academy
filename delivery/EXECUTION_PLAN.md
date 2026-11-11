# Course execution plan — SDA-v1

`SDA-MS01` is the recommended first delivery scope. The [delivery plan](PLAN.md#delivery-milestones) lists the nine handoffs, and [backlog.json](backlog.json) defines their exact Story membership and outputs. The sequence below groups work into reviewable packages. Concrete draft inputs determine readiness within the authorized scope.

## Intake and execution

1. Select the Stories in the authorized milestone scope. For each Story, reuse or create one Issue/spec/state/worklog, check task status, and declare the exact inputs, output paths and current versions. Give each artifact one writer.
2. Verify the [approved baseline](../curriculum/approved-baseline.json) at intake. Reuse the exact approved outline, inventory, coverage matrix and review. Use the six-step lesson template for a lesson and a scoped package graph for integration, capstone or audit.
3. Draft independent Stories or sections in parallel where practical. For `composition` inputs, finish the consuming section once the exact upstream draft is available. Resolve `preview` and `reference` links against current drafts at validation. Record which downstream section or assessment item uses each input.
4. Validate the package after both independent reviews pass on its current artifacts. If a change affects another package, update the affected content and rerun the relevant checks and reviews. Reuse valid evidence, and refresh module coverage files for the versions that pass.
5. Hand off the reviewed draft artifacts and evidence, with unresolved findings visible. Human acceptance can cover a single package or several together. Merge and publication require explicit human approval.

## Milestone work batches

Each module integration can finish as soon as its own lesson drafts pass validation. An integration in the same milestone can be prepared independently while other lessons are in progress.

| Milestone | Lesson or package batch | Handoff dependencies |
|---|---|---|
| `SDA-MS01` | M00-L01–L02, then M01-L01–L04 as two small batches. | Finish M00-INT and M01-INT with the validated drafts from each respective module. |
| `SDA-MS02` | M02-L01–L04 and M03-L01–L03. | Resolve the discovery failure-trace preview in M03-L02 against M03-L03. Finish M02-INT and M03-INT. |
| `SDA-MS03` | M04-L01–L05 and M05-L01–L03. | Finish M04-INT and M05-INT with their current topic and outcome evidence. |
| `SDA-MS04` | M06-L01–L03 and M07-L01–L03. | Resolve M06-L01's policy preview against M06-L02. Check M07-L01's references to M03-L01 and M07-L02. Finish M06-INT and M07-INT. |
| `SDA-MS05` | M08-L01–L03 and M09-L01–L03. | Finish M08-INT and M09-INT. Record the current M08-L03 retrieval draft for the search cases that use it in MS06. |
| `SDA-MS06` | M10-L01–L08. Start the independent cases and independent sections of the others. | Resolve M10-L02's indexing reference to M08-L03. Finish M10-L03's retrieval composition with the M08-L03 draft and M10-L06's cache flow with the M06-L03 draft. Finish M10-INT. |
| `SDA-MS07` | M11-L01–L09. | Finish M11-INT with the ID and rate-limit comparison and all nine lesson coverage records. |
| `SDA-MS08` | M12-L01–L06 and M13-L01. | Finish M12-INT and M13-INT. Check the OOD examples and architecture comparison against their own outcomes. |
| `SDA-MS09` | `SDA-CP-01` and `SDA-COURSE-AUDIT`. | Draft the capstone from the approved scope. Start audit reconciliation once all 14 module evidence packages and the validated capstone are available. |

## First delivery scope

`SDA-MS01` contains six lesson packages, two module integrations and 46 mapped topic IDs. The two rows below are the recommended work batches within the milestone. Module approval can be recorded together at handoff.

| Batch | Story IDs | Deliverable |
|---|---|---|
| Design method | `SDA-M00-L01`, `SDA-M00-L02`, `SDA-M00-INT` | Two reviewed teaching and assessment pairs plus the document-sharing design brief, reference solution, decision summary and module evidence. |
| System design foundations | `SDA-M01-L01`, `SDA-M01-L02`, `SDA-M01-L03`, `SDA-M01-L04`, `SDA-M01-INT` | Four reviewed pairs covering capacity and latency, performance and scalability, consistency and partitions, and availability and failover. The integration models an order-status workload and compares two failure policies. |

For both batches, prepare the module exercise and decision summary alongside the lesson drafts where possible. Complete integration against the current validated teaching and assessment pairs. The MS01 handoff includes both `taught-coverage.csv` files covering the 46 assigned topics and both `outcome-portfolio.json` files covering all lesson and module synthesis outcomes.

## Handoff checks

- **Lesson package.** The teaching and assessment drafts have matching current technical/provenance and teaching/coverage verdicts, and package validation passes. Each mapped topic points to an explanatory heading and its current teaching hash. Each outcome points to a teaching section and assessment evidence.
- **Module package.** The integrated brief, reference solution and rubric, decision summary, `taught-coverage.csv`, and `outcome-portfolio.json` are present at the backlog paths. Reconcile the approved topic assignments and the current lesson and module outcomes before marking module validation complete.
- **Course package.** The capstone evaluates all six transfer outcomes with its marketplace scenario and rubric. The independent audit checks actual teaching for all 473 topic mappings, reconciles the current outcome portfolio and cross-module references, and passes the [strict taught-stage check](../docs/workflow-contract.md#full-primer-coverage-data-contract) with its current verdict. The audit delivers the combined taught matrix, outcome portfolio and review artifacts listed in the backlog.
