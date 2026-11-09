# AI Content Workflow — Agent Runbook

## Goal
Produce source-grounded draft lessons through specialist agents, preserve progress across provider changes, and prevent completed work from repeating. Never self-publish learner-facing content.

## Durable records
- Canonical task requirements: `.academy/specs/<TASK-ID>.json` (goal, scope, constraints, DoD, acceptance criteria).
- Execution state: `.academy/state/tasks/<TASK-ID>.json` (owner, dependency graph, fingerprints, run metadata, output hashes).
- Worklog: `.academy/state/worklog/<TASK-ID>.jsonl` (append-only event/checkpoint history).
- GitHub Issue: owner, branch, dependencies, links, short coordination summary. It does not duplicate the spec.
- Git commits and PR: durable outputs, audit history, and review surface.

## Before starting or switching AI
1. Read `AGENTS.md` and `.academy/state/README.md`.
2. Open the Issue; verify task ID, owner, branch, dependencies, and linked PR.
3. Read the canonical spec, task JSON, and worklog.
4. Inspect Git status/branch/commits.
5. Run `python scripts/taskctl.py status <TASK-ID>`.
6. Do not repeat SKIP; resume unchanged RESUME; inspect STALE; do not start BLOCKED.
7. Ensure spec has no placeholders and every DoD/acceptance criterion applies to its relevant step(s).
8. Commit state/worklog after each state mutation; checkpoint and commit before handoff.

## Multi-agent workflow
### Phase A — Research and curriculum (parallel)
- Parent starts only READY research and curriculum steps.
- Source researcher produces claim/source evidence and unresolved facts.
- Curriculum designer maps prerequisites, outcomes, and sequencing.
- Wait for both; parent reconciles shared files and evidence.

### Phase B — Author
- Author one assigned lesson with unique output paths.
- Use approved evidence and original prose/examples/exercises/quizzes.
- Parent owns shared source registry, manifests, and task state.

### Phase C — Independent review
- Technical, pedagogical, and provenance reviewers each use their shared skill and write to distinct report files.
- Parent consolidates findings; maximum two revision cycles.

### Phase D — Validate and hand off
- Run `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`.
- Commit outputs, then use `taskctl complete`; commit state/worklog.
- Report artifact paths, commits, sources, verdicts, structural validation, unresolved claims, and next action.
- Stop at `automation_complete` / `ready_for_human_review`. Human approval, merge, and publication remain separate explicit gates.

## Start and complete integrity
- `start` requires Git-tracked, clean input/spec files. It records starting commit, input/spec hashes, and output hashes at start.
- `complete` rechecks inputs/spec, verifies output files are tracked and clean, and requires new committed output changes.
- If an unchanged artifact is intentionally reused, pass `--reuse-output PATH --reuse-reason "..."`; it is visible in state and worklog.
- An output existing before a run is not proof it was produced by that run.

## Concurrency and permissions
- One active writer per task/lesson; task state is not a distributed lock.
- Reviewers may run concurrently only with different report paths.
- Codex subagents inherit parent permissions; "do not edit" is not a hard read-only permission boundary.
- Claude Code profiles and Codex profiles are adapters over shared skills in `.agents/skills/`.
