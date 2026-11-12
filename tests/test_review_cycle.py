"""Small regression suite for the explicit, bounded module-review revision loop."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import review_cycle


class ReviewCycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.root_patch = patch.object(review_cycle, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.temp.cleanup)
        reports = review_cycle.state_path("m00").parent
        reports.mkdir(parents=True)
        (reports / "technical.md").write_text("Technical findings", encoding="utf-8")
        (reports / "pedagogy.md").write_text("Pedagogy findings", encoding="utf-8")

    def test_initial_findings_trigger_two_bounded_revision_rounds(self):
        first = review_cycle.record("m00", "revise", "ready-for-human-review")
        self.assertEqual((first["revision_attempts"], first["status"]), (0, "needs_revision"))
        for attempt in (1, 2):
            state = review_cycle.begin_revision("m00")
            self.assertEqual((state["revision_attempts"], state["status"]), (attempt, "revising"))
            state = review_cycle.record("m00", "revise", "revise")
        self.assertEqual(state["status"], "blocked")
        self.assertEqual(len(state["review_history"]), 3)
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "No eligible"):
            review_cycle.begin_revision("m00")

    def test_ready_state_prevents_unrequested_rerun(self):
        result = review_cycle.record("m00", "ready-for-human-review", "ready-for-human-review")
        self.assertEqual(result["status"], "ready")
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "already recorded"):
            review_cycle.record("m00", "revise", "revise")
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "No eligible"):
            review_cycle.begin_revision("m00")

    def test_resume_and_manual_block(self):
        review_cycle.record("m00", "revise", "revise")
        review_cycle.begin_revision("m00")
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "No eligible"):
            review_cycle.begin_revision("m00")
        stopped = review_cycle.stop("m00", "No verifiable source for a critical claim")
        self.assertEqual(stopped["status"], "blocked")
        self.assertIn("verifiable source", stopped["stop_reason"])

    def test_lesson_cycles_are_independent_and_do_not_wait_for_module(self):
        a = "M00-L01"
        b = "M00-L02"
        for target in (a, b):
            reports = review_cycle.state_path(target).parent
            reports.mkdir(parents=True)
            for role in ("technical", "pedagogy"):
                (reports / f"{role}.md").write_text("Independent review", encoding="utf-8")
        first = review_cycle.record(a, "ready-for-human-review", "ready-for-human-review")
        second = review_cycle.record(b, "revise", "ready-for-human-review")
        self.assertEqual(first["status"], "ready")
        self.assertEqual(first["module"], "m00")
        self.assertEqual(first["lesson"], a)
        self.assertEqual(second["status"], "needs_revision")
        self.assertIsNone(review_cycle.load("m00"))
        self.assertEqual(review_cycle.begin_revision(b)["revision_attempts"], 1)
        self.assertEqual(review_cycle.load(a)["revision_attempts"], 0)
        self.assertEqual(review_cycle.load(b)["status"], "revising")

    def test_lesson_record_requires_its_own_report(self):
        target = "M00-L03"
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "Missing nonempty technical"):
            review_cycle.record(target, "ready-for-human-review", "ready-for-human-review")
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "Target must"):
            review_cycle.state_path("../bad")
    def test_missing_report_never_records_success(self):
        (review_cycle.state_path("m00").parent / "technical.md").unlink()
        with self.assertRaisesRegex(review_cycle.ReviewCycleError, "Missing nonempty technical"):
            review_cycle.record("m00", "ready-for-human-review", "ready-for-human-review")
        self.assertFalse(review_cycle.state_path("m00").exists())


if __name__ == "__main__":
    unittest.main()
