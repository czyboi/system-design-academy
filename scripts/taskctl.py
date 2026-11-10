#!/usr/bin/env python3
"""Schema-validated task state manager for System Design Academy.

A completed step is reusable only when its current input fingerprint and all
committed output hashes match the values recorded at completion.
"""
from __future__ import annotations

import argparse
import hashlib
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


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


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


def load_spec(data: dict[str, Any], execution_ready: bool = False) -> dict[str, Any]:
    path = relpath(data["spec_path"])
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise TaskError(f"Cannot read task specification {path}: {exc}") from exc
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


def validate_task(data: dict[str, Any]) -> None:
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
    load_spec(data)

def step_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {step["step_id"]: step for step in data["steps"]}


def output_hashes(step: dict[str, Any]) -> dict[str, str | None]:
    return {p: sha256_file(relpath(p)) for p in step["output_paths"]}



def step_spec_slice(spec: dict[str, Any], step_id: str) -> dict[str, Any]:
    def relevant(field: str) -> list[dict[str, Any]]:
        return sorted(
            [item for item in spec[field] if "*" in item["applies_to"] or step_id in item["applies_to"]],
            key=lambda item: item["id"],
        )
    return {
        "goal": spec["goal"],
        "scope": spec["scope"],
        "constraints": spec["constraints"],
        "definition_of_done": relevant("definition_of_done"),
        "acceptance_criteria": relevant("acceptance_criteria"),
    }


def step_spec_hash(data: dict[str, Any], step_id: str) -> str:
    return canonical_hash(step_spec_slice(load_spec(data), step_id))


def step_fingerprint(data: dict[str, Any], step_id: str, memo: dict[str, str] | None = None) -> str:
    memo = memo if memo is not None else {}
    if step_id in memo:
        return memo[step_id]
    step = step_map(data)[step_id]
    dependency_state = {}
    for dep_id in step["depends_on"]:
        dep = step_map(data)[dep_id]
        dependency_state[dep_id] = {
            "fingerprint": step_fingerprint(data, dep_id, memo),
            "outputs": output_hashes(dep),
        }
    payload = {
        "step_id": step_id,
        "definition_version": str(step["definition_version"]),
        "task_spec_hash": step_spec_hash(data, step_id),
        "input_hashes": {path: sha256_file(relpath(path)) for path in step["input_paths"]},
        "dependencies": dependency_state,
    }
    # Preserve fingerprints for historical tasks without the new contract.
    for field in ("review", "requires_reviews", "revision_cycle"):
        if field in step:
            payload[field] = step[field]
    result = canonical_hash(payload)
    memo[step_id] = result
    return result

