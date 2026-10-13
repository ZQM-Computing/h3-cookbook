#!/usr/bin/env python3
"""Example 05: H3 in DuckDB analytical queries."""
import duckdb

# Load DuckDB H3 extension (community extension)
con = duckdb.connect()
con.execute("INSTALL h3 FROM community; LOAD h3;")

# Create synthetic data with lat/lng
con.execute("""
    CREATE TABLE points AS
    SELECT * FROM (VALUES
        (29.02, -80.93, 10),
        (29.03, -80.92, 20),
        (29.01, -80.91, 30),
        (29.04, -80.90, 40),
        (29.00, -80.94, 50)
    ) AS t(lat, lng, value)
""")

# Query 1: count by H3 cell
result1 = con.execute("""
    SELECT
        h3_latlng_to_cell(lat, lng, 8) as h3_cell,
        COUNT(*) as cnt,
        AVG(value) as avg_value
    FROM points
    GROUP BY h3_cell
    ORDER BY cnt DESC
""").fetchdf()
print("Aggregation by H3 cell:")
print(result1)

# Query 2: spatial join with H3 cells
result2 = con.execute("""
    SELECT
        h3_latlng_to_cell(lat, lng, 8) as h3_cell,
        COUNT(*) as cnt,
        SUM(value) as total
    FROM points
    GROUP BY h3_cell
    HAVING COUNT(*) >= 1
""").fetchdf()
print("\nFiltered aggregation:")
print(result2)

con.close()
