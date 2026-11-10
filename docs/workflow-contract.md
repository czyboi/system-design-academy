# Workflow CLI contract

## Compact defaults and reusable course gate

The procedure is defined only in the shared [module-pipeline skill](../.agents/skills/module-pipeline/SKILL.md). Templates now contain three course-planning steps, six lesson-package steps or two tooling steps. The six-step lesson path is research, plan-gate, author, technical-review, teaching-review, validation. Existing historical task graphs are not changed automatically.

The technical review also executes provenance-review; the teaching review also executes pedagogical-review and language checks. Reports distinguish each assigned dimension, and a material failure in either makes the combined verdict negative. Reviewers are independent from the author and each other. Both lesson reviews bind the exact teaching file, assessment, evidence, course plan, inventory and matrix. A clear first pass ends at the same paths: no automatic revision, final-copy or recheck stage.

The course review binds plan, inventory and matrix, independently checks full-source enumeration and plan pedagogy, and includes `checks: {"coverage": "pass", "pedagogy": "pass"}` only when both pass. A legacy coverage-only report cannot be imported as this acceptance gate.

Before starting a lesson's plan-gate, verify the declared shared inputs with:

```text
python scripts/check_course_coverage.py --inventory curriculum/source-inventory.json --matrix curriculum/coverage.csv --plan CURRICULUM_MASTER.md --stage plan --review curriculum/review.json
```

These are future canonical paths selected at intake, not a claim that accepted artifacts already exist. Failure blocks authoring. On success, verify the selected lesson ID exists in the plan and matches the task scope, copy only the unchanged accepted verdict JSON to the task plan-gate output, and record its source path/hash and reuse reason in the worklog. Commit that output, complete plan-gate, then commit state/worklog. No independent reviewer rerun is required for an unchanged accepted course gate. This does not reuse a lesson review or waive actual-teaching review.

The checker is read-only; it neither creates content nor produces an approval. Do not author missing curriculum during a lesson or workflow task. Resolve a separately authorized course task first. The current historical revision-3 candidate still has a pedagogy blocker and is not an accepted gate.

## Full Primer coverage data contract

The strict checker complements the older, looser `validate_content.py --scope curriculum` mapping check. Full-Primer claims must use the strict checker; a loose check cannot substitute for it.

Inventory JSON has `repository` equal to `https://github.com/donnemartin/system-design-primer`, a full 40-character `revision` SHA, and nonempty `entries`. Each entry has a stable unique `id`, `kind` (`topic` or `resource`), and `locator` (repository path plus heading/anchor at that revision). Resource entries also need a rationale. Knowledge entries include meaningful leaf topics, example bodies, appendices, substantive additional prompts, OOD and under-development concepts. A contribution placeholder without teaching material can be a resource with an explicit reason. Reviewers independently check the actual pinned source; an author cannot hide a missing topic by omitting its inventory row or calling it a resource.

The CSV matrix has exactly one row per knowledge-topic ID and columns `topic_id,lesson,outline,disposition`. Only `mapped` and `merged` dispositions satisfy full coverage. The plan uses a heading containing each lesson ID and an outline beneath that heading. The checker verifies an outline belongs to its own lesson, rather than finding the same text anywhere in the file. Resources remain in the inventory and do not inflate the covered-topic count. Optional tracks still map every topic; deferred/outside-scope knowledge blocks completeness.

For actual course coverage, the same matrix adds `lesson_path,section,lesson_sha256` columns. Every topic needs a matching draft teaching file, an exact explanatory heading, and its current SHA-256. The checker rejects missing artifacts, stale hashes, empty headings and assessment/reference-only locations. It cannot decide whether prose really explains a mechanism: independent teaching review is mandatory.

```text
python scripts/check_course_coverage.py --inventory curriculum/source-inventory.json --matrix curriculum/coverage.csv --plan CURRICULUM_MASTER.md --stage taught
```

A final independent course coverage/pedagogy verdict must bind the inventory, matrix, plan and all teaching files referenced by the matrix. Run the same command with `--review PATH` to verify that accepted verdict. All lesson packages additionally need current accepted technical/provenance and teaching reviews. Course completion is still not human approval or publication.

Updating a taught-evidence matrix changes its hash, so preserve the earlier accepted plan matrix for in-flight tasks and create a new versioned matrix/verdict when adding teaching evidence. Select exact versioned paths at intake. Never silently rewrite shared inputs of a running task or relabel a plan-stage verdict as a taught-stage verdict.

## Conditional revisions

On a negative lesson review, declare a revision step with unique new pair paths, `revision_cycle: 1`, and completed review dependencies without `requires_reviews`. Add two combined rechecks bound to the revised pair plus its evidence and course inputs; repoint validation to those accepted gates. Preserve the original pair and verdicts. A necessary second revision uses new paths and cycle 2. No third automated revision is allowed without separate user-authorized work. Rechecks inspect changed content and affected dependencies and verify all current artifact hashes. Passing content is not copied merely to produce a file named final.

