# Workflow Feedback Retrospective

**Task:** SD-WORKFLOW-FEEDBACK-SYMLINK-TEST  
**Date:** 2026-11-09  
**Feedback source:** User follow-up after the DB-01 English revision

## Feedback and disposition

| Feedback | Cause | Disposition and durable change | Verification |
|---|---|---|---|
| The previous DB-01 revision was edited by the parent without a new specialist review, and the user could not see reusable improvements to agent behavior. | The revision report disclosed that no independent post-revision review occurred, but the workflow had no required feedback-retrospective step or promotion rule. A chat correction could remain only in the conversation. | Applied. AGENTS.md now routes feedback to the task worklog/report and reusable changes to shared skills, QA checks, or regression tests. The module-pipeline and task-handoff skills read prior feedback and require disposition/retrospective. The lesson-authoring skill requires independent review outputs for substantive revisions and forbids treating author self-review as independent. Provider profiles were not edited because repository rules keep shared procedures in .agents/skills. | Validate the procedure text and repository content; preserve this retrospective in the task run. |
| The symlink unit test was skipped and the user asked why it could not run in the workspace. | The first test failure came from sandbox restrictions on the default Windows temporary directory. Moving TEMP/TMP into the workspace fixed that. A separate WinError 1314 then showed that this process cannot create an OS symlink; using D: does not grant that privilege. | Applied. The test fixture now uses the repository's ignored .tmp directory. The symlink-path guard is tested by simulating Path.is_symlink at the filesystem boundary and asserting relpath rejects the path, so the unit test no longer needs to create a symlink or skip. | Run the full suite with default environment variables and confirm that the guard test executes with no privilege-dependent skip. |

## Learning carried forward

Chat feedback becomes reusable only after a durable repository change is committed. Task-specific decisions stay with that task's worklog and retrospective; reusable workflow rules live in shared skills and have a regression check when practical. Agent profile files remain role/configuration adapters.

For substantial lesson changes, the parent should assign distinct author and reviewer outputs, then reconcile the independent findings. If those reviews cannot be performed, the task must state the gap and leave the review gate open.
