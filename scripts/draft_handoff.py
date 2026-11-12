#!/usr/bin/env python3
"""Validate completed Academy draft packages and safely push their Git handoff.

No AI calls, content edits, full test suite, auto-fixes, PRs or merges.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if __package__:
    from . import taskctl, review_cycle, learning_memory
else:
    import taskctl
    import review_cycle
    import learning_memory

ROOT = Path(__file__).resolve().parents[1]
FEATURE_BRANCH = re.compile(r"^(codex|feature|feat)/[A-Za-z0-9._/-]+$")


class HandoffError(Exception):
    pass


def git(*args: str, capture: bool = False) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True,
                            capture_output=True)
    if result.returncode:
        raise HandoffError(f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip() if capture else ""


def task_paths(task_id: str) -> set[str]:
    """Stage only recorded task artifacts, not the rest of the working tree."""
    state = taskctl.load_task(task_id)
    completed = [step for step in state["steps"] if step["status"] == "completed"]
    if not completed or not any(
        ("lessons" in Path(path).parts or "integrated" in Path(path).parts)
        for step in completed for path in step["output_paths"]
    ):
        raise HandoffError(f"{task_id}: no completed lesson/integration draft outputs")
    for step in state["steps"]:
        if step["step_id"] in {"research", "author"} and step["status"] != "completed":
            raise HandoffError(f"{task_id}: {step['step_id']} has not completed")
        if step["status"] == "running" and any(
            taskctl.relpath(path).exists() for path in step["output_paths"]
        ):
            raise HandoffError(f"{task_id}: running step {step['step_id']} has partial output; checkpoint first")

    paths = {
        state["spec_path"],
        f".academy/state/tasks/{task_id}.json",
        f".academy/state/worklog/{task_id}.jsonl",
    }
    for step in completed:
        paths.update(step["output_paths"])
    for path in paths:
        if not taskctl.relpath(path).is_file():
            raise HandoffError(f"{task_id}: missing required handoff file: {path}")
    return paths


def validation_commands(paths: set[str]) -> list[list[str]]:
    lessons = sorted(p for p in paths if re.fullmatch(r"modules/m\d+/lessons/M\d+-L\d+\.md", p))
    assessments = sorted(p for p in paths if re.fullmatch(r"modules/m\d+/assessments/M\d+-L\d+\.md", p))
    if bool(lessons) != bool(assessments) or len(lessons) != len(assessments):
        raise HandoffError("lesson and assessment must both be declared for scoped validation")
    expected = {p.replace("/lessons/", "/assessments/") for p in lessons}
    if set(assessments) != expected:
        raise HandoffError("lesson and assessment canonical paths do not match")
    commands = []
    for lesson in lessons:
        assessment = lesson.replace("/lessons/", "/assessments/")
        commands.append([sys.executable, "scripts/validate_content.py", "--scope", "lesson",
                         "--lesson", lesson, "--assessment", assessment])
    integrated = sorted(p for p in paths if re.fullmatch(
        r"modules/m\d+/integrated/(brief|solution-rubric[^/]*|decision-summary[^/]*)\.md", p
    ))
    for path in integrated:
        commands.append([sys.executable, "scripts/validate_format.py", "--path", path])
    if not commands:
        raise HandoffError("No eligible lesson/assessment or integrated Markdown artifact to validate")
    return commands


def feature_branch(task_id: str) -> str:
    branch = git("branch", "--show-current", capture=True)
    if not branch:
        raise HandoffError("Detached HEAD: check out a branch before draft handoff")
    if FEATURE_BRANCH.fullmatch(branch) and ".." not in branch and "//" not in branch:
        return branch
    prefix = f"codex/drafts-{task_id.lower()}"
    for index in range(1, 100):
        candidate = prefix if index == 1 else f"{prefix}-{index}"
        exists = subprocess.run(["git", "show-ref", "--verify", "--quiet",
                                 f"refs/heads/{candidate}"], cwd=ROOT).returncode == 0
        if not exists:
            git("switch", "-c", candidate)
            return candidate
    raise HandoffError("Could not allocate an unused feature branch")


def required_module_paths(module: str) -> set[str]:
    """Identify the complete module lesson and integration packages from the approved backlog."""
    backlog = json.loads((ROOT / "delivery/backlog.json").read_text(encoding="utf-8"))
    stories = [
        item for item in backlog.get("items", [])
        if item.get("type") == "Story"
        and item.get("parent") == f"SDA-{module.upper()}"
        and item.get("package_kind") in {"lesson", "module-integration"}
    ]
    if not stories or not any(s.get("package_kind") == "module-integration" for s in stories):
        raise HandoffError(f"{module}: no complete lesson/integration Story set in backlog")
    required = set()
    for story in stories:
        outputs = story.get("outputs", {})
        for kind in ("teaching", "assessment"):
            path = outputs.get(kind)
            if not isinstance(path, str) or not path:
                raise HandoffError(f"{story.get('key')}: missing {kind} output in backlog")
            required.add(path)
    return required


def review_report_paths(values: list[str], task_files: set[str]) -> set[str]:
    """Allow paired lesson reviews immediately; module reviews only at module close."""
    if not values:
        return set()
    modules = {
        p.split("/")[1] for p in task_files
        if re.fullmatch(r"modules/m\d+/(?:lessons|assessments|integrated)/[^/]+", p)
    }
    roles: dict[str, set[str]] = {}
    for value in values:
        match = re.fullmatch(
            r"modules/(m\d{2})/reviews/automatic/(?:lessons/(M\d{2}-L\d{2})/)?(technical|pedagogy)\.md",
            value,
        )
        if not match or match.group(1) not in modules:
            raise HandoffError(f"Review report must belong to a selected module: {value}")
        module, lesson, role = match.groups()
        if lesson and lesson[:3].lower() != module:
            raise HandoffError(f"Lesson report module mismatch: {value}")
        if not taskctl.relpath(value).is_file():
            raise HandoffError(f"Missing review report: {value}")
        if not taskctl.relpath(value).read_text(encoding="utf-8").strip():
            raise HandoffError(f"Empty review report: {value}")
        target = lesson or module
        roles.setdefault(target, set()).add(role)
        if lesson:
            needed = {f"modules/{module}/lessons/{lesson}.md",
                      f"modules/{module}/assessments/{lesson}.md"}
        else:
            needed = required_module_paths(module)
        missing = needed - task_files
        if missing:
            scope = "lesson" if lesson else "module"
            raise HandoffError(f"{target}: {scope} review cannot be handed off before its complete draft: {sorted(missing)}")
    for target, present in roles.items():
        if present != {"technical", "pedagogy"}:
            raise HandoffError(f"{target}: both technical and pedagogy reports must be supplied")
        state = review_cycle.load(target)
        if not state or state["status"] == "revising" or not state["review_history"]:
            raise HandoffError(f"{target}: record both reviewer verdicts before handing off reports")
    return set(values) | {
        review_cycle.state_path(target).relative_to(ROOT).as_posix() for target in roles
    }


def deliver(task_ids: list[str], remote: str = "origin",
            review_reports: list[str] | None = None) -> None:
    all_paths: set[str] = set()
    for task_id in task_ids:
        all_paths.update(task_paths(task_id))
    # Persist an in-progress revision counter even during the following draft handoff.
    modules = {p.split("/")[1] for p in all_paths
               if re.fullmatch(r"modules/m\d+/(?:lessons|assessments|integrated)/[^/]+", p)}
    for module in modules:
        if review_cycle.load(module) is not None:
            all_paths.add(f"modules/{module}/reviews/automatic/cycle.json")
    lessons = {
        Path(path).stem for path in all_paths
        if re.fullmatch(r"modules/m\\d{2}/lessons/M\\d{2}-L\\d{2}\\.md", path)
    }
    for lesson in lessons:
        if review_cycle.load(lesson) is not None:
            all_paths.add(review_cycle.state_path(lesson).relative_to(ROOT).as_posix())
    all_paths.update(review_report_paths(review_reports or [], all_paths))
    if review_reports:
        # Persist newly verified cross-module prevention rules together with QA reports.
        learning_memory.read_memory()
        all_paths.add(learning_memory.MEMORY)
    print(f"Lightweight validation for {len(task_ids)} task(s)", flush=True)
    for command in validation_commands(all_paths):
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            raise HandoffError("Validation FAILED; no commit or push. Fix manually, then rerun handoff")

    # Refuse to bundle unrelated staged changes into the automated commit.
    previously_staged = git("diff", "--cached", "--name-only", "-z", capture=True)
    extras = set(filter(None, previously_staged.split("\x00"))) - all_paths
    if extras:
        raise HandoffError("Unrelated staged files; unstage before handoff: " + ", ".join(sorted(extras)))

    branch = feature_branch(task_ids[0])
    git("add", "--", *sorted(all_paths))
    has_changes = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode
    if has_changes not in (0, 1):
        raise HandoffError("Cannot inspect staged Git changes")
    if has_changes == 1:
        git("commit", "-m", "docs(content): draft handoff " + ", ".join(task_ids))
    git("push", "--set-upstream", remote, f"HEAD:refs/heads/{branch}")
    for task_id in task_ids:
        result = subprocess.run([sys.executable, "scripts/taskctl.py", "handoff", task_id], cwd=ROOT)
        if result.returncode:
            raise HandoffError(f"{task_id}: remote push succeeded but handoff check failed; inspect task state")
    print(f"Drafts validated and pushed to {remote}/{branch}. No PR, review or merge performed.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_ids", nargs="+", help="One or more completed Academy draft task IDs")
    parser.add_argument("--remote", default="origin", help="Git remote to push (default: origin)")
    parser.add_argument("--review-report", action="append", default=[],
                        help="Optional lesson/module review report; supply both technical and pedagogy for each target")
    args = parser.parse_args(argv)
    try:
        deliver(list(dict.fromkeys(args.task_ids)), args.remote, args.review_report)
    except (HandoffError, taskctl.TaskError, OSError, ValueError) as exc:
        print(f"HANDOFF FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
