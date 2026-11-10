# Workflow CLI contract

## Review results

A review step declares `review.artifact_paths` (also explicit input_paths) and `review.verdict_path` (one of its owned outputs). It produces an explanatory Markdown report plus JSON:

```json
{
  "verdict": "revise",
  "artifact_hashes": {"modules/example/lesson.md": "actual SHA-256 of the file bytes"},
  "findings": [{"id": "T-1", "severity": "major", "status": "open"}]
}
```

Verdicts: block, revise, ready-for-human-review. Severities: blocker, major, minor, note. Finding status: open or resolved. Every artifact must have its exact current hash; an accepted verdict cannot contain open blocker/major findings. The JSON is structural evidence supplied by the reviewer, not proof of technical truth or reviewer identity.

`requires_reviews` lists direct review dependencies whose verdicts must be clear. Ordinary `depends_on` requires completed, fresh execution only, allowing a revision to consume negative findings. Changing review contracts invalidates their fingerprints. Historical tasks without these additive fields retain their previous semantics; migrate an active legacy graph before relying on enforced review gates.

Steps marked revision_cycle count toward a task-wide maximum of two automated revision starts (resuming an interrupted run does not consume another start). The engine refuses a third start; the parent records an awaiting-human hold. This limit applies to tagged revisions, so intake must classify them accurately. Further user-authorized revision work uses a new scoped task.

## Read-only inspection and execution controls

```text
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py reconcile TASK-ID
python scripts/taskctl.py hold TASK-ID --state paused --reason "User asked to stop"
python scripts/taskctl.py hold TASK-ID --state awaiting-human --reason "Two revisions still leave a blocker"
python scripts/taskctl.py resume-task TASK-ID --reason "User explicitly authorized resumption"
```

Status never writes. Reconcile, hold and resume-task mutate state/worklog and must be committed. Holds block both start (including --resume) and complete. They do not cancel a running external process: the parent must stop its worker as well. The command records a supplied decision; it cannot authenticate human authorization.

## Runtime metadata

Start accepts `--model` and `--reasoning-effort` for observed runtime values. Omit unavailable values. Complete optionally accepts `--usage-file PATH`, a repository-relative JSON object with observed nonnegative counters: input_tokens, output_tokens, cached_input_tokens, reasoning_tokens and elapsed_seconds. The worklog stores the supplied counters and runtime model beside the run ID. Counts may have provider-specific inclusion rules; do not blindly sum reasoning with output tokens or infer subscription cost from API rates. This CLI does not collect runtime usage automatically.

## Content validation

```text
python scripts/validate_content.py
python scripts/validate_content.py --scope workflow
python scripts/validate_content.py --scope curriculum --plan path/to/plan.md --matrix path/to/coverage.csv
python scripts/validate_content.py --scope lesson --lesson path/to/lesson.md --assessment path/to/assessment.md
```

Default repo scope checks current `modules/*/lessons/*.md` packages and explicit `modules/*/content-manifest.json` manifests. A content manifest has draft status and a packages array of lesson/assessment repository-relative paths, including case studies if applicable. An empty authoring repository is valid; a missing explicitly selected/manifested artifact fails. The old pilot-manifest.json is a historical inventory after the user-directed content reset, not a declaration that those files currently exist. Historical runs and immutable input snapshots are excluded from global link checks; selected artifacts are still checked explicitly.

Lesson YAML includes prerequisites, outcome IDs and its assessment path. Companion YAML includes status: draft, lesson path, and outcome_map entries with taught_in (exact lesson heading) and items (EX-1, Q1, etc.). Each of 5–8 Q-numbered checks has Answer: and Explanation:. Structural mapping cannot establish teaching depth or assessment quality.

Curriculum matrices are CSV with topic, locator, disposition, lesson, outline and rationale columns. Mapped/merged rows identify existing lesson/outline text. Optional/deferred/outside-scope rows require a rationale. Independent coverage review establishes completeness against the pinned source.

## Model configuration

Project and default subagent: GPT-6.1 Sol/high. Technical reviewer: GPT-6 Astra/high. Pedagogy: GPT-6.1 Terra/medium. Provenance: Sol/medium. Other named roles: Sol/high. Four concurrent subagents, excluding the parent. Custom profile settings take precedence over spawn defaults; inspect actual runtime metadata when evaluating cost. Claude profiles keep model: inherit because OpenAI model IDs do not configure Claude.

Configuration was checked against [official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [model catalog](https://developers.openai.com/api/docs/models) on 2026-11-10. Availability is host/account-dependent. These are workload-based starting choices, not benchmark results; new sessions may be needed to reload profiles.
