#!/usr/bin/env python3
"""Structural checks for System Design Academy content.

This does not establish factual correctness, source quality, legal rights,
or pedagogical quality. Those require separate review gates.
"""
from __future__ import annotations

import csv
import argparse
import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FRONT_MATTER = (
    "id", "title", "status", "level", "estimated_time", "source_review_date"
)
REQUIRED_SECTIONS = {
    "learning outcomes": re.compile(r"^##\s+(?:\d+\.\s*)?Learning outcomes\b", re.I | re.M),
    "motivation": re.compile(r"^##\s+Problem and motivation", re.I | re.M),
    "mechanism": re.compile(r"^##\s+Core concepts and mechanisms", re.I | re.M),
    "worked example": re.compile(r"^##\s+Worked example", re.I | re.M),
    "trade-offs": re.compile(r"^##\s+Trade-offs and failure modes", re.I | re.M),
    "references": re.compile(r"^##\s+(?:\d+\.\s*)?References\b", re.I | re.M),
}


def parse_front_matter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    try:
        fields = yaml.safe_load(text[4:end])
        return fields if isinstance(fields, dict) else {}
    except yaml.YAMLError:
        return {}


def local_path(value):
    path = ROOT / value
    if Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError(f'Expected repository-relative artifact path: {value}')
    path.resolve().relative_to(ROOT.resolve())
    return path


def validate_pair(lesson, assessment):
    errors = []
    if lesson.resolve() == assessment.resolve():
        return ['Lesson and assessment must have distinct paths']
    try:
        text = lesson.read_text(encoding='utf-8')
        quiz = assessment.read_text(encoding='utf-8')
    except OSError as exc:
        return [str(exc)]
    front, companion = parse_front_matter(text), parse_front_matter(quiz)
    if front.get('status') != 'draft' or companion.get('status') != 'draft':
        errors.append('Lesson and assessment must remain draft')
    try:
        if local_path(companion.get('lesson', '')).resolve() != lesson.resolve():
            errors.append('Assessment must reference its companion lesson')
    except (ValueError, TypeError):
        errors.append('Invalid companion lesson reference')
    if re.search(r'^#{2,3}\s+(?:Practical exercise|Exercise|Knowledge checks?|Answer key|Answer guide|Rubric)\b', text, re.I | re.M):
        errors.append(f'{lesson}: assessment content belongs in the companion artifact')
    for heading in ('Practical exercise', 'Knowledge checks', 'Answer key / rubric'):
        if not re.search(r'^##\s+'+re.escape(heading)+r'\s*$', quiz, re.I | re.M):
            errors.append(f'{assessment}: missing {heading}')
    matches = list(re.finditer(r'^###\s+(Q\d+)\b[^\n]*', quiz, re.M))
    ids = [m[1] for m in matches]
    if not 5 <= len(ids) <= 8 or len(set(ids)) != len(ids):
        errors.append('Assessment needs 5–8 uniquely identified knowledge checks')
    for i, match in enumerate(matches):
        block = quiz[match.end():matches[i+1].start() if i+1 < len(matches) else len(quiz)]
        if not re.search(r'\bAnswer\s*:', block) or not re.search(r'\bExplanation\s*:', block):
            errors.append(f'{match[1]} needs Answer: and Explanation:')
    outcomes = front.get('outcomes')
    mapping = companion.get('outcome_map')
    headings = {h.strip().lower() for h in re.findall(r'^##\s+(.+)$', text, re.M)}
    if not isinstance(front.get('prerequisites'), list):
        errors.append('Lesson prerequisites must be a list')
    if not isinstance(outcomes, list) or not outcomes or not all(isinstance(x, str) and x for x in outcomes):
        errors.append('Lesson outcomes must be a nonempty list of IDs')
    elif len(set(outcomes)) != len(outcomes):
        errors.append('Outcome IDs must be unique')
    elif not isinstance(mapping, dict) or set(mapping) != set(outcomes):
        errors.append('Assessment outcome_map must cover every lesson outcome exactly')
    else:
        for outcome, entry in mapping.items():
            if not isinstance(entry, dict):
                errors.append(f'Invalid mapping for {outcome}')
                continue
            section, items = entry.get('taught_in'), entry.get('items')
            if not isinstance(section, str) or section.lower() not in headings:
                errors.append(f'{outcome} needs an existing teaching section')
            if not isinstance(items, list) or not items or any(not isinstance(x,str) or x not in set(ids)|{'EX-1'} for x in items):
                errors.append(f'{outcome} needs existing assessment items')
    return errors


