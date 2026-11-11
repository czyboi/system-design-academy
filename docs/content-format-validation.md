# Authoring format validator — Step 2

This is the deterministic, **read-only** check for the [candidate Authoring Format Contract v1](authoring-format-contract-v1.md). A passing format check does **not** prove technical truth, teaching quality, human approval, complete Mermaid syntax, or actual website rendering.

## How to run

- Validate all currently authored files: `python scripts/validate_format.py`
- Validate a single file: `python scripts/validate_format.py --path modules/m04/lessons/M04-L01.md`
- Run ordinary tests: `python -m unittest discover -s tests -v`
- CI additionally sets `SDA_TEST_PINNED_CONTENT=1` after fetching pinned MS01/MS02 commits, checking 13 selected lesson/assessment pairs and 12 integrated teaching artifacts **without copying or rewriting them**.

Zero lesson files in the current branch is a valid input; the historical CI regression independently tests past outputs.

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
- Pinned regression checks Markdown representation but disables local link-existence checks for historical Git objects (they are not in the working tree). It checks links in current checked-out artifacts.
- CI regression needs pinned commits to stay fetchable from `codex/SDA-MS01` and `codex/SDA-MS02`. When branches are retired, plan a stable immutable fixture source rather than skipping these tests.
- Errors are diagnostic. No automatic AI retries, no extra agents, and no additional LLM calls.
- No teaching content, source evidence, old skills, historical reviews, existing validator, website loader, human approval or publication gate changed here.

See Step 3 for revision/hash selection and Step 4 for publication.
