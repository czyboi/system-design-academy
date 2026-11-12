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

Legacy milestone lesson drafts are not imported into this branch; the approved SDA-v1 curriculum, backlog and task history remain intact. The website will parse the exact Markdown/YAML files authored by AI using standard libraries, without any separate content adapter. The author completes the requested draft; the parent orchestrator then runs a lightweight scoped validation-and-Git handoff, once per completed batch. The lesson author uses the [assessment-design skill](.agents/skills/assessment-design/SKILL.md), [source governance](GOVERNANCE.md) and compact [content-format skill](.agents/skills/content-format/SKILL.md) to follow [Authoring Format Contract v1](docs/authoring-format-contract-v1.md) without a new agent step. **Independent technical and pedagogy review runs automatically once per completed module**, including all lesson/assessment pairs and the integrated design. Open actionable findings are sent back to the original Author for **up to two targeted correction rounds**, each followed by independent re-review. Separate targeted reviews and broader content validation remain on demand. Focused per-draft data/format validation runs automatically before committing/pushing to a feature branch. Python regression tests run automatically in GitHub Actions for pull requests and pushes to `main`. No fingerprint, checksum or automatic stale cascade changes completed task history. The owner can explicitly reopen a step, flag a previously reviewed draft as needing review, or invoke a focused check.

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

For backlog lessons, `init` resolves the correct Lesson ID-based teaching/assessment/evidence output paths from `delivery/backlog.json` and validates task state/spec before writing. Each lesson has exactly one canonical lesson/assessment/evidence path from the backlog; Git records revisions. Repository-wide validators reject obsolete nested lesson revisions, manifests and orphan assessments. `status` warns about missing completed outputs without changing historical status. The parent runs `scripts/draft_handoff.py` after a completed lesson or integration batch; it validates only the generated lesson/assessment pairs and integrated Markdown, selectively commits generated outputs plus task memory, pushes to an existing feature branch (or creates `codex/drafts-*`), and verifies remote handoff. The standalone `taskctl handoff` command remains a read-only Git synchronization check; `--local-only` is for agents sharing a checkout. Neither Git check is a factual or teaching-quality review; at **module closure**, the parent runs the two separate reviewer agents and includes their reports in a subsequent feature-branch handoff.

Marking a task complete records the work performed; it does not mean the current draft was independently reviewed. A `reviewed` content status does not constitute human publishing approval.

### Automatic draft handoff; broader checks on request

```bash
pip install -r requirements-dev.txt
# Parent orchestrator runs after completed draft task(s):
python scripts/draft_handoff.py SD-M00-L01 SD-M00-L02
# At module close, parent reviews with existing Sol High + Terra Medium agent profiles.
# On findings: review_cycle.py record → begin-revision → Author patches → targeted re-review
# (at most two automatic corrections); final report handoff:
python scripts/draft_handoff.py SD-M00-L01 SD-M00-L02 SD-M00-INTEGRATION --review-report modules/m00/reviews/automatic/technical.md --review-report modules/m00/reviews/automatic/pedagogy.md
# Extra checks are on demand:
python scripts/validate_content.py --scope lesson --lesson PATH --assessment PATH
# Combined metadata, Markdown and structural validation:
python scripts/validate_content.py --scope repo
python scripts/taskctl.py validate
python -m unittest discover -s tests -v
```

For pinned Primer coverage, invoke `python scripts/check_course_coverage.py --inventory PATH --matrix PATH --plan PATH --stage plan` (or `--stage taught`) when desired. These are deterministic **data/safety** checks, not factual or pedagogical reviews. If a scoped check or push fails, generated files remain local and the agent reports the blocker instead of starting a blind retry loop; deterministic format fixes may be made only within the affected work. No force-push, PR creation, merge or publication is performed. Author checks teaching depth and assessment completeness. Two independent reviewers audit each completed module automatically and send specific findings back to Author for bounded corrections. Each correction is reviewed again; after two unsuccessful rounds, outstanding problems require human direction. There is not yet a website renderer to test actual browser output.

GitHub Actions: **Content validation → Run workflow** runs content validation manually. **Python regression tests** runs automatically on pull requests and pushes to `main`, and can also be run manually.

A representative [three-lesson quality pilot](docs/quality-pilot.md) is scoped but not yet generated or reviewed; data-check PASS must not be mistaken for quality or real browser rendering.

See [workflow contract](docs/workflow-contract.md), [task state protocol](.academy/state/README.md), [module pipeline](.agents/skills/module-pipeline/SKILL.md), and [automatic module review](.agents/skills/module-quality-review/SKILL.md). Historical reports and accepted curriculum evidence remain in Git for traceability.
