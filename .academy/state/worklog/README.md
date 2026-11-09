# Worklog

Each task gets `.academy/state/worklog/<TASK-ID>.jsonl`. The CLI appends a compact JSON event for creation, step definition, start/resume, checkpoint, completion, and invalidation.

Treat this log as append-only. Do not rewrite or summarize earlier events in place. Correct a mistake with a new event and an explanatory note. The task JSON is the current snapshot; the JSONL file is its event history.

The log is not intended for secrets, full prompts containing sensitive data, private user data, or large model transcripts. Store only a short checkpoint and links/paths to repository artifacts.