# Workflow contract — scoped draft handoff and automatic module-close reviews

## Default task graphs

The [shared module-pipeline skill](../.agents/skills/module-pipeline/SKILL.md) is the orchestration procedure. New templates are minimal:

- **Course planning:** one `plan` step producing a new versioned plan, source inventory and coverage matrix.
- **Lesson package:** `research` → `author`, then a parent-owned `draft_handoff.py` invocation outside the task graph. Author uses the declared authoring, assessment, governance and compact format instructions. Handoff performs scoped deterministic data/format validation and feature-branch Git delivery. At completion of **all lesson Stories plus the module-integration Story**, the parent also invokes two independent module-quality reviewer agents and hands off their reports. There are no extra authoring task steps.
- **Tooling:** one `implementation` step.

**Task authoring ends at draft completion, but the parent continues to scoped draft handoff and, at module closure, independent automatic Technical and Pedagogy Review.** Additional user-directed reviews outside the bounded module correction loop, full regression tests, repository-wide validation and course audits remain **on demand**. The handoff never claims teaching quality or human approval. Historical task graphs are not reopened.

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
# After completed lesson/integration drafts, parent validates, commits and pushes the selected task artifacts:
python scripts/draft_handoff.py TASK-ID [TASK-ID ...]
# For non-draft handoff after manually committing/pushing artifacts, spec, state and worklog:
python scripts/taskctl.py handoff TASK-ID
# Only for a handoff within the same checkout:
python scripts/taskctl.py handoff TASK-ID --local-only
python scripts/taskctl.py hold TASK-ID --state paused --reason "User paused"
python scripts/taskctl.py resume-task TASK-ID --reason "User resumed"
```

`status` is read-only. `reconcile` persists aggregate status computed only from explicit step/hold fields. No automatic STALE, checksum, fingerprint, dirty-input block, unchanged-output reuse flag or dependency hash cascade exists. The CLI requires declared inputs when starting and checks declared outputs, dependencies and any existing review gate when completing; a completed step may later lose outputs without changing status (read-only `WARNING` in `status`). `handoff` is an explicit, read-only Git tracking/cleanliness check for completed output files, spec, task state and worklog. The new `draft_handoff.py` helper first runs the existing scoped lesson/assessment validator (and format validation for integrated brief/solution/summary pages), then stages only declared completed outputs and spec/state/worklog, commits and pushes once per batch. It uses an existing `codex/`, `feature/` or `feat/` branch, or creates `codex/drafts-*` when on `main` or another non-feature branch. It rejects unrelated staged files, never force-pushes or merges, and stops/report failures without auto-fixes. For cross-environment handoff it also checks any **existing partial output from a running step** (not-yet-created outputs remain optional), then verifies local HEAD equals the upstream branch currently advertised by the remote; configure tracking with `git push -u origin HEAD` and push future commits before handoff. Use `--local-only` only when agents share a checkout. Remote access happens exclusively during this explicit command; no checksum or automatic state change occurs.

For a backlog lesson, `init ... --template .academy/state/task.template.json` resolves `EVIDENCE_PATH`, `TEACHING_PATH` and `ASSESSMENT_PATH` from the Story identified by `proposed_task_id` and validates its module. Task ID (`SD-M00-L01`) is not the filename Lesson ID (`M00-L01`). A missing/ambiguous Story fails instead of guessing a path. Initialization validates both task state and its spec before writing files, so invalid templates do not leave a stranded spec.

`complete --usage-file PATH` may record observed input/output/cached/reasoning tokens and elapsed time. The tool does not infer usage or cost. New files never record hashes; legacy task hash fields and prior reports remain historical data.

## Automatic per-lesson QA, lightweight module synthesis and optional reviews

The standing default is **two independent reviewer agents right after each individual lesson draft passes scoped validation/Git handoff**, without waiting for the module. Keep existing profiles: `technical_reviewer` (Sol High) audits correctness and primary-source provenance; `pedagogy_reviewer` (Terra Medium) audits teaching and lesson-level curriculum coverage. They each review the canonical lesson/evidence/assessment pair, write specific findings and terminal verdicts, and do not rewrite content. Both reports and the separate bounded lesson cycle live at `modules/mXX/reviews/automatic/lessons/MXX-LYY/{technical.md,pedagogy.md,cycle.json}`. Parent records explicit `taskctl review-status` by scope and persists the reports with `draft_handoff.py --review-report`.

```bash
# After writing and handing off the single lesson:
python scripts/review_cycle.py record M01-L02 --technical revise --pedagogy ready-for-human-review
# If correction is actionable, reserve at most two revisions on THIS lesson:
python scripts/review_cycle.py begin-revision M01-L02
# Author patches only cited content; parent runs scoped draft handoff then both
# independent reviewers perform targeted re-review and record updated verdicts.
python scripts/draft_handoff.py SD-M01-L02 --review-report modules/m01/reviews/automatic/lessons/M01-L02/technical.md --review-report modules/m01/reviews/automatic/lessons/M01-L02/pedagogy.md
```

A `ready` or `blocked` cycle does not automatically restart. An interrupted `revising` cycle resumes its existing attempt; no unlimited repair loops. A blocked lesson requires explicit human action and is not silently carried into downstream authoring. For multiple lessons, review and correct each before drafting dependent lessons so confirmed mistakes can be avoided early.

**Module synthesis:** After **all** lesson QA cycles are ready and the integration Story draft is handed off, invoke the same two independent reviewers once more for integration and **only** cross-lesson consistency, prerequisite progression, module coverage, duplicated content and interactions between designs. Reuse accepted per-lesson reports; do **not** redo full technical source/assessment audits for unchanged lessons. Keep the existing module-scoped paths `modules/mXX/reviews/automatic/{technical.md,pedagogy.md,cycle.json}` and `python scripts/review_cycle.py record mXX ...`. At most two separate module-synthesis correction rounds. If module corrections materially change an accepted lesson, explicitly flag and target re-review that affected lesson before declaring module ready.

Findings in either stage must locate a specific artifact/section, identify `blocker`, `major`, `minor` or `note`, record `open`/`resolved` status, and include the source/curriculum evidence that supports resolution. Allowed verdicts are `block`, `revise`, and `ready-for-human-review`; open blocker/major findings forbid a clear verdict. Drafts, reviewer verdicts and data validation are never human publication approval. Full instructions are in `.agents/skills/module-quality-review/SKILL.md`.

Additional standalone or dimension-specific review remains on demand. A combined technical/provenance or pedagogy/coverage assignment uses existing specialist skills but does not add new agent types or a quality score. `review-status --scope technical|pedagogy|coverage|provenance|REVIEW-STEP-ID` records only that scope. Material changes after review must be flagged `needs_review` explicitly; no checksum-based freshness check is implied. Historical named review gates retain their explicit status/verdict requirements.

## Verified cross-module learning (after successful correction)

Immediately after **a corrected lesson** or module synthesis has reached `ready` with independent re-review, the parent may extract a **small number** of reusable, evidence-backed resolved findings. `learning_memory.py record --module mXX --lesson MXX-LYY` reads the lesson's own review cycle and final report; without `--lesson`, it reads the module synthesis cycle. In either case it refuses unresolved/blocked work, revision-0 claims and missing exact reviewer-cited evidence. `.academy/knowledge/lessons-learned.json` stores concise hints, not the full reports or unverified AI opinions. Later Authors/reviewers retrieve at most three role- and tag-matched hints with `learning_memory.py suggest`. Repeated incidents in the **same module** do not count as cross-module recurrence.

`learning_memory.py promotions` identifies reusable errors independently confirmed across **two distinct modules**. A possible Skill improvement is proposed only through a **separate human-reviewed PR**, never a silent edit/merge, and only after verifying sources, consistency and redundancy. No extra agent role, skill auto-edit or model fine-tuning is introduced.

## Automatic scoped draft checks; all broader checks on demand

```bash
# Parent executes once per completed draft batch (requires Git remote credentials):
python scripts/draft_handoff.py SD-M00-L01 SD-M00-L02
# Lesson and module review-report handoff examples are in the preceding section.
# Parent handles two independent reviewers; this script handles only validation/Git.
# Optional standalone checks:
# Structural mapping, YAML metadata and Markdown safety in one command:
python scripts/validate_content.py --scope lesson --lesson PATH --assessment PATH
python scripts/validate_content.py --scope repo
# Independent checks remain available on demand:
python scripts/validate_content.py --scope curriculum --plan PATH --matrix PATH
python scripts/validate_content.py --scope workflow
python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage plan
python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage taught
python scripts/taskctl.py validate
python -m unittest discover -s tests -v
```

The draft handoff automatically runs only selected lesson/assessment/integrated checks and includes any existing lesson/module QA cycle state. The parent, not Python, invokes the author and independent reviewers in the bounded feedback loop. Run all other checks only when specifically requested. The combined validator reuses the Markdown format module and never transforms lesson content; heading titles, the number of questions, and the presence of answer/rubric keywords are not format constraints. Those requirements remain with Author's self-check and any requested substantive review. Current Markdown checks are parser/safety smoke tests only; real browser rendering must be tested with the actual website renderer when it exists. New lessons use exactly one canonical `modules/mXX/lessons/MXX-LYY.md` and `modules/mXX/assessments/MXX-LYY.md` pair per Lesson ID, with Git as the revision history; source evidence remains under `modules/mXX/evidence/`. Repository-wide checks reject nested lesson revisions, `content-manifest.json` and orphan assessments. The approved `curriculum/revision-1/` directory is syllabus history and remains unchanged. The strict coverage checker may also be given `--review PATH` to check a **supplied** course verdict's coverage/pedagogy flags; it no longer compares artifact hashes or treats a changed lesson's SHA as stale. It remains a structural check, not evidence of factual or teaching quality.

GitHub Actions `content-validation.yml` has **workflow_dispatch only**; select **Content validation → Run workflow** to run those checks manually. Python regression tests run separately on pull requests and pushes to `main`, and can also be started manually.

## Full Primer coverage data contract

The inventory has `repository: https://github.com/donnemartin/system-design-primer`, a full 40-character Git **commit ID** in `revision`, and stable unique topic/resource entries (`id`, `kind`, `locator`). A resource entry needs a rationale. Include meaningful README body leaves, solution bodies, appendix and OOD concepts; linked third-party catalogs remain resources rather than recursively imported teaching text. The pinned commit ID identifies the source revision; it is not a checksum used to transition task state.

