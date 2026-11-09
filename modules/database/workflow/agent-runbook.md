# AI Content Workflow — Agent Runbook

## Goal

Produce draft lessons through coordinated specialist subagents, preserve progress across model/provider changes, prevent completed work from being repeated, and create reviewable Git changes. Never self-publish learner-facing content.

## Durable state locations

- GitHub Issue: task goal, Definition of Done, owner, dependencies, high-level status, branch, and PR link.
- `.academy/state/tasks/<TASK-ID>.json`: step states, dependencies, input fingerprints, output hashes, and next action.
- `.academy/state/worklog/<TASK-ID>.jsonl`: append-only checkpoints and event history.
- Git commits: the actual outputs. A step is not complete until its declared outputs are tracked and committed.
- GitHub Project: optional view over Issues/PRs; do not store a second copy of step progress there.

## Before starting or switching AI

1. Read root `AGENTS.md` and `.academy/state/README.md`.
2. Open the matching GitHub Issue; verify task ID, goal, owner, branch, dependencies, and linked PR.
3. Read task JSON and JSONL worklog.
4. Inspect `git status`, current branch, latest commit, and PR.
5. Run `python scripts/taskctl.py status <TASK-ID>`.
6. Do not repeat `SKIP`; resume `RESUME` from its checkpoint; inspect `STALE`; do not start `BLOCKED` work.
7. If this is genuinely new work, follow `task-intake` and create a state record before delegation.

## Inputs

- `curriculum/database-module.md`
- `sources/source-registry.csv`
- `governance/content-guidelines.md`
- `governance/attribution-policy.md`
- `governance/qa-checklist.md`
- `workflow/lesson-template.md`
- The exact GitHub Issue acceptance criteria and task-specific input paths declared in task JSON.

## Multi-agent workflow

### Phase A — Prepare (parallel, no shared writes)

1. Parent identifies the task and checks each step state. Start only steps that are `READY`.
2. Spawn `source_researcher` with `source-research`. It returns claim/source evidence and unresolved facts.
3. Spawn `curriculum_designer` with `curriculum-design`. It returns prerequisite gaps, outcome mapping, and sequencing.
4. Wait for both. Parent reconciles evidence and owns shared source/curriculum files.
5. Commit the declared outputs and mark each step complete using `taskctl`.

### Phase B — Author (bounded writes)

6. Spawn `lesson_author` with `lesson-authoring` and `assessment-design`. Assign exactly one lesson file and unique output paths.
7. The author uses approved evidence and creates original prose, Mermaid, examples, exercises, quizzes, answers, and rubrics.
8. Parent checks output and updates shared files. No other agent edits the same paths.
9. Commit outputs and update task state through `taskctl`.

### Phase C — Independent review (parallel, separate report paths)

10. Spawn `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer` in parallel.
11. Wait for all three. Consolidate findings with severity, location, evidence, and recommended action.
12. Assign corrections to `lesson_author`; maximum two revision cycles. Record changed inputs so fingerprints can invalidate only affected steps.

### Phase D — Validate and hand off

13. Run `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`.
14. Store the validation report in its declared output path, commit it, and mark the step complete.
15. Prepare QA reports, source registry updates, run report, and draft PR.
16. Stop at `ready-for-human-review`; only a human can approve or publish.

## Checkpoint and resume protocol

Before a model/provider change or context end, run:

```bash
python scripts/taskctl.py checkpoint TASK-ID STEP-ID \
  --note "Completed work, evidence checked, files changed, unresolved items" \
  --next-action "One concrete next action for the next agent"
```

The next agent must inspect the saved checkpoint and files before resuming:

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME --resume
```

If a completed step is `STALE`, inspect the diff first. Use `invalidate TASK-ID STEP-ID --reason "..." --cascade` only when intentionally rerunning that step and its dependents. Do not delete or overwrite old artifacts automatically.

## Permissions and concurrency

- One active writer per task/lesson. GitHub Issue identifies the owner; the branch and output paths define the write scope.
- Read-only reviewers may run in parallel only when each has a distinct report path.
- A custom subagent's "do not edit" instruction is not enforced access control. Subagents inherit parent permissions; configure the parent/host session for actual read-only behavior.
- The state JSON is not a distributed lock. Two independent clones must coordinate ownership in GitHub before writing.
- Concurrency is capped at four; each subagent consumes additional model/tool usage.
- Stop after two unsuccessful revision cycles or when evidence is insufficient.

## Research tiers

- Standard search: bounded factual lookup.
- Document analysis: read exact official documentation already identified.
- Deep Research: disputed topics or synthesis across many independent sources.

## Output contract

For each lesson: lesson Markdown (`status: draft`), technical report, pedagogy report, provenance report, claim/source evidence, unresolved issues, and human actions.

Final report: task ID, step state (`SKIP`/`READY`/`STALE` etc.), artifact paths/commit SHAs, source coverage, three review verdicts, structural validation, unresolved claims, and PR link.