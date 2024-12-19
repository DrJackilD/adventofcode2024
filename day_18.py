"""
I modified the input for this day, added the additional two lines at the beginning
with the size of the grid and the starting number of already corrupted coordinates
(in case somebody wants to test it with different values)
"""

from collections import deque
from typing import Deque, TypeAlias

INPUT_FILE = "input_18.txt"

XYPair: TypeAlias = tuple[int, int]


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                if self.rank[root_x] == self.rank[root_y]:
                    self.rank[root_x] += 1


def no_longer_possible_after(
    size: int, falling: list[XYPair], forward_to: int
) -> XYPair:
    falling.reverse()
    ds = DisjointSet(size * size)

    grid = [[0] * size for _ in range(size)]

    def get_connections(x: int, y: int) -> list[XYPair]:
        return [
            (x, y + 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x, y - 1),
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
        ]

    for i in range(forward_to):
        x, y = falling.pop()
        grid[x][y] = -1

        for nx, ny in get_connections(x, y):
            if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] == -1:
                ds.union(x * size + y, nx * size + ny)

    right_top_bytes: set[int] = set()
    left_bottom_bytes: set[int] = set()
    while falling:
        x, y = falling.pop()
        grid[x][y] = -1

        if x == 0 or y == size - 1:
            right_top_bytes.add(x * size + y)

        if y == 0 or x == size - 1:
            left_bottom_bytes.add(x * size + y)

        for nx, ny in get_connections(x, y):
            if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] == -1:
                ds.union(x * size + y, nx * size + ny)

        right_connection = None
        for rt in right_top_bytes:
            if ds.find(rt) == ds.find(x * size + y):
                right_connection = rt
                break

        left_connection = None
        for lb in left_bottom_bytes:
            if ds.find(lb) == ds.find(x * size + y):
                left_connection = lb
                break

        if right_connection and left_connection:
            return x, y

    return (-1, -1)


def find_path(size: int, falling: list[XYPair], forward_to: int) -> int:
    """
    Find the shortest path from the top-left corner to the bottom-right corner of the grid
    :param size: size of the grid
    :param falling: list of corrupted coordinates
    :param forward_to: how many already falled coordinates we have at the beginning
    """
    falling.reverse()  # make it a stack
    grid = [[0] * size for _ in range(size)]
    start = (0, 0)

    for _ in range(forward_to):
        corrupted = falling.pop()
        grid[corrupted[0]][corrupted[1]] = -1

    q: Deque[tuple[XYPair, int]] = (
        deque(  # queue with tuple of (coordinate, total steps)
            [(start, 0)]
        )
    )
    while q:
        level = len(q)

        for _ in range(level):
            (x, y), steps = q.popleft()
            if x == size - 1 and y == size - 1:
                return steps  # reached the end of the grid

            for nx, ny in [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] == 0:
                    q.append(((nx, ny), steps + 1))
                    grid[nx][ny] = 1
    return -1


if __name__ == "__main__":
    coordinates = []
    forward_to = 0
    with open(INPUT_FILE) as f:
        size = int(f.readline().strip())
        forward_to = int(f.readline().strip())

        for line in f:
            coordinates.append(
                tuple(reversed(list((int(coord) for coord in line.strip().split(",")))))
            )

    print(find_path(size, coordinates[:], forward_to))  # part 1
    print(
        tuple(reversed(no_longer_possible_after(size, coordinates, forward_to)))
    )  # part 2, for some reason they using the reversed coordinates -_-
