# Data files

The production dataset is committed here:

- `retention.csv`: the supplied aggregate BigQuery export (1,768 data rows; four filter variants; 40 weekly cohorts).
- `run_meta.json`: source table and date-window parameters.

The CSV is also mirrored at `docs/data/retention.csv` because the static research page reads that published copy. Keep both copies identical when updating the dataset.

To validate the production data locally:

```bash
python -c "from pathlib import Path; from nearret.metrics import load, analyse; data, meta = load(Path('data/retention.csv'), Path('data/run_meta.json')); print(analyse(data)['headline']['verdict'])"
python -m unittest -v
python rebuild.py  # refresh THESIS.md without overwriting docs/index.html
```

Do not use `python rebuild.py --demo` for submission data. Demo data is synthetic and lives under the ignored `demo/` directory.
