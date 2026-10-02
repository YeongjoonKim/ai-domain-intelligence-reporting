"""운영 집계와 합성 예제를 혼동하거나 민감 원문을 공개하지 않도록 검사한다."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


class ObservationContractTests(unittest.TestCase):
    def setUp(self):
        self.observation=json.loads((ROOT/'docs/data-inventory-20261002.json').read_text())

    def test_aggregate_only_table_contract(self):
        self.assertEqual(self.observation['kind'], 'read_only_operational_aggregate_observation_not_public_demo_fixture')
        names=[]
        for row in self.observation['tables']:
            self.assertFalse(set(row)-{'table','rows','count_kind','dates'})
            self.assertEqual(row['count_kind'],'exact')
            self.assertIs(type(row['rows']),int)
            self.assertGreaterEqual(row['rows'],0)
            names.append(row['table'])
        self.assertEqual(len(names),len(set(names)))

    def test_eligibility_not_storage_or_model_usage(self):
        funnel=self.observation['krei_eligibility_funnel']
        self.assertLessEqual(funnel['report_eligible'],funnel['current_metrics'])
        self.assertLessEqual(funnel['report_eligible'],funnel['status_eligible'])
        self.assertLessEqual(funnel['status_eligible'],funnel['all_metrics'])
        self.assertIn('not a newly generated report',self.observation['retrieval_probe']['scope'])
        self.assertNotIn('signals',self.observation['retrieval_probe']['results']['agri_weather'])

    def test_selected_screens_registered_and_provenance_documented(self):
        manifest=json.loads((ROOT/'docs/screenshots/manifest.json').read_text())
        text=(ROOT/'docs/screenshots.md').read_text()
        for name in ('protection-forecast-regions','seed-growing-degree-days','seed-insight-opening'):
            relative='docs/screenshots/'+name+'.png'
            self.assertIn(relative,manifest['files'])
            self.assertIn(name+'.png',text)
            self.assertTrue((ROOT/relative).is_file())
