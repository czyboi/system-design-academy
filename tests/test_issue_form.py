"""Structural checks for GitHub issue forms used by this repository."""
import unittest
from pathlib import Path
import yaml


class AcademyIssueFormTests(unittest.TestCase):
    def test_task_form_uses_description_and_requires_owner(self):
        path = Path(__file__).resolve().parents[1] / ".github/ISSUE_TEMPLATE/academy-task.yml"
        form = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIn("description", form)
        self.assertNotIn("about", form)
        fields = {item.get("id"): item for item in form["body"]}
        self.assertTrue(fields["owner"]["validations"]["required"])
        for key in ("spec_file", "state_file", "working_branch"):
            self.assertTrue(fields[key]["validations"]["required"])
