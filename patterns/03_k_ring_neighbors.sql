-- Pattern 03: K-Ring Neighbors
-- h3.grid_disk(cell, k) returns cells within k distance
-- SELECT unnest(h3.grid_disk(cell, 2)) AS neighbor

-- K-ring for aggregation smoothing
-- SELECT cell, avg(value) OVER (PARTITION BY grid_disk(cell,1))
