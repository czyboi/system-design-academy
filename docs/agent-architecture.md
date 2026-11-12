# Agent architecture — user-directed execution

## Layers

| Layer | Responsibility | Location |
| --- | --- | --- |
| Shared skills | Research, curriculum, authoring, optional reviews and handoff | `.agents/skills/` |
| Provider profiles | Role and model configuration | `.codex/agents/`, `.claude/agents/` |
| Parent orchestrator | Authorization, scoped delegation, task state, final handoff | `AGENTS.md`, module-pipeline |
| Persistent memory | Canonical task specs, explicit state, append-only history | `.academy/specs/`, `.academy/state/`, Git |
| GitHub | Issues, ownership, PR review and commits | GitHub |

Shared skills are canonical. A profile is an adapter, not an independently duplicated workflow. Only the parent changes shared task state; subagents own bounded, non-overlapping work. A task JSON is not a distributed lock.

## Specialist roles

- Source researcher: evidence for claims.
- Curriculum designer: outline, prerequisites and coverage mapping.
- Lesson author: English original draft lesson and assessment.
- Technical, provenance, coverage and pedagogy reviewers: **optional, explicitly requested** audits.
- PR reviewer: explicitly requested code/change review.

## Task and review status

`.academy/specs/<TASK-ID>.json` is the requirements source; Issue prose is coordination. `.academy/state/tasks/<TASK-ID>.json` records explicit step statuses, checkpoints and separate `review_status`; the JSONL worklog records past actions.

Task completion is not recomputed from file bytes, task requirements or dependencies. There are no active fingerprints, SHA-256 snapshots or automatic STALE cascades. `invalidate` reopens only when explicitly commanded. Review state changes manually (`not_reviewed`, `in_review`, `reviewed`, `needs_review`). Old hashes in historical files are not interpreted.

## Default operation

Research and author one draft package, then stop. Code validators, AI reviewers, revision cycles and content audits run independently only when requested. A reviewer does not automatically launch validation, and a validation command does not call AI reviewers. Use Git commits and worklog checkpoints for continuity, not content fingerprints.

Review status is not a human publishing approval. Do not merge or publish without user authorization. Host/sandbox permissions — not agent text — enforce read-only access; Codex child agents inherit parent permissions. Coordinate one writer to prevent races.

The official curriculum version remains SDA-v1 under `curriculum/revision-1/`. Use it as the default for authoring unless the user selects a newer approved version.
