"""Integration tests for task-spec fingerprinting and reproducible task execution."""
from __future__ import annotations

import json
import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SOURCE_ROOT = Path(__file__).resolve().parents[1]


class AggregateTaskStatusTests(unittest.TestCase):
    def test_default_task_dag_is_not_reported_blocked_while_a_phase_is_runnable(self):
        from scripts import taskctl

        template = json.loads((SOURCE_ROOT / ".academy/state/task.template.json").read_text(encoding="utf-8"))
        data = {"steps": template["steps"]}
        initial_states = {step["step_id"]: "BLOCKED" for step in data["steps"]}
        initial_states.update({"research": "READY", "curriculum": "READY"})
        with patch.object(taskctl, "step_status", side_effect=lambda _data, step: (initial_states[step["step_id"]], "fixture")):
            taskctl.refresh_task_status(data)
        self.assertEqual(data["automation_status"], "not_started")

        phase_states = dict(initial_states, research="SKIP", curriculum="READY")
        next(step for step in data["steps"] if step["step_id"] == "research")["status"] = "completed"
        with patch.object(taskctl, "step_status", side_effect=lambda _data, step: (phase_states[step["step_id"]], "fixture")):
            taskctl.refresh_task_status(data)
        self.assertEqual(data["automation_status"], "in_progress")


