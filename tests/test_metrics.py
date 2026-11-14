import functools
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from nearret import metrics, render, synthetic
from compare_burnin import compare as compare_burn_in

ROOT = Path(__file__).resolve().parent.parent
LAST_WEEK = date(2026, 11, 2)  # a Monday


@functools.lru_cache(maxsize=None)
def build(trend, seed=7):
    tmp = Path(tempfile.mkdtemp())
    synthetic.write_demo(tmp, LAST_WEEK, trend=trend, seed=seed)
    data, meta = metrics.load(tmp / "retention.csv", tmp / "run_meta.json")
    return data, meta, metrics.analyse(data)


class BurnInComparisonTests(unittest.TestCase):
    def test_same_export_compares_to_zero_difference(self):
        data, meta, _ = build(0.06)
        meta12, meta26 = dict(meta), dict(meta)
        meta12["burn_in_weeks"], meta26["burn_in_weeks"] = 12, 26
        result = compare_burn_in(data, meta12, data, meta26)
        row = result["variants"]["filtered_50"]
        self.assertEqual(row["12_week_burn_in"]["week4_trend"]["verdict"],
                         row["26_week_burn_in"]["week4_trend"]["verdict"])
        self.assertEqual(row["12_week_burn_in"]["retention_by_week"],
                         row["26_week_burn_in"]["retention_by_week"])


class WilsonTests(unittest.TestCase):
    def test_known_value(self):
        p, lo, hi = metrics.wilson(50, 100)
        self.assertAlmostEqual(p, 0.5)
        self.assertAlmostEqual(lo, 0.4038, places=3)
        self.assertAlmostEqual(hi, 0.5962, places=3)

    def test_edges(self):
        self.assertEqual(metrics.wilson(0, 100)[1], 0.0)
        self.assertAlmostEqual(metrics.wilson(100, 100)[2], 1.0)


class LoadTests(unittest.TestCase):
    def test_missing_data_is_a_clear_error(self):
        with self.assertRaises(FileNotFoundError) as cm:
            metrics.load(Path("/nonexistent/retention.csv"), Path("/nonexistent/run_meta.json"))
        self.assertIn("fetch_data.py", str(cm.exception))

    def test_cohort_size_is_week_zero_and_zero_filled(self):
        data, meta, _ = build(0.06)
        c = data["all"][0]
        self.assertEqual(c.retained[0], c.size)
        newest = data["all"][-1]
        self.assertEqual(max(newest.retained), 0)  # newest cohort is only observed at k=0
        self.assertLessEqual(newest.week, metrics.last_complete_week(meta))
        self.assertTrue(all(v >= 0 for v in c.retained.values()))

    def test_filters_only_remove_accounts(self):
        data, _, _ = build(0.06)
        for a, b in zip(data["all"], data["filtered_20"]):
            self.assertGreaterEqual(a.size, b.size)


class VerdictTests(unittest.TestCase):
    def test_improving_trend_detected(self):
        self.assertEqual(build(0.12)[2]["headline"]["verdict"], "improving")

    def test_declining_trend_detected(self):
        self.assertEqual(build(-0.12)[2]["headline"]["verdict"], "declining")

    def test_flat_trend_is_not_called_a_change(self):
        self.assertEqual(build(0.0)[2]["headline"]["verdict"], "no clear change")

    def test_cohort_diagnostics_report_weighting_and_concentration(self):
        data, _, analysis = build(0.06)
        d = analysis["cohort_diagnostics"]
        self.assertEqual(d["mature_cohorts"], 36)
        self.assertGreaterEqual(d["mean_cohort_rate"], 0.0)
        self.assertGreaterEqual(d["pooled_rate"], 0.0)
        self.assertGreater(d["top_five_share"], 0.0)
        self.assertLessEqual(d["top_five_share"], 1.0)
        self.assertGreaterEqual(d["top_five_return_share"], 0.0)
        self.assertGreater(d["other_cohorts_pooled_rate"], 0.0)
        self.assertGreaterEqual(d["max_cohort_size"], d["median_cohort_size"])
        self.assertEqual(len(d["top_five_cohorts"]), 5)
        self.assertGreater(d["top_five_accounts_all"], d["top_five_accounts_filtered20"])
        self.assertIn("all_accounts", d["top_five_cohorts"][0])

    def test_group_size_and_ordering(self):
        h = build(0.06)[2]["headline"]
        self.assertEqual(h["group_size"], 8)
        self.assertLess(h["early_span"][1], h["recent_span"][0])

    def test_too_few_cohorts_raises(self):
        data, _, _ = build(0.06)
        with self.assertRaises(ValueError):
            metrics.compare_groups(data["all"][:10])


