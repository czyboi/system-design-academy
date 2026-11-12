#!/usr/bin/env python3
"""Explicit, bounded state for lesson and module review/revision cycles.

Only records decisions/counters; never invokes AI, edits lessons or merges.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_REVISIONS = 2
VERDICTS = ("block", "revise", "ready-for-human-review")


class ReviewCycleError(Exception):
    pass


def state_path(target: str) -> Path:
    if re.fullmatch(r"m\d{2}", target):
        return ROOT / "modules" / target / "reviews" / "automatic" / "cycle.json"
    if re.fullmatch(r"M\d{2}-L\d{2}", target):
        return ROOT / "modules" / target[:3].lower() / "reviews" / "automatic" / "lessons" / target / "cycle.json"
    raise ReviewCycleError("Target must be a canonical module (m01) or lesson (M01-L02) ID")


def expected_fields(target: str) -> dict:
    state_path(target)  # Validate the ID before touching any state.
    return {"module": target[:3].lower(), "lesson": target} if target.startswith("M") else {"module": target}


def load(module: str) -> dict | None:
    path = state_path(module)
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    identity = expected_fields(module)
    if (not isinstance(value, dict) or any(value.get(key) != val for key, val in identity.items())
            or (not module.startswith("M") and value.get("lesson") is not None)
            or type(value.get("revision_attempts")) is not int
            or value["revision_attempts"] not in range(MAX_REVISIONS + 1)
            or value.get("status") not in {"needs_revision", "revising", "ready", "blocked"}
            or not isinstance(value.get("review_history"), list)):
        raise ReviewCycleError(f"Invalid review cycle state: {path}")
    return value


def save(module: str, state: dict) -> dict:
    path = state_path(module)
    path.parent.mkdir(parents=True, exist_ok=True)
    state.update(expected_fields(module))
    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return state


def record(module: str, technical: str, pedagogy: str) -> dict:
    """Record actual reviewer decisions after reports are written; do not infer AI verdicts."""
    if technical not in VERDICTS or pedagogy not in VERDICTS:
        raise ReviewCycleError("Unexpected reviewer verdict")
    current = load(module)
    if current and current["status"] != "revising":
        raise ReviewCycleError("Review result already recorded; no revision is in progress")
    for role in ("technical", "pedagogy"):
        report = state_path(module).parent / f"{role}.md"
        if not report.is_file() or not report.read_text(encoding="utf-8").strip():
            raise ReviewCycleError(f"Missing nonempty {role} report: {report}")
    state = current or {**expected_fields(module), "revision_attempts": 0, "review_history": []}
    attempts = state["revision_attempts"]
    accepted = technical == pedagogy == "ready-for-human-review"
    state["status"] = "ready" if accepted else ("blocked" if attempts >= MAX_REVISIONS else "needs_revision")
    state["review_history"].append({
        "round": attempts, "technical": technical, "pedagogy": pedagogy,
        "result": state["status"]
    })
    return save(module, state)


def begin_revision(module: str) -> dict:
    """Reserve one revision round before dispatching the author."""
    current = load(module)
    if not current or current["status"] != "needs_revision":
        raise ReviewCycleError("No eligible unresolved review cycle; initial reviews must be recorded first")
    if current["revision_attempts"] >= MAX_REVISIONS:
        raise ReviewCycleError("Automatic revision limit reached; human review required")
    current["revision_attempts"] += 1
    current["status"] = "revising"
    return save(module, current)


def stop(module: str, reason: str) -> dict:
    """Stop safely when a claim, source or reviewer disagreement cannot be resolved."""
    current = load(module)
    if not current:
        raise ReviewCycleError("No review cycle to stop")
    if not reason.strip():
        raise ReviewCycleError("Stopping requires a reason")
    current["status"] = "blocked"
    current["stop_reason"] = reason.strip()
    return save(module, current)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["record", "begin-revision", "status", "stop"])
    parser.add_argument("module", help="Review target: lesson M01-L02 or module m01")
    parser.add_argument("--technical", choices=VERDICTS)
    parser.add_argument("--pedagogy", choices=VERDICTS)
    parser.add_argument("--reason", default="")
    args = parser.parse_args(argv)
    try:
        if args.action == "record":
            if not args.technical or not args.pedagogy:
                raise ReviewCycleError("record requires both --technical and --pedagogy")
            state = record(args.module, args.technical, args.pedagogy)
        elif args.action == "begin-revision":
            state = begin_revision(args.module)
        elif args.action == "stop":
            state = stop(args.module, args.reason)
        else:
            state = load(args.module)
            if state is None:
                raise ReviewCycleError(f"{args.module}: no review cycle record")
        print(json.dumps(state, ensure_ascii=False, indent=2))
    except (OSError, ValueError, ReviewCycleError) as exc:
        print(f"REVIEW CYCLE FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
