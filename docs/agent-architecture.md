# Agent Architecture

## Shared and provider-specific layers

| Layer | Responsibility | Repository location |
|---|---|---|
| Shared skills | Canonical procedures for research, curriculum, authoring, assessment, review, intake, and handoff | .agents/skills/ |
| Codex adapters | Codex-specific role/configuration | .codex/agents/*.toml |
| Claude Code adapters | Claude Code project subagents with YAML frontmatter | .claude/agents/*.md |
| Orchestration | Parent sequences/delegates, owns shared files/state, synthesizes results | module-pipeline skill + AGENTS.md |
| Persistent memory | Requirements, run state, checkpoints, artifact history | .academy/specs/, .academy/state/, Git commits |

The skill content is canonical. Provider-specific agent files point to shared skills and add only role/configuration details. Do not fork the instructions per provider.

A skill is a reusable procedure, not an autonomous worker. A subagent is a specialist worker, not a durable workflow engine. The parent owns orchestration and task-state transitions.

## Roles

- Parent/orchestrator: scope, canonical specification, ownership, shared files, checkpoints, decisions, final PR.
- source_researcher: claim-level source evidence.
- curriculum_designer: prerequisite map and learning sequence.
- lesson_author: assigned draft lesson and assessments.
- technical_reviewer: independent factual review.
- pedagogy_reviewer: learning design and assessment review.
- provenance_reviewer: citation, attribution, and asset-rights review.

## Canonical task records

- .academy/specs/<TASK-ID>.json: goal, scope, constraints, Definition of Done, acceptance criteria, and step applicability. This is canonical.
- GitHub Issue: owner, branch, dependencies, PR/spec/state links, and short coordination summary. It is not a second copy of requirements.
- .academy/state/tasks/<TASK-ID>.json: step DAG, active run, checkpoint, fingerprints, output hashes, and automation lifecycle.
- .academy/state/worklog/<TASK-ID>.jsonl: append-only event history.
- Git commits: durable outputs and audit trail.
- GitHub PR: review and integration status.

## Spec-aware idempotency

Each step fingerprint covers its ID and definition version, hashes of declared file inputs, the canonical hash of its relevant specification slice, and dependency fingerprints/output hashes.

A specification slice includes global goal/scope/constraints and only DoD/acceptance-criteria entries applying to that step. Changing one step-specific criterion invalidates that step and downstream dependents; unrelated steps remain SKIP. A global goal/scope/constraint change invalidates all steps because those assumptions apply to the task as a whole.

Before start, taskctl requires Git-tracked clean inputs/specification and records a starting commit and input/output snapshots. Complete rechecks those snapshots and requires outputs to be tracked, clean, and committed after start. An unchanged existing output needs explicit, reasoned reuse.

## Automation and human lifecycle

The CLI controls only the automation lifecycle: not_started → in_progress → automation_complete (or blocked).

Human lifecycle is separate: automation_complete → ready_for_human_review → human_approved → published. These transitions are not controlled by taskctl. Human review, PR approval/merge, and publication remain explicit human actions.

## Safe parallelism and permissions

- Parallelize independent research/review tasks with unique output paths.
- Parent owns shared files, task-state transitions, and final integration.
- Never let multiple agents write the same lesson or task state.
- The task JSON is not a distributed lock; use GitHub Issue ownership for one active writer.
- Codex subagents inherit parent session permissions; role instructions do not enforce read-only security.
- Claude agent frontmatter is configuration, not a substitute for host permissions.
- Stop after two unsuccessful revision cycles or when evidence is insufficient.

## Provider usage

Codex: use .codex/agents/ and shared skills under .agents/skills/. Configure actual permissions at the parent/host session layer.

Claude Code: project subagents live in .claude/agents/*.md with YAML frontmatter. Each profile explicitly points to the canonical skill in .agents/skills/. The profile is an adapter, not a duplicate skill manual.

Other providers / ChatGPT Work: do not assume they load Codex or Claude-specific profiles. Give role instructions explicitly and ask the agent to read the same specification, state, worklog, and shared skill. Run repository scripts where possible; do not claim validation otherwise.

## Limits

This is a repository-based checkpoint system, not a remote job runner or distributed lock service. It supports provider handoff through committed files; separate clones must still coordinate writer ownership through GitHub.
