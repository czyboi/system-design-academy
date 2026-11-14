---
name: module-pipeline
description: Run Academy drafts with scoped validation, safe Git handoff and independent per-lesson reviews and module synthesis QA.
---

# Module pipeline — lightweight draft handoff, lesson QA and module synthesis

## Intake
Read task-intake, current Issue, canonical spec, explicit state, worklog, Git status/commits and prior feedback. Respect holds and user scope. One writer per task. Choose the current approved curriculum baseline (SDA-v1: `curriculum/revision-1/`) unless the user selects another. For lesson tasks, `taskctl init` must resolve author/evidence output paths from that Story's `delivery/backlog.json` outputs, not the Task ID. Before assigning a new lesson, derive up to 8 meaningful topic tags from its Story/outcomes (lowercase hyphenated slugs), run `python scripts/learning_memory.py suggest --tags TAGS --role lesson_author --limit 3`, and include **only matching verified prevention reminders** in the author handoff. An empty result is normal. Never pass the full lessons-learned JSON or treat prior AI findings as authoritative sources.

## Default drafting (author stays focused; parent owns QA)

**Course task:** one plan step creating a *new versioned* inventory, course plan and source-to-lesson coverage matrix. Use pinned Primer source and original educational material. Do not overwrite the approved SDA-v1 snapshot.

**Lesson task:** two steps.
1. `research` — gather source evidence for the assigned lesson. Reuse existing evidence when suitable. Do not refresh the whole Primer inventory per lesson.
2. `author` — read the declared `lesson-authoring`, `assessment-design`, `content-format` and source governance instructions; write the original English draft lesson and separate companion assessment at their **single canonical paths**. Git records subsequent revisions. Include prerequisites, outcomes, motivating problem, mechanism, worked example, decision criteria, failure modes, references, exercise, 5–8 checks with explanations and a rubric. Use the approved outline and assigned topics.

**Tooling task:** one `implementation` step with scoped outputs.

After the requested lesson/integration draft is produced, call `taskctl complete` and persist state/output. Then the **parent orchestrator** (not each author subagent) must run `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]` once for the finished task(s). For a multi-lesson batch, pass all completed draft Task IDs together to validate each lesson/assessment pair and integrated page, commit only declared outputs plus spec/state/worklog, and push once. The helper stays on an existing `codex/`, `feature/` or `feat/` branch or creates a new `codex/drafts-*` branch; it never pushes to `main`, force-pushes, opens a PR, merges or publishes. It runs scoped deterministic Python data/format checks only, not the full regression suite. On validation or Git failure, stop and report which step failed; preserve drafts and do not auto-correct or launch a revision loop. Draft authoring completion does **not** imply independent content review or publication approval. Course/tooling tasks retain manual Git handoff.

## PR only after the requested generation batch finishes

**One user request = one generation batch = at most one Draft PR**, regardless of how many lessons or modules it contains. For example, "generate three lessons" means one PR for exactly those three requested lesson Task IDs; do not wait for the milestone and do not create a PR at each lesson handoff.

