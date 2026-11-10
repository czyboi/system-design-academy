"""Full-source coverage regressions; these fixtures do not claim teaching quality."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_course_coverage as checker

ROOT = Path(__file__).resolve().parents[1]


class FullCoverageTests(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.root = Path(self.temp.name)
        self.root_patch = patch.object(checker, 'ROOT', self.root)
        self.root_patch.start()
        self.inventory = {'repository': checker.PRIMER, 'revision': 'a' * 40, 'entries': [
            {'id': 'replication', 'kind': 'topic', 'locator': 'README.md#replication'},
            {'id': 'tuning', 'kind': 'topic', 'locator': 'README.md#sql-tuning'},
            {'id': 'translations', 'kind': 'resource', 'locator': 'README-vi.md', 'rationale': 'Duplicate language resource'},
        ]}
        self.write_inventory()
        (self.root / 'plan.md').write_text('# Plan\n## SD-01 Replication\nReplica mechanisms\n## SD-02 Tuning\nQuery diagnosis\n', encoding='utf-8')
        self.rows = [dict(topic_id='replication', lesson='SD-01', outline='Replica mechanisms', disposition='mapped'),
                     dict(topic_id='tuning', lesson='SD-02', outline='Query diagnosis', disposition='merged')]
        self.write_matrix()

    def tearDown(self):
        self.root_patch.stop()
        self.temp.cleanup()

    def write_inventory(self):
        (self.root / 'inventory.json').write_text(json.dumps(self.inventory), encoding='utf-8')

    def write_matrix(self):
        fields = ['topic_id', 'lesson', 'outline', 'disposition', 'lesson_path', 'section', 'lesson_sha256']
        with (self.root / 'matrix.csv').open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.rows)

    def errors(self, stage='plan', review=None):
        return checker.validate('inventory.json', 'matrix.csv', 'plan.md', stage, review)

    def add_teaching(self):
        for row in self.rows:
            path = self.root / (row['lesson'] + '.md')
            path.write_text(f"---\nid: {row['lesson']}\nstatus: draft\n---\n# Lesson\n## Mechanism\nAn explanation for the structural test.\n", encoding='utf-8')
            row.update(lesson_path=path.name, section='Mechanism', lesson_sha256=checker.digest(path))
        self.write_matrix()

    def write_review(self, stage='plan'):
        paths = ['inventory.json', 'matrix.csv', 'plan.md']
        if stage == 'taught':
            paths += [row['lesson_path'] for row in self.rows]
        self.review = {'verdict': 'ready-for-human-review', 'artifact_hashes': {p: checker.digest(self.root / p) for p in paths},
                       'checks': {'coverage': 'pass', 'pedagogy': 'pass'}, 'findings': []}
        self.save_review()

    def save_review(self):
        (self.root / 'review.json').write_text(json.dumps(self.review), encoding='utf-8')

    def test_full_plan_maps_all_topics_and_resources_do_not_inflate_it(self):
        self.assertEqual(self.errors(), [])

    def test_dropped_topic_cannot_pass(self):
        self.rows.pop()
        self.write_matrix()
        self.assertIn('Missing knowledge topic: tuning', self.errors())

    def test_deferred_or_optional_knowledge_cannot_pass_full_coverage(self):
        for disposition in ('optional', 'deferred', 'outside-scope', 'mention-only', 'assessment-only'):
            with self.subTest(disposition=disposition):
                self.rows[0]['disposition'] = disposition
                self.write_matrix()
                self.assertTrue(any('cannot defer' in e for e in self.errors()))

    def test_duplicate_inventory_or_matrix_and_unknown_topics_fail(self):
        self.rows.append(dict(self.rows[0]))
        self.write_matrix()
        self.assertTrue(any('duplicate' in e for e in self.errors()))
        self.rows[-1]['topic_id'] = 'unknown'
        self.write_matrix()
        self.assertTrue(any('Unknown' in e for e in self.errors()))
        self.inventory['entries'].append(dict(self.inventory['entries'][0]))
        self.write_inventory()
        self.assertTrue(any('unique' in e for e in self.errors()))

    def test_inventory_must_be_pinned_and_resource_exclusions_explained(self):
        self.inventory['revision'] = 'main'
        self.write_inventory()
        self.assertTrue(self.errors())
        self.inventory['revision'] = 'a' * 40
        del self.inventory['entries'][-1]['rationale']
        self.write_inventory()
        self.assertTrue(self.errors())

    def test_outline_in_another_lesson_is_not_coverage(self):
        self.rows[0]['outline'] = 'Query diagnosis'
        self.write_matrix()
        self.assertTrue(any('inside its own lesson' in e for e in self.errors()))

    def test_planned_mapping_cannot_count_as_taught(self):
        self.assertTrue(self.errors('taught'))
        self.add_teaching()
        self.assertEqual(self.errors('taught'), [])

    def test_stale_hash_or_absent_lesson_fails_taught_gate(self):
        self.add_teaching()
        path = self.root / self.rows[0]['lesson_path']
        path.write_text(path.read_text() + '\nChanged claim.\n', encoding='utf-8')
        self.assertTrue(any('stale lesson hash' in e for e in self.errors('taught')))
        path.unlink()
        self.assertTrue(any('Missing artifact' in e for e in self.errors('taught')))

    def test_assessment_references_and_empty_headings_cannot_count_as_teaching(self):
        self.add_teaching()
        self.rows[0]['section'] = 'References'
        self.write_matrix()
        self.assertTrue(any('not teaching evidence' in e for e in self.errors('taught')))
        self.rows[0]['section'] = 'Mechanism'
        path = self.root / self.rows[0]['lesson_path']
        text = path.read_text().replace('An explanation for the structural test.', '<!-- TODO -->\n### Subheading')
        path.write_text(text, encoding='utf-8')
        self.rows[0]['lesson_sha256'] = checker.digest(path)
        self.write_matrix()
        self.assertTrue(any('empty' in e for e in self.errors('taught')))
        path.write_text(text.replace('status: draft', 'status: draft\nlesson: another.md\noutcome_map: {}'), encoding='utf-8')
        self.assertTrue(any('assessment' in e for e in self.errors('taught')))

    def test_plan_review_reuse_requires_exact_hashes_and_both_checks(self):
        self.write_review()
        self.assertEqual(self.errors(review='review.json'), [])
        self.review['checks']['pedagogy'] = 'revise'
        self.save_review()
        self.assertTrue(self.errors(review='review.json'))
        self.write_review()
        (self.root / 'plan.md').write_text((self.root / 'plan.md').read_text() + '\nChanged scope\n', encoding='utf-8')
        self.assertTrue(any('artifact hashes' in e for e in self.errors(review='review.json')))

    def test_negative_or_false_clear_review_cannot_be_reused(self):
        self.write_review()
        self.review['verdict'] = 'revise'
        self.save_review()
        self.assertTrue(self.errors(review='review.json'))
        self.review['verdict'] = 'ready-for-human-review'
        self.review['findings'] = [{'id': 'P1', 'severity': 'major', 'status': 'open'}]
        self.save_review()
        self.assertTrue(any('unresolved material' in e for e in self.errors(review='review.json')))

    def test_final_course_review_binds_all_taught_artifacts(self):
        self.add_teaching()
        self.write_review('taught')
        self.assertEqual(self.errors('taught', 'review.json'), [])
        del self.review['artifact_hashes'][self.rows[0]['lesson_path']]
        self.save_review()
        self.assertTrue(self.errors('taught', 'review.json'))

    def test_missing_malformed_or_escaping_inputs_fail_closed(self):
        for contents in ('[]', '{bad', '{}'):
            (self.root / 'inventory.json').write_text(contents, encoding='utf-8')
            self.assertTrue(self.errors())
        self.assertTrue(checker.validate('../inventory.json', 'matrix.csv', 'plan.md'))

    def test_fake_headings_and_title_are_not_teaching_sections(self):
        for text, heading in [('# Lesson\n## References\nA URL\n', 'Lesson'),
                              ('# Lesson\n```md\n## Mechanism\nFake\n```\n', 'Mechanism'),
                              ('# Lesson\n<!--\n## Mechanism\nFake\n-->\n', 'Mechanism')]:
            with self.subTest(heading=heading, text=text):
                with self.assertRaises(ValueError):
                    checker.section(text, heading)

    def test_real_heading_ignores_duplicate_inside_code(self):
        text = '# Lesson\n## Reference architecture\nActual explanation.\n```md\n## Reference architecture\nExample\n```\n'
        self.assertIn('Actual explanation', checker.section(text, 'Reference architecture'))
        self.add_teaching()
        path = self.root / self.rows[0]['lesson_path']
        path.write_text(path.read_text().replace('## Mechanism', '## Reference architecture'), encoding='utf-8')
        self.rows[0].update(section='Reference architecture', lesson_sha256=checker.digest(path))
        self.write_matrix()
        self.assertEqual(self.errors('taught'), [])


if __name__ == '__main__':
    unittest.main()
