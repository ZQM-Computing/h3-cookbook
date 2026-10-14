"""Example 02: Aggregate points by H3 cell."""

import h3
import numpy as np
import pandas as pd

# Create synthetic points
np.random.seed(42)
n = 1000
lats = np.random.uniform(29.00, 29.05, n)
lngs = np.random.uniform(-80.95, -80.90, n)
values = np.random.randint(1, 100, n)

# Convert to H3 cells (resolution 8)
resolution = 8
cells = [h3.latlng_to_cell(lat, lng, resolution) for lat, lng in zip(lats, lngs)]

# Aggregate by cell
df = pd.DataFrame({"cell": cells, "value": values})
agg = df.groupby("cell").agg(count=("value", "count"), mean=("value", "mean"), sum=("value", "sum")).reset_index()

print(f"Total points: {n}")
print(f"Unique H3 cells: {len(agg)}")
print("Top 5 cells by count:")
print(agg.nlargest(5, "count")[["cell", "count", "mean"]])
