from itertools import product
from typing import TypeAlias

INPUT_FILE = "input_20.txt"

Grid: TypeAlias = list[list[str]]
XYPair: TypeAlias = tuple[int, int]
Distances: TypeAlias = dict[XYPair, int]

WALL = "#"
START = "S"
END = "E"


def number_of_cheats(distances: Distances, cheat_time: int, min_distance: int) -> int:
    ans = 0

    for x, y in distances:
        for dx, dy in product(range(-cheat_time, cheat_time + 1), repeat=2):
            if dx == dy == 0 or abs(dx) + abs(dy) > cheat_time:
                continue

            nx, ny = x + dx, y + dy
            if (nx, ny) not in distances:
                continue

            distance = distances[(nx, ny)] - distances[(x, y)]
            manhattan = abs(nx - x) + abs(ny - y)

            if distance - manhattan >= min_distance:
                ans += 1
    return ans


def get_distances(grid: Grid) -> Distances:
    n, m = len(grid), len(grid[0])
    start = next((i, j) for j in range(m) for i in range(n) if grid[i][j] == START)

    distances = {}
    pos = start
    distance = 0
    while pos:
        distances[pos] = distance
        x, y = pos

        if grid[x][y] == END:
            break

        distance += 1
        for nx, ny in (
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ):
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] == WALL or (nx, ny) in distances:
                    continue
                pos = nx, ny
                break
    return distances


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        grid = [list(line.strip()) for line in f.readlines()]
    coordinates = get_distances(grid)
    print(number_of_cheats(coordinates, 2, 100))
    print(number_of_cheats(coordinates, 20, 100))
