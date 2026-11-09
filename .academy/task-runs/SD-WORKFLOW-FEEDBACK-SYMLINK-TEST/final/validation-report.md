# Feedback Workflow and Symlink Test — Validation Report

**Task:** SD-WORKFLOW-FEEDBACK-SYMLINK-TEST  
**Date:** 2026-11-09  
**Status:** Automation validation only

## Commands and results

| Command | Result | What it establishes |
|---|---|---|
| python -m pip install -r requirements-dev.txt | Passed; required packages were already installed. Pip exited 0 but printed cleanup warnings for temporary directories in the sandbox-managed Windows temp path. | Development dependencies are available. The pip cleanup warnings are separate from the test fixture issue. |
| python scripts/validate_content.py | Passed. Seven lesson files found, 20 source-registry rows, 0 internal Markdown links checked, 10 shared skills, and 6 custom agents. | Content structure and repository configuration pass the current structural checks; this does not establish factual or pedagogical quality. |
| python -m unittest discover -s tests -v | Passed: 13 tests, 0 failures, 0 skips. | The complete unit suite runs with default environment settings. TaskCtl fixtures now live under the repository's ignored .tmp directory. The symlink guard test simulates Path.is_symlink and asserts relpath rejects that path component without creating a real OS symlink. |
| python scripts/taskctl.py validate | Passed. | Task specification/state schema and task graph validation. |

The prior test failure had two distinct causes: sandbox permissions blocked TemporaryDirectory under the default Windows temp location, while WinError 1314 separately blocked creating a real symlink. Moving fixtures under the repository fixes the first. A mocked filesystem boundary makes the guard unit test independent of the second. This suite does not test Windows' real symlink-creation API.

## Durable feedback changes

- AGENTS.md now requires task feedback to be recorded and reusable process lessons to be promoted through scoped shared-skill, QA, or regression-test changes.
- module-pipeline and task-handoff now read relevant prior feedback, record dispositions, and carry unresolved items through handoffs.
- lesson-authoring now requires independent review outputs for substantive revisions and prohibits calling author self-review independent.
- Provider-specific agent profiles were not changed; repository policy keeps shared procedures in .agents/skills.

The full feedback-to-change mapping is in review/feedback-retrospective.md.
