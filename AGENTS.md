# System Design Academy — Agent Instructions

## Boundaries
- Work only on the user-authorized task, module and lesson IDs. Never expand scope or generate other lessons implicitly.
- The official SDA-v1 plan is in `curriculum/revision-1/`; root-level course files are historical candidates. Use the chosen approved version at intake.
- Original English teaching content for middle/senior engineers; keep learner-facing lessons `status: draft`. Use one canonical lesson/assessment/evidence file per Lesson ID from the backlog, and Git for revisions; no nested lesson revisions or content manifests.
- Use exact primary-source references when making technical claims. Primer is a licensed topic map, not the sole factual authority; create original teaching, examples, diagrams and exercises.
- Do not fabricate citations, legal permissions, benchmarks or test results. Do not commit credentials or private learner data.
- Never publish, merge or claim human approval without an explicit user decision.

## Task memory and explicit state
- For a meaningful multi-step task, reuse or create a GitHub Issue, `.academy/specs/<TASK-ID>.json`, `.academy/state/tasks/<TASK-ID>.json`, and `.academy/state/worklog/<TASK-ID>.jsonl`.
- Read spec, state, worklog, relevant feedback and Git history before working. One active writer per task. The Issue coordinates ownership; the spec is authoritative.
- `python scripts/taskctl.py status TASK-ID` reads only recorded states. `SKIP` means explicitly completed, `READY` means eligible, `RESUME` means in progress, and `BLOCKED` means a dependency, hold or manual review gate requires attention.
- No automatic `STALE`, checksums, fingerprints or dependency invalidation. Editing files/specs never changes a completed step's status.
- Start only authorized pending/reopened work; `taskctl start` and `complete` record progress. Only `taskctl invalidate TASK-ID STEP-ID --reason "..."` reopens completed work. `--cascade` must be specifically requested; do not infer cascades.
- Explicitly flag meaningful changes to reviewed content with `taskctl review-status TASK-ID --scope technical --state needs_review --reason "..."` (or the affected scope). The default `general` scope does not certify technical, pedagogy or named review gates. Review status is not publication approval.
- Preserve old task/worklog/report history; legacy hashes are inert. For generated lesson/integration drafts, the parent runs `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]` after task completion: focused validation, selective commit/push to a feature branch, then remote `taskctl handoff`. For other work, commit/push and invoke `taskctl handoff TASK-ID` explicitly. `--local-only` is only for agents sharing a checkout. No checksums or automatic merge. A completed task with missing files shows a warning; its historical status remains unchanged.

## Default workflow
- `.academy/state/task.template.json`: research → author draft lesson + companion assessment. The author reads `assessment-design`, `content-format` and `GOVERNANCE.md` (declared inputs) for outcome alignment, source integrity and safe Markdown without compromising depth. `init` resolves all three output paths from the matching `delivery/backlog.json` Story (`proposed_task_id`), not by concatenating Task ID.
- `.academy/state/course.template.json`: draft a new versioned plan/inventory/matrix.
- `.academy/state/workflow.template.json`: implementation.
- After the requested lesson or integration draft is complete, the **parent orchestrator** runs `python scripts/draft_handoff.py TASK-ID [TASK-ID ...]` once per batch. It invokes only scoped, deterministic lesson/assessment or integrated Markdown checks, then commits/pushes declared artifacts and task memory to a `codex/`, `feature/` or `feat/` branch (creating a `codex/drafts-*` branch if necessary). On validation or Git failure, stop and report; never auto-fix, force-push or merge. No extra task step, full test suite or CI invocation; any automatic revisions run only inside the bounded module review loop after quality findings. **After a complete module's lesson and integration drafts have been handed off**, the parent MUST follow `.agents/skills/module-quality-review/SKILL.md`: run independent `technical_reviewer` and `pedagogy_reviewer` using unchanged model settings, record findings, **automatically assign targeted fixes to the appropriate Author**, then re-review changed content and dependencies, capped at two correction rounds through `scripts/review_cycle.py`. Commit/push both reports and persistent cycle state via `draft_handoff.py --review-report`. On unresolved critical issues or exhausted rounds, stop and report. Incomplete modules do not trigger review.
- Beyond the standing **automatic module-close review**, an explicit **review** request invokes only the requested reviewer(s): technical/source rights, teaching/coverage/pedagogy, or comprehensive. Reviewer findings must be attributable to content locations; unresolved blocker/major findings cannot be declared clear.
- Additional **validation** (repository-wide, coverage, task schemas or tests) is on demand; the scoped draft handoff check is the sole automatic exception. A review request does not imply broad validation, and validation never implies AI review.
- Before Author and module reviewers begin, the parent selects only context-relevant verified past corrections via `python scripts/learning_memory.py suggest --tags TAGS --role ROLE --limit 3`. After a successful corrective re-review, the parent uses `learning_memory.py record` to save concise source-backed generalizable prevention rules; blocked/unresolved findings never enter reusable memory. Repeated confirmed mistakes across two modules produce a separate skill-update PR for human approval, not automatic skill edits. Follow `module-quality-review` for evidence and lifecycle requirements.
- Keep teaching and assessment separate; outcomes must be taught and assessed. AI writes canonical Markdown/YAML for direct website consumption; no custom converter. The single format authority is `docs/authoring-format-contract-v1.md`, while teaching quality remains with the authoring/assessment skills and `GOVERNANCE.md`. Read `.agents/skills/module-pipeline/SKILL.md` for details.
- User approval is required before publication, including when a draft has passed optional review and structural checks.

## Parallelism and permissions
- The parent orchestrator owns shared files and task state; delegate only bounded, non-overlapping outputs.
- One active writer per task. The task JSON is not a distributed lock.
- Agent instructions are not an access-control mechanism. Codex subagents inherit parent permissions; enforce boundaries in the actual host/sandbox.
- Stop at unresolved evidence or user-controlled decisions. Never spawn additional tasks to satisfy optional gates without authorization.
