#!/usr/bin/env python3
"""Repository learning memory from independently reviewed, corrected module findings.

This CLI is deterministic: no model calls, content scoring or skill-file mutations.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

if __package__:
    from . import review_cycle
else:
    import review_cycle

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ".academy/knowledge/lessons-learned.json"
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
TAG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FINDING = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,35}\Z")
ROLES = {"lesson_author", "technical_reviewer", "pedagogy_reviewer"}
REVIEW_ROLES = {"technical", "pedagogy"}


class LearningError(Exception):
    pass


def memory_path() -> Path:
    return ROOT / MEMORY


def read_memory() -> dict:
    path = memory_path()
    if not path.is_file():
        raise LearningError(f"Missing knowledge store: {MEMORY}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or data.get("schema_version") != 1
            or not isinstance(data.get("entries"), list)):
        raise LearningError("Invalid knowledge store schema")
    if any(not isinstance(item, dict) or not isinstance(item.get("key"), str)
           or not isinstance(item.get("occurrences"), list)
           for item in data["entries"]):
        raise LearningError("Invalid knowledge entry")
    keys = [item["key"] for item in data["entries"]]
    if len(keys) != len(set(keys)):
        raise LearningError("Duplicate knowledge keys")
    return data


def write_memory(data: dict) -> None:
    path = memory_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent,
                                     prefix=".memory-", suffix=".tmp", delete=False) as out:
        temp = Path(out.name)
        try:
            json.dump(data, out, indent=2, ensure_ascii=False)
            out.write("\n")
        except Exception:
            temp.unlink(missing_ok=True)
            raise
    os.replace(temp, path)


def labels(value: str, allowed: set[str] | None = None) -> list[str]:
    parts = [part.strip().lower() for part in value.split(",")]
    pattern = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*\Z") if allowed else TAG
    if not 1 <= len(parts) <= 8 or any(not pattern.fullmatch(p) for p in parts):
        raise LearningError("Expected 1-8 comma-separated lowercase hyphenated tags")
    if len(set(parts)) != len(parts):
        raise LearningError("Duplicate tags")
    if allowed and not set(parts).issubset(allowed):
        raise LearningError(f"Invalid role: {set(parts) - allowed}")
    return parts


def short_text(value: str, name: str, limit: int = 360) -> str:
    if not isinstance(value, str) or not 15 <= len(value.strip()) <= limit:
        raise LearningError(f"{name} must be 15-{limit} characters")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise LearningError(f"{name} must be a single line without controls")
    return value.strip()


def evidence_ref(value: str) -> str:
    """Require a source, never an unchecked reviewer-only assertion."""
    url = urlsplit(value)
    if url.scheme == "https" and url.netloc and not url.username and not url.password:
        return value
    path = Path(value)
    if (path.is_absolute() or ".." in path.parts or "\\" in value
            or not value.startswith(("curriculum/", "docs/", "modules/"))):
        raise LearningError("Evidence must be an HTTPS source or safe repository document path")
    if not (ROOT / path).is_file():
        raise LearningError(f"Missing source evidence: {value}")
    return value


def record(*, module: str, finding_id: str, review_role: str, key: str,
           tags: str, problem: str, prevention: str, evidence: str,
           applies_to: str) -> dict:
    if not KEY.fullmatch(key) or len(key) > 70:
        raise LearningError("Knowledge key must be a stable slug of <=70 characters")
    if review_role not in REVIEW_ROLES or not FINDING.fullmatch(finding_id):
        raise LearningError("Invalid reviewer role or finding ID")
    current = review_cycle.load(module)
    if (not current or current["status"] != "ready"
            or current["revision_attempts"] < 1):
        raise LearningError("Only independently re-reviewed, successfully corrected findings can be learned")
    report = f"modules/{module}/reviews/automatic/{review_role}.md"
    report_path = ROOT / report
    if not report_path.is_file():
        raise LearningError(f"Missing reviewer report: {report}")
    text = report_path.read_text(encoding="utf-8")
    located = re.search(r"(?<![\w-])" + re.escape(finding_id)
                        + r"(?![\w-])[^\n]{0,240}\bresolved\b", text, re.IGNORECASE)
    if not located:
        raise LearningError(f"{finding_id} is not explicitly marked resolved in the final {review_role} report")
    tags_list = labels(tags)
    roles_list = labels(applies_to, ROLES)
    problem = short_text(problem, "Problem")
    prevention = short_text(prevention, "Prevention")
    evidence = evidence_ref(evidence)
    if evidence not in text:
        raise LearningError("Primary/curriculum evidence must appear exactly in the final reviewer report")
    data = read_memory()
    existing = next((item for item in data["entries"] if item["key"] == key), None)
    if existing:
        if (existing["problem"] != problem or existing["prevention"] != prevention
                or existing["tags"] != tags_list or existing["applies_to"] != roles_list):
            raise LearningError("Existing key has different guidance; reconcile conflicting rules manually")
        entry = existing
    else:
        entry = {"key": key, "tags": tags_list, "problem": problem,
                 "prevention": prevention, "applies_to": roles_list, "occurrences": []}
    occurrence = {"module": module, "finding_id": finding_id,
                  "review_role": review_role, "report": report, "evidence": evidence}
    same = [item for item in entry["occurrences"]
            if (item["module"], item["finding_id"], item["review_role"])
            == (module, finding_id, review_role)]
    if same:
        if same[0] != occurrence:
            raise LearningError("Conflicting evidence for existing occurrence")
        return {"key": key, "result": "unchanged", "modules": len({x["module"] for x in entry["occurrences"]})}
    entry["occurrences"].append(occurrence)
    if not existing:
        data["entries"].append(entry)
    data["entries"].sort(key=lambda x: x["key"])
    write_memory(data)
    return {"key": key, "result": "recorded",
            "modules": len({x["module"] for x in entry["occurrences"]})}


def suggest(tags: str, role: str, limit: int = 3) -> list[dict]:
    if role not in ROLES:
        raise LearningError("Invalid target role")
    if not 1 <= limit <= 5:
        raise LearningError("At most five relevant memories can be injected per task")
    wanted = set(labels(tags))
    matches = []
    for entry in read_memory()["entries"]:
        if role not in entry.get("applies_to", []):
            continue
        overlap = len(wanted.intersection(entry.get("tags", [])))
        if overlap:
            matches.append((overlap, len({o["module"] for o in entry["occurrences"]}),
                            entry["key"], entry))
    matches.sort(key=lambda x: (-x[0], -x[1], x[2]))
    return [
        {"key": entry["key"], "problem": entry["problem"],
         "prevention": entry["prevention"],
         "review_evidence": entry["occurrences"][-1]["report"]}
        for _, _, _, entry in matches[:limit]
    ]


def promotions() -> list[dict]:
    """Recurring independently fixed problems: propose skill changes, never apply them."""
    candidates = []
    for entry in read_memory()["entries"]:
        modules = sorted({o["module"] for o in entry["occurrences"]})
        if len(modules) >= 2:
            candidates.append({"key": entry["key"], "modules": modules,
                               "problem": entry["problem"],
                               "suggested_rule": entry["prevention"],
                               "requires": "Check for conflicts and open a separate reviewable PR; do not edit skills automatically"})
    return candidates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("record", help="Record a re-reviewed correction with primary-source evidence")
    for name in ("module", "finding-id", "review-role", "key", "tags", "problem",
                 "prevention", "evidence", "applies-to"):
        p.add_argument("--" + name, required=True)
    p = sub.add_parser("suggest", help="Select only short, role-relevant verified memories")
    p.add_argument("--tags", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--limit", type=int, default=3)
    sub.add_parser("promotions", help="Identify repeated problems for reviewable skill PRs")
    args = parser.parse_args(argv)
    try:
        if args.action == "record":
            result = record(module=args.module, finding_id=args.finding_id,
                            review_role=args.review_role, key=args.key, tags=args.tags,
                            problem=args.problem, prevention=args.prevention,
                            evidence=args.evidence, applies_to=args.applies_to)
        elif args.action == "suggest":
            result = suggest(args.tags, args.role, args.limit)
        else:
            result = promotions()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (LearningError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"LEARNING MEMORY FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
