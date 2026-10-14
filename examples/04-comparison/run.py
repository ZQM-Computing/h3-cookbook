"""Example 04: Compare H3 with S2 and Geohash."""

import h3

lat, lng = 29.02, -80.93

# H3
h3_cell = h3.latlng_to_cell(lat, lng, 9)
h3_area = h3.cell_area(h3_cell, unit="km^2")
print(f"H3: {h3_cell}")
print(f"  Area: {h3_area:.6f} km2")
print(f"  Boundary vertices: {len(h3.cell_to_boundary(h3_cell))}")

# H3 at different resolutions
print("\nH3 at different resolutions:")
for res in range(5, 16, 2):
    c = h3.latlng_to_cell(lat, lng, res)
    area = h3.cell_area(c, unit="km^2")
    print(f"  Resolution {res}: cell={c}, area={area:.6f} km2")

# H3 hierarchy: parent-child relationship
print("\nH3 hierarchy (parent-child):")
for res in range(5, 16, 2):
    c = h3.latlng_to_cell(lat, lng, res)
    parent = h3.cell_to_parent(c, res - 2) if res > 5 else None
    children = h3.cell_to_children(c, res + 2) if res < 15 else []
    print(f"  Res {res}: {c}")
    if parent:
        print(f"    Parent (res {res - 2}): {parent}")
    if children:
        print(f"    Children (res {res + 2}): {len(children)} cells")
