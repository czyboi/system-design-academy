# Course execution plan — SDA-v1

Select one, several or all nine milestones when authorizing a run. The [delivery plan](PLAN.md#delivery-milestones) lists their handoffs, and [backlog.json](backlog.json) defines their Story membership and outputs. Independent work can proceed across the selected milestones. Concrete draft inputs determine when the sections that use them can finish.

## Intake and execution

1. Take the union of the Story IDs in the selected milestones. For each Story, reuse or create one Issue/spec/state/worklog, check task status, and use `outputs.teaching`, `outputs.assessment` and `outputs.evidence` from that Story (not filenames formed from the proposed Task ID). Give each artifact one writer.
2. Read the [approved SDA-v1 baseline](../curriculum/README.md) at intake. Use its approved outline, inventory and coverage matrix as the default. Use the two-step draft lesson template; integration, capstone and audits run only when separately authorized.
3. Draft independent Stories or sections in parallel where practical. For `composition` inputs, finish the consuming section once the exact upstream draft is available. Resolve `preview` and `reference` links when the user requests validation or integration review. If a needed draft is missing outside the selected scope, report the specific dependency and continue independent work in scope. Record which downstream section or assessment item uses each input.
4. Finish the authorized drafts and stop. Run technical/source review, coverage/pedagogy review or Python validators only when the user requests them. On substantive edits to reviewed material, explicitly flag `needs_review`; do not infer stale states or trigger review loops automatically.
5. Commit the draft output files, task specification, state and worklog; then run `taskctl handoff TASK-ID` before cross-agent transfer. Hand off current draft artifacts, any requested review reports and unresolved findings. A completed draft does not imply it was reviewed/validated. Human acceptance, merge and publication require explicit human approval.

## Work by milestone

Each module integration can be drafted as soon as its required lesson drafts exist; quality checks and approval are separate user-triggered steps. Prepare integration work while lessons are in progress. Across milestones, use the concrete inputs listed below to decide what can finish.

| Milestone | Lesson or package batch | Handoff dependencies |
|---|---|---|
| `SDA-MS01` | M00-L01–L02 and M01-L01–L04. | Finish M00-INT and M01-INT with the validated drafts from each respective module. |
| `SDA-MS02` | M02-L01–L04 and M03-L01–L03. | Resolve the discovery failure-trace preview in M03-L02 against M03-L03. Finish M02-INT and M03-INT. |
| `SDA-MS03` | M04-L01–L05 and M05-L01–L03. | Finish M04-INT and M05-INT with their current topic and outcome evidence. |
| `SDA-MS04` | M06-L01–L03 and M07-L01–L03. | Resolve M06-L01's policy preview against M06-L02. Check M07-L01's references to M03-L01 and M07-L02. Finish M06-INT and M07-INT. |
| `SDA-MS05` | M08-L01–L03 and M09-L01–L03. | Finish M08-INT and M09-INT. Record the current M08-L03 retrieval draft for the search cases that use it in MS06. |
| `SDA-MS06` | M10-L01–L08. Start the independent cases and independent sections of the others. | Resolve M10-L02's indexing reference to M08-L03. Finish M10-L03's retrieval composition with the M08-L03 draft and M10-L06's cache flow with the M06-L03 draft. Finish M10-INT. |
| `SDA-MS07` | M11-L01–L09. | Finish M11-INT with the ID and rate-limit comparison and all nine lesson coverage records. |
| `SDA-MS08` | M12-L01–L06 and M13-L01. | Finish M12-INT and M13-INT. Check the OOD examples and architecture comparison against their own outcomes. |
| `SDA-MS09` | `SDA-CP-01` and `SDA-COURSE-AUDIT`. | Draft the capstone from the approved scope. Start audit reconciliation once all 14 module evidence packages and the validated capstone are available. |

## Handoff checks

- **Lesson package.** The teaching and assessment drafts exist. Any requested review/validation evidence is reported separately, with manual `review_status`. Each mapped topic has a candidate teaching section; each outcome maps to lesson and assessment evidence.
- **Module package.** The integrated brief, reference solution and rubric, decision summary, `taught-coverage.csv`, and `outcome-portfolio.json` are present at the backlog paths. Reconcile the approved topic assignments and the current lesson and module outcomes before marking module validation complete.
- **Course package.** The capstone evaluates all six transfer outcomes with its marketplace scenario and rubric. When requested, the independent audit checks actual teaching for all 473 topic mappings and reconciles the outcome portfolio; the strict taught-stage checker is a separate user-triggered operation. The audit delivers the combined taught matrix, outcome portfolio and review artifacts listed in the backlog.
