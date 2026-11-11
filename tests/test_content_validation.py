"""Regression tests for teaching/assessment separation and scoped validation."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

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
        self.assessment.write_text(f'''---
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

    def test_assessment_leakage_is_rejected(self):
        with self.lesson.open('a',encoding='utf-8') as f:
            f.write('## Knowledge check\nA question\n')
        self.assertTrue(any('companion artifact' in x for x in self.pair_errors()))

    def test_missing_companion_and_same_path_are_rejected(self):
        self.assertTrue(validator.validate_pair(self.lesson,self.lesson))
        self.assessment.unlink()
        self.assertTrue(self.pair_errors())

    def test_missing_explanation_and_unmapped_outcome_are_rejected(self):
        text=self.assessment.read_text().replace('Explanation: Reason.','',1).replace('  LO-1:', '  LO-2:')
        self.assessment.write_text(text,encoding='utf-8')
        errors=self.pair_errors()
        self.assertTrue(any('Explanation:' in x for x in errors))
        self.assertTrue(any('every lesson outcome' in x for x in errors))

    def test_missing_taught_section_and_nonexistent_item_are_rejected(self):
        text=self.assessment.read_text().replace('Core concepts and mechanisms','Missing section').replace('[Q1, EX-1]','[Q99]')
        self.assessment.write_text(text,encoding='utf-8')
        self.assertTrue(any('existing teaching section' in x for x in self.pair_errors()))
        self.assertTrue(any('existing assessment items' in x for x in self.pair_errors()))

    def test_draft_only_and_question_count(self):
        self.assessment.write_text(self.assessment.read_text().replace('status: draft','status: published').replace('### Q5','### Q4'),encoding='utf-8')
        errors=self.pair_errors()
        self.assertTrue(any('remain draft' in x for x in errors))
        self.assertTrue(any('uniquely' in x for x in errors))

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
    def test_six_step_template_preserves_gates_without_forced_revisions(self):
        template=json.loads((ROOT/'.academy/state/task.template.json').read_text())
        steps={s['step_id']:s for s in template['steps']}
        self.assertEqual(len(steps), 6)
        self.assertIn('plan-gate',steps['author']['requires_reviews'])
        self.assertEqual(len(steps['author']['output_paths']),2)
        self.assertNotIn('revision', steps)
        self.assertFalse(any('recheck' in sid for sid in steps))
        for gate in ('technical-review', 'teaching-review'):
            self.assertIn(gate,steps['validation']['requires_reviews'])
            self.assertTrue(set(steps['author']['output_paths']).issubset(steps[gate]['review']['artifact_paths']))
            self.assertTrue(set(steps['plan-gate']['review']['artifact_paths']).issubset(steps[gate]['review']['artifact_paths']))
        self.assertIn('.agents/skills/provenance-review/SKILL.md',steps['technical-review']['input_paths'])
        self.assertIn('.agents/skills/curriculum-coverage-review/SKILL.md',steps['teaching-review']['input_paths'])
        self.assertIn('.agents/skills/pedagogical-review/SKILL.md',steps['teaching-review']['input_paths'])
        self.assertEqual(steps['technical-review']['depends_on'], ['author'])
        self.assertEqual(steps['teaching-review']['depends_on'], ['author'])
        self.assertIn('curriculum/review.json', steps['plan-gate']['input_paths'])

    def test_compact_templates_have_unique_owners_and_bound_review_inputs(self):
        for name, count in (('task', 6), ('course', 3), ('workflow', 2)):
            data=json.loads((ROOT/f'.academy/state/{name}.template.json').read_text())
            data['task_id']='TEST-TEMPLATE'
            taskctl.validate_json_schema(data,ROOT/'.academy/state/schema/task.schema.json','Template')
            self.assertEqual(len(data['steps']), count)
            outputs=[]
            for step in data['steps']:
                outputs.extend(step['output_paths'])
                self.assertFalse(set(step['input_paths']) & set(step['output_paths']))
                if step.get('review'):
                    self.assertTrue(set(step['review']['artifact_paths']).issubset(step['input_paths']))
                    self.assertIn(step['review']['verdict_path'],step['output_paths'])
            self.assertEqual(len(outputs),len(set(outputs)))

    def test_template_schema_and_role_models(self):
        import tomllib
        template=json.loads((ROOT/'.academy/state/task.template.json').read_text())
        template['task_id']='TEST-TEMPLATE'
        taskctl.validate_json_schema(template,ROOT/'.academy/state/schema/task.schema.json','Template')
        for path in (ROOT/'.codex/agents').glob('*.toml'):
            profile=tomllib.loads(path.read_text())
            self.assertIn(profile['model'],{'gpt-6.1-sol','gpt-6-astra','gpt-6.1-terra'})
            self.assertIn(profile['model_reasoning_effort'],{'medium','high'})

    def test_requested_role_model_routing(self):
        import tomllib
        config=tomllib.loads((ROOT/'.codex/config.toml').read_text())
        self.assertEqual(config['model'], 'gpt-6.1-sol')
        self.assertEqual(config['agents']['default_subagent_model'], 'gpt-6.1-terra')
        for name, model in (('workflow-architect','gpt-6.1-sol'), ('pr-reviewer','gpt-6.1-sol'),
                            ('technical-reviewer','gpt-6.1-sol'), ('spec-implementer','gpt-6.1-terra'),
                            ('lesson-author','gpt-6.1-terra'), ('curriculum-designer','gpt-6.1-sol')):
            profile=tomllib.loads((ROOT/f'.codex/agents/{name}.toml').read_text())
            self.assertEqual(profile['model'], model, name)
        self.assertIn('ambiguous', (ROOT/'.codex/agents/spec-implementer.toml').read_text())

    def test_repository_and_workflow_accept_empty_authoring_inventory(self):
        for scope in ('repo','workflow'):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validator.main(['--scope',scope]),0)

    def test_explicit_missing_lesson_fails(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(validator.main(['--scope','lesson','--lesson','.tmp/missing-lesson.md','--assessment','.tmp/missing-assessment.md']),1)


if __name__ == '__main__':
    unittest.main()
