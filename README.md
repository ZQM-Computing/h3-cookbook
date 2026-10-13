# H3 Patterns

Production-tested H3 hexagonal hierarchical grid patterns for geospatial aggregation and indexing.

## Who this is for

Data scientists, urban planners, and logistics analysts.

## What's inside

- `examples/` — Runnable scripts with sample data
- `tests/` — Validation tests for each pattern

## Patterns

| # | Pattern | Description |
|---|---------|-------------|
| 1 | Indexing | Point to cell, cell to point |
| 2 | Aggregation | Bin and aggregate by H3 cell |
| 3 | Visualization | Static and interactive maps |
| 4 | Comparison | H3 vs S2 vs Geohash |
| 5 | DuckDB integration | H3 in analytical queries |
| 6 | Performance | Benchmarks and optimization |

## Requirements

- Python 3.11+
- h3 >= 4.0
- DuckDB >= 1.0

## Quick start

```bash
pip install -e .
pytest
```

## License

MIT — see LICENSE file.

## Related repositories

- [ZQM Geospatial Patterns](https://github.com/ZQM-Computing/geospatial-patterns) — umbrella index of all geospatial pattern repos
- [postgis-patterns](https://github.com/ZQM-Computing/postgis-patterns) — production PostGIS patterns & best practices
- [duckdb-spatial-patterns](https://github.com/ZQM-Computing/duckdb-spatial-patterns) — DuckDB Spatial patterns for analytical geospatial SQL
- [geospatial-api-reference](https://github.com/ZQM-Computing/geospatial-api-reference) — OGC API - Features with FastAPI + PostGIS
- [qgis-resources](https://github.com/ZQM-Computing/qgis-resources) — QGIS expressions, PyQGIS, styles, and QField guides
- [proxmox-ceph-operations](https://github.com/ZQM-Computing/proxmox-ceph-operations) — Proxmox VE + Ceph operations runbooks
- [ollama-fleet-patterns](https://github.com/ZQM-Computing/ollama-fleet-patterns) — Ollama fleet operations & a minimal RAG reference

*Part of [ZQM Labs](https://github.com/ZQM-Computing) — games, gear & a little mischief.*

