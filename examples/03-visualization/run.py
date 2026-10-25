"""Example 03: Visualize H3 grids."""

import h3
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon

# Create a center cell and its neighbors
center = h3.latlng_to_cell(29.02, -80.93, 9)
neighbors = h3.grid_disk(center, 1)  # center + 6 neighbors

fig, ax = plt.subplots(figsize=(8, 8))
colors = plt.cm.viridis(np.linspace(0, 1, len(neighbors)))

for i, cell in enumerate(neighbors):
    boundary = h3.cell_to_boundary(cell)
    poly = MplPolygon(
        [(lng, lat) for lat, lng in boundary], closed=True, fill=True, facecolor=colors[i], edgecolor="black", alpha=0.7
    )
    ax.add_patch(poly)
    center_lat, center_lng = h3.cell_to_latlng(cell)
    ax.text(center_lng, center_lat, cell[-5:], ha="center", va="center", fontsize=6)

ax.set_aspect("equal")
ax.set_title(f"H3 Grid: {len(neighbors)} cells around {center}")
plt.savefig("h3_grid.png", dpi=150, bbox_inches="tight")
print("Saved to h3_grid.png")

# Heatmap: aggregate points into H3 cells and color by count
np.random.seed(42)
lats = np.random.normal(29.02, 0.01, 500)
lngs = np.random.normal(-80.93, 0.01, 500)
cells = [h3.latlng_to_cell(lat, lng, 9) for lat, lng in zip(lats, lngs)]
unique, counts = np.unique(cells, return_counts=True)

fig, ax = plt.subplots(figsize=(8, 8))
for cell, count in zip(unique, counts):
    boundary = h3.cell_to_boundary(cell)
    poly = MplPolygon(
        [(lng, lat) for lat, lng in boundary],
        closed=True,
        fill=True,
        facecolor=plt.cm.Reds(count / max(counts)),
        edgecolor="gray",
    )
    ax.add_patch(poly)

ax.set_aspect("equal")
ax.set_title("H3 Point Density Heatmap")
plt.savefig("h3_heatmap.png", dpi=150, bbox_inches="tight")
print("Saved to h3_heatmap.png")
