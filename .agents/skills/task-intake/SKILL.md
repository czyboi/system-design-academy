---
name: task-intake
description: Create or claim a well-scoped Academy task, carry current user direction into its canonical specification, and prevent duplicate or conflicting work before agents start.
---

# Task Intake

1. Search GitHub Issues and `.academy/state/tasks/` for matching task IDs, lessons, goals, and output paths. Reuse equivalent work.
2. Read the repository task-state README, matching issue/spec/state/worklog, relevant module plan and governance, and prior user/reviewer feedback. Carry forward applicable feedback; do not rely on chat memory alone.
3. Resolve the current target learner, experience level, learner-facing language, teaching-versus-assessment split, module/lesson scope, and source revision. Use current explicit user direction over older project defaults and task prose, then record the decision and its source in the canonical spec/worklog. The Academy's current defaults are middle/senior system-design learners and English-only learner-facing content.
4. Confirm one active writer and a named owner before execution.
5. Initialize with:
   `python scripts/taskctl.py init <TASK-ID> --module <MODULE> --goal "..." --owner "@username" --template .academy/state/task.template.json`.
6. Edit `.academy/specs/<TASK-ID>.json` as the canonical source for goal, scope, constraints, Definition of Done, and acceptance criteria. Give every requirement an ID and `applies_to` list. Remove placeholders before starting.
7. Declare a distinct teaching lesson path and companion assessment path. Define outcome-to-lesson-section-to-assessment-item mapping and include the practical exercise, 5–8 checks, answers, and rubric in the companion assessment. Do not specify question banks inside the teaching lesson.
8. Add both coverage gates to substantive module work: an independent plan-stage source-topic audit before authoring and a separate post-authoring audit of actual lesson teaching. Declare separate report paths. The curriculum designer and author cannot self-approve these gates.
9. Adjust task-state steps to exact inputs, outputs, definition versions, and dependencies. Input paths must not also be outputs in the same step; each output has one owner. Include the required independent technical, pedagogical, provenance/language, and coverage reviews as applicable.
10. Put links, owner, branch, dependencies, and a short summary in the GitHub Issue. Do not duplicate detailed scope or acceptance criteria there.
11. Commit the specification, task state, worklog, and immutable inputs before execution. Run `python scripts/taskctl.py status <TASK-ID>`; resolve stale/resume/blocked steps before assigning work.

Never invent completion records or mark a step complete from chat narrative. Use `taskctl complete` only after declared outputs are verifiably committed.
