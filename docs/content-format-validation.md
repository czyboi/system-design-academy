# Validate canonical content

**One public command** checks actual teaching/assessment data, when explicitly requested:

```bash
python scripts/validate_content.py --scope repo
# For one lesson pair:
python scripts/validate_content.py --scope lesson --lesson modules/m01/lessons/M01-L02.md --assessment modules/m01/assessments/M01-L02.md
```

The combined command checks canonical paths, YAML metadata and duplicate keys, outcome mappings, stable question/exercise IDs, Markdown safety, images/assets and a conservative subset of Mermaid syntax. `scripts/validate_format.py` remains a reusable internal module (with a targeted diagnostic CLI), **not another required authoring or validation stage**.

Heading wording, section counts, lesson length and source URL counts are not schema requirements. Source quality, worked examples, depth, failure analysis, legal rights and pedagogy remain the responsibility of the authoring/assessment skills and optional independent review.

GitHub Actions **Python regression tests** runs automatically against isolated fixtures on PRs and pushes to main. **Content validation** is `workflow_dispatch` only, and runs the combined command plus task-state validation when deliberately started. No LLM is used in these deterministic checks.

Format PASS does not establish technical truth, teaching quality, browser/diagram rendering or publication approval. The website later reads and renders the same Markdown/YAML with ordinary libraries, preserving content instead of converting it to another schema. Unsupported technically necessary syntax should be reported, not deleted.
