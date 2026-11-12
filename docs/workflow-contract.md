# Workflow contract — manual reviews and checks

## Default task graphs

The [shared module-pipeline skill](../.agents/skills/module-pipeline/SKILL.md) is the orchestration procedure. New templates are minimal:

- **Course planning:** one `plan` step producing a new versioned plan, source inventory and coverage matrix.
- **Lesson package:** `research` → `author`. Author uses the declared authoring, assessment, governance and compact format instructions to produce a source-grounded draft lesson and separate companion assessment. No additional agent stage is added. This adds no agent stage or automatic review.
- **Tooling:** one `implementation` step.

**The authoring path ends at draft completion.** Python validation, independent AI review, rework and full course audits are **not automatic**. Invoke each separately only upon explicit user instruction. Existing historical graphs remain as recorded; their completed work is not reopened by this policy change.

## Explicit lifecycle CLI

```bash
python scripts/taskctl.py init TASK-ID --module MODULE --goal "..." --owner "@owner" --template .academy/state/task.template.json
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py checkpoint TASK-ID STEP-ID --note "..." --next-action "..."
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT --resume
python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "User requested a redo"
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "Explicit full redo" --cascade
python scripts/taskctl.py review-status TASK-ID --scope technical --state needs_review --reason "Substantive technical change"
python scripts/taskctl.py review-status TASK-ID --scope pedagogy --state in_review --reason "Requested teaching review"
# After committing AND pushing artifacts, spec, state and worklog:
python scripts/taskctl.py handoff TASK-ID
# Only for a handoff within the same checkout:
python scripts/taskctl.py handoff TASK-ID --local-only
python scripts/taskctl.py hold TASK-ID --state paused --reason "User paused"
python scripts/taskctl.py resume-task TASK-ID --reason "User resumed"
```

`status` is read-only. `reconcile` persists aggregate status computed only from explicit step/hold fields. No automatic STALE, checksum, fingerprint, dirty-input block, unchanged-output reuse flag or dependency hash cascade exists. The CLI requires declared inputs when starting and checks declared outputs, dependencies and any existing review gate when completing; a completed step may later lose outputs without changing status (read-only `WARNING` in `status`). `handoff` is an explicit, read-only Git tracking/cleanliness check for completed output files, spec, task state and worklog. For cross-environment handoff it also verifies local HEAD equals the upstream branch currently advertised by the remote; configure tracking with `git push -u origin HEAD` and push future commits before handoff. Use `--local-only` only when agents share a checkout. Remote access happens exclusively during this explicit command; no checksum or automatic state change occurs.

For a backlog lesson, `init ... --template .academy/state/task.template.json` resolves `EVIDENCE_PATH`, `TEACHING_PATH` and `ASSESSMENT_PATH` from the Story identified by `proposed_task_id` and validates its module. Task ID (`SD-M00-L01`) is not the filename Lesson ID (`M00-L01`). A missing/ambiguous Story fails instead of guessing a path. Initialization validates both task state and its spec before writing files, so invalid templates do not leave a stranded spec.

`complete --usage-file PATH` may record observed input/output/cached/reasoning tokens and elapsed time. The tool does not infer usage or cost. New files never record hashes; legacy task hash fields and prior reports remain historical data.

## Optional independent reviews

When requested, review the specified artifact and dimensions only. Available reviewers:

- **Technical + provenance:** correctness, assumptions, primary-source support, citation/asset rights.
- **Coverage + pedagogy:** actual explanatory teaching, source mapping, outcomes and assessment quality.
- **Course plan:** full Primer enumeration plus plan pedagogy.
- **Targeted:** changed section and affected dependencies, when the user explicitly chooses it.

A negative review should provide actionable findings. A minimal JSON verdict may be:

```json
{
  "verdict": "revise",
  "findings": [{"id": "T-1", "severity": "major", "status": "open"}]
}
```

