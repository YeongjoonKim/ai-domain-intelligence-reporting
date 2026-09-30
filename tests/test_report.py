"""실제 사업 규칙이 아닌 합성 데이터의 의미 경계를 검사한다."""
import json
from pathlib import Path
import unittest
from src.report_demo import build_report, grounded_projection, markdown

DATA = json.loads((Path(__file__).parents[1] / "examples/observations.json").read_text())


class ReportTests(unittest.TestCase):
    def test_decimal_change(self):
        result = build_report(DATA)
        self.assertEqual(result["insights"][0]["delta"], "12")
        self.assertEqual(result["insights"][0]["percent"], "15.00")

    def test_insufficient_history(self):
        self.assertEqual(build_report(DATA)["insights"][-1]["status"], "insufficient_history")

    def test_units_not_mixed(self):
        rows = [dict(DATA[0]), dict(DATA[1], unit="baskets")]
        self.assertTrue(all(x["status"] == "insufficient_history"
                            for x in build_report(rows)["insights"]))

    def test_zero_baseline(self):
        result = build_report([dict(DATA[0], value="0"), DATA[1]])
        self.assertIsNone(result["insights"][0]["percent"])

    def test_future_rejected(self):
        result = build_report([dict(DATA[0], period="2031-01-01")])
        self.assertEqual(len(result["rejected"]), 1)

    def test_invalid_numbers(self):
        for value in ["NaN", "Infinity", "-1", "text", True]:
            with self.subTest(value=value):
                self.assertEqual(len(build_report([dict(DATA[0], value=value)])["rejected"]), 1)

    def test_private_origin_rejected(self):
        self.assertEqual(build_report([dict(DATA[0], synthetic=False)])["insights"], [])

    def test_duplicate_id_rejected(self):
        self.assertEqual(len(build_report([DATA[0], DATA[0]])["rejected"]), 1)

    def test_same_period_conflict(self):
        result = build_report([DATA[0], dict(DATA[1], period=DATA[0]["period"])])
        self.assertEqual(result["insights"][0]["status"], "conflicting_period")

    def test_claim_projection(self):
        report = build_report(DATA)
        self.assertTrue(grounded_projection(report["insights"], report))
        self.assertFalse(grounded_projection([dict(report["insights"][0], delta="999")], report))

    def test_render_discloses_mock(self):
        output = markdown(build_report(DATA))
        self.assertIn("Reconstructed Public Demo", output)
        self.assertIn("No LLM", output)

    def test_markup_not_allowed_in_identifiers(self):
        result = build_report([dict(DATA[0], item="<script>alert(1)</script>")])
        self.assertEqual(result["insights"], [])
        self.assertEqual(len(result["rejected"]), 1)


if __name__ == "__main__":
    unittest.main()
