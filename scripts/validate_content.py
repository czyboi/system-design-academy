#!/usr/bin/env python3
"""Read-only data-contract checks; not a review of lesson/assessment quality.

Only verify required metadata, canonical artifact links, and parse/render safety.
Do not infer teaching depth, question quality or exercise completeness from prose.
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

# One command for structural and Markdown validation; format metadata lives in validate_format.
if __package__:
    from . import validate_format as format_rules
else:
    import validate_format as format_rules

ROOT = Path(__file__).resolve().parents[1]

def parse_front_matter(text: str) -> dict:
    """Read YAML with the same strict parser used by format validation."""
    try:
        return format_rules.split_front_matter(text)[0]
    except ValueError:
        return {}


def local_path(value):
    path = ROOT / value
    if Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError(f'Expected repository-relative artifact path: {value}')
    path.resolve().relative_to(ROOT.resolve())
    return path


def validate_pair(lesson: Path, assessment: Path) -> list[str]:
    """Check only file representation and stable structured links, never prose quality."""
    if lesson.resolve() == assessment.resolve():
        return ["Lesson and assessment must have distinct paths"]
    try:
        lesson_text = lesson.read_text(encoding="utf-8")
        assessment_text = assessment.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [str(exc)]

    errors = format_rules.validate_document(lesson_text, lesson, root=ROOT, kind="lesson")
    errors += format_rules.validate_document(assessment_text, assessment, root=ROOT, kind="assessment")
    front = parse_front_matter(lesson_text)
    companion = parse_front_matter(assessment_text)

    for source, value, expected, label in (
        (lesson, front.get("assessment"), assessment, "Lesson must reference its companion assessment"),
        (assessment, companion.get("lesson"), lesson, "Assessment must reference its companion lesson"),
    ):
        try:
            if not isinstance(value, str) or not value.strip() or local_path(value).resolve() != expected.resolve():
                errors.append(f"{source}: {label}")
        except (ValueError, TypeError):
            errors.append(f"{source}: invalid companion path; {label.lower()}")

    lesson_id = front.get("id")
    if isinstance(lesson_id, str) and lesson_id.strip():
        if lesson.stem != lesson_id:
            errors.append(f"{lesson}: filename must match lesson ID")
        if companion.get("id") != f"{lesson_id}-assessment":
            errors.append(f"{assessment}: assessment ID must match lesson ID")
    outcomes = front.get("outcomes")
    outcome_map = companion.get("outcome_map")
    if isinstance(outcomes, list) and all(isinstance(item, str) for item in outcomes):
        if len(outcomes) != len(set(outcomes)):
            errors.append(f"{lesson}: outcome IDs must be unique")
        if not isinstance(outcome_map, dict) or set(outcome_map) != set(outcomes):
            errors.append(f"{assessment}: outcome_map must cover every lesson outcome exactly")
        elif any(
            not isinstance(entry, dict)
            or not isinstance(entry.get("taught_in"), str)
            or not entry["taught_in"].strip()
            or not isinstance(entry.get("items"), list)
            or not entry["items"]
            or any(not isinstance(item, str) or not item.strip() for item in entry["items"])
            for entry in outcome_map.values()
        ):
            errors.append(f"{assessment}: every outcome_map entry needs a heading label and item ID strings")
    else:
        errors.append(f"{lesson}: outcomes must be a list of IDs")

    # Whether the referenced headings/items exist, their substance, 5–8 useful
    # questions, a defensible rubric, and coverage are assessed by an independent
    # content review when requested—not by brittle Markdown keyword guessing.
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


def discover_canonical_content() -> tuple[list[Path], list[Path], list[str]]:
    """One lesson and one assessment at stable paths; Git tracks revisions."""
    lessons: list[Path] = []
    assessments: list[Path] = []
    errors: list[str] = []
    for module in sorted((ROOT / "modules").glob("*")):
        if not module.is_dir():
            continue
        if (module / "content-manifest.json").exists():
            errors.append(f"{module.relative_to(ROOT)}: content-manifest.json is obsolete; use one canonical file per lesson")
        for folder, found in (("lessons", lessons), ("assessments", assessments)):
            directory = module / folder
            found.extend(sorted(directory.glob("*.md")))
            for nested in sorted(directory.glob("**/*.md")):
                if nested.parent != directory:
                    errors.append(f"{nested.relative_to(ROOT)}: nested lesson/assessment revisions are unsupported; use Git history")
    return lessons, assessments, errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=['repo','workflow','curriculum','lesson'], default='repo')
    for name in ('lesson','assessment','plan','matrix'):
        parser.add_argument('--'+name, help='Repository-relative artifact path')
    args = parser.parse_args(argv)
    errors: list[str] = []
    lesson_ids: list[str] = []

    lesson_files: list[Path] = []
    assessment_files: list[Path] = []
    pairs: dict[Path, Path] = {}
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
            lesson_files, assessment_files, discovery_errors = discover_canonical_content()
            errors.extend(discovery_errors)
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

        lesson_id = front.get("id", "")
        if isinstance(lesson_id, str) and lesson_id:
            lesson_ids.append(lesson_id)
            if path.stem != lesson_id:
                errors.append(f"{rel}: canonical lesson filename must equal lesson ID {lesson_id}.md")
        else:
            errors.append(f'{rel}: lesson id must be a nonempty string')

        try:
            assessment = pairs.get(path) or local_path(front['assessment'])
            pairs[path] = assessment
            if args.scope == 'repo':
                expected = path.parent.parent / 'assessments' / path.name
                if assessment != expected:
                    errors.append(f"{rel}: expected canonical companion {expected.relative_to(ROOT)}")
            errors.extend(validate_pair(path, assessment))
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{rel}: missing/invalid assessment path: {exc}')

    if len(lesson_ids) != len(set(lesson_ids)):
        errors.append("Duplicate lesson IDs found in lesson front matter")
    if args.scope == 'repo':
        # Integrated packages share the Markdown rules, not the lesson schema.
        try:
            for artifact in format_rules.discover(ROOT):
                if "integrated" in artifact.parts:
                    errors.extend(format_rules.validate_document(
                        artifact.read_text(encoding='utf-8'), artifact, root=ROOT, kind='integrated'
                    ))
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"Cannot validate integrated content: {exc}")
        used = set(pairs.values())
        for assessment in assessment_files:
            if assessment not in used:
                errors.append(f"{assessment.relative_to(ROOT)}: orphan assessment without a companion lesson")

    source_count = 0
    if args.scope == 'repo':
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

    # Validate repo-local Agent Skills.
    skills_root = ROOT / ".agents/skills"
    skill_count = 0
    if args.scope == 'workflow':
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
    if args.scope == 'repo':
        for path in ROOT.rglob("*.md"):
            parts = path.relative_to(ROOT).parts
            if args.scope != 'repo' and path not in selected and parts[0] == 'modules':
                continue
            # Nested obsolete drafts are rejected by canonical discovery; do not treat
            # their Markdown links as part of the active course.
            if (args.scope == 'repo' and len(parts) > 4 and parts[0] == 'modules'
                    and parts[2] in {'lessons', 'assessments'}):
                continue
            if path not in selected and any(part in path.relative_to(ROOT).parts for part in ('.git','.tmp','inputs','runs','task-runs')):
                continue
            # Paired lessons/assessments have already been checked by validate_document.
            if path in selected:
                continue
            try:
                count, issues = format_rules.validate_markdown_links(
                    path.read_text(encoding="utf-8"), path, root=ROOT
                )
                checked_links += count
                errors.extend(issues)
            except (OSError, UnicodeError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: cannot validate Markdown links: {exc}")

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
