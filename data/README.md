# Research data

This directory contains the exact metadata and result artifacts used by the dashboard and generated thesis.

- `schema.json`: live table/column inventory, including partition metadata.
- `metrics.json`: calculated cohort metrics and chart data.

Do not commit credentials, temporary query exports containing secrets, or fabricated/sample metrics. The dashboard intentionally renders an empty state when no complete metrics artifact exists.
