# Hosted dashboard status page

`index.html` is an honest status page. It contains no metrics because no real BigQuery result has been fetched yet.

Run `python rebuild.py --demo` to generate the full synthetic dashboard locally in `demo/index.html`. After fetching real data, run `python rebuild.py` to generate the real-data dashboard in `docs/index.html` and the written thesis.
