"""Regression tests for explicitly managed task state and opt-in review."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE_ROOT = Path(__file__).resolve().parents[1]


class AggregateTaskStatusTests(unittest.TestCase):
    def test_default_draft_template_does_not_require_reviews_or_validation(self):
        from scripts import taskctl

        template = json.loads((SOURCE_ROOT / ".academy/state/task.template.json").read_text())
        data = {"steps": template["steps"], "execution_control": "active"}
        self.assertEqual([s["step_id"] for s in data["steps"]], ["research", "author"])
        self.assertFalse(any(s.get("requires_reviews") or s.get("review") for s in data["steps"]))
        self.assertEqual(taskctl.step_status(data, data["steps"][0])[0], "READY")
        self.assertEqual(taskctl.step_status(data, data["steps"][1])[0], "BLOCKED")
        taskctl.refresh_task_status(data)
        self.assertEqual(data["automation_status"], "not_started")
        data["steps"][0]["status"] = "completed"
        self.assertEqual(taskctl.step_status(data, data["steps"][1])[0], "READY")
        taskctl.refresh_task_status(data)
        self.assertEqual(data["automation_status"], "in_progress")


class TaskCtlExplicitStateTests(unittest.TestCase):
    def setUp(self):
        temp_root = SOURCE_ROOT / ".tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="academy-taskctl-", dir=temp_root)
        self.root = Path(self.tmp.name)
        for folder in ("scripts", ".academy/state/schema", ".academy/state", "docs", "outputs"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        for path in ("scripts/taskctl.py", ".academy/state/schema/task.schema.json",
                     ".academy/state/schema/spec.schema.json"):
            shutil.copy2(SOURCE_ROOT / path, self.root / path)
        (self.root / "docs/input.md").write_text("input-v1\n", encoding="utf-8")
        spec = {
            "schema_version": 1, "task_id": "${TASK_ID}", "revision": 1, "goal": "${GOAL}",
            "scope": {"in_scope": ["A tested task"], "out_of_scope": []},
            "constraints": ["Keep original task history"],
            "definition_of_done": [{"id": "dod", "text": "Outputs exist", "applies_to": ["*"]}],
            "acceptance_criteria": [{"id": "ac", "text": "Explicit progress", "applies_to": ["*"]}],
        }
        (self.root / ".academy/state/spec.template.json").write_text(json.dumps(spec), encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "taskctl@example.com")
        self.git("config", "user.name", "TaskCtl Test")
        self.git("add", ".")
        self.git("commit", "-qm", "test fixture")
        self.cli("init", "TEST-1", "--module", "demo", "--goal", "A tested task", "--owner", "tester")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        result = subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def cli(self, *args, expected=0):
        result = subprocess.run([os.environ.get("PYTHON", "python"), "scripts/taskctl.py", *args],
                                cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def add_step(self, name, output, depends=(), input_path="docs/input.md"):
        self.cli("add-step", "TEST-1", name, "--title", name, "--definition-version", "v1",
                 "--input-paths", input_path, "--output-paths", output, "--depends-on", *depends)

    def output(self, path, text="generated\n"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def run_step(self, name, output):
        self.cli("start", "TEST-1", name, "--agent", "tester")
        self.output(output)
        self.cli("complete", "TEST-1", name, "--agent", "tester")

    def state(self):
        return json.loads((self.root / ".academy/state/tasks/TEST-1.json").read_text(encoding="utf-8"))

    def edit_state(self, fn):
        path = self.root / ".academy/state/tasks/TEST-1.json"
        data = self.state()
        fn(data)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def test_completed_ignores_spec_input_and_output_edits(self):
        self.add_step("research", "outputs/research.md")
        self.run_step("research", "outputs/research.md")
        spec = self.root / ".academy/specs/TEST-1.json"
        value = json.loads(spec.read_text(encoding="utf-8"))
        value["acceptance_criteria"][0]["text"] = "Updated requirement"
        spec.write_text(json.dumps(value), encoding="utf-8")
        (self.root / "docs/input.md").write_text("input-v2\n", encoding="utf-8")
        self.output("outputs/research.md", "new lesson content\n")
        result = self.cli("status", "TEST-1")
        self.assertIn("- research: SKIP", result)
        self.assertIn("automation=automation_complete", result)
        self.assertNotIn("STALE", result)

    def test_legacy_metadata_is_ignored_not_recomputed(self):
        self.add_step("research", "outputs/research.md")
        self.run_step("research", "outputs/research.md")
        self.edit_state(lambda data: data["steps"][0].update(
            completed_fingerprint="previous-checksum", completed_output_hashes={"outputs/research.md": "old"}
        ))
        self.output("outputs/research.md", "updated\n")
        self.assertIn("- research: SKIP", self.cli("status", "TEST-1"))

    def test_running_work_survives_input_changes(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        (self.root / "docs/input.md").write_text("edited while running\n", encoding="utf-8")
        self.output("outputs/research.md")
        self.cli("complete", "TEST-1", "research")
        self.assertIn("- research: SKIP", self.cli("status", "TEST-1"))

    def test_missing_inputs_rejected_but_dirty_or_untracked_inputs_allowed(self):
        self.add_step("research", "outputs/research.md")
        (self.root / "docs/input.md").write_text("dirty\n", encoding="utf-8")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        self.add_step("missing", "outputs/missing.md", input_path="docs/missing.md")
        self.assertIn("Required input file is missing", self.cli("start", "TEST-1", "missing",
                                                                   "--agent", "tester", expected=2))

    def test_declared_output_must_exist_but_need_not_be_committed_or_changed(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        self.assertIn("Missing declared outputs", self.cli("complete", "TEST-1", "research", expected=2))
        self.output("outputs/research.md")
        self.cli("complete", "TEST-1", "research")
        self.add_step("reuse", "outputs/reuse.md")
        self.output("outputs/reuse.md", "already exists\n")
        self.cli("start", "TEST-1", "reuse", "--agent", "tester")
        self.cli("complete", "TEST-1", "reuse")

    def test_reopen_is_explicit_and_cascade_is_only_on_request(self):
        self.add_step("research", "outputs/research.md")
        self.add_step("author", "outputs/author.md", depends=("research",))
        self.run_step("research", "outputs/research.md")
        self.run_step("author", "outputs/author.md")
        (self.root / "docs/input.md").write_text("new input\n", encoding="utf-8")
        self.assertIn("- author: SKIP", self.cli("status", "TEST-1"))
        self.cli("invalidate", "TEST-1", "research", "--reason", "User requested new research")
        status = self.cli("status", "TEST-1")
        self.assertIn("- research: READY", status)
        self.assertIn("- author: SKIP", status)
        self.cli("invalidate", "TEST-1", "research", "--reason", "Scope changed", "--cascade")
        status = self.cli("status", "TEST-1")
        self.assertIn("- author: BLOCKED", status)
        self.assertIn("automation=in_progress", status)

    def test_completed_cannot_restart_without_explicit_reopen(self):
        self.add_step("research", "outputs/research.md")
        self.run_step("research", "outputs/research.md")
        self.assertIn("SKIP", self.cli("start", "TEST-1", "research", "--agent", "tester"))
        self.cli("invalidate", "TEST-1", "research", "--reason", "New scope")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        self.assertEqual(self.state()["steps"][0]["attempts"], 2)

    def test_resume_does_not_require_equal_input_snapshot(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester", "--run-id", "run-1")
        self.cli("checkpoint", "TEST-1", "research", "--note", "Source verified",
                 "--next-action", "Write summary")
        (self.root / "docs/input.md").write_text("changed\n", encoding="utf-8")
        self.assertIn("Resumed", self.cli("start", "TEST-1", "research", "--agent", "tester", "--resume"))
        self.assertEqual(self.state()["steps"][0]["run_id"], "run-1")
        self.output("outputs/research.md")
        self.cli("complete", "TEST-1", "research")

    def test_review_status_is_explicit_and_not_publication_approval(self):
        self.add_step("author", "outputs/lesson.md")
        self.run_step("author", "outputs/lesson.md")
        self.cli("review-status", "TEST-1", "--state", "reviewed", "--reason", "Manual content review")
        self.output("outputs/lesson.md", "edited after content review\n")
        self.assertEqual(self.state()["review_status"], "reviewed")
        self.cli("review-status", "TEST-1", "--state", "needs_review", "--reason", "Substantive edit")
        self.assertEqual(self.state()["review_status"], "needs_review")
        self.assertIn("- author: SKIP", self.cli("status", "TEST-1"))
        result = self.cli("review-status", "TEST-1", "--state", "in_review", "--reason", "", expected=2)
        self.assertIn("reason", result)

    def test_status_is_read_only_and_reconcile_uses_explicit_steps(self):
        self.add_step("author", "outputs/lesson.md")
        self.run_step("author", "outputs/lesson.md")
        task = self.root / ".academy/state/tasks/TEST-1.json"
        worklog = self.root / ".academy/state/worklog/TEST-1.jsonl"
        before = (task.read_bytes(), worklog.read_bytes())
        self.cli("status", "TEST-1")
        self.assertEqual(before, (task.read_bytes(), worklog.read_bytes()))
        self.edit_state(lambda data: data.update(automation_status="not_started"))
        self.cli("reconcile", "TEST-1")
        self.assertEqual(self.state()["automation_status"], "automation_complete")

    def test_hold_blocks_start_resume_and_complete(self):
        self.add_step("research", "outputs/research.md")
        self.cli("hold", "TEST-1", "--reason", "User paused")
        self.assertIn("paused", self.cli("start", "TEST-1", "research", "--agent", "tester", expected=2))
        self.cli("resume-task", "TEST-1", "--reason", "User resumed")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        self.cli("hold", "TEST-1", "--state", "awaiting-human", "--reason", "User decision pending")
        self.assertIn("awaiting-human", self.cli("complete", "TEST-1", "research", expected=2))

    def make_review_graph(self):
        self.add_step("review", "outputs/verdict.json")
        self.add_step("revision", "outputs/revised.md", depends=("review",))
        self.add_step("author", "outputs/lesson.md", depends=("review",))
        self.edit_state(lambda data: (
            data["steps"][0].update(review={"artifact_paths": ["docs/input.md"],
                                            "verdict_path": "outputs/verdict.json"},
                                    input_paths=["docs/input.md"]),
            data["steps"][2].update(requires_reviews=["review"])
        ))

    def write_verdict(self, verdict="ready-for-human-review", findings=None):
        self.output("outputs/verdict.json", json.dumps({"verdict": verdict, "findings": findings or []}))

    def test_review_gate_requires_completed_step_and_scoped_decision(self):
        self.make_review_graph()
        self.cli("start", "TEST-1", "review", "--agent", "reviewer")
        self.write_verdict("block", [{"id": "T1", "severity": "blocker", "status": "open"}])
        self.cli("complete", "TEST-1", "review")
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))
        # Mutating the verdict file is not the same as accepting a review.
        self.write_verdict()
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))
        self.assertIn("needs an explicit reviewed decision", self.cli("status", "TEST-1"))
        # An overall/general decision cannot substitute for a named review gate.
        self.cli("review-status", "TEST-1", "--state", "reviewed", "--reason", "Overall note")
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))
        self.cli("review-status", "TEST-1", "--scope", "review",
                 "--state", "in_review", "--reason", "New inspection started")
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))
        self.cli("review-status", "TEST-1", "--scope", "review",
                 "--state", "reviewed", "--reason", "Reviewed current evidence")
        self.assertIn("- author: READY", self.cli("status", "TEST-1"))
        (self.root / "docs/input.md").write_text("changed\\n", encoding="utf-8")
        self.assertIn("- author: READY", self.cli("status", "TEST-1"))
        self.cli("review-status", "TEST-1", "--scope", "review",
                 "--state", "needs_review", "--reason", "Content changed")
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))
        self.cli("review-status", "TEST-1", "--scope", "review",
                 "--state", "reviewed", "--reason", "Reviewed again")
        self.cli("review-status", "TEST-1", "--state", "in_review", "--reason", "Overall review underway")
        self.assertIn("- author: BLOCKED", self.cli("status", "TEST-1"))

    def test_scoped_review_cannot_be_accepted_without_completed_clear_verdict(self):
        self.make_review_graph()
        self.assertIn("must be completed", self.cli("review-status", "TEST-1", "--scope", "review",
                   "--state", "reviewed", "--reason", "Premature", expected=2))
        self.cli("start", "TEST-1", "review", "--agent", "reviewer")
        self.write_verdict("block", [{"id": "T1", "severity": "blocker", "status": "open"}])
        self.cli("complete", "TEST-1", "review")
        self.assertIn("does not have an accepted verdict", self.cli("review-status", "TEST-1",
                      "--scope", "review", "--state", "reviewed", "--reason", "Premature", expected=2))

    def test_legacy_review_graph_retains_historical_acceptance(self):
        self.make_review_graph()
        self.cli("start", "TEST-1", "review", "--agent", "reviewer")
        self.write_verdict()
        self.cli("complete", "TEST-1", "review")
        self.edit_state(lambda data: (data.pop("review_status", None),
                                     data.pop("review_statuses", None)))
        self.assertIn("- author: READY", self.cli("status", "TEST-1"))

    def test_review_scopes_are_independent(self):
        self.cli("review-status", "TEST-1", "--scope", "technical",
                 "--state", "reviewed", "--reason", "Technical review")
        self.cli("review-status", "TEST-1", "--scope", "pedagogy",
                 "--state", "needs_review", "--reason", "Teaching review outstanding")
        state = self.state()["review_statuses"]
        self.assertEqual(state["technical"]["status"], "reviewed")
        self.assertEqual(state["pedagogy"]["status"], "needs_review")
        self.assertEqual(self.state()["review_status"], "not_reviewed")

    def test_review_rejects_unresolved_major_findings(self):
        self.make_review_graph()
        self.cli("start", "TEST-1", "review", "--agent", "reviewer")
        self.write_verdict(findings=[{"id": "M1", "severity": "major", "status": "open"}])
        self.assertIn("unresolved material", self.cli("complete", "TEST-1", "review", expected=2))

    def test_runtime_usage_logged_without_estimating_cost(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester",
                 "--model", "fixture-model", "--reasoning-effort", "medium")
        self.output("outputs/research.md")
        self.output("outputs/usage.json", '{"input_tokens": 100, "output_tokens": 10}')
        self.cli("complete", "TEST-1", "research", "--usage-file", "outputs/usage.json")
        log = (self.root / ".academy/state/worklog/TEST-1.jsonl").read_text().splitlines()
        event = json.loads(log[-1])
        self.assertEqual(event["runtime"]["model"], "fixture-model")
        self.assertEqual(event["usage"], {"input_tokens": 100, "output_tokens": 10})

    def test_revision_budget_and_path_safety_remain(self):
        self.add_step("revision", "outputs/revision.md")
        self.edit_state(lambda data: data["steps"][0].update(revision_cycle=1, attempts=2))
        self.assertIn("Two automated revision", self.cli("start", "TEST-1", "revision",
                                                         "--agent", "tester", expected=2))
        absolute = self.cli("add-step", "TEST-1", "absolute", "--title", "absolute",
                            "--definition-version", "v1", "--input-paths", "/etc/passwd",
                            "--output-paths", "outputs/a.md", expected=2)
        self.assertIn("Unsafe repository-relative path", absolute)

    def test_missing_completed_output_warns_without_staling_task(self):
        self.add_step("research", "outputs/research.md")
        self.run_step("research", "outputs/research.md")
        (self.root / "outputs/research.md").unlink()
        result = self.cli("status", "TEST-1")
        self.assertIn("- research: SKIP", result)
        self.assertIn("WARNING: Missing output", result)
        self.assertEqual(self.state()["steps"][0]["status"], "completed")

    def test_handoff_requires_committed_outputs_and_memory(self):
        self.add_step("research", "outputs/research.md")
        self.run_step("research", "outputs/research.md")
        response = self.cli("handoff", "TEST-1", expected=2)
        self.assertIn("Handoff not ready", response)
        self.assertIn("Not Git-tracked: outputs/research.md", response)
        self.git("add", ".")
        self.git("commit", "-qm", "commit entire task handoff")
        self.assertIn("HANDOFF READY", self.cli("handoff", "TEST-1"))
        (self.root / "outputs/research.md").write_text("unsaved change", encoding="utf-8")
        self.assertIn("Uncommitted:", self.cli("handoff", "TEST-1", expected=2))
        self.git("add", ".")
        self.git("commit", "-qm", "sync handoff")
        (self.root / "outputs/research.md").unlink()
        self.assertIn("Missing:", self.cli("handoff", "TEST-1", expected=2))

    def test_new_lesson_init_uses_backlog_story_paths(self):
        (self.root / "delivery").mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_ROOT / ".academy/state/task.template.json",
                     self.root / ".academy/state/task.template.json")
        story = {"type": "Story", "package_kind": "lesson",
                 "proposed_task_id": "SD-M00-L01", "lesson_id": "M00-L01",
                 "key": "SDA-M00-L01",
                 "outputs": {"teaching": "modules/m00/lessons/M00-L01.md",
                             "assessment": "modules/m00/assessments/M00-L01.md",
                             "evidence": "modules/m00/evidence/M00-L01.md"}}
        (self.root / "delivery/backlog.json").write_text(json.dumps({"items": [story]}), encoding="utf-8")
        self.assertIn("does not match declared module",
                      self.cli("init", "SD-M00-L01", "--module", "M01", "--goal", "Wrong",
                               "--owner", "tester", "--template", ".academy/state/task.template.json",
                               expected=2))
        self.cli("init", "SD-M00-L01", "--module", "M00", "--goal", "Write draft",
                 "--owner", "tester", "--template", ".academy/state/task.template.json")
        state = json.loads((self.root / ".academy/state/tasks/SD-M00-L01.json").read_text())
        self.assertEqual(state["steps"][0]["output_paths"], [story["outputs"]["evidence"]])
        self.assertEqual(state["steps"][1]["output_paths"],
                         [story["outputs"]["teaching"], story["outputs"]["assessment"]])
        self.assertIn(story["outputs"]["evidence"], state["steps"][1]["input_paths"])
        self.assertNotIn("SD-M00-L01.md", str(state["steps"][1]["output_paths"]))
        self.assertIn("Expected one lesson Story",
                      self.cli("init", "SD-M00-L02", "--module", "M00", "--goal", "Unknown",
                               "--owner", "tester", "--template", ".academy/state/task.template.json",
                               expected=2))

    def test_all_backlog_lesson_paths_are_resolvable(self):
        from scripts import taskctl
        backlog = json.loads((SOURCE_ROOT / "delivery/backlog.json").read_text(encoding="utf-8"))
        stories = [item for item in backlog["items"] if item.get("package_kind") == "lesson"]
        self.assertEqual(len(stories), 57)
        for story in stories:
            with self.subTest(story=story["key"]):
                module = story["lesson_id"].split("-")[0]
                resolved = taskctl.lesson_paths_from_backlog(story["proposed_task_id"], module)
                self.assertEqual(resolved["TEACHING_PATH"], story["outputs"]["teaching"])
                self.assertEqual(resolved["ASSESSMENT_PATH"], story["outputs"]["assessment"])
                self.assertEqual(resolved["EVIDENCE_PATH"], story["outputs"]["evidence"])

    def test_symlink_path_guard_and_no_publish_command(self):
        from scripts import taskctl

        link = self.root / "docs/link.md"
        with patch.object(taskctl, "ROOT", self.root):
            with patch.object(taskctl.Path, "is_symlink", autospec=True) as is_symlink:
                is_symlink.side_effect = lambda candidate: candidate == link
                with self.assertRaisesRegex(taskctl.TaskError, "Symlink path components are not allowed"):
                    taskctl.relpath("docs/link.md")
        self.assertNotEqual(subprocess.run(["python", "scripts/taskctl.py", "publish", "TEST-1"],
                                          cwd=self.root, capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
