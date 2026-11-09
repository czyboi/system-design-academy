# System Design Academy

An AI-assisted, source-grounded curriculum project for backend engineers learning system design.

> Project status: Early development. The Database module is a pilot, not publication-ready courseware.

## Repository structure

- .agents/skills/: canonical shared procedures for all providers.
- .codex/agents/: Codex-specific role adapters.
- .claude/agents/: Claude Code role adapters referencing shared skills.
- .academy/specs/: canonical, versioned task specifications.
- .academy/state/: execution state, JSON Schema, templates, and append-only worklogs.
- scripts/taskctl.py: spec-aware fingerprints and reproducible execution gates.
- scripts/validate_content.py: structural course-content validation.
- tests/: task engine and configuration integration tests.
- modules/database/: Database pilot content and workflow.

## Hybrid task state and anti-repeat protocol

Each task has one canonical specification at .academy/specs/<TASK-ID>.json. It contains the goal, scope, constraints, Definition of Done, and acceptance criteria. The GitHub Issue coordinates ownership, branch, dependencies, and links; it must not duplicate detailed requirements.

Execution state lives in .academy/state/tasks/<TASK-ID>.json; event/checkpoint history is appended to .academy/state/worklog/<TASK-ID>.jsonl. All AI providers use the same JSON/JSONL records and Git commits.

Initialize a task with:

    pip install -r requirements-dev.txt
    python scripts/taskctl.py init TASK-ID --module MODULE --goal "..." --owner "@username" --template .academy/state/task.template.json

Edit the generated task specification and remove all TODO placeholders before starting. Declare which steps each DoD/acceptance criterion governs.

Run python scripts/taskctl.py status TASK-ID. The engine returns SKIP, RESUME, READY, STALE, or BLOCKED. A fingerprint includes the relevant specification slice, declared input hashes, definition version, and dependency fingerprints/output hashes. A step-specific criterion change invalidates only that step and its downstream dependencies; unrelated work remains reusable.

Start requires committed, clean inputs/specification and records the starting commit plus input/output snapshots. Complete verifies the inputs/spec are unchanged and the outputs are committed/changed during the run. Intentional reuse of an unchanged artifact requires --reuse-output PATH --reuse-reason "...".

See .academy/state/README.md and docs/task-state-and-idempotency.md for the full protocol.

## Automation versus human approval

The CLI can reach automation_complete only. Human review, approval, PR merge, and publication remain separate human-controlled gates. Passing CI is structural validation, not factual, legal, or pedagogical approval. Never auto-publish learner-facing content.

## Agent architecture

Shared procedures live in .agents/skills/. Codex profiles are in .codex/agents/; Claude Code project profiles are in .claude/agents/ and point to shared skills rather than copying instructions. The parent orchestrator owns dependencies, state transitions, shared files, and final synthesis.

## First pilot: Database

Start with modules/database/README.md. It contains seven lessons, one capstone case study, a source registry, templates, workflow, and a first-pass QA report.

## Validation

    pip install -r requirements-dev.txt
    python scripts/validate_content.py
    python -m unittest discover -s tests -v
    python scripts/taskctl.py validate

Structural CI does not establish factual correctness, source availability, legal permission, executable lab correctness, or teaching quality. See GOVERNANCE.md and the Database attribution policy.
