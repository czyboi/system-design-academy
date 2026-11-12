# Authoring format validation

Deterministic, read-only validation for [Authoring Format Contract v1](authoring-format-contract-v1.md). It **does not** certify factual correctness, teaching quality, legal rights or release approval.

## Usage (on demand)

```bash
python scripts/validate_content.py --scope lesson --lesson modules/m01/lessons/M01-L02.md --assessment modules/m01/assessments/M01-L02.md
python scripts/validate_content.py --scope repo
python scripts/validate_format.py
python scripts/validate_format.py --path modules/m01/lessons/M01-L02.md
```

**Python regression tests** run automatically in GitHub Actions for PRs/pushes to `main` with isolated fixtures. The **Content validation** GitHub Actions workflow is `workflow_dispatch` only; it checks actual source artifacts only when deliberately launched. No AI review or automatic re-generation is triggered.

## Canonical content convention

- One lesson file per ID under `modules/mXX/lessons/` and one companion file under `modules/mXX/assessments/`.
- Git tracks edits. No nested lesson revisions, content selection manifest or automatic preference for the newest file.
- Repository-wide content checks reject nested lesson/assessment revisions, obsolete `content-manifest.json` and unreferenced companion assessments; format discovery also refuses noncanonical revisions.
- The approved syllabus at `curriculum/revision-1/` remains authoritative and is unrelated to lesson file versioning.

## Format checks and limits

- YAML front matter; CommonMark/GFM including code and tables; unsafe links/path traversal, missing image alt, local asset existence, raw HTML/MDX and fenced-code closure.
- Mermaid checks only supported declarations, emptiness and unsafe directives—not full Mermaid grammar or browser fidelity.
- Inline formulas in literal code are preserved; unsupported display math must be addressed by renderer capability, not by deleting the explanation.
- Assessments may use normal or bold `Answer:`/`Explanation:` labels. Structural teaching and outcome mapping are checked separately by `validate_content.py`.
- Actual website rendering, sanitization and diagram layout require a future renderer test; reviewing technical truth, educational depth and source quality remains an independent human-requested activity.

Historical MS01/MS02 snapshot tests were intentionally retired. Current regression tests use synthetic fixtures only; old lesson snapshots are not required by the new workflow.
