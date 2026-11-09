# Persistent task state and idempotent execution

This directory is the repository's durable execution memory. It is deliberately plain JSON/JSONL so that Codex, Claude Code, ChatGPT Work, and other agents can read it without a provider-specific memory feature or extra runtime dependency.

## Source of truth

- **GitHub Issue:** task identity, goal, acceptance criteria, owner, high-level status, dependencies, and cross-agent handoff link.
- **Task state JSON:** exact steps, dependencies, input fingerprints, output hashes, active run, and checkpoint. This is the execution source of truth for one task.
- **Git commits:** durable artifacts. A step cannot be marked complete until all declared outputs are tracked and committed.
- **Worklog JSONL:** append-only-by-convention event history. Never rewrite old events; add a new event instead.
- **GitHub PR:** review and integration status. The Project board is a view over Issues/PRs, not a second task database.

Do not copy the same detailed progress into several places. Put a short summary and links in the Issue; keep step-level execution state here.

## Create a task

```bash
python scripts/taskctl.py init SD-DB-INDEXES \
  --module database \
  --goal "Create and review the indexes lesson" \
  --template .academy/state/task.template.json
```

The template is a starter pipeline. Adjust its `input_paths`, `output_paths`, and `definition_version` values for the exact module/lesson. Add or remove steps if the task is smaller/larger. Every output path must have exactly one owning step.

Without `--template`, `init` creates an empty task and `add-step` can define steps:

```bash
python scripts/taskctl.py add-step SD-DB-INDEXES research \
  --title "Research primary sources" \
  --definition-version v1 \
  --input-paths .agents/skills/source-research/SKILL.md GOVERNANCE.md \
  --output-paths modules/database/workflow/runs/SD-DB-INDEXES/evidence.md
```

## Normal agent protocol

1. Read root `AGENTS.md`, the linked GitHub Issue, task JSON, and this guide.
2. Run `python scripts/taskctl.py status TASK-ID` before doing work.
3. `SKIP` means **do not repeat**: the exact inputs and all outputs still match the completion record.
4. `RESUME` means inspect the saved checkpoint and existing files, then run `start ... --resume`; do not start over.
5. `STALE` means the input fingerprint or output has changed. Inspect the diff and decide which step(s) need to run again. Never overwrite artifacts blindly.
6. `READY` means dependencies are fresh and the step may start. Start it before editing.
7. After every state-mutating `taskctl` command, commit the task JSON and its JSONL worklog to the active branch. Commit the `start` state before editing files, and commit a checkpoint before switching context/provider.
8. Commit the step's declared output files, then run `complete`. Commit the updated task JSON/worklog after completion too. If it rejects the completion, resolve the Git/output issue rather than editing state manually.
9. Update the GitHub Issue with a brief summary, current state file path, branch/PR, and next action.

Example:

```bash
python scripts/taskctl.py status SD-DB-INDEXES
python scripts/taskctl.py start SD-DB-INDEXES research --agent source_researcher
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl && git commit -m "Start source research step"
# create and commit the declared output(s)
python scripts/taskctl.py checkpoint SD-DB-INDEXES research \
  --note "Verified the index behavior against the cited PostgreSQL docs; MySQL comparison remains open." \
  --next-action "Finish the MySQL version check and update the evidence note."
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl && git commit -m "Checkpoint source research"
python scripts/taskctl.py complete SD-DB-INDEXES research --agent source_researcher
git add .academy/state/tasks/SD-DB-INDEXES.json .academy/state/worklog/SD-DB-INDEXES.jsonl && git commit -m "Record completed source research"
```

## Fingerprint and skip rules

A step fingerprint is SHA-256 over canonical JSON containing:

- its `step_id` and `definition_version`;
- SHA-256 hashes (or explicit missing markers) of every declared `input_path`;
- each dependency's current fingerprint and output hashes.

A step is reusable only when its stored completion fingerprint matches the newly calculated fingerprint, every declared output exists, and each current output hash matches the stored output hash. This protects against both changed inputs and someone editing a supposedly completed artifact.

When any upstream dependency changes, dependent fingerprints change automatically. The tool reports the dependent step as `BLOCKED` until upstream work is completed again; afterward it becomes `STALE`/`READY` as appropriate. It does not automatically delete or overwrite old work.

Bump `definition_version` whenever the task-specific prompt, acceptance criteria, or procedure changes in a way that should force the step to run again. Prefer adding the relevant prompt/specification as an `input_path`, so edits invalidate the step automatically.

## Commands

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME
python scripts/taskctl.py start TASK-ID STEP-ID --agent AGENT-NAME --resume
python scripts/taskctl.py checkpoint TASK-ID STEP-ID --note "..." --next-action "..."
python scripts/taskctl.py complete TASK-ID STEP-ID --agent AGENT-NAME
python scripts/taskctl.py invalidate TASK-ID STEP-ID --reason "..." --cascade
python scripts/taskctl.py validate
```

`invalidate --cascade` is for deliberate human decisions or an explicit workflow reset. Most source/template changes are detected from hashes without manual invalidation.

## Concurrency boundary

Use one active writer per task/lesson. The GitHub Issue identifies the owner; the branch and output paths identify the write scope. Parallel reviewers may read the same draft and write distinct review reports. Do not run two authors against the same task or shared paths. The JSON task state is not a distributed lock service: separate clones can race, so resolve ownership in the Issue before starting a writer.

## Limitations

This is a lightweight file-based checkpoint system, not a hosted workflow engine. It does not provide atomic distributed leases, automatic retries, remote job execution, or guaranteed synchronization between two independent clones. GitHub's commit history and PR review remain the audit trail. A future orchestrator can consume this state format without replacing it.