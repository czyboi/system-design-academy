# System Design Academy

An AI-assisted, source-grounded curriculum project for backend engineers learning system design.

> **Project status:** Early development. The Database module is a pilot, not publication-ready courseware.

## Goals

- Build a structured learning path from fundamentals to production-scale system design.
- Treat source provenance, technical accuracy, and teaching quality as explicit quality gates.
- Use AI to research, draft, diagram, and assess lessons while retaining human approval before publication.
- Keep all authored content versioned in Markdown and diagrams-as-code where practical.

## Repository layout

```text
.
├── PROJECT_SPEC.md             # Scope, principles, roles, and acceptance criteria
├── CURRICULUM_MASTER.md        # Academy-wide curriculum map
├── GOVERNANCE.md               # Source, license, QA, and publishing rules
├── GITHUB_SETUP.md             # One-time remote repository setup
├── modules/
│   └── database/               # Database pilot: lessons, case study, QA, sources, workflow
├── docs/                       # Project decisions and operating notes
└── .github/                    # Pull request template
```

## First pilot: Database

Start with [`modules/database/README.md`](modules/database/README.md). It contains 7 lessons, one capstone case study, source registry, author/reviewer prompts, a lesson template, and a first-pass QA report.

## Non-negotiable rules

1. Do not invent citations, technical guarantees, product versions, benchmark numbers, or source licenses.
2. Prefer standards and official technical documentation for version-specific claims.
3. Distinguish general distributed-systems principles from vendor-specific behavior.
4. Do not copy third-party diagrams, code, images, notebooks, or flashcards without verifying their individual rights.
5. Keep AI-created lessons in `draft` until the QA gate and human review pass.
6. Never auto-publish learner-facing content.

## Source attribution

The Database pilot is informed by Donne Martin's [System Design Primer](https://github.com/donnemartin/system-design-primer), whose repository `LICENSE.txt` states CC BY 4.0 for the author's code and resources. This project does not assume that external links or third-party assets inside that repository share the same license. See [`GOVERNANCE.md`](GOVERNANCE.md) and [`modules/database/governance/attribution-policy.md`](modules/database/governance/attribution-policy.md).

## Getting started

1. Read [`PROJECT_SPEC.md`](PROJECT_SPEC.md) and [`GOVERNANCE.md`](GOVERNANCE.md).
2. Inspect the Database pilot before using it as the standard for future modules.
3. Run the bounded Codex/Work tasks in `modules/database/workflow/run-database-pilot.md`.
4. Review the output and QA report; do not mark it approved without a qualified human review.
5. Read `AGENTS.md` before asking a coding agent to modify this repository.
6. Read `docs/agent-architecture.md` for the skills/roles/handoff model. Run `python scripts/validate_content.py`; GitHub Actions checks lesson structure, skills, agent profiles, TOML config, and relative links.

See [`GITHUB_SETUP.md`](GITHUB_SETUP.md) for connecting this local starter to a new private GitHub repository.
