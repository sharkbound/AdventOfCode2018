import numpy as np

PLOT_GRID = True

WIDTH = 354
HEIGHT = 359

grid = np.zeros((WIDTH, HEIGHT), dtype=np.int)


def dist_to_all_points(pos):
    return sum(manhattan_distance(pos, p[:-1]) for p in points)


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def closest_point(point):
    distances = [(manhattan_distance(point, p[:-1]), p) for p in points]
    min_dist, min_point = min(distances, key=lambda x: x[0])

    if any(1 for dist, p in distances if dist == min_dist and p[2] != min_point[2]):
        return None

    return min_point


DEFAULT_POINT_ID = 0, 0, 0

with open('data.txt') as f:
    points = [(*map(int, line.split(',')), i) for i, line in enumerate(f, 1)]
    non_infinite_points = set(id for _, _, id in points)

for i, p in enumerate(points, 1):
    grid[p[:-1]] = i

if PLOT_GRID:
    import matplotlib.pyplot as plt

    for i in np.ndindex(grid.shape):
        grid[i] = dist_to_all_points(i) < 10_000

    plt.imshow(grid)
    plt.show()

print(sum(1 for i in np.ndindex(grid.shape) if dist_to_all_points(i) < 10_000))
