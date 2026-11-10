---
name: task-intake
description: Claim one bounded Academy task, select a compact graph, and preserve canonical requirements and accepted coverage evidence.
---

# Task Intake

1. Search GitHub Issues and task records for equivalent work. Read matching spec/state/worklog, issue, relevant prior feedback, `.academy/state/README.md`, Git status/branch/commits and taskctl status. Do not duplicate work or resume held historical tasks without explicit direction.
2. Record current user scope, deliverables, target learners (default middle/senior), language (English), source revision and exclusions in the canonical spec. One owner @username and one active writer. The Issue links the spec; it is not a second requirements document.
3. Select a template: `.academy/state/course.template.json` for course plans, `task.template.json` for one lesson package, `workflow.template.json` for tooling. Run `taskctl init TASK-ID --module MODULE --goal "..." --owner "@username" --template PATH`. Replace placeholders, output filenames and module-specific guidance with exact paths. Workflow tasks replace the sample implementation report path with the actual edited files; no lesson gates apply.
4. Each DoD and acceptance criterion declares applies_to. Declare clean tracked inputs, unique output ownership and explicit dependencies. Do not snapshot the entire repo or create an Issue per review/research step. Use Git history for historical baselines unless an exact immutable file input is needed.
5. For full-course scope, retain all Primer knowledge topics; deferred/excluded knowledge cannot count as full coverage. Inventory and source-to-lesson matrix are shared course artifacts. Independently audit completeness and plan pedagogy once per changed artifact set. A topic classified as a resource needs a justified, independently checked reason.
6. For lesson packages, choose an already accepted plan/inventory/matrix and matching course verdict. The plan-gate step verifies exact hashes and reuses that verdict; it must not fabricate acceptance or rerun course planning for each lesson. Missing/negative/stale/legacy-only gates block authoring. Select the exact lesson ID and assigned topic rows without changing the shared plan.
7. Keep teaching and companion assessment separate. Declare the paired contract and all outcome mappings. Use two independent combined review steps per module-pipeline: technical+provenance, and actual coverage+pedagogy/language. Reviewers are distinct from the author and each other. Each review binds the pair, evidence and coverage inputs; validation requires both accepted verdicts.
8. Follow module-pipeline for conditional revisions only when findings require them. No mandatory final copy or duplicate recheck pass. Additional specialist reviews are scoped to unresolved risks, not automatically created for every lesson.
9. Commit complete spec/state/worklog before execution. Start only READY, resume only unchanged RESUME, inspect STALE, skip SKIP and stop on BLOCKED. Commit state mutations; commit outputs before complete. Use explicit output reuse with reason when applicable.

Use artifact-bound verdicts and execution_control holds as documented in docs/workflow-contract.md. A completed negative review is not acceptance. Scope-specific validation and human approval remain separate. Never infer completion from chat narrative.