The course matrix has a unique row per knowledge topic with `topic_id,lesson,outline,disposition`. Full coverage allows only `mapped`/`merged`; every topic including optional tracks needs an exact lesson and real outline. The checker verifies each outline belongs to that lesson's section.

For taught-stage structural checks, add `lesson_path,section` per row. The referenced draft teaching lesson must exist, match its ID and contain a real explanatory section. Questions, assessment text, titles and citations alone are not teaching. `lesson_sha256` is not required or checked; legacy columns are ignored. Mapping/completeness and actual depth remain separate questions that a human or explicitly requested independent reviewer must assess.

The user-approved official SDA-v1 baseline is at [curriculum/revision-1/](../curriculum/README.md). Do not overwrite it with course-planning drafts. Preserve old approved-baseline files as historical decision evidence; no new checksum-based approval gate is introduced.

## Release boundary and model routing

No content is published or merged solely because a task reached `automation_complete`, code validation passed or a reviewer said `ready-for-human-review`. Approval and publication require an explicit human action.

Model routing defaults remain in Codex/Claude profile files; the parent may delegate bounded roles and record observed runtime model/usage when available. The standing module-close rule always triggers the two existing reviewer roles; other reviewer invocations are by explicit user request. Neither QA nor task completion constitutes human approval.
