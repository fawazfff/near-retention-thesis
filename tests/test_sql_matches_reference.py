"""Runs sql/retention.sql (translated to DuckDB) on fake transactions and checks it
returns exactly what the pure-Python reference returns. This validates the logic,
not BigQuery itself. Skipped if duckdb or sqlglot is not installed."""
import unittest
from datetime import date, datetime
from pathlib import Path

from nearret import synthetic

try:
    import duckdb
    import sqlglot
except ImportError:  # pragma: no cover
    duckdb = sqlglot = None

SQL = (Path(__file__).resolve().parent.parent / "sql" / "retention.sql").read_text()


@unittest.skipIf(duckdb is None, "pip install duckdb sqlglot to run this check")
class SqlMatchesReference(unittest.TestCase):
    def run_case(self, seed, cohort_weeks, burn_in):
        params = synthetic.make_params(date(2026, 11, 2), cohort_weeks, burn_in)
        txs = synthetic.synthetic_transactions(params, seed=seed)
        body = SQL
        for k in ("scan_start", "start_date", "end_date", "last_week_start"):
            body = body.replace("@" + k, f"DATE '{params[k]}'")
        body = body.replace("@max_weeks", str(params["max_weeks"]))
        body = body.replace("`bigquery-public-data.crypto_near_mainnet_us.transactions`", "transactions")
        duck_sql = sqlglot.transpile(body, read="bigquery", write="duckdb")[0]
        con = duckdb.connect()
        con.execute("CREATE TABLE transactions (block_date DATE, signer_account_id VARCHAR)")
        con.executemany("INSERT INTO transactions VALUES (?, ?)", [(d, a) for a, d in txs])
        got = [(v, c.date() if isinstance(c, datetime) else c, int(k), int(n))
               for v, c, k, n in con.execute(duck_sql).fetchall()]
        self.assertEqual(sorted(got), sorted(synthetic.reference_retention(txs, params)))

    def test_default_shape(self):
        self.run_case(seed=3, cohort_weeks=30, burn_in=8)

    def test_other_seed_and_burn_in(self):
        self.run_case(seed=11, cohort_weeks=24, burn_in=12)


if __name__ == "__main__":
    unittest.main()
