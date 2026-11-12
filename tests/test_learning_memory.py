"""Focused regressions for durable, evidence-gated reviewer lessons learned."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import learning_memory, review_cycle


class LearningMemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for module in (learning_memory, review_cycle):
            override = patch.object(module, "ROOT", self.root)
            override.start()
            self.addCleanup(override.stop)
        store = learning_memory.memory_path()
        store.parent.mkdir(parents=True)
        store.write_text('{"schema_version":1,"entries":[]}', encoding="utf-8")

    def ready(self, module, attempts=1):
        parent = review_cycle.state_path(module).parent
        parent.mkdir(parents=True, exist_ok=True)
        (parent / "technical.md").write_text(
            "| T-1 | resolved | verified using primary evidence |\n"
            "| T-2 | resolved | verified using primary evidence |\n", encoding="utf-8")
        (parent / "pedagogy.md").write_text(
            "| P-1 | resolved | fixed ambiguous example |\n", encoding="utf-8")
        review_cycle.save(module, {
            "module": module, "status": "ready", "revision_attempts": attempts,
            "review_history": [{"round": attempts, "technical": "ready-for-human-review",
                                "pedagogy": "ready-for-human-review", "result": "ready"}],
        })

    def arguments(self, module="m00", finding_id="T-1", key="distinguish-two-consistencies"):
        return dict(module=module, finding_id=finding_id, review_role="technical",
                    key=key, tags="consistency,distributed-systems",
                    problem="Conflating different meanings of consistency in design explanations.",
                    prevention="Differentiate each consistency contract with an operation-level example.",
                    evidence="https://www.rfc-editor.org/rfc/rfc9110",
                    applies_to="lesson_author,technical_reviewer")

    def test_only_successful_independent_re_review_can_be_learned(self):
        with self.assertRaisesRegex(learning_memory.LearningError, "successfully corrected"):
            learning_memory.record(**self.arguments())
        self.ready("m00", attempts=0)
        with self.assertRaisesRegex(learning_memory.LearningError, "successfully corrected"):
            learning_memory.record(**self.arguments())
        self.ready("m00", attempts=1)
        arguments = self.arguments()
        arguments["finding_id"] = "T-9"
        with self.assertRaisesRegex(learning_memory.LearningError, "does not appear"):
            learning_memory.record(**arguments)
        self.assertEqual(learning_memory.read_memory()["entries"], [])

    def test_relevant_retrieval_and_idempotent_recording(self):
        self.ready("m00")
        self.assertEqual(learning_memory.record(**self.arguments())["result"], "recorded")
        self.assertEqual(learning_memory.record(**self.arguments())["result"], "unchanged")
        entries = learning_memory.read_memory()["entries"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(entries[0]["occurrences"]), 1)
        result = learning_memory.suggest("consistency,cache", "lesson_author")
        self.assertEqual([item["key"] for item in result], ["distinguish-two-consistencies"])
        self.assertEqual(learning_memory.suggest("security", "lesson_author"), [])
        self.assertEqual(learning_memory.suggest("consistency", "pedagogy_reviewer"), [])

    def test_repetition_means_independent_modules_and_only_proposes_skills(self):
        self.ready("m00")
        self.ready("m01")
        learning_memory.record(**self.arguments())
        self.assertEqual(learning_memory.promotions(), [])
        learning_memory.record(**self.arguments(finding_id="T-2"))
        self.assertEqual(learning_memory.promotions(), [])
        self.assertEqual(learning_memory.record(**self.arguments(module="m01"))["modules"], 2)
        candidates = learning_memory.promotions()
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["modules"], ["m00", "m01"])
        self.assertEqual(len(learning_memory.read_memory()["entries"]), 1)

    def test_conflicting_guidance_and_unsafe_memory_are_rejected(self):
        self.ready("m00")
        learning_memory.record(**self.arguments())
        args = self.arguments()
        args["prevention"] = "An incompatible rule that conflicts with the established prevention."
        with self.assertRaisesRegex(learning_memory.LearningError, "reconcile conflicting"):
            learning_memory.record(**args)
        args = self.arguments(key="unchecked-evidence")
        args["evidence"] = "javascript:fake()"
        with self.assertRaisesRegex(learning_memory.LearningError, "HTTPS source"):
            learning_memory.record(**args)
        with self.assertRaisesRegex(learning_memory.LearningError, "At most five"):
            learning_memory.suggest("consistency", "lesson_author", limit=10)
        self.assertEqual(len(json.loads(learning_memory.memory_path().read_text())["entries"]), 1)


if __name__ == "__main__":
    unittest.main()
