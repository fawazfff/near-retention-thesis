# Hosted dashboard

`index.html` is the published Apple-inspired research dashboard. It loads the supplied aggregate cohort export from `data/retention.csv` and the calculated summary from `data/summary.json`.

The dashboard does not run BigQuery or fetch live chain data. The CSV did not include its original BigQuery job ID, exact execution timestamp, bytes processed, or query hash. These are marked as unavailable rather than estimated or invented.

The repository also contains a reproducible Python analysis pipeline. Run `python rebuild.py` to regenerate the report and thesis from the canonical `data/retention.csv`. That older report generator is maintained separately from the published dashboard design; do not replace `docs/index.html` with its output unless intentionally migrating the design.

Run `python rebuild.py --demo` only for a clearly labelled synthetic preview under `demo/`. It does not overwrite the supplied research data or published dashboard.
