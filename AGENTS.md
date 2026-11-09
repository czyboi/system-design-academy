# System Design Academy — Repository Instructions

## Project guardrails
- Work only on the explicitly requested module and lesson IDs.
- Prefer standards/RFCs and official vendor documentation. Record exact URL/section, product/version, and date checked.
- Treat System Design Primer as topic map and licensed source material, not sole technical authority. Do not translate it paragraph-by-paragraph or copy third-party assets without separate rights checks.
- Create original explanations, examples, diagrams, exercises, quizzes, and answer explanations.
- Keep generated lessons at `status: draft`. Never merge a PR or publish learner-facing content without explicit human approval.
- Never invent citations, benchmarks, guarantees, versions, licenses, or test results. Mark unresolved claims.
- Never commit credentials, API keys, tokens, learner data, or secrets.

## Persistent task protocol
- For every multi-step task, find or create the matching GitHub Issue and task ID. Reuse equivalent work; do not create duplicates.
- The canonical requirements are in `.academy/specs/<TASK-ID>.json`. Do not treat Issue prose as a second specification.
- The task execution state is `.academy/state/tasks/<TASK-ID>.json`; event history is `.academy/state/worklog/<TASK-ID>.jsonl`.
- Read `.academy/state/README.md`, the Issue, spec, state, and worklog before acting. Inspect branch, commits, and `git status`.
- Run `python scripts/taskctl.py status <TASK-ID>`. Never repeat `SKIP`; inspect and selectively handle `STALE`; resume only unchanged `RESUME`; start only `READY`; do not run `BLOCKED`.
- Initialize with `python scripts/taskctl.py init TASK-ID --module MODULE --goal "..." --owner "@username" --template .academy/state/task.template.json`. Complete the spec and remove placeholders before execution.
- `start` records clean tracked input/spec hashes and a starting commit. Commit the task state/worklog before editing.
- Commit declared outputs before `complete`. Completion verifies input/spec stability and requires new committed output, unless intentional reuse is explicitly recorded with `--reuse-output PATH --reuse-reason "..."`.
- Commit state/worklog after every mutation. Checkpoint and commit before handing off to another provider/session.
- One active writer per task. The JSON state is not a distributed lock.

## Skills and agents
- Shared procedures live only in `.agents/skills/`. Codex profiles live in `.codex/agents/`; Claude Code project subagents live in `.claude/agents/`.
- Provider-specific files must reference the shared skill and define only role/configuration; do not fork the procedure into provider profiles.
- Parent/orchestrator owns task state, shared files, final synthesis, and PR preparation. Use specialist agents only on bounded, distinct outputs.
- A "do not edit" instruction is not an enforced permission boundary. Codex subagents inherit parent permissions. Configure actual host/session permissions where read-only behavior is required.
- Do not have multiple agents edit the same output. Maximum two automated revision cycles; stop for human judgment if a critical disagreement remains.

## Content and approval gates
- Every lesson needs outcomes, prerequisites, motivating problem, mechanism, worked example, trade-offs/failure modes, exercise, 5–8 knowledge checks with explanations, and direct references.
- Map every learning outcome to an assessment. Distinguish general principles from vendor-specific semantics.
- Run `pip install -r requirements-dev.txt`, `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate`.
- CI structural validation does not establish factual correctness, legal rights, source reachability, or pedagogical quality.
- Automation completion is not human approval. Keep the PR draft until reviewers explicitly approve; never auto-publish learner-facing content.
