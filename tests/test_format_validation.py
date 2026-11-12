"""Format-only regression tests for current authoring contracts."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_format import PARSER, discover, validate_document

def draft(body: str, **overrides: str) -> str:
    fields = {
        "id": "M04-L01", "title": "Test", "status": "draft",
        "level": "intermediate", "prerequisites": "[]",
        "outcomes": "[M04-L01-LO1]",
        "assessment": "modules/m04/assessments/M04-L01.md",
        "source_review_date": "2026-11-12",
    }
    fields.update(overrides)
    front = "\n".join(f"{k}: {v}" for k, v in fields.items())
    return f"---\n{front}\n---\n# Test\n\n{body}\n"


class FormatValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "modules/m04/lessons/M04-L01.md"
        self.source.parent.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def check(self, body: str, **front: str) -> list[str]:
        return validate_document(draft(body, **front), self.source, root=self.root)

    def test_gfm_tables_code_inline_and_plain_diagrams(self):
        body = "| Col | Value |\n| --- | --- |\n| A | B |\n\n`code`\n\n```text\nA -> B\n```"
        self.assertEqual(self.check(body), [])
        self.assertIn("table_open", [t.type for t in PARSER.parse(body)])

    def test_fences_preserve_html_and_urls_as_literally_taught_code(self):
        self.assertEqual(self.check('```html\n<script>x</script>\n```\n\n`javascript:alert(1)`'), [])

    def test_unclosed_fence_rejected(self):
        self.assertTrue(any("unclosed fenced" in x for x in self.check("```java\nclass X {}")))

    def test_nested_fenced_code_remains_valid(self):
        body = "- nested example\n\n    ```java\n    class X {}\n    ```\n"
        self.assertEqual(self.check(body), [])

    def test_raw_html_and_mdx_rejected(self):
        self.assertTrue(any("raw HTML" in x for x in self.check("<script>alert(1)</script>")))
        self.assertTrue(any("raw HTML" in x for x in self.check("<CustomWidget />")))

    def test_unsafe_url_rejected(self):
        self.assertTrue(any("unsafe link" in x for x in self.check("[click](javascript:alert(1))")))

    def test_missing_local_asset_and_traversal_rejected(self):
        self.assertTrue(any("missing local asset" in x for x in self.check("![diagram](../assets/missing.svg)")))
        self.assertTrue(any("escapes repository" in x for x in self.check("![diagram](../../../../etc/passwd)")))

    def test_empty_image_alt_rejected(self):
        self.assertTrue(any("alt text" in x for x in self.check("![](https://example.com/picture.svg)")))

    def test_mermaid_smoke_and_unsafe_directives(self):
        valid = "```mermaid\nflowchart LR\nA --> B\n```"
        self.assertEqual(self.check(valid), [])
        self.assertTrue(any("empty Mermaid" in x for x in self.check("```mermaid\n\n```")))
        self.assertTrue(any("unrecognized Mermaid" in x for x in self.check("```mermaid\nnot-a-diagram\n```")))
        self.assertTrue(any("runtime directives" in x for x in self.check("```mermaid\nflowchart LR\n%%{init: {securityLevel: 'loose'}}%%\n```")))

    def test_missing_and_duplicate_yaml_fields_rejected(self):
        self.assertTrue(any("missing metadata" in x for x in self.check("Body", title="")))
        body = draft("Body").replace("title: Test", "title: Test\ntitle: Duplicate")
        self.assertTrue(any("duplicate YAML key" in x for x in validate_document(body, self.source, root=self.root)))

    def test_draft_and_optional_metadata_rules(self):
        self.assertEqual(self.check("Body"), [])
        self.assertTrue(any("status: draft" in x for x in self.check("Body", status="published")))
        self.assertTrue(any("prerequisites" in x for x in self.check("Body", prerequisites="wrong")))

    def test_assessment_plain_and_emphasized_labels(self):
        assessment = """---
id: M04-L01-assessment
status: draft
lesson: modules/m04/lessons/M04-L01.md
outcome_map:
  M04-L01-LO1:
    taught_in: Worked example
    items: [Q1, EX-1]
---
# Assessment
## Knowledge checks
### Q1
**Answer:** Yes.
**Explanation:** Because.
### Q2
Answer: Yes.
Explanation: Because.
"""
        self.assertEqual(validate_document(assessment, self.root/'modules/m04/assessments/M04-L01.md', root=self.root), [])

    def test_canonical_discovery_rejects_revision_folders_and_manifest(self):
        module = self.root / "modules/m04"
        lesson = module / "lessons/M04-L01.md"
        companion = module / "assessments/M04-L01.md"
        for path in (lesson, companion):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n", encoding="utf-8")
        self.assertEqual(discover(self.root), [companion, lesson])
        nested = module / "lessons/revision-1/M04-L01.md"
        nested.parent.mkdir()
        nested.write_text("old revision\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "nested lesson/assessment revisions"):
            discover(self.root)
        nested.unlink()
        (module / "content-manifest.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "content-manifest.json is obsolete"):
            discover(self.root)


    def test_free_form_rich_lesson_does_not_need_section_conversion(self):
        body = ('## Why the cache fails\n\nA causal explanation.\n\n'
                '| Option | Failure mode |\n| --- | --- |\n| A | Eviction |\n\n'
                '```mermaid\nflowchart LR\nA --> B\n```\n\n'
                '## Context-specific heading\n\nThe important trade-off.\n')
        source = draft(body)
        self.assertEqual(validate_document(source, self.source, root=self.root), [])
        self.assertIn(body, source)

    def test_unsafe_literal_link_in_fenced_example_is_not_a_real_link(self):
        fence = chr(96) * 3
        self.assertEqual(self.check(f'{fence}md\n[example](javascript:alert(1))\n{fence}'), [])

    def test_metadata_types_and_iso_date_are_enforced(self):
        self.assertTrue(any('level must be a nonempty string' in x
                            for x in self.check('Body', level='[senior]')))
        self.assertTrue(any('ISO date' in x
                            for x in self.check('Body', source_review_date='false')))
        self.assertEqual(self.check('Body', source_review_date='2026-11-12'), [])
        assessment = """---
id: 42
status: draft
lesson: modules/m04/lessons/M04-L01.md
outcome_map:
  M04-L01-LO1:
    taught_in: Mechanism walkthrough
    items: [EX-1, Q1]
---
# Assessment
"""
        self.assertTrue(any('id must be a nonempty string' in x for x in
                            validate_document(assessment, self.root/'modules/m04/assessments/M04-L01.md', root=self.root)))

    def test_legacy_integrated_package(self):
        text = "---\nid: M04-EX1\nstatus: draft\n---\n# Brief\n## Exercise\nExplain an architecture.\n"
        self.assertEqual(validate_document(text, self.root/'modules/m04/integrated/brief.md', root=self.root), [])


if __name__ == "__main__":
    unittest.main()
