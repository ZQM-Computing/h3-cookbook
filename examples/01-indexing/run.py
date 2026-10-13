#!/usr/bin/env python3
"""Example 01: H3 indexing — point to cell, cell to point."""
import h3

# Point to H3 cell
lat, lng = 29.02, -80.93
cell = h3.latlng_to_cell(lat, lng, 9)
print(f"Point ({lat}, {lng}) -> H3 cell: {cell}")

# Cell to point (centroid)
center = h3.cell_to_latlng(cell)
print(f"Cell {cell} -> centroid: ({center[0]:.6f}, {center[1]:.6f})")

# Cell to boundary polygon
boundary = h3.cell_to_boundary(cell)
print(f"Cell boundary: {len(boundary)} vertices")
for vertex in boundary[:3]:
    print(f"  {vertex}")
print("  ...")

# Different resolutions
for res in range(5, 16, 2):
    c = h3.latlng_to_cell(lat, lng, res)
    area_km2 = h3.cell_area(c, unit="km^2")
    print(f"Resolution {res}: cell={c}, area={area_km2:.6f} km2")
