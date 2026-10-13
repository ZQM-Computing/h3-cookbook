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
