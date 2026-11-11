#!/usr/bin/env python3
"""Check full pinned Primer coverage, not factual truth or teaching quality.

Inventory completeness and teaching depth still require independent review.
This command is read-only and never generates course content or a verdict.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRIMER = "https://github.com/donnemartin/system-design-primer"


def excluded_heading(title: str) -> bool:
    """Identify non-teaching sections without excluding real concepts like reference architecture."""
    return bool(re.fullmatch(
        r"(?:references?|attribution(?: and change notes)?|knowledge checks?|quiz|"
        r"answer key(?:\s*/\s*rubric)?|rubric|(?:practical )?exercise|learning outcomes)",
        title.strip(), re.I,
    ))


def artifact(value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
        raise ValueError(f"Expected repository-relative path: {value!r}")
    path = ROOT / value
    path.resolve().relative_to(ROOT.resolve())
    if not path.is_file():
        raise ValueError(f"Missing artifact: {value}")
    return path


def section(text: str, title: str, *, lesson_id: bool = False) -> str:
    """Resolve one heading and its body; reject ambiguous duplicate headings."""
    text = re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=re.S)
    text = re.sub(r"(?m)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[^\n]*(?:\n|$)", lambda m: re.sub(r"[^\n]", " ", m.group()), text, flags=re.S)
    headings = list(re.finditer(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", text, re.M))
    matches = []
    for i, heading in enumerate(headings):
        found = (re.search(r"(?<![\w-])" + re.escape(title) + r"(?![\w-])", heading[2])
                 if lesson_id else heading[2].strip() == title)
        if found:
            if not lesson_id and len(heading[1]) == 1:
                raise ValueError("Document title is not a teaching section")
            end = next((h.start() for h in headings[i + 1:] if len(h[1]) <= len(heading[1])), len(text))
            if not lesson_id:
                if excluded_heading(heading[2]):
                    raise ValueError("A title, reference or assessment section is not teaching evidence")
                end = next((h.start() for h in headings[i + 1:]
                            if h.start() < end and excluded_heading(h[2])), end)
            body = text[heading.end():end]
            matches.append(body.strip())
    if len(matches) != 1:
        raise ValueError(f"Expected one heading for {title!r}, found {len(matches)}")
    return matches[0]


def check_review(path: Path) -> None:
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict) or result.get("verdict") != "ready-for-human-review":
        raise ValueError("Course review is not accepted for human review")
    if result.get("checks") != {"coverage": "pass", "pedagogy": "pass"}:
        raise ValueError("Course review must explicitly pass both coverage and pedagogy")
    findings = result.get("findings")
    if not isinstance(findings, list):
        raise ValueError("Course review requires findings")
    seen = set()
    for finding in findings:
        if (not isinstance(finding, dict) or not isinstance(finding.get("id"), str)
                or not finding["id"].strip() or finding["id"] in seen
                or finding.get("severity") not in {"blocker", "major", "minor", "note"}
                or finding.get("status") not in {"open", "resolved"}):
            raise ValueError("Invalid or duplicate course review finding")
        seen.add(finding["id"])
        if finding["severity"] in {"blocker", "major"} and finding["status"] == "open":
            raise ValueError("Course review has an unresolved material finding")


def validate(inventory_path: str, matrix_path: str, plan_path: str,
             stage: str = "plan", review_path: str | None = None) -> list[str]:
    errors = []
    try:
        inventory_file, matrix_file, plan_file = map(artifact, (inventory_path, matrix_path, plan_path))
        inventory = json.loads(inventory_file.read_text(encoding="utf-8"))
        if not isinstance(inventory, dict):
            raise ValueError("Inventory must be an object")
        if inventory.get("repository") != PRIMER or not re.fullmatch(r"[0-9a-f]{40}", str(inventory.get("revision", ""))):
            raise ValueError("Inventory must pin the System Design Primer repository and a full commit SHA")
        entries = inventory.get("entries")
        if not isinstance(entries, list) or not entries:
            raise ValueError("Inventory needs nonempty entries")
        topics, seen = set(), set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("Inventory entry must be an object")
            key = entry.get("id")
            if not isinstance(key, str) or not key.strip() or key in seen:
                raise ValueError("Inventory IDs must be nonempty and unique")
            seen.add(key)
            locator = entry.get("locator")
            if (not isinstance(locator, str) or not locator.strip() or "://" in locator
                    or locator.startswith(("/", "\\")) or ".." in locator.split("/")):
                raise ValueError(f"{key}: locator must name a path/anchor at the pinned revision")
            if entry.get("kind") == "topic":
                topics.add(key)
            elif entry.get("kind") != "resource" or not str(entry.get("rationale", "")).strip():
                raise ValueError(f"{key}: use topic or a resource with an explicit rationale")
        if not topics:
            raise ValueError("Inventory must contain knowledge topics, not only resources")
        with matrix_file.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required = {"topic_id", "lesson", "outline", "disposition"}
            if stage == "taught":
                required |= {"lesson_path", "section"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError(f"Coverage matrix needs columns: {', '.join(sorted(required))}")
            rows = list(reader)
        plan = plan_file.read_text(encoding="utf-8")
        mapped = set()
        for row in rows:
            key = row.get("topic_id", "")
            if key not in topics or key in mapped:
                errors.append(f"Unknown, non-topic or duplicate matrix ID: {key}")
                continue
            mapped.add(key)
            if row.get("disposition") not in {"mapped", "merged"}:
                errors.append(f"{key}: full coverage cannot defer, omit or exclude knowledge topics")
            try:
                lesson, outline = row.get("lesson", ""), row.get("outline", "")
                if not lesson or not outline or outline not in section(plan, lesson, lesson_id=True):
                    raise ValueError("Mapping must name an outline inside its own lesson section")
                if stage == "taught":
                    path = artifact(row.get("lesson_path", ""))
                    text = path.read_text(encoding="utf-8")
                    front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
                    metadata = yaml.safe_load(front[1]) if front else {}
                    if not isinstance(metadata, dict) or metadata.get("id") != lesson or metadata.get("status") != "draft":
                        raise ValueError("Taught evidence must be the matching draft teaching lesson")
                    if metadata.get("lesson") or "outcome_map" in metadata:
                        raise ValueError("An assessment cannot count as a teaching lesson")
                    heading = row.get("section", "")
                    if not heading or excluded_heading(heading):
                        raise ValueError("A title, reference or assessment section is not teaching evidence")
                    body = section(text, heading)
                    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
                    body = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.M)
                    if not body.strip():
                        raise ValueError("Teaching section is empty")
            except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
                errors.append(f"{key}: {exc}")
        errors.extend(f"Missing knowledge topic: {key}" for key in sorted(topics - mapped))
        if review_path:
            check_review(artifact(review_path))
    except (OSError, ValueError, TypeError, csv.Error) as exc:
        errors.append(str(exc))
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("inventory", "matrix", "plan"):
        parser.add_argument("--" + name, required=True, help="Repository-relative artifact")
    parser.add_argument("--stage", choices=("plan", "taught"), default="plan")
    parser.add_argument("--review", help="Optionally check an existing review verdict (no artifact hashes)")
    args = parser.parse_args(argv)
    errors = validate(args.inventory, args.matrix, args.plan, args.stage, args.review)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{'FAILED' if errors else 'PASSED'}: full coverage structure ({args.stage}); independent source enumeration and teaching review still required.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
