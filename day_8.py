from collections import defaultdict
from typing import Generator

INPUT_FILE = "input_8.txt"


def calculate_antinodes(
    point: tuple[int, int],
    diff: tuple[int, int],
    dimensions: tuple[int, int],
    first: bool,
) -> Generator[tuple[int, int], None]:
    x, y = point
    dx, dy = diff
    rows, cols = dimensions
    antinodes = {(x, y)} if first else set()
    nx, ny = x + dx if first else x, y + dy if first else y
    while 0 <= nx < rows and 0 <= ny < cols:
        if (nx, ny) not in antinodes:
            antinodes.add((nx, ny))
            yield (nx, ny)
        if first:
            break
        nx, ny = nx + dx, ny + dy


def antinodes(grid: list[str], transient: bool = False) -> set[tuple[int, int]]:
    antennas = defaultdict(list)
    nodes = set()
    n, m = len(grid), len(grid[0])

    for i in range(n):
        for j in range(m):
            if grid[i][j] == ".":
                continue

            ant_type = grid[i][j]
            for x, y in antennas[ant_type]:
                dx, dy = i - x, j - y
                for node in calculate_antinodes(
                    (x, y), (dx * -1, dy * -1), (n, m), not transient
                ):
                    nodes.add(node)
                for node in calculate_antinodes(
                    (i, j), (dx, dy), (n, m), not transient
                ):
                    nodes.add(node)
            antennas[ant_type].append((i, j))
    return nodes


if __name__ == "__main__":
    grid = []
    with open(INPUT_FILE) as f:
        for line in f:
            grid.append(list(line.strip()))
    print(len(antinodes(grid)))  # part 1
    print(len(antinodes(grid, transient=True)))  # part 2
