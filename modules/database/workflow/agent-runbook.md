# AI Content Workflow — Agent Runbook

## Goal

Produce draft lessons from an approved curriculum and source registry, then create a reviewable Git change. The system must never self-publish a lesson to learners.

## Important operating model

ChatGPT Plus is the workspace/model subscription, not an unlimited autonomous workflow engine. Codex/Work can execute bounded tasks, but a durable unattended pipeline with scheduling, retries, state, API billing and automatic GitHub PR creation generally requires an external orchestrator and API access. For the first pilot, use a human-triggered Codex task with a fixed input/output contract. Do not claim background execution or unlimited usage.

## Inputs

- `curriculum/database-module.md`
- `sources/source-registry.csv`
- `governance/content-guidelines.md`
- `governance/attribution-policy.md`
- `governance/qa-checklist.md`
- lesson template / existing approved sample

## Task loop

For each lesson ID:

1. **Plan:** list lesson outcomes and prerequisite dependencies.
2. **Retrieve:** read the relevant Primer section and official source pages. Prefer exact official documentation sections rather than broad search snippets.
3. **Research decision:**
   - Standard lookup for bounded factual questions.
   - Document analysis when the exact source is already known.
   - Deep Research only when the problem requires synthesis across many independent sources or unresolved disagreements.
4. **Draft:** write a new lesson; do not paraphrase the source paragraph-by-paragraph.
5. **Diagram:** generate Mermaid source and explain each component/arrow.
6. **Assess:** create questions and a worked solution/rubric mapped to outcomes.
7. **Self-review:** run technical, citation, pedagogical and license checks.
8. **Claim audit:** produce a table of high-impact claims and their direct supporting references. Any unsupported claim becomes `needs-human-verification`.
9. **Publish draft:** write lesson to a branch or local working tree and report changed files. Do not merge/publish automatically.

## Author prompt

You are a technical curriculum author for backend engineers learning system design. Create exactly one lesson using the approved curriculum and lesson template. Use source material for factual grounding, not as text to translate or reproduce. Prefer official documentation and standards. Separate general principles from engine-specific behavior. Include assumptions, trade-offs, failure modes, one worked example, 5–8 assessment questions and detailed answers. Cite direct sources next to version-sensitive or important technical claims. Do not invent URLs, versions, measurements or guarantees. Add attribution and change notes if adapted expression is used. Set `status: draft` in front matter.

## Reviewer prompt

Act as an independent technical and pedagogical reviewer. Do not rewrite the lesson first. Produce:
1. Critical factual errors, each with exact claim, why it is wrong/uncertain, and authoritative source.
2. Unsupported claims or weak citations.
3. Vendor/version conflations.
4. Missing assumptions or trade-offs.
5. Pedagogical gaps and learning outcomes not assessed.
6. License/attribution issues.
7. Verdict: `block`, `revise`, or `ready-for-human-review`.

Do not approve a claim merely because it sounds plausible. If source access is unavailable, mark it unverified.

## Output contract

- `lessons/DB-xx-*.md`
- `qa/DB-xx-review.md`
- update source registry with exact source URLs, product/version, section, date checked, and relevant claim.
- concise run report: generated files, claims needing human verification, unresolved questions, tests/checks run.

## Retry policy

- Retry only technical/tool failures, not disagreement with a reviewer.
- Maximum two automated revision cycles per lesson.
- If the same critical issue remains after two cycles, stop and request human judgment.
- Keep previous drafts in Git history.

## Publication gate

Only a human can change status from `ready-for-human-review` to `approved` or `published` after completing the QA checklist. Legal review is required for any uncertain third-party asset or substantial adaptation.
