#!/usr/bin/env python3
"""Structural checks for System Design Academy content.

This does not establish factual correctness, source quality, legal rights,
or pedagogical quality. Those require separate review gates.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = ROOT / "modules/database/lessons"
SOURCE_CSV = ROOT / "modules/database/sources/source-registry.csv"
MANIFEST = ROOT / "modules/database/pilot-manifest.json"

REQUIRED_FRONT_MATTER = (
    "id", "title", "status", "level", "estimated_time", "source_review_date"
)
REQUIRED_SECTIONS = {
    "learning outcomes": re.compile(r"^##\s+(?:\d+\.\s*)?Learning outcomes\b", re.I | re.M),
    "exercise": re.compile(r"^##\s+(?:(?:\d+\.\s*)?Practical )?Exercise\b", re.I | re.M),
    "knowledge check": re.compile(r"^##\s+(?:\d+\.\s*)?Knowledge check\b", re.I | re.M),
    "answer key": re.compile(r"^#{2,3}\s+(?:\d+\.\s*)?(?:Answer key|Answer guide)\b", re.I | re.M),
    "references": re.compile(r"^##\s+(?:\d+\.\s*)?References\b", re.I | re.M),
}


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields


def main() -> int:
    errors: list[str] = []
    lesson_ids: list[str] = []

    lesson_files = sorted(LESSONS_DIR.glob("*.md")) if LESSONS_DIR.exists() else []
    if not lesson_files:
        errors.append("No lesson Markdown files found")

    for path in lesson_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        front = parse_front_matter(text)

        if not front:
            errors.append(f"{rel}: missing or malformed YAML front matter")
            continue

        for field in REQUIRED_FRONT_MATTER:
            if not front.get(field):
                errors.append(f"{rel}: missing front-matter field '{field}'")

        lesson_id = front.get("id", "")
        if lesson_id:
            lesson_ids.append(lesson_id)
            if not path.name.startswith(lesson_id):
                errors.append(f"{rel}: filename should begin with lesson ID {lesson_id}")

        status = front.get("status", "").lower()
        if status not in {"draft", "ready-for-human-review"}:
            errors.append(f"{rel}: invalid status '{status}'; generated content must not be approved/published")

        for section, pattern in REQUIRED_SECTIONS.items():
            if not pattern.search(text):
                errors.append(f"{rel}: missing required section '{section}'")

        urls = set(re.findall(r"https?://[^\s)\]>]+", text))
        if len(urls) < 2:
            errors.append(f"{rel}: expected at least 2 explicit source URLs; found {len(urls)}")

    if len(lesson_ids) != len(set(lesson_ids)):
        errors.append("Duplicate lesson IDs found in lesson front matter")

    source_count = 0
    if not SOURCE_CSV.exists():
        errors.append("Missing source registry CSV")
    else:
        try:
            with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                required = {"id", "title", "url", "publisher_or_author", "checked_date"}
                missing = required - set(reader.fieldnames or [])
                if missing:
                    errors.append(f"Source registry missing columns: {', '.join(sorted(missing))}")
                rows = list(reader)
                source_count = len(rows)
                source_ids: list[str] = []
                for row_number, row in enumerate(rows, start=2):
                    source_id = (row.get("id") or "").strip()
                    if not source_id:
                        errors.append(f"Source registry row {row_number}: missing id")
                    source_ids.append(source_id)
                    parsed = urlparse((row.get("url") or "").strip())
                    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                        errors.append(f"Source registry row {row_number}: invalid URL")
                    for field in ("title", "publisher_or_author", "checked_date"):
                        if not (row.get(field) or "").strip():
                            errors.append(f"Source registry row {row_number}: missing {field}")
                if len(source_ids) != len(set(source_ids)):
                    errors.append("Duplicate source IDs found")
        except (OSError, csv.Error) as exc:
            errors.append(f"Cannot parse source registry: {exc}")

    if not MANIFEST.exists():
        errors.append("Missing pilot manifest JSON")
    else:
        try:
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            if manifest.get("status") != "draft":
                errors.append("Pilot manifest status must remain 'draft'")
            listed = manifest.get("lessons")
            if not isinstance(listed, list):
                errors.append("Manifest 'lessons' must be an array")
            else:
                case_ids = {item for item in listed if item not in lesson_ids}
                case_dir = ROOT / "modules/database/case-studies"
                for case_id in case_ids:
                    if not any(case_dir.glob(f"{case_id}*.md")):
                        errors.append(f"Manifest case study has no matching file: {case_id}")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Cannot parse pilot manifest: {exc}")


    # Validate repo-local Agent Skills.
    skills_root = ROOT / ".agents/skills"
    skill_count = 0
    if not skills_root.exists():
        errors.append("Missing .agents/skills directory")
    else:
        for skill_file in sorted(skills_root.glob("*/SKILL.md")):
            skill_text = skill_file.read_text(encoding="utf-8")
            skill_front = parse_front_matter(skill_text)
            rel_skill = skill_file.relative_to(ROOT)
            for field in ("name", "description"):
                if not skill_front.get(field):
                    errors.append(f"{rel_skill}: missing skill field '{field}'")
            if not skill_text.split("---", 2)[-1].strip():
                errors.append(f"{rel_skill}: empty skill instructions")
            skill_count += 1
        if skill_count == 0:
            errors.append("No SKILL.md files found under .agents/skills")

    # Validate custom Codex agent profiles and project settings.
    agents_root = ROOT / ".codex/agents"
    agent_count = 0
    if not agents_root.exists():
        errors.append("Missing .codex/agents directory")
    else:
        for agent_file in sorted(agents_root.glob("*.toml")):
            rel_agent = agent_file.relative_to(ROOT)
            try:
                agent_config = tomllib.loads(agent_file.read_text(encoding="utf-8"))
            except (OSError, tomllib.TOMLDecodeError) as exc:
                errors.append(f"{rel_agent}: invalid TOML: {exc}")
                continue
            for field in ("name", "description", "developer_instructions"):
                if not isinstance(agent_config.get(field), str) or not agent_config[field].strip():
                    errors.append(f"{rel_agent}: missing/empty '{field}'")
            if "sandbox_mode" in agent_config:
                errors.append(f"{rel_agent}: custom subagents inherit parent permissions; sandbox_mode is not an enforceable per-agent setting")
            agent_count += 1
        if agent_count == 0:
            errors.append("No custom agent TOML files found under .codex/agents")

    config_path = ROOT / ".codex/config.toml"
    if not config_path.exists():
        errors.append("Missing .codex/config.toml")
    else:
        try:
            codex_config = tomllib.loads(config_path.read_text(encoding="utf-8"))
            max_threads = codex_config.get("agents", {}).get("max_concurrent_threads_per_session")
            if not isinstance(max_threads, int) or not 1 <= max_threads <= 16:
                errors.append(".codex/config.toml: max_concurrent_threads_per_session must be an integer from 1 to 16")
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f".codex/config.toml: invalid TOML: {exc}")

    checked_links = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            checked_links += 1
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)}: relative link escapes repository: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken relative link: {target}")

    print("System Design Academy content validation")
    print(f"Lessons found: {len(lesson_ids)}")
    print(f"Source registry rows: {source_count}")
    print(f"Internal Markdown links checked: {checked_links}")
    print(f"Skills found: {skill_count}")
    print(f"Custom agents found: {agent_count}")
    print("Scope: structural checks only; not factual, legal, or pedagogical approval.")

    if errors:
        print(f"\nFAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nPASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