class RenderTests(unittest.TestCase):
    def test_thesis_has_no_unfilled_placeholders_and_demo_banner(self):
        _, meta, a = build(0.06)
        text = render.build_thesis(a, meta, ROOT / "templates" / "THESIS.template.md", demo=True)
        self.assertNotIn("{{", text)
        self.assertIn("SYNTHETIC DEMO DATA", text)

    def test_html_demo_banner_and_numbers(self):
        _, meta, a = build(0.06)
        html = render.build_html(a, meta, "SELECT 1", demo=True)
        self.assertIn("SYNTHETIC DEMO DATA", html)
        self.assertIn(a["headline"]["verdict"], html)

    def test_real_render_has_no_banner(self):
        _, meta, a = build(0.06)
        html = render.build_html(a, meta, "SELECT 1", demo=False)
        self.assertNotIn("SYNTHETIC DEMO DATA", html)

    def test_supplied_data_thesis_renders_without_unknown_metadata_claims(self):
        canonical_csv = ROOT / "data" / "retention.csv"
        published_csv = ROOT / "docs" / "data" / "retention.csv"
        meta_path = ROOT / "data" / "run_meta.json"
        self.assertEqual(canonical_csv.read_bytes(), published_csv.read_bytes())
        data, meta = metrics.load(canonical_csv, meta_path)
        self.assertEqual(meta["row_count"], len(canonical_csv.read_text().splitlines()) - 1)
        analysis = metrics.analyse(data)
        summary = json.loads((ROOT / "docs" / "data" / "summary.json").read_text())
        self.assertEqual(summary["protocol_economics_status"]["active_maximum_annual_issuance_percent"], 2.5)
        self.assertEqual(summary["protocol_economics_status"]["hsp_029"]["target_issuance_percent"], 1.6)
        self.assertEqual(summary["protocol_economics_status"]["hsp_027"]["developer_gas_rebate_percent"], 0)
        self.assertIn("90-day grace period", summary["protocol_economics_status"]["hsp_029"]["status"])
        self.assertEqual(summary["security_risks"][0]["reported_amount_usd"], 3800000)
        self.assertEqual(summary["market_context"]["defillama_trailing_year_revenue_usd"], 9640000)
        self.assertGreater(summary["market_context"]["defillama_tvl_usd"], summary["market_context"]["coingecko_tvl_usd"])
        self.assertAlmostEqual(summary["cohort_diagnostics"]["pooled_rate_percent"],
                               analysis["cohort_diagnostics"]["pooled_rate"] * 100, places=10)
        windows = analysis["retention_windows"]
        self.assertEqual([x["week"] for x in windows], [1, 4, 8, 12])
        self.assertEqual([x["cohorts"] for x in windows], [39, 36, 32, 28])
        self.assertEqual([x["accounts"] for x in windows], [4695104, 4627825, 3941854, 3906626])
        self.assertEqual([x["returned"] for x in windows], [44255, 18989, 11345, 8007])
        text = render.build_thesis(analysis, meta, ROOT / "templates" / "THESIS.template.md", demo=False)
        self.assertNotIn("{{", text)
        self.assertIn("2.41%", text)
        self.assertIn("0.41%", text)
        self.assertIn("job ID, query execution timestamp, bytes processed and query hash were not included", text)
        self.assertIn("Investment interpretation", text)
        self.assertGreater(analysis["cohort_diagnostics"]["top_five_share"], 0.8)
        self.assertAlmostEqual(analysis["cohort_diagnostics"]["top_five_return_share"], 0.24, places=2)
        page = (ROOT / "docs" / "index.html").read_text()
        self.assertIn("88.4%", page)
        attribution = (ROOT / "sql" / "contract_attribution.sql").read_text()
        self.assertIn("@max_first_week_transactions", attribution)
        self.assertIn("receiver_interactions", attribution)
        self.assertNotIn("FUNCTION_CALL", attribution)
        sql = (ROOT / "sql" / "retention.sql").read_text()
        self.assertIn("bigquery-public-data.crypto_near_mainnet_us.transactions", sql)
        self.assertNotIn("bigquery-public-data.crypto_near_mainnet.transactions", sql)
        self.assertIn("id=\"milestoneRows\"", page)
        self.assertIn("id=\"outlierRows\"", page)
        self.assertIn("After &gt;20 filter", page)
        self.assertIn("0.082%", page)
        self.assertIn("id=\"economics\"", page)
        self.assertIn("26-week comparison", page)
        self.assertIn("contract_attribution.sql", page)


