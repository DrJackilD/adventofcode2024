from collections import defaultdict
from heapq import heappop, heappush
from typing import TypeAlias

Maze: TypeAlias = list[list[str]]
XYPair: TypeAlias = tuple[int, int]

INPUT_FILE = "input_16.txt"
WALL = "#"
START = "S"
END = "E"


def solve(maze: Maze) -> tuple[set[XYPair], int]:
    x, y = next((i, row.index(START)) for i, row in enumerate(maze) if START in row)
    ex, ey = next((i, row.index(END)) for i, row in enumerate(maze) if END in row)

    costs: dict[tuple[int, int, int, int], int | float] = defaultdict(
        lambda: float("inf")
    )
    costs[(x, y, 0, 1)] = 0
    path: tuple[XYPair] = ((x, y),)
    q = [(0, path, 0, 1)]
    min_path = set()
    min_cost = float("inf")

    while q:
        cost, path, dx, dy = heappop(q)
        x, y = path[-1]

        if (x, y) == (ex, ey):
            min_cost = min(min_cost, cost)
            if cost <= min_cost:
                min_path |= set(path)
            continue

        for nx, ny, new_cost, ndx, ndy in (
            (x + dx, y + dy, cost + 1, dx, dy),
            (x, y, cost + 1000, dy, -dx),
            (x, y, cost + 1000, -dy, dx),
        ):
            if maze[nx][ny] == WALL:
                continue

            if new_cost <= costs[(nx, ny, ndx, ndy)]:
                costs[(nx, ny, ndx, ndy)] = new_cost
                new_path = path + ((nx, ny),)
                heappush(q, (new_cost, new_path, ndx, ndy))  # type: ignore
    return min_path, min_cost  # type: ignore


if __name__ == "__main__":
    maze: Maze = []
    with open(INPUT_FILE) as f:
        for line in f:
            maze.append(list(line.strip()))
    min_path, min_cost = solve(maze)
    print(min_cost)  # part 1
    print(len(min_path))  # part 2
