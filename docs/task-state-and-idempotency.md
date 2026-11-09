# Task state, checkpoints, and idempotency

## Canonical task specification

Every task has one versioned source of truth:
`.academy/specs/<TASK-ID>.json`.

It contains the task goal, scope, constraints, Definition of Done, acceptance criteria, and per-step applicability. GitHub Issue is the coordination surface and links to that file; it must not maintain a competing copy of the detailed requirements. When Issue prose conflicts with the committed specification, the specification wins and the Issue summary should be corrected.

Execution state is stored separately in `.academy/state/tasks/<TASK-ID>.json`; event history is appended to `.academy/state/worklog/<TASK-ID>.jsonl`.

## Selective fingerprints

A step fingerprint includes its definition version, declared input hashes, dependency fingerprints/output hashes, and the hash of its relevant spec slice. The slice includes global goal/scope/constraints plus only DoD and acceptance-criteria entries whose `applies_to` includes that step or `*`.

Consequences:
- changing one step's acceptance criterion invalidates that step and its downstream dependency chain;
- independent steps remain `SKIP`;
- changing global goal, scope, or constraints invalidates every step because these are task-wide assumptions.

The task specification is validated against `.academy/state/schema/spec.schema.json`. Execution is blocked while DoD or acceptance criteria contain placeholders or lack applicability to a step.

## Reproducible execution

Before a step starts, `taskctl` requires the declared inputs and task spec to be Git-tracked and clean. It records:
- starting Git commit;
- SHA-256 of each declared input and the task spec;
- output hashes as they existed at start;
- active spec hash and step fingerprint.

At completion it verifies that inputs/specification did not change, the starting commit is an ancestor of HEAD, outputs exist and are tracked/clean, and every output changed in a commit after start. An unchanged pre-existing output is accepted only with explicit `--reuse-output` and a recorded reason. Reuse is narrow and visible in the task state/worklog.

A completed step is reusable only when its current fingerprint and output hashes still match and the outputs remain tracked/clean.

## Automation and human lifecycle

`taskctl` controls only the automation lifecycle:
`not_started → in_progress → automation_complete` (or `blocked`).

Human review and release are explicit separate states:
`automation_complete → ready_for_human_review → human_approved → published`.

These are not transitions managed by taskctl. Human review/approval, PR merge, and learner-facing publication remain explicit human actions. CI passing is not human approval.

## Cross-provider handoff

The receiving AI:
1. Reads the GitHub Issue for owner, branch, dependencies, and links.
2. Reads the task specification, state, and JSONL worklog from the current branch.
3. Inspects Git status, commits, and the PR.
4. Runs `python scripts/taskctl.py status <TASK-ID>`.
5. Does not repeat `SKIP`; resumes only unchanged `RESUME`; starts only `READY`; inspects `STALE`; waits on `BLOCKED`.
6. Commits the start/checkpoint before handoff and outputs before marking complete.
7. Reports the state-file, spec-file, latest commit, blockers, and next action in the Issue.

The state file is not a distributed lock. GitHub ownership must establish one active writer per task.
