# Validate canonical content

**One public command** checks actual teaching/assessment data, when explicitly requested:

```bash
python scripts/validate_content.py --scope repo
# For one lesson pair:
python scripts/validate_content.py --scope lesson --lesson modules/m01/lessons/M01-L02.md --assessment modules/m01/assessments/M01-L02.md
```

The combined command checks canonical paths, YAML metadata and duplicate keys, companion references, outcome-map **field shape**, Markdown safety and local assets. It does **not** count question IDs, infer exercise/rubric completeness from keywords, require particular heading names, or declare learning-outcome coverage from labels. `scripts/validate_format.py` remains a reusable internal module (with a targeted diagnostic CLI), **not another required authoring or validation stage**.

Heading wording, section counts, lesson length and source URL counts are not schema requirements. Source quality, worked examples, depth, failure analysis, legal rights and pedagogy remain the responsibility of the authoring/assessment skills and optional independent review.

GitHub Actions **Python regression tests** runs automatically against isolated fixtures on PRs and pushes to main. **Content validation** is `workflow_dispatch` only, and runs the combined command plus task-state validation when deliberately started. No LLM is used in these deterministic checks.

Format PASS does not establish technical truth, teaching quality, browser/diagram rendering or publication approval. **There is no website renderer yet**: the current check is limited to Markdown parser/safety smoke tests, not real browser rendering. Once the website exists, exercise the actual renderer rather than building a second Markdown interpretation layer. Unsupported technically necessary syntax should be reported, not deleted.
