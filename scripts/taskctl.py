#!/usr/bin/env python3
"""Small, dependency-free task state manager for System Design Academy.

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
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / ".academy" / "state"
TASK_DIR = STATE_DIR / "tasks"
LOG_DIR = STATE_DIR / "worklog"
TASK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


class TaskError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def relpath(value: str) -> Path:
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        raise TaskError(f"Unsafe repository-relative path: {value!r}")
    return ROOT.joinpath(*p.parts)


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


def validate_task(data: dict[str, Any]) -> None:
    required = {"schema_version", "task_id", "module_id", "goal", "status", "steps"}
    missing = required - set(data)
    if missing:
        raise TaskError(f"Task state missing fields: {', '.join(sorted(missing))}")
    if data["schema_version"] != 1:
        raise TaskError(f"Unsupported schema_version: {data['schema_version']!r}")
    if not isinstance(data["task_id"], str) or not TASK_ID_RE.fullmatch(data["task_id"]):
        raise TaskError("Invalid task_id")
    if data["status"] not in {"not_started", "in_progress", "blocked", "complete"}:
        raise TaskError(f"Invalid task status: {data['status']!r}")
    if not isinstance(data["steps"], list):
        raise TaskError("steps must be an array")
    ids: set[str] = set()
    outputs: dict[str, str] = {}
    for step in data["steps"]:
        if not isinstance(step, dict):
            raise TaskError("Each step must be an object")
        for field in ("step_id", "title", "status", "depends_on", "definition_version", "input_paths", "output_paths"):
            if field not in step:
                raise TaskError(f"Step missing field {field!r}")
        sid = step["step_id"]
        if not isinstance(sid, str) or not re.fullmatch(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$", sid):
            raise TaskError(f"Invalid step_id: {sid!r}")
        if sid in ids:
            raise TaskError(f"Duplicate step_id: {sid}")
        ids.add(sid)
        if step["status"] not in {"pending", "running", "completed", "invalidated", "blocked"}:
            raise TaskError(f"Invalid status for {sid}: {step['status']!r}")
        if not isinstance(step["depends_on"], list) or not isinstance(step["input_paths"], list) or not isinstance(step["output_paths"], list):
            raise TaskError(f"depends_on/input_paths/output_paths must be arrays for {sid}")
        if not step["output_paths"]:
            raise TaskError(f"Step {sid} must declare at least one output path")
        for value in step["input_paths"] + step["output_paths"]:
            relpath(value)
        for output in step["output_paths"]:
            if output in outputs:
                raise TaskError(f"Output path {output!r} is owned by both {outputs[output]} and {sid}")
            outputs[output] = sid
    for step in data["steps"]:
        for dep in step["depends_on"]:
            if dep not in ids:
                raise TaskError(f"Step {step['step_id']} depends on unknown step {dep!r}")
    # Detect dependency cycles with depth-first traversal.
    by_id = {s["step_id"]: s for s in data["steps"]}
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


def step_map(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {step["step_id"]: step for step in data["steps"]}


def output_hashes(step: dict[str, Any]) -> dict[str, str | None]:
    return {p: sha256_file(relpath(p)) for p in step["output_paths"]}


def step_fingerprint(data: dict[str, Any], step_id: str, memo: dict[str, str] | None = None) -> str:
    memo = memo if memo is not None else {}
    if step_id in memo:
        return memo[step_id]
    step = step_map(data)[step_id]
    input_hashes = {p: sha256_file(relpath(p)) for p in step["input_paths"]}
    dependency_state = {}
    for dep_id in step["depends_on"]:
        dep = step_map(data)[dep_id]
        dependency_state[dep_id] = {
            "fingerprint": step_fingerprint(data, dep_id, memo),
            "outputs": output_hashes(dep),
        }
    result = canonical_hash({
        "step_id": step_id,
        "definition_version": str(step["definition_version"]),
        "input_hashes": input_hashes,
        "dependencies": dependency_state,
    })
    memo[step_id] = result
    return result


def step_status(data: dict[str, Any], step: dict[str, Any], memo: dict[str, str] | None = None) -> tuple[str, str]:
    sid = step["step_id"]
    states = step_map(data)
    for dep_id in step["depends_on"]:
        dep = states[dep_id]
        dep_state, _ = step_status(data, dep, memo)
        if dep_state != "SKIP":
            return "BLOCKED", f"dependency {dep_id} is {dep_state.lower()}"
    current_fp = step_fingerprint(data, sid, memo)
    current_outputs = output_hashes(step)
    if step["status"] == "running":
        if step.get("active_fingerprint") == current_fp:
            return "RESUME", "step was in progress; inspect checkpoint and existing files"
        return "STALE", "inputs changed while step was running; reconcile before resuming"
    if step["status"] == "completed":
        if step.get("completed_fingerprint") == current_fp and all(v is not None for v in current_outputs.values()) and step.get("completed_output_hashes") == current_outputs:
            return "SKIP", "fingerprint and committed output hashes match"
        return "STALE", "input fingerprint or output artifact changed"
    if step["status"] == "invalidated":
        return "READY", step.get("invalidation_reason", "manually invalidated")
    if step["status"] == "blocked":
        return "READY", "blocked state cleared; re-check inputs before starting"
    return "READY", "not completed"


def refresh_task_status(data: dict[str, Any]) -> None:
    if data["steps"] and all(step_status(data, s)[0] == "SKIP" for s in data["steps"]):
        data["status"] = "complete"
    elif any(s["status"] == "running" for s in data["steps"]):
        data["status"] = "in_progress"
    elif any(step_status(data, s)[0] == "BLOCKED" for s in data["steps"]):
        data["status"] = "blocked"
    elif any(s["status"] != "pending" for s in data["steps"]):
        data["status"] = "in_progress"
    else:
        data["status"] = "not_started"


def git_output(args: list[str]) -> str:
    try:
        result = subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise TaskError(f"Git command failed ({' '.join(args)}): {exc}") from exc
    return result.stdout.strip()


def require_committed_outputs(step: dict[str, Any]) -> str:
    for value in step["output_paths"]:
        path = relpath(value)
        if not path.is_file():
            raise TaskError(f"Output not found: {value}")
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", value], cwd=ROOT, text=True, capture_output=True)
        if tracked.returncode != 0:
            raise TaskError(f"Output is not tracked by Git yet: {value}. Commit it before marking the step complete.")
        changed = subprocess.run(["git", "status", "--porcelain", "--", value], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()
        if changed:
            raise TaskError(f"Output has uncommitted changes: {value}. Commit it before marking the step complete.")
    return git_output(["rev-parse", "HEAD"])


def cmd_init(args: argparse.Namespace) -> None:
    path = task_path(args.task_id)
    if path.exists():
        raise TaskError(f"Task already exists: {path.relative_to(ROOT)}")
    if args.template:
        template_path = relpath(args.template)
        try:
            raw = template_path.read_text(encoding="utf-8")
            rendered = raw.replace("{{TASK_ID}}", args.task_id).replace("{{MODULE_ID}}", args.module).replace("{{GOAL}}", args.goal)
            data = json.loads(rendered)
        except (OSError, json.JSONDecodeError) as exc:
            raise TaskError(f"Cannot load task template {args.template}: {exc}") from exc
        data["created_at"] = now()
        data["updated_at"] = now()
    else:
        data = {
            "schema_version": 1,
            "task_id": args.task_id,
            "module_id": args.module,
            "goal": args.goal,
            "status": "not_started",
            "current_phase": None,
            "created_at": now(),
            "updated_at": now(),
            "steps": [],
            "notes": "",
        }
    validate_task(data)
    save_task(data)
    log_event(args.task_id, "task_created", module_id=args.module, goal=args.goal)
    print(f"Created {path.relative_to(ROOT)}. Add step definitions to its steps array, then run `status`.")


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
    print(f"{data['task_id']} | {data['module_id']} | {data['status']}")
    print(data["goal"])
    memo: dict[str, str] = {}
    for step in data["steps"]:
        state, reason = step_status(data, step, memo)
        print(f"- {step['step_id']}: {state} — {reason}")
        if step.get("checkpoint", {}).get("next_action"):
            print(f"  next: {step['checkpoint']['next_action']}")
    if not data["steps"]:
        print("No steps are defined yet.")


def cmd_start(args: argparse.Namespace) -> None:
    data = load_task(args.task_id)
    states = step_map(data)
    if args.step_id not in states:
        raise TaskError(f"Unknown step: {args.step_id}")
    step = states[args.step_id]
    state, reason = step_status(data, step)
    if state == "SKIP":
        print(f"SKIP {args.step_id}: {reason}. Do not repeat this step.")
        return
    if state == "RESUME":
        if not args.resume:
            raise TaskError(f"Step is already running. Inspect its checkpoint and use --resume; {reason}.")
    elif state != "READY":
        raise TaskError(f"Cannot start {args.step_id}: {state} — {reason}")
    missing = [p for p in step["input_paths"] if not relpath(p).is_file()]
    if missing:
        raise TaskError("Required input file(s) missing: " + ", ".join(missing))
    run_id = args.run_id or f"{args.task_id}-{args.step_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    step["status"] = "running"
    step["active_fingerprint"] = step_fingerprint(data, args.step_id)
    step["run_id"] = run_id
    step["agent"] = args.agent
    step["started_at"] = now()
    step.setdefault("attempts", 0)
    if not args.resume:
        step["attempts"] += 1
    data["current_phase"] = args.step_id
    data["updated_at"] = now()
    data["status"] = "in_progress"
    save_task(data)
    log_event(args.task_id, "step_resumed" if args.resume else "step_started", step_id=args.step_id, agent=args.agent, run_id=run_id, fingerprint=step["active_fingerprint"])
    print(f"{'Resumed' if args.resume else 'Started'} {args.task_id}/{args.step_id}; run_id={run_id}")


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
    step = step_map(data).get(args.step_id)
    if step is None:
        raise TaskError(f"Unknown step: {args.step_id}")
    if step["status"] != "running":
        raise TaskError(f"Cannot complete {args.step_id}: status is {step['status']}, not running")
    current_fp = step_fingerprint(data, args.step_id)
    if current_fp != step.get("active_fingerprint"):
        raise TaskError("Inputs changed during execution. Do not mark complete; reconcile and re-run from the current fingerprint.")
    commit_sha = require_committed_outputs(step)
    hashes = output_hashes(step)
    if any(v is None for v in hashes.values()):
        raise TaskError("One or more output hashes could not be calculated")
    step["status"] = "completed"
    step["completed_fingerprint"] = current_fp
    step["completed_output_hashes"] = hashes
    step["completed_at"] = now()
    step["completed_by"] = args.agent or step.get("agent", "unknown")
    step["completed_commit"] = commit_sha
    step.pop("active_fingerprint", None)
    data["updated_at"] = now()
    refresh_task_status(data)
    save_task(data)
    log_event(args.task_id, "step_completed", step_id=args.step_id, run_id=step.get("run_id"), fingerprint=current_fp, output_hashes=hashes, commit=commit_sha)
    print(f"Completed {args.task_id}/{args.step_id} at {commit_sha[:12]}; outputs are fingerprinted.")


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
    p.add_argument("--template", help="Repository-relative JSON task template")
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
    p = sub.add_parser("start", help="Claim a ready step or resume an interrupted one")
    p.add_argument("task_id")
    p.add_argument("step_id")
    p.add_argument("--agent", required=True)
    p.add_argument("--run-id")
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