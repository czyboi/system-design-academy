# Persistent task state and idempotent execution

## Canonical records

Each task has three separate durable records:

- **Task specification** — `.academy/specs/<TASK-ID>.json`. This is the only canonical source for goal, scope, constraints, Definition of Done, and acceptance criteria. It is versioned and committed with the work.
- **Task execution state** — `.academy/state/tasks/<TASK-ID>.json`. This stores owner, step graph, execution lifecycle, fingerprints, run baseline, checkpoints, and artifact hashes. It references the specification but does not duplicate its requirements.
- **Worklog** — `.academy/state/worklog/<TASK-ID>.jsonl`. Append-only event/checkpoint history.

GitHub Issue is the coordination interface: task ID, owner, branch, links to the specification/state/PR, dependencies, and a short summary. It is not a second specification. When there is a conflict, the committed specification file wins; update the Issue summary/link to match.

Git commits are the durable artifacts. The task state file is not a distributed lock. Use one active writer per task/lesson and coordinate ownership in the Issue.

## Create a task

Install development dependencies once:

```bash
pip install -r requirements-dev.txt
```

Create the state and specification templates:

```bash
python scripts/taskctl.py init SD-DB-INDEXES \
  --module database \
  --goal "Create and review the indexes lesson" \
  --owner "@username" \
  --template .academy/state/task.template.json
```

This creates:
- `.academy/state/tasks/SD-DB-INDEXES.json`
- `.academy/specs/SD-DB-INDEXES.json`

Edit the specification before execution. Replace all TODO placeholders; specify the scope, constraints, DoD, and testable acceptance criteria. Every DoD and acceptance criterion must declare `applies_to`: a list of step IDs or `["*"]`. Use step-specific IDs to avoid invalidating unrelated work. Add/remove task steps and make every output path unique.

Commit the specification, task state, and worklog before starting. The task owner is mandatory.

## Execution protocol

1. Read `AGENTS.md`, the GitHub Issue, task specification, task state, and worklog.
2. Inspect branch, `git status`, and recent commits.
3. Run `python scripts/taskctl.py status TASK-ID`.
4. Respect calculated results: `SKIP` = do not repeat; `RESUME` = continue from checkpoint; `READY` = eligible to start; `STALE` = inspect and selectively rerun; `BLOCKED` = resolve dependency first.
5. Before editing, run `start`. It requires committed and clean inputs/specification, and records the starting commit plus SHA-256 input/output snapshots. Commit the updated task JSON/worklog before editing.
6. Commit output files before `complete`. Completion verifies input/specification snapshots, dependency fingerprints, committed outputs, and output changes after the start commit.
7. If an unchanged pre-existing artifact is intentionally reused, explicitly provide `--reuse-output PATH --reuse-reason "..." `. Reuse is recorded in the completion event. Do not use this to hide output edits.
8. After every state mutation, commit task JSON and JSONL worklog. Checkpoint before a provider/context handoff and commit it.
9. Update the GitHub Issue with short progress and links, never duplicate the canonical specification.

Example:

```bash
python scripts/taskctl.py status SD-DB-INDEXES
python scripts/taskctl.py start SD-DB-INDEXES research --agent source_researcher
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl
git commit -m "Start source research"

# Produce and commit the declared output(s).
python scripts/taskctl.py checkpoint SD-DB-INDEXES research \
  --note "Verified PostgreSQL behavior; MySQL comparison remains open." \
  --next-action "Complete the MySQL check."
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl
git commit -m "Checkpoint source research"

# After committing outputs:
python scripts/taskctl.py complete SD-DB-INDEXES research --agent source_researcher
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl
git commit -m "Record source research completion"
```

## Fingerprints and selective invalidation

Each step fingerprint includes:
- the step ID and `definition_version`;
- hashes of declared input files;
- a hash of the relevant task-specification slice: goal, scope, constraints, and only DoD/acceptance criteria applying to this step (or `*`);
- dependency fingerprints and output hashes.

Thus, changing a step-specific acceptance criterion invalidates that step and downstream dependents. Independent steps remain reusable. Changing global goal/scope/constraints intentionally invalidates all steps because those changes may alter the whole task.

A completed step is `SKIP` only if its fingerprint matches, every output exists, output hashes match, and outputs remain Git-tracked and clean. The engine does not silently rewrite prior artifacts.

## Automation versus human decisions

The CLI manages **automation only**. Its final aggregate state is `automation_complete`, never `approved` or `published`.

Human workflow is separate and explicit:
`in_progress → automation_complete → ready_for_human_review → human_approved → published`.

The latter three are controlled through human GitHub review/merge or the future publishing process, not taskctl. A passing CI check is structural validation, not human approval, technical truth, or legal clearance.

## Commands

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME --resume
python scripts/taskctl.py checkpoint TASK-ID STEP-ID --note "..." --next-action "..."
python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT-NAME
python scripts/taskctl.py complete TASK-ID STEP-ID --reuse-output path/to/file --reuse-reason "..."
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "..." --cascade
python scripts/taskctl.py validate
```

## Portability and boundaries

Task specification/state/worklog are plain JSON/JSONL so every provider can read them. Provider-specific agent profiles are thin wrappers over the shared skills under `.agents/skills/`. The CLI requires Python, Git, and dependencies in `requirements-dev.txt`.

This is a lightweight repository-based checkpoint system, not a distributed lock or hosted workflow engine. It cannot prevent two independent clones from racing; coordinate one active writer in GitHub.

## Review gates, task controls and scoped checks

`status` now computes its display without writing files. Use `reconcile TASK-ID` explicitly to save aggregate status. A historical task becoming stale does not authorize rerunning it.

`hold TASK-ID --state paused --reason "User decision"` and `hold ... --state awaiting-human --reason "Unresolved blocker"` prevent start/resume and completion. Use `resume-task TASK-ID --reason "Explicit user resumption"` only after that direction. Existing tasks default to active for compatibility; consult their worklog for older stop decisions before migrating or starting them.

New review contracts bind verdicts to exact artifact hashes. Completing a review records execution, including a negative verdict; `requires_reviews` separately controls acceptance. Revisions may depend on negative reviews without requiring acceptance. See [CLI contract](../../docs/workflow-contract.md) for JSON and commands.

Use `validate_content.py --scope workflow` for tooling, `--scope curriculum --plan PATH --matrix PATH` for plan plus CSV coverage, and `--scope lesson --lesson PATH --assessment PATH` for each selected package. The default repository check validates current canonical packages and shared configuration. Historical pilot inventories and run snapshots are not active content manifests.
