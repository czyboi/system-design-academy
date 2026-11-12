"""Focused regressions for automatic lightweight draft handoff."""
from __future__ import annotations

from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts import draft_handoff


class DraftHandoffTests(unittest.TestCase):
    def test_validation_is_scoped_to_declared_pairs_and_integrated_pages(self):
        paths = {
            "modules/m00/lessons/M00-L01.md",
            "modules/m00/assessments/M00-L01.md",
            "modules/m00/evidence/M00-L01.md",
            "modules/m00/integrated/brief.md",
            "modules/m00/integrated/evidence.md",
        }
        commands = draft_handoff.validation_commands(paths)
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0][2:], ["--scope", "lesson", "--lesson",
                                             "modules/m00/lessons/M00-L01.md", "--assessment",
                                             "modules/m00/assessments/M00-L01.md"])
        self.assertEqual(commands[1][2:], ["--path", "modules/m00/integrated/brief.md"])

    def test_missing_companion_rejects_handoff(self):
        with self.assertRaisesRegex(draft_handoff.HandoffError, "both be declared"):
            draft_handoff.validation_commands({"modules/m00/lessons/M00-L01.md"})

    def test_default_branch_creates_a_feature_branch(self):
        with patch.object(draft_handoff, "git", side_effect=["main", ""]) as call, \
             patch.object(draft_handoff.subprocess, "run", return_value=SimpleNamespace(returncode=1)):
            branch = draft_handoff.feature_branch("SD-M00-L01")
        self.assertEqual(branch, "codex/drafts-sd-m00-l01")
        self.assertEqual(call.call_args_list[-1].args, ("switch", "-c", branch))

    def test_failed_validation_does_not_commit_or_push(self):
        paths = {"modules/m00/lessons/M00-L01.md", "modules/m00/assessments/M00-L01.md"}
        with patch.object(draft_handoff, "task_paths", return_value=paths), \
             patch.object(draft_handoff.subprocess, "run", return_value=SimpleNamespace(returncode=1)), \
             patch.object(draft_handoff, "git") as git:
            with self.assertRaisesRegex(draft_handoff.HandoffError, "Validation FAILED"):
                draft_handoff.deliver(["SD-M00-L01"])
            git.assert_not_called()

    def test_unrelated_staged_files_cannot_leak_into_commit(self):
        paths = {"modules/m00/lessons/M00-L01.md", "modules/m00/assessments/M00-L01.md"}
        with patch.object(draft_handoff, "task_paths", return_value=paths), \
             patch.object(draft_handoff.subprocess, "run", return_value=SimpleNamespace(returncode=0)), \
             patch.object(draft_handoff, "git", return_value="secrets.txt\x00") as git:
            with self.assertRaisesRegex(draft_handoff.HandoffError, "Unrelated staged"):
                draft_handoff.deliver(["SD-M00-L01"])
            self.assertEqual(git.call_count, 1)


if __name__ == "__main__":
    unittest.main()
