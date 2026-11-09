"""Integration tests for taskctl; uses only the Python standard library and Git."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "taskctl.py"


class TaskCtlIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        shutil.copy2(SOURCE_SCRIPT, self.root / "scripts" / "taskctl.py")
        (self.root / "docs").mkdir()
        (self.root / "outputs").mkdir()
        (self.root / "docs" / "input.md").write_text("source version 1\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "taskctl-test@example.com")
        self.git("config", "user.name", "TaskCtl Test")
        self.git("add", "scripts/taskctl.py", "docs/input.md")
        self.git("commit", "-qm", "fixture")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True)
        if result.returncode:
            raise AssertionError(result.stderr)
        return result.stdout.strip()

    def cli(self, *args: str, expected: int = 0) -> str:
        result = subprocess.run(
            [os.environ.get("PYTHON", "python"), "scripts/taskctl.py", *args],
            cwd=self.root,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def create_task(self) -> None:
        self.cli("init", "TEST-1", "--module", "demo", "--goal", "Test idempotency")
        self.cli(
            "add-step", "TEST-1", "research",
            "--title", "Produce evidence",
            "--definition-version", "v1",
            "--input-paths", "docs/input.md",
            "--output-paths", "outputs/evidence.md",
        )

    def test_completed_step_is_skipped_until_input_changes(self) -> None:
        self.create_task()
        self.cli("start", "TEST-1", "research", "--agent", "tester", "--run-id", "run-1")
        (self.root / "outputs/evidence.md").write_text("evidence for source v1\n", encoding="utf-8")
        self.git("add", "outputs/evidence.md")
        self.git("commit", "-qm", "commit evidence")
        self.cli("complete", "TEST-1", "research", "--agent", "tester")
        self.assertIn("SKIP", self.cli("status", "TEST-1"))
        self.assertIn("SKIP research", self.cli("start", "TEST-1", "research", "--agent", "tester", expected=0))
        (self.root / "docs/input.md").write_text("source version 2\n", encoding="utf-8")
        self.git("add", "docs/input.md")
        self.git("commit", "-qm", "update source")
        self.assertIn("STALE", self.cli("status", "TEST-1"))

    def test_dependent_step_is_blocked_until_prerequisite_is_current(self) -> None:
        self.create_task()
        self.cli(
            "add-step", "TEST-1", "author",
            "--title", "Write lesson",
            "--definition-version", "v1",
            "--input-paths", "docs/input.md",
            "--output-paths", "outputs/lesson.md",
            "--depends-on", "research",
        )
        self.assertIn("BLOCKED", self.cli("status", "TEST-1"))

    def test_complete_rejects_uncommitted_output(self) -> None:
        self.create_task()
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        (self.root / "outputs/evidence.md").write_text("not committed\n", encoding="utf-8")
        result = self.cli("complete", "TEST-1", "research", expected=2)
        self.assertIn("not tracked by Git yet", result)

    def test_output_edit_invalidates_completion(self) -> None:
        self.create_task()
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        (self.root / "outputs/evidence.md").write_text("original\n", encoding="utf-8")
        self.git("add", "outputs/evidence.md")
        self.git("commit", "-qm", "commit original")
        self.cli("complete", "TEST-1", "research")
        (self.root / "outputs/evidence.md").write_text("manual edit\n", encoding="utf-8")
        self.git("add", "outputs/evidence.md")
        self.git("commit", "-qm", "tamper completed output")
        self.assertIn("STALE", self.cli("status", "TEST-1"))


if __name__ == "__main__":
    unittest.main()