At request intake, identify the exact batch Task IDs and choose a stable new lowercase batch ID, reused if this same invocation resumes. Start a **dedicated branch from current \`origin/main\`** before authoring (for example: \`git fetch origin main && git switch -c codex/gen-<batch-id> origin/main\`). Never reuse a prior generation batch, milestone branch or existing PR branch for a different request. Keep all scoped handoffs and applicable Stage A/Stage B reviews and corrections for this batch on that single branch; \`draft_handoff.py\` continues to commit/push without opening PRs.

**Only at the very end of this user-requested generation**, after every requested Task has completed authoring, all applicable bounded automatic QA/report handoffs have finished (including honest blocked outcomes), and the final content/report commit has been pushed, the parent runs:

\`\`\`bash
python scripts/finalize_generation_pr.py <batch-id> TASK-ID [TASK-ID ...]
\`\`\`

Supply **only** the Task IDs from this request. The finalizer verifies the branch matches the batch, is pushed and clean, and contains no files outside the declared tasks/QA evidence. It checks for an existing PR from the same head before creating a Draft PR; reruns reuse the existing open PR instead of creating duplicates. A closed/merged PR stops rather than silently making another. On a failed check, report the blocker rather than falling back to a milestone-wide PR. Leave unresolved QA findings visible in Draft. Never merge, approve or publish automatically.

**Automatic per-lesson review:** Right after each completed lesson's scoped validation and feature-branch handoff, parent MUST run Stage A of `.agents/skills/module-quality-review/SKILL.md`. Invoke existing independent `technical_reviewer` (Sol High) and `pedagogy_reviewer` (Terra Medium) for that lesson/evidence/assessment pair. Record separate lesson reports and the dedicated lesson `review_cycle.py` state. If findings exist, delegate at most **two targeted author correction rounds per lesson**, with independent targeted re-review after each. Push both reports/cycle/task memory through `draft_handoff.py --review-report`; this requires **no other lesson** to be drafted. If blocked, report why, rather than silently moving on. For multi-lesson runs, resolve each lesson's review before authoring dependent lessons.

**Automatic module-close synthesis:** Once **all lesson review cycles are ready** and the integration Story has completed draft handoff, run Stage B of `module-quality-review` once: both existing reviewers evaluate the **integrated package and module-wide cross-lesson consistency, progression, coverage and duplication**, relying on earlier lesson QA. Do **not** repeat full audits of accepted lessons. Use the separate module `review_cycle.py` state for at most **two focused synthesis correction rounds**; material changes to an accepted lesson require an explicit `review_cycle.py reopen MXX-LYY --reason "..."` and independent targeted re-review of that lesson. All content remains draft until human approval. Python does not invoke reviewers, run extra suites, silently merge or publish.

## Additional or targeted review on user request

Automatic lesson QA and module-close synthesis follow the preceding rules and are already user-authorized. For separate or targeted review requests, read the chosen reviewer skill(s); check only the specified content and review dimensions. Technical + provenance and teaching coverage + pedagogy are available combined review assignments, but neither pair is automatically launched. The user may request one dimension or a targeted section instead. Write the requested Markdown findings and, only when a review task declares it, a JSON verdict with `verdict` and `findings`; no artifact hashes. Reviewer independence matters when explicitly requested. Never claim release approval.

Explicitly update `review-status --scope SCOPE` (`in_review`, `reviewed` or `needs_review`) with a reason; preserve separate technical, provenance, coverage and pedagogy decisions. For a named review gate, scope is the review step ID and its step must be completed with a clear verdict. If material changes are later made to reviewed content, mark `needs_review`. Cosmetic changes need not reset it. The system does not inspect hashes or infer review freshness.

## If the user requests validation

Run only the extra Python commands selected by the user from `docs/workflow-contract.md`. Repository-wide validation, course coverage, task schema checks and the test suite remain on demand; scoped draft checks are already run by `draft_handoff.py`. Validation is read-only for content and does not run AI reviews, create teaching text or publish anything.

## Revisions and handoff

Edit or redo only what the user requested. To reopen completed work, issue `taskctl invalidate TASK-ID STEP-ID --reason "..."`; `--cascade` only on an explicit instruction. Never repeat `SKIP` by interpreting an old report or changed spec as stale. One can perform small authorized edits within the current draft without reopening the historical authoring task; update review state if material.

Task state and JSONL worklog record decisions. Git records content. For default lesson/integration drafts use the automatic `draft_handoff.py` command above and, when the complete module reaches QA, the paired reviewer-report handoff described by `module-quality-review`; for other work commit/push explicitly and run `taskctl handoff TASK-ID`. Use `--local-only` solely when agents share a checkout; neither mode computes task hashes. Handoff never substitutes for independent content review. User authorization is required before PR merge, human approval or publication. The owner authorizes at most **two author correction rounds per reviewed lesson** and **two separate synthesis correction rounds per module**; any additional revision requires new explicit user direction.
