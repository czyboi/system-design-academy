"""Structural checks for GitHub issue forms and provider agent adapters."""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class AcademyIssueFormTests(unittest.TestCase):
    def test_task_form_uses_description_and_requires_owner(self):
        path = ROOT / ".github/ISSUE_TEMPLATE/academy-task.yml"
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIn("description", form)
        self.assertNotIn("about", form)
        fields = {item.get("id"): item for item in form["body"]}
        self.assertTrue(fields["owner"]["validations"]["required"])
        for key in ("spec_file", "state_file", "working_branch"):
            self.assertTrue(fields[key]["validations"]["required"])


class ClaudeAgentAdapterTests(unittest.TestCase):
    def test_project_agents_reference_shared_skills_without_copying_them(self):
        expected = {
            "source-researcher.md": ".agents/skills/source-research/SKILL.md",
            "curriculum-designer.md": ".agents/skills/curriculum-design/SKILL.md",
            "lesson-author.md": ".agents/skills/lesson-authoring/SKILL.md",
            "technical-reviewer.md": ".agents/skills/technical-review/SKILL.md",
            "pedagogy-reviewer.md": ".agents/skills/pedagogical-review/SKILL.md",
            "provenance-reviewer.md": ".agents/skills/provenance-review/SKILL.md",
        }
        folder = ROOT / ".claude/agents"
        self.assertTrue(folder.is_dir())
        for filename, skill_path in expected.items():
            path = folder / filename
            self.assertTrue(path.is_file(), filename)
            raw = path.read_text(encoding="utf-8")
            self.assertTrue(raw.startswith("---\n"), filename)
            _, frontmatter, body = raw.split("---", 2)
            metadata = yaml.safe_load(frontmatter)
            self.assertTrue(metadata.get("name"), filename)
            self.assertTrue(metadata.get("description"), filename)
            self.assertIn(skill_path, body)
            self.assertTrue((ROOT / skill_path).is_file(), skill_path)
            self.assertLess(len(body), 1500, "Agent adapters should not duplicate full skill instructions")


if __name__ == "__main__":
    unittest.main()