if __name__ == "__main__":
    unittest.main()


class FetchHelpersTests(unittest.TestCase):
    def test_output_paths_keep_default_rebuild_compatible(self):
        import fetch_data
        default_csv, default_meta = fetch_data.output_paths(ROOT / "data", "retention")
        long_csv, long_meta = fetch_data.output_paths(ROOT / "data", "retention_26w")
        self.assertEqual(default_csv.name, "retention.csv")
        self.assertEqual(default_meta.name, "run_meta.json")
        self.assertEqual(long_csv.name, "retention_26w.csv")
        self.assertEqual(long_meta.name, "retention_26w_meta.json")

    def test_window_is_monday_aligned_and_complete(self):
        import fetch_data
        w = fetch_data.window(date(2026, 11, 13), cohort_weeks=40, burn_in_weeks=12, max_weeks=12)
        self.assertEqual(w["last_week_start"], "2026-11-02")      # Monday of last complete week
        self.assertEqual(w["end_date"], "2026-11-08")             # Sunday before today's week
        self.assertEqual(date.fromisoformat(w["start_date"]).weekday(), 0)
        self.assertEqual(date.fromisoformat(w["scan_start"]).weekday(), 0)
        self.assertEqual((date.fromisoformat(w["last_week_start"]) - date.fromisoformat(w["start_date"])).days // 7 + 1, 40)
        w26 = fetch_data.window(date(2026, 11, 13), 40, 26, 12, date(2026, 11, 2))
        self.assertEqual(w26["start_date"], w["start_date"])
        self.assertEqual(w26["last_week_start"], w["last_week_start"])
        self.assertEqual(w26["scan_start"], "2025-08-04")
        self.assertEqual(w["scan_start"], "2025-11-10")

    def test_fixed_last_week_start_rejects_non_monday(self):
        import fetch_data
        with self.assertRaises(ValueError):
            fetch_data.window(date(2026, 11, 13), 40, 26, 12, date(2026, 11, 3))

    def test_window_rejects_too_short_cohort_history(self):
        import fetch_data
        with self.assertRaises(ValueError):
            fetch_data.window(date(2026, 11, 13), cohort_weeks=18, burn_in_weeks=12, max_weeks=12)

    def test_literals_leave_no_parameters(self):
        import fetch_data
        w = fetch_data.window(date(2026, 11, 13), 40, 12, 12)
        sql = fetch_data.with_literals((ROOT / "sql" / "retention.sql").read_text(), w)
        self.assertNotIn("@scan_start", sql)
        self.assertNotIn("@max_weeks", sql)
        self.assertIn("DATE '2026-11-02'", sql)
