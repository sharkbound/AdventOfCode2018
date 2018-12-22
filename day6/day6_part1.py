import numpy as np

PLOT_GRID = True

WIDTH = 354
HEIGHT = 359

grid = np.zeros((WIDTH, HEIGHT), dtype=np.int)


def point_area(point_id):
    return np.count_nonzero(grid[np.where(grid == point_id)])


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
    non_infinite_points = set(id for _, _, id in points)

for i, p in enumerate(points, 1):
    grid[p[:-1]] = i
    seen_points.add(p[:-1])

for i, _ in np.ndenumerate(grid):
    if PLOT_GRID and i in seen_points:
        grid[i] = 255

    closest_point_id = closest_point(i)

    if closest_point_id and (not i[0] or i[0] == WIDTH - 1 or not i[1] or i[1] == HEIGHT - 1):
        non_infinite_points.discard(closest_point_id[2])
        # print(f'discarding: {closest_point_id[2]}, '
        #       f'W:{WIDTH - 1}, H:{HEIGHT - 1}, '
        #       f'X: {i[0]}, Y: {i[1]}')

    grid[i] = (closest_point_id or DEFAULT_POINT_ID)[2]

if PLOT_GRID:
    import matplotlib.pyplot as plt

    for p in points:
        if p[2] not in non_infinite_points:
            grid[np.where(grid == p[2])] = 0

    plt.imshow(grid)
    plt.show()

print(max(map(point_area, non_infinite_points)))
