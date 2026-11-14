# Hosted dashboard

`index.html` is the published Apple-inspired research dashboard. It loads the supplied aggregate cohort export from `data/retention.csv` and the calculated summary from `data/summary.json`.

The dashboard does not run BigQuery or fetch live chain data. It displays the committed cohort snapshot and calculated summary.

The repository also contains a reproducible Python analysis pipeline. Run `python rebuild.py` to regenerate `THESIS.md` from the canonical `data/retention.csv`; this preserves the designed dashboard. Only use `python rebuild.py --overwrite-dashboard` if you intentionally want to replace `docs/index.html` with the simpler generated report page.

Run `python rebuild.py --demo` only for a clearly labelled synthetic preview under `demo/`. It does not overwrite the supplied research data or published dashboard.