def validate_plan(plan, matrix):
    errors = []
    try:
        text = plan.read_text(encoding='utf-8')
        with matrix.open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.DictReader(handle))
        if not rows or not re.search(r'^##\s+', text, re.M):
            errors.append('Plan needs outlines and a nonempty coverage matrix')
        for row in rows:
            if any(not row.get(k) for k in ('topic','locator','disposition')):
                errors.append('Coverage rows need topic, pinned source locator and disposition')
            if row.get('disposition') in ('mapped','merged'):
                if not row.get('lesson') or not row.get('outline') or row['lesson'] not in text or row['outline'] not in text:
                    errors.append('Mapped topics must identify an existing lesson and outline')
            elif row.get('disposition') not in ('optional','deferred','outside-scope') or not row.get('rationale'):
                errors.append('Excluded topics need a recognized disposition and rationale')
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['repo','workflow','curriculum','lesson'], default='repo')
    for name in ('lesson','assessment','plan','matrix'):
        parser.add_argument('--'+name, help='Repository-relative artifact path')
    args = parser.parse_args(argv)
    errors: list[str] = []
    lesson_ids: list[str] = []

    lesson_files = sorted((ROOT/'modules').glob('*/lessons/*.md')) if args.scope == 'repo' else []
    pairs = {}
    try:
        if args.scope == 'lesson':
            if not args.lesson or not args.assessment:
                parser.error('lesson scope requires --lesson and --assessment')
            lesson_files = [local_path(args.lesson)]
            pairs[lesson_files[0]] = local_path(args.assessment)
        elif args.scope == 'curriculum':
            if not args.plan or not args.matrix:
                parser.error('curriculum scope requires --plan and --matrix (CSV)')
            errors.extend(validate_plan(local_path(args.plan), local_path(args.matrix)))
        if args.scope == 'repo':
            for manifest in (ROOT/'modules').glob('*/content-manifest.json'):
                value = json.loads(manifest.read_text(encoding='utf-8'))
                if value.get('status') != 'draft' or not isinstance(value.get('packages'),list):
                    errors.append(f'{manifest}: expected a draft packages manifest')
                    continue
                for item in value['packages']:
                    lesson = local_path(item['lesson'])
                    pairs[lesson] = local_path(item['assessment'])
                    if lesson not in lesson_files:
                        lesson_files.append(lesson)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))

    for path in lesson_files:
        if not path.is_file():
            errors.append(f'Missing selected lesson: {path}')
            continue
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
        if isinstance(lesson_id, str) and lesson_id:
            lesson_ids.append(lesson_id)
            if not path.name.startswith(lesson_id):
                errors.append(f"{rel}: filename should begin with lesson ID {lesson_id}")
        else:
            errors.append(f'{rel}: lesson id must be a nonempty string')

        status = str(front.get("status", "")).lower()
        if status != "draft":
            errors.append(f"{rel}: invalid status '{status}'; generated content must not be approved/published")

        for section, pattern in REQUIRED_SECTIONS.items():
            if not pattern.search(text):
                errors.append(f"{rel}: missing required section '{section}'")
        try:
            assessment = pairs.get(path) or local_path(front['assessment'])
            pairs[path] = assessment
            errors.extend(validate_pair(path, assessment))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{rel}: missing/invalid assessment path: {exc}')

        urls = set(re.findall(r"https?://[^\s)\]>]+", text))
        if len(urls) < 2:
            errors.append(f"{rel}: expected at least 2 explicit source URLs; found {len(urls)}")

    if len(lesson_ids) != len(set(lesson_ids)):
        errors.append("Duplicate lesson IDs found in lesson front matter")

    source_count = 0
    for registry in sorted((ROOT/'modules').glob('*/sources/source-registry.csv')):
        try:
            with registry.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                required = {"id", "title", "url", "publisher_or_author", "checked_date"}
                missing = required - set(reader.fieldnames or [])
                if missing:
                    errors.append(f"Source registry missing columns: {', '.join(sorted(missing))}")
                rows = list(reader)
                source_count += len(rows)
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

    # The retired pilot-manifest.json is historical planning data. Active
    # manifests use content-manifest.json and explicit package artifact paths.


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
            for field in ("name", "description", "developer_instructions", "model", "model_reasoning_effort"):
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
            if not codex_config.get('agents', {}).get('default_subagent_model'):
                errors.append('Missing default subagent model')
        except (OSError, tomllib.TOMLDecodeError) as exc:
            errors.append(f".codex/config.toml: invalid TOML: {exc}")

    checked_links = 0
    selected = set(lesson_files) | set(pairs.values())
    if args.scope == 'curriculum' and args.plan:
        try:
            selected.add(local_path(args.plan))
        except (ValueError, TypeError):
            pass
    for path in ROOT.rglob("*.md"):
        if args.scope != 'repo' and path not in selected and path.relative_to(ROOT).parts[0] == 'modules':
            continue
        if path not in selected and any(part in path.relative_to(ROOT).parts for part in ('.git','.tmp','inputs','runs','task-runs')):
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
    print(f"Scope: {args.scope}; structural checks only; not factual, legal, or pedagogical approval.")

    if errors:
        print(f"\nFAILED: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nPASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
