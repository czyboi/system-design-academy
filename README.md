# System Design Academy

Source-grounded System Design course development for middle/senior engineers. Learner-facing material is original, English-language, and draft until explicit human approval.

## Current state

The user approved **SDA-v1** on 2026-11-10: 14 modules, 57 lessons and a cross-module capstone. The official baseline is linked from [curriculum/README.md](curriculum/README.md); the root-level earlier plan is a historical candidate. The [delivery plan](delivery/PLAN.md) and [backlog](delivery/backlog.json) describe future learning packages and dependencies.

## Explicit, lightweight workflow

| Work | Default task steps | Template |
| --- | --- | --- |
| Course plan | Create a new versioned plan, inventory and topic matrix | `.academy/state/course.template.json` |
| Lesson draft | Research → author lesson and assessment | `.academy/state/task.template.json` |
| Tooling change | Implementation | `.academy/state/workflow.template.json` |

Legacy milestone lesson drafts are not imported into this branch; the approved SDA-v1 curriculum, backlog and task history remain intact. The website will parse the exact Markdown/YAML files authored by AI using standard libraries, without any separate content adapter. The agent completes the requested draft and stops. The lesson author uses the [assessment-design skill](.agents/skills/assessment-design/SKILL.md), [source governance](GOVERNANCE.md) and compact [content-format skill](.agents/skills/content-format/SKILL.md) to follow [Authoring Format Contract v1](docs/authoring-format-contract-v1.md) without a new agent step. **AI review and content validation are manual, independent requests.** Python regression tests run automatically in GitHub Actions for pull requests and pushes to `main`. No fingerprint, checksum or automatic stale cascade changes completed task history. The owner can explicitly reopen a step, flag a previously reviewed draft as needing review, or invoke a focused check.

Task specs and history: `.academy/specs/`, `.academy/state/tasks/`, `.academy/state/worklog/`. Agent skills: `.agents/skills/`. Code: `scripts/`, lessons: `modules/`.

## Useful commands

```bash
python scripts/taskctl.py status TASK-ID
python scripts/taskctl.py start TASK-ID author --agent lesson_author
python scripts/taskctl.py complete TASK-ID author --agent lesson_author
python scripts/taskctl.py review-status TASK-ID --scope technical --state needs_review --reason "Revised a technical claim"
# Run after committing and pushing output, task state, spec and worklog:
python scripts/taskctl.py handoff TASK-ID
# Same-checkout handoff only:
python scripts/taskctl.py handoff TASK-ID --local-only
python scripts/taskctl.py invalidate TASK-ID author --reason "User requested a rewrite"
```

For backlog lessons, `init` resolves the correct Lesson ID-based teaching/assessment/evidence output paths from `delivery/backlog.json` and validates task state/spec before writing. Each lesson has exactly one canonical lesson/assessment/evidence path from the backlog; Git records revisions. Repository-wide validators reject obsolete nested lesson revisions, manifests and orphan assessments. `status` warns about missing completed outputs without changing historical status. The manual `handoff` command checks Git tracking, clean state and upstream remote synchronization; `--local-only` is for agents sharing a checkout. It does not check content quality.

Marking a task complete records the work performed; it does not mean the current draft was independently reviewed. A `reviewed` content status does not constitute human publishing approval.

### Validation — run only when requested

```bash
pip install -r requirements-dev.txt
python scripts/validate_content.py --scope lesson --lesson PATH --assessment PATH
# Combined metadata, Markdown and structural validation:
python scripts/validate_content.py --scope repo
python scripts/taskctl.py validate
python -m unittest discover -s tests -v
```

For pinned Primer coverage, invoke `python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage plan` (or `--stage taught`) when desired. These are deterministic **data/safety** checks, not factual or pedagogical reviews. Author checks teaching depth and assessment completeness; independent qualitative review remains on demand. There is not yet a website renderer to test actual browser output.

GitHub Actions: **Content validation → Run workflow** runs content validation manually. **Python regression tests** runs automatically on pull requests and pushes to `main`, and can also be run manually.

See [workflow contract](docs/workflow-contract.md), [task state protocol](.academy/state/README.md), and [module pipeline](.agents/skills/module-pipeline/SKILL.md). Historical reports and accepted curriculum evidence remain in Git for traceability.
