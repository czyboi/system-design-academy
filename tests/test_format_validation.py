"""Format-only tests; pinned milestone regression is run by GitHub CI."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_format import PARSER, split_front_matter, validate_document

MS01 = "e823c8d72e59f1691ce7bfc65f37c209066eca99"
MS02 = "ec753d7bcfd69ad68e5fff260aeb088059e42540"
ROOT = Path(__file__).resolve().parents[1]


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

    def test_legacy_integrated_package(self):
        text = "---\nid: M04-EX1\nstatus: draft\n---\n# Brief\n## Exercise\nExplain an architecture.\n"
        self.assertEqual(validate_document(text, self.root/'modules/m04/integrated/brief.md', root=self.root), [])


@unittest.skipUnless(os.getenv("SDA_TEST_PINNED_CONTENT") == "1", "pinned milestone commits are fetched by CI")
class PinnedMilestoneRegression(unittest.TestCase):
    """Read Git objects directly, never copy or edit hash-bound lesson files."""

    def test_all_13_review_selected_lessons_and_assessments(self):
        for commit, module, lesson_count, revised in (
            (MS01, "m00", 2, {}),
            (MS01, "m01", 4, {"M01-L02"}),
            (MS02, "m02", 4, {"M02-L02"}),
            (MS02, "m03", 3, {}),
        ):
            for number in range(1, lesson_count + 1):
                lesson_id = f"{module.upper()}-L{number:02d}"
                suffix = f"revision-1/{lesson_id}.md" if lesson_id in revised else f"{lesson_id}.md"
                teaching = f"modules/{module}/lessons/{suffix}"
                assessment = f"modules/{module}/assessments/{suffix}"
                for kind, path in (("lesson", teaching), ("assessment", assessment)):
                    with self.subTest(commit=commit, path=path):
                        proc = subprocess.run(
                            ["git", "show", f"{commit}:{path}"], cwd=ROOT,
                            check=True, capture_output=True, text=True, encoding="utf-8",
                        )
                        problems = validate_document(proc.stdout, ROOT / path, kind=kind, check_local_links=False)
                        self.assertEqual(problems, [], "\n".join(problems))
                        metadata, _, _ = split_front_matter(proc.stdout)
                        if kind == "lesson":
                            self.assertEqual(metadata["id"], lesson_id)
                            self.assertEqual(metadata["assessment"], assessment)
                        else:
                            self.assertEqual(metadata["lesson"], teaching)

    def test_four_module_integrated_packages(self):
        for commit, module, summary in (
            (MS01, "m00", "decision-summary.md"),
            (MS01, "m01", "decision-summary-r1.md"),
            (MS02, "m02", "decision-summary.md"),
            (MS02, "m03", "decision-summary-r1.md"),
        ):
            for name in ("brief.md", "solution-rubric.md", summary):
                path = f"modules/{module}/integrated/{name}"
                with self.subTest(path=path):
                    proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT,
                                          check=True, capture_output=True, text=True, encoding="utf-8")
                    problems = validate_document(proc.stdout, ROOT / path, kind="integrated", check_local_links=False)
                    self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
