# Authoring format validator — Step 2

This is the deterministic, **read-only** check for [Authoring Format Contract v1](authoring-format-contract-v1.md). A passing format check does **not** prove technical truth, teaching quality, human approval, complete Mermaid syntax, or actual website rendering.

## How to run

- Validate all currently authored files: `python scripts/validate_format.py`
- Validate a single file: `python scripts/validate_format.py --path modules/m04/lessons/M04-L01.md`
- Run ordinary tests: `python -m unittest discover -s tests -v`
- GitHub Actions **Python regression tests** runs synthetic unit tests automatically on PRs and pushes to `main`; it does **not** run content validation on the real lessons.
- GitHub Actions **Content validation** is `workflow_dispatch` only. Its Markdown and structural checks run only when explicitly triggered.

For a module containing `content-manifest.json`, repository-wide validators check the explicitly selected lesson/assessment revision paths. An inactive older revision is not silently treated as the active lesson. Nested revisions without a manifest are an error for structural validation.

## Checked

- YAML front matter mappings and duplicate keys; current lesson/assessment/integrated metadata structures without forcing new SEO/schema fields.
- CommonMark + GFM tables/strikethrough via `markdown-it-py`.
- Unclosed fenced code blocks, raw HTML and MDX-style tags, unsafe link schemes, traversal, missing local assets, image alt text, and unsafe Mermaid directives.
- Conservative Mermaid declaration and empty-diagram checks. No diagram quota; format cannot override educational quality.
- Standalone `$$` math markers are flagged as unsupported until renderer support is added; fenced code remains literal.
- Plain and bold answer/explanation labels are both permitted. Existing `scripts/validate_content.py` continues checking lesson/assessment linkage, outcomes, question count and instructional structure.

## Limits and operational caveats

- **Mermaid validation is smoke-only**, not full grammar or browser rendering. Recognized declarations do not guarantee valid diagrams. Step 5 owns renderer-level tests and visual QA.
- Markdown validation does not sanitize HTML for the future website. The website must enforce its own safe rendering.
- Synthetic fixtures test syntax and artifact selection without fetching old Git commits or changing existing reviewed files.
- The active manifest and current checked-out artifacts determine what repository-wide validators inspect; historical commit-pinned snapshot regression tests are deliberately removed.
- Errors are diagnostic. No automatic AI retries, no extra agents, and no additional LLM calls.
- The validator does not change teaching content, evidence, historical reviews, human approval or publication status.

Future website content selection and publication approval are separate steps; no task-state hashes are involved.
