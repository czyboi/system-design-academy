"""Regression tests for teaching/assessment separation and scoped validation."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import validate_content as validator
from scripts import taskctl

ROOT = Path(__file__).resolve().parents[1]


class ContentContractTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.tmp'
        base.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.temp.name)
        self.lesson = self.root/'TEST-1.md'
        self.assessment = self.root/'assessment.md'
        self.lesson.write_text('''---
id: TEST-1
title: Test lesson
status: draft
level: intermediate
source_review_date: 2026-11-11
prerequisites: []
outcomes: [LO-1]
assessment: PLACEHOLDER_ASSESSMENT
---
# Test lesson
## Learning outcomes
LO-1: Make a decision.
## Problem and motivation
Choose a representation for this workload.
## Core concepts and mechanisms
Explanation.
## Worked example
Apply the decision criteria to one request.
## Trade-offs and failure modes
Discuss what happens when the input changes.
## References
- https://example.com/reference-a
- https://example.com/reference-b
''', encoding='utf-8')
        lesson_path = self.lesson.relative_to(ROOT).as_posix()
        assessment_path = self.assessment.relative_to(ROOT).as_posix()
        self.lesson.write_text(
            self.lesson.read_text().replace('PLACEHOLDER_ASSESSMENT', assessment_path),
            encoding='utf-8'
        )
        self.assessment.write_text(f'''---
id: TEST-1-assessment
status: draft
lesson: {lesson_path}
outcome_map:
  LO-1:
    taught_in: Core concepts and mechanisms
    items: [Q1, EX-1]
---
# Assessment
## Practical exercise
EX-1: Solve this problem.
## Knowledge checks
'''+''.join(f'### Q{i}\nQuestion.\nAnswer: Yes.\nExplanation: Reason.\n' for i in range(1,6))+'## Answer key / rubric\nSolution.\n', encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def pair_errors(self):
        return validator.validate_pair(self.lesson,self.assessment)

    def test_separate_pair_maps_every_outcome(self):
        self.assertEqual(self.pair_errors(), [])

    def test_lesson_scope_accepts_a_complete_pair_without_a_duration(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', self.assessment.relative_to(ROOT).as_posix(),
            ])
        self.assertEqual(result, 0, output.getvalue())

    def test_heading_wording_does_not_control_data_validation(self):
        with self.lesson.open('a', encoding='utf-8') as f:
            f.write('## Knowledge check\nA question for the reader\n')
        self.assertEqual(self.pair_errors(), [])

    def test_missing_companion_and_same_path_are_rejected(self):
        self.assertTrue(validator.validate_pair(self.lesson,self.lesson))
        self.assessment.unlink()
        self.assertTrue(self.pair_errors())

    def test_missing_explanation_is_quality_review_but_outcome_keys_are_structural(self):
        text = self.assessment.read_text().replace('Explanation: Reason.', '', 1)
        self.assessment.write_text(text, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        self.assessment.write_text(text.replace('  LO-1:', '  LO-2:'), encoding='utf-8')
        self.assertTrue(any('every lesson outcome' in x for x in self.pair_errors()))

    def test_outcome_map_labels_are_shape_checked_not_interpreted_as_quality(self):
        text = self.assessment.read_text().replace('Core concepts and mechanisms', 'Another explanation')
        text = text.replace('[Q1, EX-1]', '[Q99]')
        self.assessment.write_text(text, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        self.assessment.write_text(text.replace('items: [Q99]', 'items: []'), encoding='utf-8')
        self.assertTrue(any('heading label and item ID strings' in x for x in self.pair_errors()))

    def test_draft_required_but_question_count_not_inferred(self):
        text = self.assessment.read_text().replace('### Q5', '### Another heading')
        self.assessment.write_text(text, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        self.assessment.write_text(text.replace('status: draft', 'status: published'), encoding='utf-8')
        self.assertTrue(any('status: draft' in x for x in self.pair_errors()))

    def test_flexible_headings_do_not_block_valid_teaching(self):
        lesson = self.lesson.read_text(encoding='utf-8')
        for old, new in (
            ('Learning outcomes', 'Learning objectives'),
            ('Problem and motivation', 'Scenario and constraints'),
            ('Core concepts and mechanisms', 'Mechanism walkthrough'),
            ('Worked example', 'End-to-end design walkthrough'),
            ('Trade-offs and failure modes', 'Failure analysis and alternatives'),
            ('References', 'Primary sources'),
        ):
            lesson = lesson.replace(old, new)
        self.lesson.write_text(lesson, encoding='utf-8')
        quiz = self.assessment.read_text(encoding='utf-8')
        quiz = quiz.replace('Core concepts and mechanisms', 'Mechanism walkthrough')
        quiz = quiz.replace('## Practical exercise', '## Applied design challenge')
        quiz = quiz.replace('## Knowledge checks', '## Check your reasoning')
        quiz = quiz.replace('## Answer key / rubric', '## Solution and rubric')
        quiz = quiz.replace('### Q', '#### Q')
        self.assessment.write_text(quiz, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', self.assessment.relative_to(ROOT).as_posix(),
            ])
        self.assertEqual(result, 0, output.getvalue())

    def test_one_validation_entry_checks_missing_metadata_and_unsafe_html(self):
        self.lesson.write_text(
            self.lesson.read_text().replace('title: Test lesson\n', '') + '\n<script>unsafe</script>\n',
            encoding='utf-8'
        )
        errors = self.pair_errors()
        self.assertTrue(any("missing metadata field 'title'" in x for x in errors))
        self.assertTrue(any('raw HTML' in x for x in errors))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', self.assessment.relative_to(ROOT).as_posix(),
            ])
        self.assertEqual(result, 1, output.getvalue())

    def test_no_minimum_source_url_quota(self):
        lesson = self.lesson.read_text(encoding='utf-8').replace(
            'https://example.com/reference-b', 'Referenced primary paper'
        )
        self.lesson.write_text(lesson, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', self.assessment.relative_to(ROOT).as_posix(),
            ])
        self.assertEqual(result, 0, output.getvalue())

    def test_lesson_assessment_link_is_checked_in_both_directions(self):
        correct_path = self.assessment.relative_to(ROOT).as_posix()
        self.lesson.write_text(
            self.lesson.read_text().replace(
                f'assessment: {correct_path}',
                'assessment: modules/m01/assessments/WRONG.md'
            ), encoding='utf-8'
        )
        self.assertTrue(any('Lesson must reference its companion assessment' in issue
                            for issue in self.pair_errors()))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', correct_path,
            ])
        self.assertEqual(result, 1, output.getvalue())

    def test_semantic_assessment_quality_not_guessed_from_code_fences(self):
        front = self.assessment.read_text().split('\n---\n', 1)[0] + '\n---\n'
        fence = chr(96) * 3
        self.assessment.write_text(front + f'# Assessment\n{fence}md\nQ1\nEX-1\nrubric\n{fence}\n', encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])

    def test_bold_answer_labels_are_read_from_rendered_markdown(self):
        quiz = self.assessment.read_text()
        quiz = quiz.replace('Answer: Yes.', '**Answer:** Yes.', 1)
        quiz = quiz.replace('Explanation: Reason.', '**Explanation:** Reason.', 1)
        self.assessment.write_text(quiz, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])

    def test_empty_answers_are_quality_issues_but_bad_outcome_types_fail(self):
        quiz = self.assessment.read_text().replace('Answer: Yes.', 'Answer:   ', 1)
        self.assessment.write_text(quiz, encoding='utf-8')
        self.assertEqual(self.pair_errors(), [])
        lesson = self.lesson.read_text().replace('outcomes: [LO-1]', 'outcomes: [{unexpected: object}]')
        self.lesson.write_text(lesson, encoding='utf-8')
        self.assertTrue(any('outcomes must' in issue for issue in self.pair_errors()))

    def test_assessment_id_must_match_its_lesson(self):
        self.assessment.write_text(
            self.assessment.read_text().replace('id: TEST-1-assessment', 'id: WRONG-assessment'),
            encoding='utf-8',
        )
        self.assertTrue(any('assessment ID must match lesson ID' in x for x in self.pair_errors()))

    def test_duplicate_yaml_keys_are_rejected_by_combined_validator(self):
        lesson = self.lesson.read_text().replace('title: Test lesson', 'title: Test lesson\ntitle: Duplicate')
        self.lesson.write_text(lesson, encoding='utf-8')
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = validator.main([
                '--scope', 'lesson', '--lesson', self.lesson.relative_to(ROOT).as_posix(),
                '--assessment', self.assessment.relative_to(ROOT).as_posix(),
            ])
        self.assertEqual(result, 1, output.getvalue())


    def test_curriculum_scope_requires_real_mapping(self):
        plan=self.root/'plan.md'; matrix=self.root/'matrix.csv'
        plan.write_text('# Plan\n## SD-01\nMechanism A\n',encoding='utf-8')
        matrix.write_text('topic,locator,disposition,lesson,outline,rationale\nA,commit/path#anchor,mapped,SD-01,Mechanism A,\n',encoding='utf-8')
        self.assertEqual(validator.validate_plan(plan,matrix),[])
        matrix.write_text(matrix.read_text().replace('SD-01','SD-99'),encoding='utf-8')
        self.assertTrue(validator.validate_plan(plan,matrix))

    def test_missing_selected_plan_fails(self):
        self.assertTrue(validator.validate_plan(self.root/'missing.md',self.root/'missing.csv'))


class WorkflowTemplateTests(unittest.TestCase):
    def test_two_step_lesson_template_does_not_require_review_or_validation(self):
        template = json.loads((ROOT / '.academy/state/task.template.json').read_text())
        steps = {step['step_id']: step for step in template['steps']}
        self.assertEqual(set(steps), {'research', 'author'})
        self.assertEqual(steps['author']['depends_on'], ['research'])
        self.assertFalse(any(step.get('review') or step.get('requires_reviews')
                             for step in steps.values()))
        self.assertEqual(steps['research']['output_paths'], ['${EVIDENCE_PATH}'])
        self.assertEqual(steps['author']['output_paths'],
                         ['${TEACHING_PATH}', '${ASSESSMENT_PATH}'])
        self.assertIn('${EVIDENCE_PATH}', steps['author']['input_paths'])
        self.assertIn('.agents/skills/content-format/SKILL.md', steps['author']['input_paths'])
        self.assertIn('.agents/skills/assessment-design/SKILL.md', steps['author']['input_paths'])
        self.assertIn('GOVERNANCE.md', steps['author']['input_paths'])
        self.assertIn('content-format', (ROOT/'.codex/agents/lesson-author.toml').read_text())
        self.assertIn('content-format', (ROOT/'.claude/agents/lesson-author.md').read_text())
        self.assertEqual(template['review_status'], 'not_reviewed')

    def test_compact_templates_have_unique_output_paths(self):
        for name, count in (('task', 2), ('course', 1), ('workflow', 1)):
            data = json.loads((ROOT / f'.academy/state/{name}.template.json').read_text())
            data['task_id'] = 'TEST-TEMPLATE'
            taskctl.validate_json_schema(data, ROOT / '.academy/state/schema/task.schema.json', 'Template')
            self.assertEqual(len(data['steps']), count)
            outputs = []
            for step in data['steps']:
                outputs.extend(step['output_paths'])
                self.assertFalse(set(step['input_paths']) & set(step['output_paths']))
                self.assertFalse(step.get('review'))
                self.assertFalse(step.get('requires_reviews'))
            self.assertEqual(len(outputs), len(set(outputs)))

    def test_template_schema(self):
        template = json.loads((ROOT / '.academy/state/task.template.json').read_text())
        template['task_id'] = 'TEST-TEMPLATE'
        taskctl.validate_json_schema(
            template, ROOT / '.academy/state/schema/task.schema.json', 'Template'
        )

    def test_repository_and_workflow_accept_isolated_empty_inventory(self):
        # Regression CI must not validate real authored lessons.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / '.agents/skills/fixture/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: fixture\ndescription: Fixture\n---\nInstructions.\n', encoding='utf-8')
            agent = root / '.codex/agents/fixture.toml'
            agent.parent.mkdir(parents=True)
            agent.write_text(
                'name = "fixture"\ndescription = "Fixture"\n'
                'developer_instructions = "Test"\nmodel = "fixture-model"\n'
                'model_reasoning_effort = "medium"\n', encoding='utf-8'
            )
            (root / '.codex/config.toml').write_text(
                '[agents]\nmax_concurrent_threads_per_session = 1\n'
                'default_subagent_model = "fixture-model"\n', encoding='utf-8'
            )
            with patch.object(validator, 'ROOT', root):
                for scope in ('repo', 'workflow'):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(validator.main(['--scope', scope]), 0)

                # Validate broken fixture lessons only, never the real repository.
                lesson = root / 'modules/fixture/lessons/BAD-L01.md'
                lesson.parent.mkdir(parents=True)
                lesson.write_text('# Missing front matter\n', encoding='utf-8')
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(validator.main(['--scope', 'repo']), 1)
                    self.assertEqual(validator.main(['--scope', 'workflow']), 0)

    def test_repo_canonical_content_rejects_nested_revisions_and_orphans(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module = root / 'modules/m01'
            lesson = module / 'lessons/M01-L02.md'
            assessment = module / 'assessments/M01-L02.md'
            lesson.parent.mkdir(parents=True)
            assessment.parent.mkdir(parents=True)
            lesson.write_text('---\nid: M01-L02\nassessment: modules/m01/assessments/M01-L02.md\n---\n', encoding='utf-8')
            assessment.write_text('---\nstatus: draft\n---\n', encoding='utf-8')
            with patch.object(validator, 'ROOT', root):
                lessons, assessments, errors = validator.discover_canonical_content()
                self.assertEqual((lessons, assessments, errors), ([lesson], [assessment], []))
                extra = module / 'assessments/M01-L03.md'
                extra.write_text('unused', encoding='utf-8')
                lessons, assessments, errors = validator.discover_canonical_content()
                self.assertIn(extra, assessments)
                nested = module / 'lessons/revision-1/M01-L02.md'
                nested.parent.mkdir()
                nested.write_text('obsolete', encoding='utf-8')
                _, _, errors = validator.discover_canonical_content()
                self.assertTrue(any('nested lesson/assessment revisions' in e for e in errors))
                (module / 'content-manifest.json').write_text('{}', encoding='utf-8')
                _, _, errors = validator.discover_canonical_content()
                self.assertTrue(any('content-manifest.json is obsolete' in e for e in errors))

    def test_repo_rejects_orphan_assessment_without_a_lesson(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / '.agents/skills/fixture/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: fixture\ndescription: Fixture\n---\nInstructions.\n', encoding='utf-8')
            agent = root / '.codex/agents/fixture.toml'
            agent.parent.mkdir(parents=True)
            agent.write_text('name = "fixture"\ndescription = "Fixture"\n'
                             'developer_instructions = "Test"\nmodel = "fixture"\n'
                             'model_reasoning_effort = "medium"\n', encoding='utf-8')
            (root / '.codex/config.toml').write_text(
                '[agents]\nmax_concurrent_threads_per_session = 1\n'
                'default_subagent_model = "fixture"\n', encoding='utf-8')
            stray = root / 'modules/m02/assessments/M02-L01.md'
            stray.parent.mkdir(parents=True)
            stray.write_text('# orphan', encoding='utf-8')
            with patch.object(validator, 'ROOT', root):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(validator.main(['--scope', 'repo']), 1)
                self.assertIn('orphan assessment', output.getvalue())


    def test_repository_link_checker_ignores_code_fences_but_checks_real_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / '.agents/skills/fixture/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: fixture\ndescription: Fixture\n---\nInstructions.\n')
            agent = root / '.codex/agents/fixture.toml'
            agent.parent.mkdir(parents=True)
            agent.write_text('name = "fixture"\ndescription = "Fixture"\n'
                             'developer_instructions = "Test"\nmodel = "fixture"\n'
                             'model_reasoning_effort = "medium"\n')
            (root / '.codex/config.toml').write_text(
                '[agents]\nmax_concurrent_threads_per_session = 1\n'
                'default_subagent_model = "fixture"\n')
            readme = root / 'README.md'
            fence = chr(96) * 3
            readme.write_text(f'{fence}md\n[example](missing-from-code.md)\n{fence}\n')
            with patch.object(validator, 'ROOT', root):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(validator.main(['--scope', 'repo']), 0, output.getvalue())
                readme.write_text(readme.read_text() + '\n[real](missing-real-link.md)\n')
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(validator.main(['--scope', 'repo']), 1)
                self.assertIn('missing-real-link.md', output.getvalue())
                self.assertNotIn('missing-from-code.md', output.getvalue())


    def test_explicit_missing_lesson_fails(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validator.main(['--scope','lesson','--lesson','.tmp/missing-lesson.md','--assessment','.tmp/missing-assessment.md']),1)


if __name__ == '__main__':
    unittest.main()