def review_result(step: dict[str, Any]) -> dict[str, Any]:
    contract = step["review"]
    try:
        result = json.loads(relpath(contract["verdict_path"]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise TaskError(f"Missing or invalid review verdict for {step['step_id']}: {exc}") from exc
    if not isinstance(result, dict) or result.get("verdict") not in {"block", "revise", "ready-for-human-review"}:
        raise TaskError("Review verdict must be block, revise, or ready-for-human-review")
    hashes = {p: sha256_file(relpath(p)) for p in contract["artifact_paths"]}
    if any(v is None for v in hashes.values()) or result.get("artifact_hashes") != hashes:
        raise TaskError(f"Review {step['step_id']} does not match the current artifact hashes")
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


def step_status(data: dict[str, Any], step: dict[str, Any], memo: dict[str, str] | None = None) -> tuple[str, str]:
    sid = step["step_id"]
    states = step_map(data)
    for dep_id in step["depends_on"]:
        dep = states[dep_id]
        dep_state, _ = step_status(data, dep, memo)
        if dep_state != "SKIP":
            return "BLOCKED", f"dependency {dep_id} is {dep_state.lower()}"
    for gate in step.get("requires_reviews", []):
        try:
            verdict = review_result(states[gate])["verdict"]
        except TaskError as exc:
            return "BLOCKED", str(exc)
        if verdict != "ready-for-human-review":
            return "BLOCKED", f"review {gate} verdict is {verdict}"
    current_fp = step_fingerprint(data, sid, memo)
    current_outputs = output_hashes(step)
    if step["status"] == "running":
        if data.get("execution_control", "active") != "active":
            return "BLOCKED", f"task is {data['execution_control']}"
        if step.get("active_fingerprint") == current_fp:
            return "RESUME", "step was in progress; inspect checkpoint and existing files"
        return "STALE", "inputs changed while step was running; reconcile before resuming"
    if step["status"] == "completed":
        if step.get("completed_fingerprint") == current_fp and all(v is not None for v in current_outputs.values()) and step.get("completed_output_hashes") == current_outputs:
            try:
                require_tracked_clean(step["output_paths"], "Completed output")
                if step.get("review"):
                    review_result(step)
            except TaskError as exc:
                return "STALE", str(exc)
            return "SKIP", "fingerprint and committed output hashes match"
        return "STALE", "input fingerprint or output artifact changed"
    if data.get("execution_control", "active") != "active":
        return "BLOCKED", f"task is {data['execution_control']}"
    if step["status"] == "invalidated":
        return "READY", step.get("invalidation_reason", "manually invalidated")
    if step["status"] == "blocked":
        return "READY", "blocked state cleared; re-check inputs before starting"
    return "READY", "not completed"



def refresh_task_status(data: dict[str, Any]) -> None:
    if data.get("execution_control", "active") != "active":
        data["automation_status"] = "blocked"
        return
    statuses = [step_status(data, step)[0] for step in data["steps"]]
    if statuses and all(status == "SKIP" for status in statuses):
        data["automation_status"] = "automation_complete"
    elif any(status in {"READY", "RESUME", "STALE"} for status in statuses):
        # A runnable or recoverable step means the task can still make progress.
        # Dependency-blocked downstream steps are expected in a healthy DAG.
        if any(step["status"] != "pending" for step in data["steps"]):
            data["automation_status"] = "in_progress"
        else:
            data["automation_status"] = "not_started"
    elif any(step["status"] == "running" for step in data["steps"]):
        data["automation_status"] = "in_progress"
    elif any(status == "BLOCKED" for status in statuses):
        data["automation_status"] = "blocked"
    elif any(step["status"] != "pending" for step in data["steps"]):
        data["automation_status"] = "in_progress"
    else:
        data["automation_status"] = "not_started"

def git_output(args: list[str]) -> str:
    try:
        result = subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise TaskError(f"Git command failed ({' '.join(args)}): {exc}") from exc
    return result.stdout.strip()



def git_checked(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    except OSError as exc:
        raise TaskError(f"Cannot execute Git: {exc}") from exc
    if check and result.returncode:
        raise TaskError(f"Git command failed ({' '.join(args)}): {result.stderr.strip()}")
    return result


def require_tracked_clean(paths: list[str], purpose: str) -> None:
    for value in paths:
        relpath(value)
        tracked = git_checked(["ls-files", "--error-unmatch", "--", value], check=False)
        if tracked.returncode:
            raise TaskError(f"{purpose} is not Git-tracked: {value}")
        dirty = git_checked(["status", "--porcelain", "--untracked-files=all", "--", value]).stdout.strip()
        if dirty:
            raise TaskError(f"{purpose} is dirty or staged: {value}. Commit or discard changes first.")


def require_committed_outputs(step: dict[str, Any]) -> str:
    for value in step["output_paths"]:
        if not relpath(value).is_file():
            raise TaskError(f"Output not found: {value}")
    require_tracked_clean(step["output_paths"], "Output")
    return git_output(["rev-parse", "HEAD"])


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
        "created_at": now(),
        "updated_at": now(),
    })
    data.pop("goal", None)
    data.pop("status", None)
    validate_json_schema(spec, SPEC_SCHEMA, "Task specification")
    save_json(spec_path, spec)
    validate_task(data)
    save_task(data)
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
    save_task(data)
    log_event(args.task_id, "step_defined", step_id=args.step_id, depends_on=args.depends_on, inputs=args.input_paths, outputs=args.output_paths)
    print(f"Added step {args.task_id}/{args.step_id}")



def cmd_status(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    refresh_task_status(data)
    spec = load_spec(data)
    print(f"{data['task_id']} | {data['module_id']} | automation={data['automation_status']} | owner={data['owner']}")
    print(f"Specification: {data['spec_path']} — {spec['goal']}")
    for step in data["steps"]:
        state, reason = step_status(data, step)
        print(f"- {step['step_id']}: {state} — {reason}")
        if step.get("checkpoint", {}).get("next_action"):
            print(f"  next: {step['checkpoint']['next_action']}")
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


def current_input_snapshot(data: dict[str, Any], step: dict[str, Any]) -> dict[str, str]:
    paths = list(step["input_paths"])
    hashes: dict[str, str] = {}
    for value in paths:
        digest = sha256_file(relpath(value))
        if digest is None:
            raise TaskError(f"Required input file is missing: {value}")
        hashes[value] = digest
    return hashes


def cmd_start(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    require_active(data)
    if not data["owner"].strip():
        raise TaskError("Set the task owner before execution")
    states = step_map(data)
    if args.step_id not in states:
        raise TaskError(f"Unknown step: {args.step_id}")
    step = states[args.step_id]
    state, reason = step_status(data, step)
    if state == "SKIP":
        print(f"SKIP {args.step_id}: {reason}. Do not repeat this step.")
        return
    if state == "RESUME" and not args.resume:
        raise TaskError(f"Step is already running. Inspect its checkpoint and use --resume; {reason}")
    if state not in {"READY", "RESUME"}:
        raise TaskError(f"Cannot start {args.step_id}: {state} — {reason}")
    load_spec(data, execution_ready=True)
    require_tracked_clean(list(step["input_paths"]) + [data["spec_path"]], "Input/specification")
    snapshot = current_input_snapshot(data, step)
    output_before = output_hashes(step)
    run_id = args.run_id or (step.get("run_id") if args.resume else None) or f"{args.task_id}-{args.step_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    if args.resume:
        if step.get("start_commit") is None or step.get("start_input_hashes") != snapshot:
            raise TaskError("Cannot resume: the starting commit or input snapshot is missing/changed; reconcile and restart.")
        git_checked(["merge-base", "--is-ancestor", step["start_commit"], "HEAD"])
        step["resume_count"] = step.get("resume_count", 0) + 1
    else:
        if step.get("revision_cycle") and sum(s.get("attempts", 0) for s in data["steps"] if s.get("revision_cycle")) >= 2:
            raise TaskError("Two automated revision runs have been used; hold awaiting-human before further work")
        for path, digest in output_before.items():
            if digest is not None:
                require_tracked_clean([path], "Existing output")
        step["start_commit"] = git_output(["rev-parse", "HEAD"])
        step["start_input_hashes"] = snapshot
        step["start_output_hashes"] = output_before
        step["attempts"] = step.get("attempts", 0) + 1
        step["started_at"] = now()
    step["status"] = "running"
    step["active_spec_hash"] = step_spec_hash(data, args.step_id)
    step["active_fingerprint"] = step_fingerprint(data, args.step_id)
    step["run_id"] = run_id
    step["agent"] = args.agent
    previous_runtime = step.get("runtime", {}) if args.resume else {}
    step["runtime"] = {"model": args.model or previous_runtime.get("model"),
                       "reasoning_effort": args.reasoning_effort or previous_runtime.get("reasoning_effort")}
    data["current_phase"] = args.step_id
    data["updated_at"] = now()
    data["automation_status"] = "in_progress"
    save_task(data)
    log_event(args.task_id, "step_resumed" if args.resume else "step_started",
              step_id=args.step_id, agent=args.agent, run_id=run_id,
              fingerprint=step["active_fingerprint"], start_commit=step["start_commit"],
              input_hashes=snapshot, runtime=step["runtime"])
    print(f"{'Resumed' if args.resume else 'Started'} {args.task_id}/{args.step_id}; start_commit={step['start_commit'][:12]}")

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
                isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v < float('inf') for v in usage.values()):
            raise TaskError("Usage must contain nonnegative finite runtime counters only")
    require_tracked_clean(list(step["input_paths"]) + [data["spec_path"]], "Input/specification")
    current_snapshot = current_input_snapshot(data, step)
    if current_snapshot != step.get("start_input_hashes"):
        raise TaskError("Declared inputs or task specification changed during execution; reconcile and restart.")
    current_spec_hash = step_spec_hash(data, args.step_id)
    current_fp = step_fingerprint(data, args.step_id)
    if current_spec_hash != step.get("active_spec_hash") or current_fp != step.get("active_fingerprint"):
        raise TaskError("Task specification, inputs, or dependencies changed during execution. Do not mark complete.")
    state, reason = step_status(data, step)
    if state != "RESUME":
        raise TaskError(f"Cannot complete {args.step_id}: {state}: {reason}")
    start_commit = step.get("start_commit")
    if not start_commit:
        raise TaskError("Missing start_commit; refusing completion without a reproducible baseline")
    git_checked(["merge-base", "--is-ancestor", start_commit, "HEAD"])
    commit_sha = require_committed_outputs(step)
    hashes = output_hashes(step)
    unchanged = {
        path for path, digest in hashes.items()
        if digest is None or digest == step.get("start_output_hashes", {}).get(path)
    }
    reused = set(args.reuse_output or [])
    unknown = reused - set(step["output_paths"])
    if unknown:
        raise TaskError("Reuse path is not a declared output: " + ", ".join(sorted(unknown)))
    if reused - unchanged:
        raise TaskError("--reuse-output may only be used for outputs unchanged since start: " + ", ".join(sorted(reused - unchanged)))
    if unchanged - reused:
        raise TaskError("Output was not produced/updated in this run. Explicitly pass --reuse-output for intentional reuse: " + ", ".join(sorted(unchanged - reused)))
    if reused and not args.reuse_reason.strip():
        raise TaskError("--reuse-reason is required when reusing unchanged outputs")
    for path in step["output_paths"]:
        changed = git_checked(["diff", "--quiet", start_commit, "HEAD", "--", path], check=False).returncode != 0
        if path not in reused and not changed:
            raise TaskError(f"Output has no committed change after start: {path}")
    step["status"] = "completed"
    step["completed_fingerprint"] = current_fp
    step["completed_spec_hash"] = current_spec_hash
    step["completed_output_hashes"] = hashes
    step["completed_at"] = now()
    step["completed_by"] = args.agent or step.get("agent", "unknown")
    step["completed_commit"] = commit_sha
    if reused:
        step["reused_outputs"] = {path: {"reason": args.reuse_reason, "at": now()} for path in sorted(reused)}
    step.pop("active_fingerprint", None)
    step.pop("active_spec_hash", None)
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "step_completed", step_id=args.step_id, run_id=step.get("run_id"),
              fingerprint=current_fp, spec_hash=current_spec_hash, output_hashes=hashes,
              commit=commit_sha, reused_outputs=sorted(reused), reuse_reason=args.reuse_reason if reused else None,
              runtime=step.get("runtime"), usage=usage)
    print(f"Completed {args.task_id}/{args.step_id} at {commit_sha[:12]}; automation={data['automation_status']}.")
    if data["automation_status"] == "automation_complete":
        print("Automation complete; human review, approval, and publication remain manual gates.")

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
        step.pop("active_fingerprint", None)
        step.pop("active_spec_hash", None)
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "steps_invalidated", step_ids=sorted(target_ids), reason=args.reason)
    print("Invalidated: " + ", ".join(sorted(target_ids)))


def cmd_validate(args: argparse.Namespace) -> None:
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
    parser = argparse.ArgumentParser(description="Idempotent task progress and handoff tracker")
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
    p = sub.add_parser("status", help="Show task state and which steps can be skipped")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_status)
    p = sub.add_parser("reconcile", help="Explicitly persist computed aggregate status")
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
    p = sub.add_parser("complete", help="Mark a step complete after its outputs are committed")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--agent")
    p.add_argument("--usage-file", help="Repository-relative JSON containing observed runtime usage counters")
    p.add_argument("--reuse-output", action="append", default=[], help="Explicitly reuse an unchanged declared output; repeat per path")
    p.add_argument("--reuse-reason", default="", help="Required reason for unchanged output reuse")
    p.set_defaults(func=cmd_complete)
    p = sub.add_parser("invalidate", help="Invalidate a step when a human decision requires it")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--reason", required=True)
    p.add_argument("--cascade", action="store_true")
    p.set_defaults(func=cmd_invalidate)
    p = sub.add_parser("validate", help="Validate all task state files")
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