class TaskCtlV2Tests(unittest.TestCase):
    def setUp(self):
        temp_root = SOURCE_ROOT / ".tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="academy-taskctl-", dir=temp_root)
        self.root = Path(self.tmp.name)
        for folder in ("scripts", ".academy/state/schema", ".academy/state", "docs", "outputs"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_ROOT / "scripts/taskctl.py", self.root / "scripts/taskctl.py")
        shutil.copy2(SOURCE_ROOT / ".academy/state/schema/task.schema.json", self.root / ".academy/state/schema/task.schema.json")
        shutil.copy2(SOURCE_ROOT / ".academy/state/schema/spec.schema.json", self.root / ".academy/state/schema/spec.schema.json")
        (self.root / "docs/input.md").write_text("input-v1\n", encoding="utf-8")
        template = {
            "schema_version": 1, "task_id": "${TASK_ID}", "revision": 1, "goal": "${GOAL}",
            "scope": {"in_scope": ["A tested task"], "out_of_scope": []},
            "constraints": ["Use committed source inputs"],
            "definition_of_done": [{"id": "dod", "text": "Outputs are validated", "applies_to": ["*"]}],
            "acceptance_criteria": [{"id": "ac", "text": "The task behaves deterministically", "applies_to": ["*"]}]
        }
        (self.root / ".academy/state/spec.template.json").write_text(json.dumps(template, indent=2), encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "taskctl@example.com")
        self.git("config", "user.name", "TaskCtl Test")
        self.git("add", "scripts", ".academy/state/schema", ".academy/state/spec.template.json", "docs/input.md")
        self.git("commit", "-qm", "test fixture")
        self.cli("init", "TEST-1", "--module", "demo", "--goal", "A tested task", "--owner", "tester")
        self.git("add", ".academy")
        self.git("commit", "-qm", "create canonical task specification")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        result = subprocess.run(["git", *args], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def cli(self, *args, expected=0):
        result = subprocess.run(
            [os.environ.get("PYTHON", "python"), "scripts/taskctl.py", *args],
            cwd=self.root, text=True, capture_output=True
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def add_step(self, name, output, depends=(), input_path="docs/input.md"):
        self.cli("add-step", "TEST-1", name, "--title", name,
                 "--definition-version", "v1", "--input-paths", input_path,
                 "--output-paths", output, "--depends-on", *depends)
        self.git("add", ".academy/state/tasks", ".academy/state/worklog")
        self.git("commit", "-qm", "declare step " + name)

    def set_scoped_spec(self, step_ids):
        path = self.root / ".academy/specs/TEST-1.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec["definition_of_done"] = [
            {"id": "dod-" + sid, "text": "Done condition for " + sid, "applies_to": [sid]}
            for sid in step_ids
        ]
        spec["acceptance_criteria"] = [
            {"id": "ac-" + sid, "text": "Acceptance condition for " + sid, "applies_to": [sid]}
            for sid in step_ids
        ]
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        self.git("add", ".academy/specs/TEST-1.json")
        self.git("commit", "-qm", "scope task criteria")

    def execute_step(self, name, output):
        self.cli("start", "TEST-1", name, "--agent", "tester")
        target = self.root / output
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("generated by this run\n", encoding="utf-8")
        self.git("add", output)
        self.git("commit", "-qm", "produce " + name)
        self.cli("complete", "TEST-1", name, "--agent", "tester")

    def test_definition_of_done_change_invalidates_only_affected_step_and_downstream(self):
        self.add_step("research", "outputs/research.md")
        self.add_step("unrelated", "outputs/unrelated.md")
        self.add_step("author", "outputs/author.md", depends=("research",))
        self.set_scoped_spec(["research", "unrelated", "author"])
        self.execute_step("research", "outputs/research.md")
        self.execute_step("unrelated", "outputs/unrelated.md")
        self.execute_step("author", "outputs/author.md")
        path = self.root / ".academy/specs/TEST-1.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec["definition_of_done"][0]["text"] = "Changed DoD for research"
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        self.git("add", ".academy/specs/TEST-1.json")
        self.git("commit", "-qm", "change research DoD")
        output = self.cli("status", "TEST-1")
        self.assertIn("- research: STALE", output)
        self.assertIn("- author: BLOCKED", output)
        self.assertIn("- unrelated: SKIP", output)

    def test_acceptance_criteria_change_invalidates_completed_step(self):
        self.add_step("research", "outputs/research.md")
        self.set_scoped_spec(["research"])
        self.execute_step("research", "outputs/research.md")
        path = self.root / ".academy/specs/TEST-1.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec["acceptance_criteria"][0]["text"] = "Changed acceptance criterion"
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        self.git("add", ".academy/specs/TEST-1.json")
        self.git("commit", "-qm", "change acceptance criteria")
        self.assertIn("STALE", self.cli("status", "TEST-1"))


    def test_unrelated_spec_change_does_not_abort_running_step(self):
        self.add_step("research", "outputs/research.md")
        self.add_step("unrelated", "outputs/unrelated.md")
        self.set_scoped_spec(["research", "unrelated"])
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        self.git("add", ".academy/state/tasks", ".academy/state/worklog")
        self.git("commit", "-qm", "persist research start")
        path = self.root / ".academy/specs/TEST-1.json"
        spec = json.loads(path.read_text(encoding="utf-8"))
        spec["acceptance_criteria"][1]["text"] = "Updated criterion for unrelated step"
        path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        self.git("add", ".academy/specs/TEST-1.json")
        self.git("commit", "-qm", "update unrelated criterion")
        target = self.root / "outputs/research.md"
        target.write_text("research output\n", encoding="utf-8")
        self.git("add", "outputs/research.md")
        self.git("commit", "-qm", "commit research output")
        self.cli("complete", "TEST-1", "research", "--agent", "tester")
        self.assertIn("- research: SKIP", self.cli("status", "TEST-1"))

    def test_start_rejects_untracked_and_dirty_inputs(self):
        self.add_step("research", "outputs/research.md", input_path="docs/input.md")
        (self.root / "docs/input.md").write_text("dirty input\n", encoding="utf-8")
        self.assertIn("dirty or staged", self.cli("start", "TEST-1", "research", "--agent", "tester", expected=2))
        self.git("checkout", "--", "docs/input.md")
        self.add_step("other", "outputs/other.md", input_path="docs/untracked.md")
        (self.root / "docs/untracked.md").write_text("not tracked\n", encoding="utf-8")
        self.assertIn("not Git-tracked", self.cli("start", "TEST-1", "other", "--agent", "tester", expected=2))

    def test_complete_rejects_input_change_during_run(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        (self.root / "docs/input.md").write_text("input-v2\n", encoding="utf-8")
        self.git("add", "docs/input.md")
        self.git("commit", "-qm", "change input mid-run")
        target = self.root / "outputs/research.md"
        target.write_text("output\n", encoding="utf-8")
        self.git("add", "outputs/research.md")
        self.git("commit", "-qm", "commit output")
        self.assertIn("changed during execution", self.cli("complete", "TEST-1", "research", expected=2))

    def test_unchanged_existing_output_requires_explicit_reuse(self):
        self.add_step("research", "outputs/research.md")
        target = self.root / "outputs/research.md"
        target.write_text("pre-existing output\n", encoding="utf-8")
        self.git("add", "outputs/research.md")
        self.git("commit", "-qm", "commit pre-existing output")
        self.cli("start", "TEST-1", "research", "--agent", "tester")
        result = self.cli("complete", "TEST-1", "research", expected=2)
        self.assertIn("not produced/updated", result)
        self.cli("complete", "TEST-1", "research", "--reuse-output", "outputs/research.md",
                 "--reuse-reason", "Verified existing output remains valid")


    def test_interrupted_step_resumes_from_checkpoint_and_original_commit(self):
        self.add_step("research", "outputs/research.md")
        self.cli("start", "TEST-1", "research", "--agent", "tester", "--run-id", "run-resume")
        self.git("add", ".academy/state/tasks", ".academy/state/worklog")
        self.git("commit", "-qm", "persist initial run")
        self.cli("checkpoint", "TEST-1", "research", "--note", "Source A verified", "--next-action", "Verify Source B")
        self.git("add", ".academy/state/tasks", ".academy/state/worklog")
        self.git("commit", "-qm", "persist checkpoint")
        resumed = self.cli("start", "TEST-1", "research", "--agent", "tester", "--resume")
        self.assertIn("Resumed", resumed)
        resumed_state = json.loads((self.root/'.academy/state/tasks/TEST-1.json').read_text(encoding='utf-8'))
        self.assertEqual(resumed_state['steps'][0]['run_id'], 'run-resume')
        output = self.root / "outputs/research.md"
        output.write_text("resumed output\n", encoding="utf-8")
        self.git("add", "outputs/research.md")
        self.git("commit", "-qm", "finish resumed work")
        self.cli("complete", "TEST-1", "research", "--agent", "tester")
        self.assertIn("SKIP", self.cli("status", "TEST-1"))

    def test_path_validation_rejects_absolute_inputs(self):
        absolute = self.cli("add-step", "TEST-1", "absolute", "--title", "absolute",
                            "--definition-version", "v1", "--input-paths", "/etc/passwd",
                            "--output-paths", "outputs/a.md", expected=2)
        self.assertIn("Unsafe repository-relative path", absolute)

    def test_path_validation_rejects_symlink_components(self):
        from scripts import taskctl

        link = self.root / "docs/link.md"

        # Simulate the filesystem metadata result so this unit test exercises
        # the guard without requiring the host to create an operating-system symlink.
        with patch.object(taskctl, "ROOT", self.root):
            with patch.object(taskctl.Path, "is_symlink", autospec=True) as is_symlink:
                is_symlink.side_effect = lambda candidate: candidate == link
                with self.assertRaisesRegex(taskctl.TaskError, "Symlink path components are not allowed"):
                    taskctl.relpath("docs/link.md")
                is_symlink.assert_any_call(link)

    def test_taskctl_does_not_offer_human_approval_or_publication_commands(self):
        result = subprocess.run(
            [os.environ.get("PYTHON", "python"), "scripts/taskctl.py", "approve", "TEST-1"],
            cwd=self.root, text=True, capture_output=True
        )
        self.assertNotEqual(result.returncode, 0)
        result = subprocess.run(
            [os.environ.get("PYTHON", "python"), "scripts/taskctl.py", "publish", "TEST-1"],
            cwd=self.root, text=True, capture_output=True
        )
        self.assertNotEqual(result.returncode, 0)

    def edit_state(self, edit):
        path = self.root / '.academy/state/tasks/TEST-1.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        edit(data)
        path.write_text(json.dumps(data, indent=2), encoding='utf-8')
        self.git('add', '.academy')
        self.git('commit', '-qm', 'update task contract')

    def test_status_is_read_only_and_reconcile_is_explicit(self):
        self.add_step('research', 'outputs/research.md')
        self.execute_step('research', 'outputs/research.md')
        (self.root / 'docs/input.md').write_text('changed\n', encoding='utf-8')
        paths = [self.root / '.academy/state/tasks/TEST-1.json', self.root / '.academy/state/worklog/TEST-1.jsonl']
        before = [p.read_bytes() for p in paths]
        self.assertIn('STALE', self.cli('status', 'TEST-1'))
        self.assertEqual(before, [p.read_bytes() for p in paths])
        self.cli('reconcile', 'TEST-1')
        self.assertNotEqual(before, [p.read_bytes() for p in paths])

    def test_task_hold_blocks_start_resume_and_complete(self):
        self.add_step('research', 'outputs/research.md')
        self.cli('hold', 'TEST-1', '--reason', 'User stopped work')
        self.assertIn('paused', self.cli('start', 'TEST-1', 'research', '--agent', 'tester', expected=2))
        self.cli('resume-task', 'TEST-1', '--reason', 'User explicitly resumed')
        self.cli('start', 'TEST-1', 'research', '--agent', 'tester')
        self.cli('hold', 'TEST-1', '--state', 'awaiting-human', '--reason', 'Revision limit reached')
        self.assertIn('awaiting-human', self.cli('start', 'TEST-1', 'research', '--agent', 'tester', '--resume', expected=2))
        self.assertIn('awaiting-human', self.cli('complete', 'TEST-1', 'research', expected=2))

    def make_review_graph(self):
        self.add_step('review', 'outputs/verdict.json')
        self.add_step('revision', 'outputs/revised.md', depends=('review',))
        self.add_step('author', 'outputs/lesson.md', depends=('review',))
        def edit(data):
            data['steps'][0]['review'] = {'artifact_paths': ['docs/input.md'], 'verdict_path': 'outputs/verdict.json'}
            data['steps'][2]['requires_reviews'] = ['review']
        self.edit_state(edit)

    def write_verdict(self, verdict='ready-for-human-review', findings=None, digest=None):
        result = {'verdict': verdict, 'artifact_hashes': {'docs/input.md': digest or hashlib.sha256((self.root/'docs/input.md').read_bytes()).hexdigest()}, 'findings': findings or []}
        (self.root/'outputs/verdict.json').write_text(json.dumps(result), encoding='utf-8')
        self.git('add', 'outputs/verdict.json')
        self.git('commit', '-qm', 'review result')

    def test_negative_review_completes_but_only_revision_is_ready(self):
        self.make_review_graph()
        self.cli('start', 'TEST-1', 'review', '--agent', 'tester')
        self.write_verdict('block', [{'id':'T1','severity':'blocker','status':'open'}])
        self.cli('complete', 'TEST-1', 'review')
        output = self.cli('status', 'TEST-1')
        self.assertIn('- review: SKIP', output)
        self.assertIn('- revision: READY', output)
        self.assertIn('- author: BLOCKED', output)
        self.assertIn('verdict is block', self.cli('start', 'TEST-1', 'author', '--agent', 'tester', expected=2))

    def test_clear_review_unlocks_gate_and_content_change_invalidates_it(self):
        self.make_review_graph()
        self.cli('start', 'TEST-1', 'review', '--agent', 'tester')
        self.write_verdict()
        self.cli('complete', 'TEST-1', 'review')
        self.assertIn('- author: READY', self.cli('status', 'TEST-1'))
        (self.root/'docs/input.md').write_text('new content\n', encoding='utf-8')
        self.git('add', 'docs/input.md')
        self.git('commit', '-qm', 'change reviewed content')
        self.assertIn('- author: BLOCKED', self.cli('status', 'TEST-1'))

    def test_review_rejects_wrong_hash_and_false_clear_verdict(self):
        self.make_review_graph()
        self.cli('start', 'TEST-1', 'review', '--agent', 'tester')
        self.write_verdict(digest='0'*64)
        self.assertIn('artifact hashes', self.cli('complete', 'TEST-1', 'review', expected=2))
        self.write_verdict(findings=[{'id':'T1','severity':'major','status':'open'}])
        self.assertIn('unresolved material', self.cli('complete', 'TEST-1', 'review', expected=2))

    def test_runtime_metadata_and_usage_are_recorded_without_inference(self):
        self.add_step('research', 'outputs/research.md')
        self.cli('start', 'TEST-1', 'research', '--agent', 'tester', '--model', 'fixture-model', '--reasoning-effort', 'medium')
        (self.root/'outputs/research.md').write_text('result\n', encoding='utf-8')
        self.git('add', 'outputs/research.md')
        self.git('commit', '-qm', 'produce result')
        (self.root/'outputs/usage.json').write_text('{"input_tokens": 100, "output_tokens": 10}', encoding='utf-8')
        self.cli('complete', 'TEST-1', 'research', '--usage-file', 'outputs/usage.json')
        event=json.loads((self.root/'.academy/state/worklog/TEST-1.jsonl').read_text(encoding='utf-8').splitlines()[-1])
        self.assertEqual(event['runtime']['model'], 'fixture-model')
        self.assertEqual(event['usage'], {'input_tokens':100,'output_tokens':10})

    def test_revision_budget_blocks_third_automated_run(self):
        self.add_step('revision', 'outputs/revision.md')
        def edit(data):
            data['steps'][0].update(revision_cycle=1, attempts=2)
        self.edit_state(edit)
        self.assertIn('Two automated revision', self.cli('start', 'TEST-1', 'revision', '--agent', 'tester', expected=2))


if __name__ == "__main__":
    unittest.main()
