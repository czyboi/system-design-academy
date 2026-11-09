# AI Content Workflow — Agent Runbook

## Goal
Produce draft lessons through coordinated specialist subagents, then create a reviewable Git change. Never self-publish learner-facing content.

## Where instructions live
- Skills: `.agents/skills/`
- Specialist subagents: `.codex/agents/`
- Project-level concurrency: `.codex/config.toml`
- Global guardrails: root `AGENTS.md`
- Role map and handoffs: `docs/agent-architecture.md`

## Inputs
- `curriculum/database-module.md`
- `sources/source-registry.csv`
- `governance/content-guidelines.md`
- `governance/attribution-policy.md`
- `governance/qa-checklist.md`
- `workflow/lesson-template.md`

## Multi-agent workflow

### Phase A — Prepare (parallel, read-only)
1. Parent creates a task manifest with lesson IDs, dependencies, exact output paths, and states.
2. Spawn `source_researcher` with the `source-research` skill. It returns claim/source evidence and unresolved facts.
3. Spawn `curriculum_designer` with the `curriculum-design` skill. It returns prerequisite gaps, outcome mapping, and sequencing.
4. Wait for both. Parent reconciles evidence and owns shared source/curriculum files.

### Phase B — Author (bounded writes)
5. Spawn `lesson_author` with `lesson-authoring` and `assessment-design`. Assign exactly one lesson file (or distinct files) and unique output paths.
6. The author uses approved evidence and creates original prose, Mermaid, examples, exercises, quizzes, answers, and rubrics.
7. Parent checks output and updates shared files. No other agent edits the same paths.

### Phase C — Independent review (parallel, read-only)
8. Spawn `technical_reviewer`, `pedagogy_reviewer`, and `provenance_reviewer` in parallel.
9. Wait for all three. Consolidate findings with severity, location, evidence, and recommended action.
10. Assign corrections to `lesson_author`; maximum two revision cycles.

### Phase D — Validate and hand off
11. Run `python scripts/validate_content.py` and report output.
12. Prepare QA reports, source registry updates, run report, and draft PR.
13. Stop at `ready-for-human-review`; only a human can approve or publish.

## Research tiers
- Standard search: bounded factual lookup.
- Document analysis: read exact official documentation already identified.
- Deep Research: disputed topics or synthesis across many independent sources.

## Parallelism and safety
- Parallelize independent read-only tasks and distinct lesson assignments.
- Never allow multiple workers to write the same lesson, source registry, manifest, or module README.
- Concurrency is capped at four; each subagent consumes additional model/tool usage.
- Stop after two unsuccessful revision cycles or when evidence is insufficient.
- Never invent source URLs, versions, SQL outputs, benchmarks, or legal conclusions.

## Output contract
For each lesson: lesson Markdown (`status: draft`), technical report, pedagogy report, provenance report, claim/source evidence, unresolved issues, and human actions.

Final report: lesson ID, paths, source coverage, three review verdicts, structural validation, unresolved claims, and PR link.
