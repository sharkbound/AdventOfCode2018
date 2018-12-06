import numpy as np

PLOT_GRID = False

WIDTH = 354
HEIGHT = 359

grid = np.zeros((WIDTH, HEIGHT), dtype=np.int)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def closest_point(point):
    distances = [(manhattan_distance(point, p[:-1]), p) for p in points]
    min_dist, min_point = min(distances, key=lambda x: x[0])

    if any(1 for dist, p in distances if dist == min_dist and p[2] != min_point[2]):
        return None

    return min_point


seen_points = set()
DEFAULT_POINT_ID = 0, 0, 0

with open('data.txt') as f:
    points = [(*map(int, line.split(',')), i) for i, line in enumerate(f, 1)]

for i, p in enumerate(points, 1):
    grid[p[:-1]] = i
    seen_points.add(p[:-1])

for i, _ in np.ndenumerate(grid):
    if i in seen_points:
        if PLOT_GRID:
            grid[i] = 255
        continue

    grid[i] = (closest_point(i) or DEFAULT_POINT_ID)[2]

if PLOT_GRID:
    import matplotlib.pyplot as plt

    plt.imshow(grid)
    plt.show()

print(max(np.count_nonzero(grid[np.where(grid == point_id)]) - 1 for _, _, point_id in points))
