#!/usr/bin/env python3
"""Explicit task lifecycle and handoff; no checksum-driven status changes."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from string import Template
from jsonschema import Draft202012Validator, FormatChecker
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".academy" / "state"
TASK_DIR = STATE_DIR / "tasks"
SPEC_DIR = ROOT / ".academy" / "specs"
TASK_SCHEMA = STATE_DIR / "schema" / "task.schema.json"
SPEC_SCHEMA = STATE_DIR / "schema" / "spec.schema.json"
LOG_DIR = STATE_DIR / "worklog"
TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class TaskError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")



def relpath(value: str) -> Path:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise TaskError(f"Invalid repository-relative path: {value!r}")
    windows = PureWindowsPath(value)
    normalized = value.replace("\\", "/")
    posix = PurePosixPath(normalized)
    if posix.is_absolute() or windows.is_absolute() or windows.drive or ".." in posix.parts or ".." in windows.parts:
        raise TaskError(f"Unsafe repository-relative path: {value!r}")
    if not posix.parts:
        raise TaskError(f"Invalid repository-relative path: {value!r}")
    cursor = ROOT
    for part in posix.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise TaskError(f"Symlink path components are not allowed: {value!r}")
    try:
        cursor.resolve(strict=False).relative_to(ROOT.resolve())
    except ValueError as exc:
        raise TaskError(f"Path escapes repository: {value!r}") from exc
    return cursor


def spec_path_for(task_id: str) -> Path:
    if not TASK_ID_RE.fullmatch(task_id):
        raise TaskError(f"Invalid task ID: {task_id!r}")
    return relpath(f".academy/specs/{task_id}.json")

def task_path(task_id: str) -> Path:
    if not TASK_ID_RE.fullmatch(task_id):
        raise TaskError("Task ID must be 1–64 letters, digits, dots, underscores, or hyphens; it must start with a letter or digit.")
    return TASK_DIR / f"{task_id}.json"


def lesson_paths_from_backlog(task_id: str, module_id: str) -> dict[str, str]:
    """Resolve lesson files from the canonical Story, never from the task ID."""
    path = ROOT / "delivery" / "backlog.json"
    try:
        backlog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TaskError(f"Cannot read lesson backlog: {exc}") from exc
    stories = [
        item for item in backlog.get("items", [])
        if item.get("type") == "Story"
        and item.get("package_kind") == "lesson"
        and item.get("proposed_task_id") == task_id
    ]
    if len(stories) != 1:
        raise TaskError(f"Expected one lesson Story with proposed_task_id={task_id}; found {len(stories)}")
    story = stories[0]
    lesson_id = story.get("lesson_id")
    if not isinstance(lesson_id, str) or not lesson_id.startswith(module_id.upper() + "-"):
        raise TaskError(f"Lesson {task_id} does not match declared module {module_id}")
    outputs = story.get("outputs", {})
    keys = {"TEACHING_PATH": "teaching", "ASSESSMENT_PATH": "assessment", "EVIDENCE_PATH": "evidence"}
    values = {"LESSON_ID": lesson_id}
    for variable, key in keys.items():
        value = outputs.get(key)
        if not isinstance(value, str) or not value:
            raise TaskError(f"Backlog Story {story['key']} has no {key} output")
        relpath(value)
        values[variable] = value
    if values["TEACHING_PATH"] == values["ASSESSMENT_PATH"]:
        raise TaskError("Lesson and assessment must have different output paths")
    return values


def load_task(task_id: str) -> dict[str, Any]:
    path = task_path(task_id)
    if not path.exists():
        raise TaskError(f"Task not found: {path.relative_to(ROOT)}. Create it with `taskctl.py init`. ")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaskError(f"Cannot read task state {path}: {exc}") from exc
    validate_task(data)
    return data


def save_task(data: dict[str, Any]) -> None:
    path = task_path(data["task_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def log_event(task_id: str, event: str, **fields: Any) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    record = {"at": now(), "task_id": task_id, "event": event, **fields}
    line = (json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    log_path = LOG_DIR / f"{task_id}.jsonl"
    # One append write per event. The log is append-only by convention; do not edit history.
    fd = os.open(log_path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)
    try:
        os.write(fd, line)
    finally:
        os.close(fd)



def validate_json_schema(data: dict[str, Any], schema_path: Path, label: str) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaskError(f"Cannot load {label} schema {schema_path}: {exc}") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data),
        key=lambda error: list(error.path),
    )
    if errors:
        error = errors[0]
        where = ".".join(str(part) for part in error.absolute_path) or "$"
        raise TaskError(f"{label} violates {schema_path.relative_to(ROOT)} at {where}: {error.message}")


def load_spec(
    data: dict[str, Any], execution_ready: bool = False,
    spec_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if spec_override is None:
        path = relpath(data["spec_path"])
        try:
            spec = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TaskError(f"Cannot read task specification {path}: {exc}") from exc
    else:
        spec = spec_override
    validate_json_schema(spec, SPEC_SCHEMA, "Task specification")
    if spec["task_id"] != data["task_id"]:
        raise TaskError("Task specification task_id does not match task state")
    step_ids = {step["step_id"] for step in data["steps"]}
    for field in ("definition_of_done", "acceptance_criteria"):
        seen: set[str] = set()
        for item in spec[field]:
            if item["id"] in seen:
                raise TaskError(f"Duplicate {field} ID: {item['id']}")
            seen.add(item["id"])
            unknown = set(item["applies_to"]) - step_ids - {"*"}
            if unknown:
                raise TaskError(f"{field} item {item['id']} references unknown steps: {', '.join(sorted(unknown))}")
            if execution_ready and re.search(r"\b(TODO|TBD|replace this|fill this)\b", item["text"], re.I):
                raise TaskError(f"Specification item {item['id']} is still a placeholder")
    if execution_ready:
        searchable = [spec["goal"], *spec["scope"]["in_scope"], *spec["scope"]["out_of_scope"], *spec["constraints"]]
        if any(re.search(r"\b(TODO|TBD|replace this|fill this)\b", value, re.I) for value in searchable):
            raise TaskError("Task goal, scope, and constraints must not contain TODO/TBD placeholders")
        if not spec["goal"].strip() or not spec["scope"]["in_scope"]:
            raise TaskError("Specification must define a goal and at least one in-scope item")
        if not spec["definition_of_done"] or not spec["acceptance_criteria"]:
            raise TaskError("Specification must define Definition of Done and acceptance criteria")
        for step in data["steps"]:
            sid = step["step_id"]
            for field in ("definition_of_done", "acceptance_criteria"):
                if not any("*" in item["applies_to"] or sid in item["applies_to"] for item in spec[field]):
                    raise TaskError(f"Step {sid} has no applicable {field} item")
    return spec


def validate_task(data: dict[str, Any], *, spec_override: dict[str, Any] | None = None) -> None:
    validate_json_schema(data, TASK_SCHEMA, "Task state")
    if not TASK_ID_RE.fullmatch(data["task_id"]):
        raise TaskError("Invalid task_id")
    if data["spec_path"] != f".academy/specs/{data['task_id']}.json":
        raise TaskError("spec_path must be .academy/specs/<TASK-ID>.json")
    if not data["owner"].strip():
        raise TaskError("Task owner must be set before execution")
    ids = {step["step_id"] for step in data["steps"]}
    if len(ids) != len(data["steps"]):
        raise TaskError("Duplicate step IDs")
    output_owners: dict[str, str] = {}
    by_id = {step["step_id"]: step for step in data["steps"]}
    for step in data["steps"]:
        sid = step["step_id"]
        if set(step["input_paths"]) & set(step["output_paths"]):
            raise TaskError(f"Step {sid} cannot own an input as an output")
        for gate in step.get("requires_reviews", []):
            if gate not in step["depends_on"] or not by_id.get(gate, {}).get("review"):
                raise TaskError(f"Step {sid} requires a direct review dependency: {gate}")
        review = step.get("review")
        if review:
            if review["verdict_path"] not in step["output_paths"]:
                raise TaskError(f"Review {sid} must own its verdict output")
            if not set(review["artifact_paths"]).issubset(step["input_paths"]):
                raise TaskError(f"Review {sid} must declare reviewed artifacts as inputs")
        for value in step["input_paths"] + step["output_paths"]:
            relpath(value)
        if not step["output_paths"]:
            raise TaskError(f"Step {sid} must declare at least one output path")
        for path in step["output_paths"]:
            if path in output_owners:
                raise TaskError(f"Output path {path!r} is owned by both {output_owners[path]} and {sid}")
            output_owners[path] = sid
        unknown = set(step["depends_on"]) - ids
        if unknown:
            raise TaskError(f"Step {sid} has unknown dependencies: {', '.join(sorted(unknown))}")
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(sid: str) -> None:
        if sid in visiting:
            raise TaskError(f"Dependency cycle detected at step {sid}")
        if sid in visited:
            return
        visiting.add(sid)
        for dep in by_id[sid]["depends_on"]:
            visit(dep)
        visiting.remove(sid)
        visited.add(sid)
    for sid in by_id:
        visit(sid)
    load_spec(data, spec_override=spec_override)

def step_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {step["step_id"]: step for step in data["steps"]}


def review_result(step: dict[str, Any]) -> dict[str, Any]:
    contract = step["review"]
    try:
        result = json.loads(relpath(contract["verdict_path"]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TaskError(f"Missing or invalid review verdict for {step['step_id']}: {exc}") from exc
    if not isinstance(result, dict) or result.get("verdict") not in {"block", "revise", "ready-for-human-review"}:
        raise TaskError("Review verdict must be block, revise, or ready-for-human-review")
    findings = result.get("findings")
    if not isinstance(findings, list):
        raise TaskError("Review findings must be a list (empty when none)")
    for finding in findings:
        if (not isinstance(finding, dict) or not isinstance(finding.get("id"), str)
                or not finding["id"].strip() or finding.get("severity") not in {"blocker", "major", "minor", "note"}
                or finding.get("status") not in {"open", "resolved"}):
            raise TaskError("Each finding needs id, severity and open/resolved status")
    if len({f["id"] for f in findings}) != len(findings):
        raise TaskError("Review finding IDs must be unique")
    if result["verdict"] == "ready-for-human-review" and any(
            f["status"] == "open" and f["severity"] in {"blocker", "major"} for f in findings):
        raise TaskError("A clear review cannot contain unresolved material findings")
    return result


def require_active(data: dict[str, Any]) -> None:
    if data.get("execution_control", "active") != "active":
        raise TaskError(f"Task is {data['execution_control']}; explicit resume-task with a user decision is required")


def review_gate_blocker(data: dict[str, Any], step: dict[str, Any]) -> str | None:
    """Check optional named review gates independently of a running step state."""
    states = step_map(data)
    gates = step.get("requires_reviews", [])
    if gates and data.get("review_status") in {"in_review", "needs_review"}:
        return f"overall review status is {data['review_status']}"
    for gate in gates:
        review_step = states[gate]
        if review_step["status"] != "completed":
            return f"review {gate} has not completed"
        # Pre-existing v2 tasks without explicit review fields keep their historical acceptance.
        legacy = "review_status" not in data and "review_statuses" not in data
        if not legacy:
            decision = data.get("review_statuses", {}).get(gate, {})
            if decision.get("status") != "reviewed":
                return f"review {gate} needs an explicit reviewed decision"
        try:
            verdict = review_result(review_step)["verdict"]
        except TaskError as exc:
            return str(exc)
        if verdict != "ready-for-human-review":
            return f"review {gate} verdict is {verdict}"
    return None


def step_status(data: dict[str, Any], step: dict[str, Any]) -> tuple[str, str]:
    """A completed step stays completed until someone explicitly reopens it."""
    status = step["status"]
    if status == "completed":
        return "SKIP", "explicitly completed; file edits never invalidate history"
    if data.get("execution_control", "active") != "active":
        return "BLOCKED", f"task is {data['execution_control']}"
    if status == "running":
        return "RESUME", "running; inspect checkpoint before resuming"
    if status == "blocked":
        return "BLOCKED", "manually blocked; reopen explicitly"
    states = step_map(data)
    for dep_id in step["depends_on"]:
        if states[dep_id]["status"] != "completed":
            return "BLOCKED", f"dependency {dep_id} is {states[dep_id]['status']}"
    blocker = review_gate_blocker(data, step)
    if blocker:
        return "BLOCKED", blocker
    if status == "invalidated":
        return "READY", step.get("invalidation_reason", "explicitly reopened")
    return "READY", "not started"


def refresh_task_status(data: dict[str, Any]) -> None:
    """Aggregate explicit step states; never inspect file contents."""
    if data.get("execution_control", "active") != "active":
        data["automation_status"] = "blocked"
    elif data["steps"] and all(s["status"] == "completed" for s in data["steps"]):
        data["automation_status"] = "automation_complete"
    elif any(s["status"] in {"running", "completed", "invalidated"} for s in data["steps"]):
        data["automation_status"] = "in_progress"
    elif any(step_status(data, s)[0] == "READY" for s in data["steps"]):
        data["automation_status"] = "not_started"
    elif any(s["status"] == "blocked" for s in data["steps"]):
        data["automation_status"] = "blocked"
    else:
        data["automation_status"] = "not_started"


def render_template(path: Path, values: dict[str, str]) -> dict[str, Any]:
    # Parse JSON first, then render string values recursively. Never mutate raw JSON text.
    data = json.loads(path.read_text(encoding="utf-8"))
    def render(value: Any) -> Any:
        if isinstance(value, str):
            return Template(value).safe_substitute(values)
        if isinstance(value, list):
            return [render(item) for item in value]
        if isinstance(value, dict):
            return {key: render(item) for key, item in value.items()}
        return value
    return render(data)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> None:
    state_path = task_path(args.task_id)
    spec_path = spec_path_for(args.task_id)
    if state_path.exists() or spec_path.exists():
        raise TaskError(f"Task or task specification already exists for {args.task_id}")
    values = {"TASK_ID": args.task_id, "MODULE_ID": args.module, "GOAL": args.goal, "OWNER": args.owner}
    if args.template and relpath(args.template) == relpath(".academy/state/task.template.json"):
        values.update(lesson_paths_from_backlog(args.task_id, args.module))
    spec = render_template(relpath(args.spec_template), values)
    spec.update({"schema_version": 1, "task_id": args.task_id, "revision": 1, "goal": args.goal})
    if args.template:
        data = render_template(relpath(args.template), values)
    else:
        data = {"steps": [], "notes": "", "current_phase": None}
    data.update({
        "schema_version": 2,
        "task_id": args.task_id,
        "module_id": args.module,
        "owner": args.owner,
        "spec_path": f".academy/specs/{args.task_id}.json",
        "automation_status": "not_started",
        "review_status": "not_reviewed",
        "created_at": now(),
        "updated_at": now(),
    })
    data.pop("goal", None)
    data.pop("status", None)
    for step in data.get("steps", []):
        for field in ("input_paths", "output_paths"):
            if any("${" in path for path in step[field]):
                raise TaskError(f"Unresolved template output or input path in {step['step_id']}")
    # Validate both artifacts before writing. A malformed task must not strand its spec.
    validate_task(data, spec_override=spec)
    try:
        save_json(spec_path, spec)
        save_task(data)
    except Exception:
        state_path.unlink(missing_ok=True)
        spec_path.unlink(missing_ok=True)
        raise
    log_event(args.task_id, "task_created", module_id=args.module, owner=args.owner, spec_path=data["spec_path"])
    print(f"Created {state_path.relative_to(ROOT)} and {spec_path.relative_to(ROOT)}. Complete the specification before execution.")

def cmd_add_step(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    if args.step_id in step_map(data):
        raise TaskError(f"Step already exists: {args.step_id}")
    new_step = {
        "step_id": args.step_id,
        "title": args.title,
        "status": "pending",
        "depends_on": args.depends_on,
        "definition_version": args.definition_version,
        "input_paths": args.input_paths,
        "output_paths": args.output_paths,
        "checkpoint": {"note": "", "next_action": ""},
        "attempts": 0,
    }
    data["steps"].append(new_step)
    validate_task(data)
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "step_defined", step_id=args.step_id, depends_on=args.depends_on, inputs=args.input_paths, outputs=args.output_paths)
    print(f"Added step {args.task_id}/{args.step_id}")



def cmd_status(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    refresh_task_status(data)
    spec = load_spec(data)
    print(f"{data['task_id']} | {data['module_id']} | automation={data['automation_status']} | review={data.get('review_status', 'not_reviewed')} | owner={data['owner']}")
    for scope, record in sorted(data.get("review_statuses", {}).items()):
        print(f"  review[{scope}]: {record['status']} — {record['reason']}")
    print(f"Specification: {data['spec_path']} — {spec['goal']}")
    for step in data["steps"]:
        state, reason = step_status(data, step)
        print(f"- {step['step_id']}: {state} — {reason}")
        if step.get("checkpoint", {}).get("next_action"):
            print(f"  next: {step['checkpoint']['next_action']}")
        if step["status"] == "completed":
            missing = [path for path in step["output_paths"] if not relpath(path).is_file()]
            if missing:
                print(f"  WARNING: Missing output(s) despite completed history: {', '.join(missing)}")
    if not data["steps"]:
        print("No steps are defined yet.")
    print("Human review, approval, and publication are separate human-controlled transitions.")


def cmd_reconcile(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    previous = data.get("automation_status")
    refresh_task_status(data)
    if previous != data["automation_status"]:
        data["updated_at"] = now()
        save_task(data)
        log_event(args.task_id, "automation_status_reconciled", previous=previous, current=data["automation_status"])
    print(f"Reconciled: {data['automation_status']}")


def cmd_control(args: argparse.Namespace) -> None:
    if not args.reason.strip():
        raise TaskError("A user decision or blocking reason is required")
    data = load_task(args.task_id)
    data["execution_control"] = "active" if args.command == "resume-task" else args.state
    data["control_reason"] = args.reason
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "task_control_changed", control=data["execution_control"], reason=args.reason)
    print(f"Task control: {data['execution_control']}")


def cmd_start(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    require_active(data)
    step = step_map(data).get(args.step_id)
    if step is None:
        raise TaskError(f"Unknown step: {args.step_id}")
    status, reason = step_status(data, step)
    if status == "SKIP":
        print(f"SKIP {args.step_id}: {reason}. Reopen explicitly with invalidate.")
        return
    if status == "RESUME" and not args.resume:
        raise TaskError(f"Step already running; inspect checkpoint and pass --resume. {reason}")
    if args.resume and status != "RESUME":
        raise TaskError("--resume requires a running step")
    if status not in {"READY", "RESUME"}:
        raise TaskError(f"Cannot start {args.step_id}: {status} — {reason}")
    load_spec(data, execution_ready=True)
    for value in step["input_paths"]:
        if not relpath(value).is_file():
            raise TaskError(f"Required input file is missing: {value}")
    if args.resume:
        step["resume_count"] = step.get("resume_count", 0) + 1
    else:
        if step.get("revision_cycle") and sum(
            s.get("attempts", 0) for s in data["steps"] if s.get("revision_cycle")
        ) >= 2:
            raise TaskError("Two automated revision runs have been used; hold awaiting-human before further work")
        step["attempts"] = step.get("attempts", 0) + 1
        step["started_at"] = now()
    step["status"] = "running"
    step["run_id"] = args.run_id or (step.get("run_id") if args.resume else None) or (
        f"{args.task_id}-{args.step_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    )
    step["agent"] = args.agent
    previous = step.get("runtime", {}) if args.resume else {}
    step["runtime"] = {"model": args.model or previous.get("model"),
                       "reasoning_effort": args.reasoning_effort or previous.get("reasoning_effort")}
    data["current_phase"] = args.step_id
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "step_resumed" if args.resume else "step_started",
              step_id=args.step_id, agent=args.agent, run_id=step["run_id"], runtime=step["runtime"])
    print(f"{'Resumed' if args.resume else 'Started'} {args.task_id}/{args.step_id}")


def cmd_checkpoint(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    step = step_map(data).get(args.step_id)
    if step is None:
        raise TaskError(f"Unknown step: {args.step_id}")
    if step["status"] != "running":
        raise TaskError(f"Cannot checkpoint {args.step_id}: status is {step['status']}, not running")
    step["checkpoint"] = {"note": args.note, "next_action": args.next_action, "at": now()}
    data["updated_at"] = now()
    save_task(data)
    log_event(args.task_id, "checkpoint", step_id=args.step_id, run_id=step.get("run_id"), note=args.note, next_action=args.next_action)
    print(f"Checkpoint saved for {args.task_id}/{args.step_id}")



def cmd_complete(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    require_active(data)
    step = step_map(data).get(args.step_id)
    if step is None:
        raise TaskError(f"Unknown step: {args.step_id}")
    if step["status"] != "running":
        raise TaskError(f"Cannot complete {args.step_id}: status is {step['status']}, not running")
    for dependency in step["depends_on"]:
        if step_map(data)[dependency]["status"] != "completed":
            raise TaskError(f"Cannot complete {args.step_id}: dependency {dependency} is not completed")
    blocker = review_gate_blocker(data, step)
    if blocker:
        raise TaskError(f"Cannot complete {args.step_id}: {blocker}")
    missing = [value for value in step["output_paths"] if not relpath(value).is_file()]
    if missing:
        raise TaskError("Missing declared outputs: " + ", ".join(missing))
    if step.get("review"):
        review_result(step)
    usage = None
    if args.usage_file:
        try:
            usage = json.loads(relpath(args.usage_file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise TaskError(f"Invalid usage file: {exc}") from exc
        allowed = {"input_tokens", "output_tokens", "cached_input_tokens", "reasoning_tokens", "elapsed_seconds"}
        if not isinstance(usage, dict) or not usage or set(usage) - allowed or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v < float("inf")
            for v in usage.values()
        ):
            raise TaskError("Usage must contain nonnegative finite runtime counters only")
    step["status"] = "completed"
    step["completed_at"] = now()
    step["completed_by"] = args.agent or step.get("agent", "unknown")
    # Historical run metadata is left untouched and is never used for state transitions.
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "step_completed", step_id=args.step_id, run_id=step.get("run_id"),
              runtime=step.get("runtime"), usage=usage)
    print(f"Completed {args.task_id}/{args.step_id}; automation={data['automation_status']}.")
    if data["automation_status"] == "automation_complete":
        print("Draft work complete. Review, validation, approval and publication are manual actions.")


def cmd_invalidate(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    states = step_map(data)
    if args.step_id not in states:
        raise TaskError(f"Unknown step: {args.step_id}")
    target_ids = {args.step_id}
    if args.cascade:
        changed = True
        while changed:
            changed = False
            for step in data["steps"]:
                if step["step_id"] not in target_ids and any(dep in target_ids for dep in step["depends_on"]):
                    target_ids.add(step["step_id"])
                    changed = True
    for sid in target_ids:
        step = states[sid]
        step["status"] = "invalidated"
        step["invalidation_reason"] = args.reason
        if sid in data.get("review_statuses", {}):
            data["review_statuses"][sid] = {
                "status": "needs_review", "reason": args.reason, "updated_at": now()
            }
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "steps_invalidated", step_ids=sorted(target_ids), reason=args.reason)
    print("Invalidated: " + ", ".join(sorted(target_ids)))


def cmd_review_status(args: argparse.Namespace) -> None:
    """Explicitly record the review dimension or named review-step decision."""
    if not args.reason.strip():
        raise TaskError("A reason is required")
    if not TASK_ID_RE.fullmatch(args.scope):
        raise TaskError("Review scope must be a nonempty identifier")
    data = load_task(args.task_id)
    review_step = step_map(data).get(args.scope)
    if review_step and not review_step.get("review"):
        raise TaskError(f"Scope {args.scope} is a task step, not a review step")
    if args.state == "reviewed" and review_step:
        if review_step["status"] != "completed":
            raise TaskError(f"Review step {args.scope} must be completed before acceptance")
        if review_result(review_step)["verdict"] != "ready-for-human-review":
            raise TaskError(f"Review step {args.scope} does not have an accepted verdict")
    previous = data.get("review_statuses", {}).get(args.scope, {}).get("status", "not_reviewed")
    data.setdefault("review_statuses", {})[args.scope] = {
        "status": args.state, "reason": args.reason, "updated_at": now()
    }
    if args.scope == "general":
        data["review_status"] = args.state
        data["review_reason"] = args.reason
    data["updated_at"] = now()
    save_task(data)
    log_event(args.task_id, "review_status_changed", scope=args.scope,
              previous=previous, current=args.state, reason=args.reason)
    print(f"Review [{args.scope}]: {previous} -> {args.state} (not publication approval)")


def verify_remote_handoff() -> str:
    """Confirm HEAD equals the configured upstream branch on the actual remote."""
    def git(*arguments: str) -> str:
        try:
            result = subprocess.run(
                ["git", *arguments], cwd=ROOT, capture_output=True, text=True, timeout=20
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise TaskError("Remote handoff verification could not complete") from exc
        if result.returncode:
            raise TaskError(
                "Remote handoff requires an accessible upstream branch; "
                "configure it with 'git push -u origin HEAD' or use --local-only "
                "for a handoff within the same checkout"
            )
        return result.stdout.strip()

    branch = git("symbolic-ref", "--quiet", "--short", "HEAD")
    remote = git("config", "--get", f"branch.{branch}.remote")
    remote_ref = git("config", "--get", f"branch.{branch}.merge")
    if remote == "." or not remote_ref.startswith("refs/heads/"):
        raise TaskError("Remote handoff requires an upstream remote branch (not a local branch)")
    local_head = git("rev-parse", "HEAD")
    advertised = git("ls-remote", "--heads", remote, remote_ref)
    remote_head = next(
        (parts[0] for line in advertised.splitlines()
         if len(parts := line.split("\t", 1)) == 2 and parts[1] == remote_ref),
        None,
    )
    if not remote_head:
        raise TaskError(f"Upstream {remote}/{remote_ref.removeprefix('refs/heads/')} is missing on remote")
    if local_head != remote_head:
        raise TaskError(
            f"Local HEAD is not pushed/synced to {remote}/{remote_ref.removeprefix('refs/heads/')}; "
            "push the branch before cross-environment handoff"
        )
    return f"{remote}/{remote_ref.removeprefix('refs/heads/')}"


def cmd_handoff(args: argparse.Namespace) -> None:
    """Manual durability check: completed outputs and memory must be committed together."""
    data = load_task(args.task_id)
    paths = [data["spec_path"], f".academy/state/tasks/{args.task_id}.json",
             f".academy/state/worklog/{args.task_id}.jsonl"]
    for step in data["steps"]:
        if step["status"] == "completed":
            paths.extend(step["output_paths"])
    problems = []
    for value in sorted(set(paths)):
        if not relpath(value).is_file():
            problems.append(f"Missing: {value}")
            continue
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", value],
            cwd=ROOT, capture_output=True, text=True
        )
        if tracked.returncode:
            problems.append(f"Not Git-tracked: {value}")
            continue
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", value],
            cwd=ROOT, capture_output=True, text=True
        )
        if dirty.returncode:
            problems.append(f"Git status failed: {value}: {dirty.stderr.strip()}")
        elif dirty.stdout.strip():
            problems.append(f"Uncommitted: {value}")
    if problems:
        raise TaskError("Handoff not ready. Commit output, spec, state and worklog:\n- " + "\n- ".join(problems))
    remote_note = "local checkout only" if args.local_only else verify_remote_handoff()
    print(f"HANDOFF READY: {args.task_id}; {len(set(paths))} committed files checked; "
          f"destination={remote_note} (no checksums)")


def cmd_validate(args: argparse.Namespace) -> None:
    """Manually validate task schemas; never called from status/start/complete."""
    errors = []
    for path in sorted(TASK_DIR.glob("*.json")) if TASK_DIR.exists() else []:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            validate_task(data)
            if path.stem != data["task_id"]:
                raise TaskError(f"filename must match task_id ({data['task_id']})")
        except (OSError, json.JSONDecodeError, TaskError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    if errors:
        print("Task state validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Task state validation passed.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Explicit task progress and handoff tracker")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init", help="Create a task state file")
    p.add_argument("task_id")
    p.add_argument("--module", required=True)
    p.add_argument("--goal", required=True)
    p.add_argument("--owner", required=True, help="Responsible GitHub username/team; required for single-writer coordination")
    p.add_argument("--template", help="Repository-relative JSON task-state template")
    p.add_argument("--spec-template", default=".academy/state/spec.template.json", help="Repository-relative task specification template")
    p.set_defaults(func=cmd_init)
    p = sub.add_parser("add-step", help="Add a step and declare its inputs, outputs, and dependencies")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--title", required=True)
    p.add_argument("--definition-version", required=True, help="Bump when the step procedure/prompt changes")
    p.add_argument("--input-paths", nargs="+", required=True)
    p.add_argument("--output-paths", nargs="+", required=True)
    p.add_argument("--depends-on", nargs="*", default=[])
    p.set_defaults(func=cmd_add_step)
    p = sub.add_parser("status", help="Read explicit task and content-review states")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("reconcile", help="Persist aggregate of explicit step states")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_reconcile)
    for command in ("hold", "resume-task"):
        p = sub.add_parser(command, help="Record a task hold or explicit user resumption")
        p.add_argument("task_id")
        p.add_argument("--reason", required=True)
        if command == "hold":
            p.add_argument("--state", choices=["paused", "awaiting-human"], default="paused")
        p.set_defaults(func=cmd_control)
    p = sub.add_parser("start", help="Claim a ready step or resume an interrupted one")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--agent", required=True)
    p.add_argument("--run-id")
    p.add_argument("--model", help="Observed runtime model, if available; do not guess")
    p.add_argument("--reasoning-effort", help="Observed runtime reasoning effort, if available")
    p.add_argument("--resume", action="store_true")
    p.set_defaults(func=cmd_start)
    p = sub.add_parser("checkpoint", help="Persist a handoff checkpoint")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--note", required=True)
    p.add_argument("--next-action", required=True)
    p.set_defaults(func=cmd_checkpoint)
    p = sub.add_parser("complete", help="Mark work complete once declared output files exist")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--agent")
    p.add_argument("--usage-file", help="Repository-relative JSON containing observed runtime usage counters")
    p.set_defaults(func=cmd_complete)
    p = sub.add_parser("invalidate", help="Invalidate a step when a human decision requires it")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--reason", required=True)
    p.add_argument("--cascade", action="store_true")
    p.set_defaults(func=cmd_invalidate)
    p = sub.add_parser("review-status", help="Explicitly update one review scope")
    p.add_argument("task_id")
    p.add_argument("--scope", default="general", help="e.g. technical, pedagogy, or named review step ID")
    p.add_argument("--state", choices=["not_reviewed", "in_review", "reviewed", "needs_review"], required=True)
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_review_status)
    p = sub.add_parser("handoff", help="Verify committed artifacts and upstream remote sync")
    p.add_argument("task_id")
    p.add_argument("--local-only", action="store_true",
                   help="Skip remote verification for handoff within the same checkout")
    p.set_defaults(func=cmd_handoff)
    p = sub.add_parser("validate", help="Manually validate task state schemas")
    p.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.func(args)
        return 0
    except TaskError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