## Review results

A review step declares `review.artifact_paths` (also explicit input_paths) and `review.verdict_path` (one of its owned outputs). It produces an explanatory Markdown report plus JSON:

```json
{
  "verdict": "revise",
  "artifact_hashes": {"modules/example/lesson.md": "actual SHA-256 of the file bytes"},
  "findings": [{"id": "T-1", "severity": "major", "status": "open"}]
}
```

Verdicts: block, revise, ready-for-human-review. Severities: blocker, major, minor, note. Finding status: open or resolved. Every artifact must have its exact current hash; an accepted verdict cannot contain open blocker/major findings. The JSON is structural evidence supplied by the reviewer, not proof of technical truth or reviewer identity.

`requires_reviews` lists direct review dependencies whose verdicts must be clear. Ordinary `depends_on` requires completed, fresh execution only, allowing a revision to consume negative findings. Changing review contracts invalidates their fingerprints. Historical tasks without these additive fields retain their previous semantics; migrate an active legacy graph before relying on enforced review gates.

Steps marked revision_cycle count toward a task-wide maximum of two automated revision starts (resuming an interrupted run does not consume another start). The engine refuses a third start; the parent records an awaiting-human hold. This limit applies to tagged revisions, so intake must classify them accurately. Further user-authorized revision work uses a new scoped task.

## Read-only inspection and execution controls

```text
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py reconcile TASK-ID
python scripts/taskctl.py hold TASK-ID --state paused --reason "User asked to stop"
python scripts/taskctl.py hold TASK-ID --state awaiting-human --reason "Two revisions still leave a blocker"
python scripts/taskctl.py resume-task TASK-ID --reason "User explicitly authorized resumption"
```

Status never writes. Reconcile, hold and resume-task mutate state/worklog and must be committed. Holds block both start (including --resume) and complete. They do not cancel a running external process: the parent must stop its worker as well. The command records a supplied decision; it cannot authenticate human authorization.

## Runtime metadata

Start accepts `--model` and `--reasoning-effort` for observed runtime values. Omit unavailable values. Complete optionally accepts `--usage-file PATH`, a repository-relative JSON object with observed nonnegative counters: input_tokens, output_tokens, cached_input_tokens, reasoning_tokens and elapsed_seconds. The worklog stores the supplied counters and runtime model beside the run ID. Counts may have provider-specific inclusion rules; do not blindly sum reasoning with output tokens or infer subscription cost from API rates. This CLI does not collect runtime usage automatically.

## Content validation

```text
python scripts/validate_content.py
python scripts/validate_content.py --scope workflow
python scripts/validate_content.py --scope curriculum --plan path/to/plan.md --matrix path/to/coverage.csv
python scripts/validate_content.py --scope lesson --lesson path/to/lesson.md --assessment path/to/assessment.md
```

Default repo scope checks current `modules/*/lessons/*.md` packages and explicit `modules/*/content-manifest.json` manifests. A content manifest has draft status and a packages array of lesson/assessment repository-relative paths, including case studies if applicable. An empty authoring repository is valid; a missing explicitly selected/manifested artifact fails. The old pilot-manifest.json is a historical inventory after the user-directed content reset, not a declaration that those files currently exist. Historical runs and immutable input snapshots are excluded from global link checks; selected artifacts are still checked explicitly.

Lesson YAML includes prerequisites, outcome IDs and its assessment path. Companion YAML includes status: draft, lesson path, and outcome_map entries with taught_in (exact lesson heading) and items (EX-1, Q1, etc.). Each of 5–8 Q-numbered checks has Answer: and Explanation:. Structural mapping cannot establish teaching depth or assessment quality.

Curriculum matrices are CSV with topic, locator, disposition, lesson, outline and rationale columns. Mapped/merged rows identify existing lesson/outline text. Optional/deferred/outside-scope rows require a rationale. Independent coverage review establishes completeness against the pinned source.

## Model configuration

Project parent: GPT-6.1 Sol/high. Default bounded subagent: GPT-6.1 Terra/medium. Workflow/architecture designer and PR reviewer: Sol/high. Spec implementer and lesson author: Terra/medium. Technical reviewer: Sol/high. Pedagogy: Terra/medium. Provenance: Sol/medium. Curriculum designer, coverage reviewer and source researcher: Sol/high. Four concurrent subagents, excluding the parent. Host-provided or explicitly selected role settings may override repository profiles; inspect actual runtime metadata rather than assuming the configured model was used. Claude profiles keep model: inherit because OpenAI model IDs do not configure Claude.

Configuration was checked against [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [model catalog](https://developers.openai.com/api/docs/models) on 2026-11-10. Availability is host/account-dependent. These are workload-based starting choices, not benchmark results; new sessions may be needed to reload profiles.