Allowed verdicts: `block`, `revise`, `ready-for-human-review`. Severities: `blocker`, `major`, `minor`, `note`. Finding status: `open` or `resolved`. A clear verdict must have no open blocker/major finding. New verdicts **do not require artifact_hashes**; old verdict metadata may remain untouched. Review does not automatically invoke Python validation. Use `review-status --scope technical|pedagogy|coverage|provenance|REVIEW-STEP-ID` to record only the requested dimension, not to approve publication. `general` does not certify other scopes. A named review gate in a new task passes only with a completed review step, explicit matching scoped `reviewed` decision and a clear verdict; `in_review` and `needs_review` block. Gate conditions are checked again at `complete` for any running step with `requires_reviews`. Historical tasks with no new review fields preserve their previous completed-review gate behavior. If content changes materially later, flag `needs_review` explicitly.

Historical optional step graphs may include `requires_reviews`; new decisions require a scoped review state in addition to the verdict and completed review step. `invalidate` on a reviewed step explicitly marks its scope `needs_review`. No checksums are compared. New default drafts do not depend on review steps.

## On-demand Python validation

```bash
python scripts/validate_content.py --scope lesson --lesson PATH --assessment PATH
python scripts/validate_content.py --scope curriculum --plan PATH --matrix PATH
python scripts/validate_content.py --scope workflow
python scripts/validate_content.py
python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage plan
python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage taught
python scripts/taskctl.py validate
python -m unittest discover -s tests -v
```

Run only the specifically selected checks. New lessons use exactly one canonical `modules/mXX/lessons/MXX-LYY.md` and `modules/mXX/assessments/MXX-LYY.md` pair per Lesson ID, with Git as the revision history; source evidence remains under `modules/mXX/evidence/`. Repository-wide checks reject nested lesson revisions, `content-manifest.json` and orphan assessments. The approved `curriculum/revision-1/` directory is syllabus history and remains unchanged. The strict coverage checker may also be given `--review PATH` to check a **supplied** course verdict's coverage/pedagogy flags; it no longer compares artifact hashes or treats a changed lesson's SHA as stale. It remains a structural check, not evidence of factual or teaching quality.

GitHub Actions `content-validation.yml` has **workflow_dispatch only**; select **Content validation → Run workflow** to run those checks manually. Python regression tests run separately on pull requests and pushes to `main`, and can also be started manually.

## Full Primer coverage data contract

The inventory has `repository: https://github.com/donnemartin/system-design-primer`, a full 40-character Git **commit ID** in `revision`, and stable unique topic/resource entries (`id`, `kind`, `locator`). A resource entry needs a rationale. Include meaningful README body leaves, solution bodies, appendix and OOD concepts; linked third-party catalogs remain resources rather than recursively imported teaching text. The pinned commit ID identifies the source revision; it is not a checksum used to transition task state.

The course matrix has a unique row per knowledge topic with `topic_id,lesson,outline,disposition`. Full coverage allows only `mapped`/`merged`; every topic including optional tracks needs an exact lesson and real outline. The checker verifies each outline belongs to that lesson's section.

For taught-stage structural checks, add `lesson_path,section` per row. The referenced draft teaching lesson must exist, match its ID and contain a real explanatory section. Questions, assessment text, titles and citations alone are not teaching. `lesson_sha256` is not required or checked; legacy columns are ignored. Mapping/completeness and actual depth remain separate questions that a human or explicitly requested independent reviewer must assess.

The user-approved official SDA-v1 baseline is at [curriculum/revision-1/](../curriculum/README.md). Do not overwrite it with course-planning drafts. Preserve old approved-baseline files as historical decision evidence; no new checksum-based approval gate is introduced.

## Release boundary and model routing

No content is published or merged solely because a task reached `automation_complete`, code validation passed or a reviewer said `ready-for-human-review`. Approval and publication require an explicit human action.

Model routing defaults remain in Codex/Claude profile files; the parent may delegate bounded roles and record observed runtime model/usage when available. Reviewer count is driven by the user's request, never automatic.
