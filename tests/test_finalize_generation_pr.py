"""Regression tests for one-PR-per-request finalization."""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from scripts import finalize_generation_pr as gp


class GenerationPrTests(unittest.TestCase):
    def test_allowed_paths_include_only_selected_tasks_and_reviews(self):
        a = {"modules/m04/lessons/M04-L01.md", "modules/m04/assessments/M04-L01.md",
             ".academy/state/tasks/SD-M04-L01.json"}
        b = {"modules/m04/lessons/M04-L02.md", "modules/m04/assessments/M04-L02.md"}
        with patch.object(gp.draft_handoff, "task_paths", side_effect=[a, b]):
            result = gp.permitted_batch_paths(["SD-M04-L01", "SD-M04-L02"])
        self.assertIn("modules/m04/reviews/automatic/lessons/M04-L01/technical.md", result)
        self.assertIn("modules/m04/reviews/automatic/lessons/M04-L02/cycle.json", result)
        self.assertNotIn("modules/m04/lessons/M04-L03.md", result)
        self.assertNotIn("modules/m04/reviews/automatic/technical.md", result)

    def test_rejects_milestone_branch_for_a_lesson_batch(self):
        with patch.object(gp, "git", return_value="codex/drafts-sda-ms03"):
            with self.assertRaisesRegex(gp.GenerationPrError, "dedicated batch branch"):
                gp.validate_batch("b01", ["SD-M04-L01"], "origin", "main")

    def test_rejects_content_from_other_batch(self):
        responses = {
            ("branch", "--show-current"): "codex/gen-b01",
            ("status", "--porcelain"): "",
            ("rev-parse", "HEAD"): "abc",
            ("rev-parse", "refs/remotes/origin/codex/gen-b01"): "abc",
            ("merge-base", "--is-ancestor", "refs/remotes/origin/main", "HEAD"): "",
            ("diff", "--name-only", "-z", "origin/main...HEAD"):
                "modules/m04/lessons/M04-L01.md\x00modules/m04/lessons/M04-L02.md\x00",
        }
        with patch.object(gp, "git", side_effect=lambda *a: responses[a]), \
             patch.object(gp, "permitted_batch_paths",
                          return_value={"modules/m04/lessons/M04-L01.md"}):
            with self.assertRaisesRegex(gp.GenerationPrError, "outside the requested batch"):
                gp.validate_batch("b01", ["SD-M04-L01"], "origin", "main")

    def test_existing_pr_reused_without_create(self):
        prior = {"number": 44, "url": "https://github.com/acme/academy/pull/44",
                 "state": "OPEN", "headRefName": "codex/gen-b01",
                 "baseRefName": "main"}
        with patch.object(gp, "validate_batch", return_value="codex/gen-b01"), \
             patch.object(gp, "gh", side_effect=[
                 "acme/academy", json.dumps([prior])]) as gh:
            url = gp.finalize("b01", ["SD-M04-L01"])
        self.assertEqual(url, prior["url"])
        self.assertEqual(gh.call_count, 2)

    def test_finalizer_creates_one_draft_pr_for_the_exact_batch(self):
        with patch.object(gp, "validate_batch", return_value="codex/gen-b02"), \
             patch.object(gp, "gh", side_effect=[
                 "acme/academy", "[]", "https://github.com/acme/academy/pull/45"]) as gh:
            url = gp.finalize("b02", ["SD-M04-L01", "SD-M04-L02", "SD-M04-L03"])
        self.assertTrue(url.endswith("/45"))
        create_args = gh.call_args.args
        self.assertEqual(create_args[:2], ("pr", "create"))
        self.assertIn("--draft", create_args)
        self.assertIn("SD-M04-L03", create_args[create_args.index("--body") + 1])

    def test_closed_pr_is_not_recreated(self):
        prior = {"number": 44, "url": "https://github.com/acme/academy/pull/44",
                 "state": "CLOSED", "headRefName": "codex/gen-b01",
                 "baseRefName": "main"}
        with patch.object(gp, "validate_batch", return_value="codex/gen-b01"), \
             patch.object(gp, "gh", side_effect=["acme/academy", json.dumps([prior])]) as gh:
            with self.assertRaisesRegex(gp.GenerationPrError, "do not create a duplicate"):
                gp.finalize("b01", ["SD-M04-L01"])
        self.assertEqual(gh.call_count, 2)


if __name__ == "__main__":
    unittest.main()
