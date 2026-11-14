#!/usr/bin/env python3
"""Open (or reuse) exactly one Draft PR at the end of a user-requested generation batch.

This is a parent-orchestrator finalizer, NOT part of per-lesson draft handoff.
The batch owns a dedicated codex/gen-<batch-id> branch created from main before
authoring. No PR is created until all requested tasks have completed and the
last applicable review handoff has been pushed. Never merges or publishes.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

if __package__:
    from . import draft_handoff
else:
    import draft_handoff

BATCH_ID = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?")
LESSON = re.compile(r"modules/(m\d{2})/lessons/(M\d{2}-L\d{2})\.md")
INTEGRATION = re.compile(r"modules/(m\d{2})/integrated/[^/]+")


class GenerationPrError(Exception):
    pass


def command(*args: str) -> str:
    try:
        result = subprocess.run(args, cwd=draft_handoff.ROOT, text=True, capture_output=True)
    except FileNotFoundError as exc:
        raise GenerationPrError(f"Required command is unavailable: {args[0]}") from exc
    if result.returncode:
        raise GenerationPrError(
            f"{' '.join(args[:3])} failed: {result.stderr.strip() or result.stdout.strip()}"
        )
    return result.stdout.strip()


def git(*args: str) -> str:
    return command("git", *args)


def gh(*args: str) -> str:
    return command("gh", *args)


def permitted_batch_paths(task_ids: list[str]) -> set[str]:
    allowed: set[str] = set()
    for task_id in task_ids:
        # task_paths insists every requested research/author output is complete.
        outputs = draft_handoff.task_paths(task_id)
        allowed.update(outputs)
        for path in outputs:
            lesson = LESSON.fullmatch(path)
            if lesson:
                module, lesson_id = lesson.groups()
                prefix = f"modules/{module}/reviews/automatic/lessons/{lesson_id}"
                allowed.update(
                    f"{prefix}/{file}" for file in ("technical.md", "pedagogy.md", "cycle.json")
                )
            integration = INTEGRATION.fullmatch(path)
            if integration:
                module = integration.group(1)
                prefix = f"modules/{module}/reviews/automatic"
                allowed.update(
                    f"{prefix}/{file}" for file in ("technical.md", "pedagogy.md", "cycle.json")
                )
    # Only shared cross-module learning evidence is allowed in addition to task artifacts.
    allowed.add(".academy/knowledge/lessons-learned.json")
    return allowed


def validate_batch(batch_id: str, task_ids: list[str], remote: str, base: str) -> str:
    if not BATCH_ID.fullmatch(batch_id):
        raise GenerationPrError("Batch ID must be a stable lowercase slug (max 60 characters)")
    if len(set(task_ids)) != len(task_ids):
        raise GenerationPrError("Duplicate task IDs in the same generation batch")
    expected_branch = f"codex/gen-{batch_id}"
    branch = git("branch", "--show-current")
    if branch != expected_branch:
        raise GenerationPrError(
            f"Expected dedicated batch branch {expected_branch}, got {branch!r}; "
            "do not reuse a prior batch or milestone branch"
        )
    if git("status", "--porcelain"):
        raise GenerationPrError("Uncommitted files remain; finish the final draft handoff first")
    local_head = git("rev-parse", "HEAD")
    pushed_head = git("rev-parse", f"refs/remotes/{remote}/{branch}")
    if local_head != pushed_head:
        raise GenerationPrError("Batch HEAD has not been pushed to its remote branch")
    git("merge-base", "--is-ancestor", f"refs/remotes/{remote}/{base}", "HEAD")
    allowed = permitted_batch_paths(task_ids)
    changed = set(filter(None, git("diff", "--name-only", "-z",
                                   f"{remote}/{base}...HEAD").split("\x00")))
    if not changed:
        raise GenerationPrError("No generated changes relative to the target branch")
    unexpected = sorted(changed - allowed)
    if unexpected:
        raise GenerationPrError(
            "Branch contains changes outside the requested batch: " + ", ".join(unexpected)
        )
    return branch


def matching_pr(repo: str, branch: str, base: str) -> dict | None:
    raw = gh("pr", "list", "--repo", repo, "--state", "all",
             "--head", branch, "--limit", "100",
             "--json", "number,url,state,headRefName,baseRefName")
    items = json.loads(raw)
    candidates = [pr for pr in items if pr.get("headRefName") == branch]
    mismatched = [pr for pr in candidates if pr.get("baseRefName") != base]
    if mismatched:
        raise GenerationPrError(
            f"Existing PR for {branch} targets a different base; do not create another PR"
        )
    if len(candidates) > 1:
        raise GenerationPrError(f"Multiple PRs already reference {branch}; resolve manually")
    return candidates[0] if candidates else None


def finalize(batch_id: str, task_ids: list[str], remote: str = "origin",
             base: str = "main") -> str:
    branch = validate_batch(batch_id, task_ids, remote, base)
    repo = gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner")
    if not repo or "/" not in repo:
        raise GenerationPrError("Could not determine the GitHub repository")
    prior = matching_pr(repo, branch, base)
    if prior:
        if prior["state"] != "OPEN":
            raise GenerationPrError(
                f"Batch already has {prior['state']} PR {prior['url']}; "
                "do not create a duplicate without a new user-requested batch"
            )
        print(f"Reusing Draft/Review PR for this batch: {prior['url']}")
        return prior["url"]

    title = f"Generation batch {batch_id}: " + ", ".join(task_ids)
    title = title[:180]
    body = (
        "## Generation batch\n\n"
        f"Batch ID: \x60{batch_id}\x60\n\n"
        "Requested task IDs (this batch only):\n"
        + "".join(f"- \x60{task_id}\x60\n" for task_id in task_ids)
        + "\n## Review and approval\n\n"
        "Generated outputs and applicable automatic QA have been handed off. "
        "This Draft PR is the user review surface for this one generation request, "
        "not the entire milestone. Any unresolved review findings remain visible in "
        "their reports; creating this PR does not certify QA success.\n\n"
        "- [ ] Resolve remaining content/reviewer findings, if any\n"
        "- [ ] Check CI and review the generated teaching/assessment artifacts\n"
        "- [ ] Obtain explicit owner approval before merge or publication\n\n"
        "No automatic merge or publication."
    )
    try:
        created = gh("pr", "create", "--repo", repo, "--base", base, "--head", branch,
                     "--draft", "--title", title, "--body", body)
    except GenerationPrError:
        # A second caller may have created the same PR between list and create.
        existing = matching_pr(repo, branch, base)
        if not existing or existing["state"] != "OPEN":
            raise
        print(f"Reusing PR created concurrently: {existing['url']}")
        return existing["url"]
    url = created.strip()
    if not url.startswith("https://github.com/"):
        raise GenerationPrError("GitHub did not return a valid PR URL")
    print(f"Created Draft PR for batch {batch_id}: {url}")
    return url


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_id", help="Stable ID reused on retries of THIS generation request")
    parser.add_argument("task_ids", nargs="+", help="Exactly the Task IDs requested for this batch")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base", default="main")
    args = parser.parse_args(argv)
    try:
        finalize(args.batch_id, args.task_ids, remote=args.remote, base=args.base)
    except (GenerationPrError, draft_handoff.HandoffError, ValueError, OSError) as exc:
        print(f"GENERATION PR FAILED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
