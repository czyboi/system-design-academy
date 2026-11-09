# System Design Academy

An AI-assisted, source-grounded curriculum project for backend engineers learning system design.

> **Project status:** Early development. The Database module is a pilot, not publication-ready courseware.

## Goals

- Build a structured learning path from fundamentals to production-scale system design.
- Treat source provenance, technical accuracy, and teaching quality as explicit quality gates.
- Use AI to research, draft, diagram, and assess lessons while retaining human approval before publication.
- Preserve task progress across AI models/providers and prevent completed work from being repeated.
- Keep all authored content versioned in Markdown and diagrams-as-code where practical.

## Repository layout

```text
.
├── PROJECT_SPEC.md             # Scope, principles, roles, and acceptance criteria
├── CURRICULUM_MASTER.md        # Academy-wide curriculum map
├── GOVERNANCE.md               # Source, license, QA, and publishing rules
├── AGENTS.md                   # Repository-wide agent guardrails
├── .agents/skills/             # Reusable specialist workflows, including intake/handoff
├── .codex/agents/              # Custom Codex subagent role profiles
├── .codex/config.toml          # Multi-agent concurrency settings
├── .academy/state/             # Durable task JSON, schema, template, and worklog
├── scripts/
│   ├── taskctl.py              # Fingerprints, checkpoints, skip/resume, output hash checks
│   └── validate_content.py     # Structural course-content validation
├── tests/                      # Dependency-free task-state integration tests
├── modules/
│   └── database/               # Database pilot: lessons, case study, QA, sources, workflow
├── docs/                       # Project decisions and operating notes
└── .github/                    # Issue/PR templates and validation workflow
```

## Persistent task state (important)

For any multi-step task, create or reuse a GitHub Issue and a state file under `.academy/state/tasks/`. Run:

```bash
python scripts/taskctl.py status TASK-ID
```

The tool calculates whether each step is `SKIP`, `RESUME`, `READY`, `STALE`, or `BLOCKED`. A step is reusable only when its current input fingerprint and committed output hashes match its completion record. Checkpoints and event history live in `.academy/state/worklog/`. This lets a different AI/provider resume from repository state rather than replaying old chat work.

Start with `.academy/state/README.md` and `docs/task-state-and-idempotency.md`. Use the `task-intake` and `task-handoff` skills before handing tasks between agents.

## First pilot: Database

Start with [`modules/database/README.md`](modules/database/README.md). It contains 7 lessons, one capstone case study, source registry, author/reviewer prompts, a lesson template, and a first-pass QA report.

## Non-negotiable rules

1. Do not invent citations, technical guarantees, product versions, benchmark numbers, or source licenses.
2. Prefer standards and official technical documentation for version-specific claims.
3. Distinguish general distributed-systems principles from vendor-specific behavior.
4. Do not copy third-party diagrams, code, images, notebooks, or flashcards without verifying their individual rights.
5. Keep AI-created lessons in `draft` until the QA gate and human review pass.
6. Never auto-publish learner-facing content.
7. A custom agent's role instructions do not enforce permissions; subagents inherit the parent session's permission mode.

## Source attribution

The Database pilot is informed by Donne Martin's [System Design Primer](https://github.com/donnemartin/system-design-primer), whose repository `LICENSE.txt` states CC BY 4.0 for the author's code and resources. This project does not assume that external links or third-party assets inside that repository share the same license. See [`GOVERNANCE.md`](GOVERNANCE.md) and [`modules/database/governance/attribution-policy.md`](modules/database/governance/attribution-policy.md).

## Getting started

1. Read [`PROJECT_SPEC.md`](PROJECT_SPEC.md) and [`GOVERNANCE.md`](GOVERNANCE.md).
2. Inspect the Database pilot before using it as the standard for future modules.
3. For a new task, create or reuse a GitHub Issue and initialize state with `python scripts/taskctl.py init TASK-ID --module MODULE --goal "..." --template .academy/state/task.template.json`.
4. Adapt the generated task JSON to the exact module, files, inputs, outputs, and acceptance criteria; commit it before delegation.
5. Run `python scripts/taskctl.py status TASK-ID` before work and follow the status it reports. Never repeat `SKIP` steps.
6. Read `docs/agent-architecture.md` for the role map and `modules/database/workflow/agent-runbook.md` for the Database workflow.
7. Run `python scripts/validate_content.py`, `python -m unittest discover -s tests -v`, and `python scripts/taskctl.py validate` before creating/updating a draft PR.

See `GITHUB_SETUP.md` for repository setup and connection details.