"""Example 06: H3 performance benchmarks."""

import time

import h3
import numpy as np

# Generate synthetic points
np.random.seed(42)
n = 10000
lats = np.random.uniform(28.95, 29.05, n)
lngs = np.random.uniform(-80.95, -80.90, n)

# Benchmark 1: point-to-cell conversion
start = time.time()
cells = [h3.latlng_to_cell(lat, lng, 9) for lat, lng in zip(lats, lngs)]
elapsed = time.time() - start
print(f"Point-to-cell: {n} points in {elapsed:.3f}s ({n / elapsed:.0f} pts/sec)")

# Benchmark 2: cell-to-point conversion
start = time.time()
points = [h3.cell_to_latlng(cell) for cell in cells]
elapsed = time.time() - start
print(f"Cell-to-point: {n} cells in {elapsed:.3f}s ({n / elapsed:.0f} cells/sec)")

# Benchmark 3: aggregation
import pandas as pd

df = pd.DataFrame({"cell": cells, "value": np.random.randint(1, 100, n)})
start = time.time()
agg = df.groupby("cell").agg(count=("value", "count"), mean=("value", "mean"))
elapsed = time.time() - start
print(f"Aggregation: {n} rows in {elapsed:.3f}s ({n / elapsed:.0f} rows/sec)")

# Benchmark 4: grid disk (neighbors)
center = h3.latlng_to_cell(29.02, -80.93, 9)
start = time.time()
for _ in range(1000):
    neighbors = h3.grid_disk(center, 2)
elapsed = time.time() - start
print(f"Grid disk (k=2): 1000 calls in {elapsed:.3f}s ({1000 / elapsed:.0f} calls/sec)")

print(f"\nUnique cells: {len(set(cells))}")
print(f"Average points per cell: {n / len(set(cells)):.1f}")
