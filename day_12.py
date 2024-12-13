"""
For Part 2 credits goes to this awesome blog post:
https://winslowjosiah.com/blog/2024/12/12/advent-of-code-2024-day-12/
which is inspired me with his edges count
(with mark every perpendicular edge in this direction as counted)
"""

from typing import TypeAlias

INPUT_FILE = "input_12.txt"
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

Grid: TypeAlias = list[list[str]]
Point: TypeAlias = tuple[int, int]
Region: TypeAlias = set[Point]


def valid(n: int, m: int, x: int, y: int) -> bool:
    return 0 <= x < n and 0 <= y < m


def get_region(grid: Grid, start: Point) -> Region:
    n, m = len(grid), len(grid[0])
    region = {start}

    def dfs(x: int, y: int):
        for to_x, to_y in DIRECTIONS:
            nx, ny = x + to_x, y + to_y
            if valid(n, m, nx, ny) and grid[nx][ny] == grid[x][y]:
                if (nx, ny) not in region:
                    region.add((nx, ny))
                    dfs(nx, ny)

    dfs(*start)
    return region


def get_region_sides(region: Region) -> int:
    sides = 0
    for to_x, to_y in DIRECTIONS:
        seen: set[Point] = set()
        for point in region:
            if point in seen:
                continue

            x, y = point
            if (x + to_x, y + to_y) in region:
                continue

            sides += 1

            for delta in (-1, 1):
                nx, ny = point
                while (nx, ny) in region and (nx + to_x, ny + to_y) not in region:
                    seen.add((nx, ny))
                    nx += to_y * delta
                    ny += to_x * delta
    return sides


def get_region_perimeter(region: Region) -> int:
    perimeter = 0
    for to_x, to_y in DIRECTIONS:
        for x, y in region:
            edges = 0
            nx, ny = x + to_x, y + to_y
            if (nx, ny) not in region:
                edges += 1
            perimeter += edges
    return perimeter


def get_fence_cost(grid: Grid, with_discount: bool = False) -> int:
    n, m = len(grid), len(grid[0])
    seen = set()

    ans = 0
    for i in range(n):
        for j in range(m):
            if (i, j) not in seen:
                region = get_region(grid, (i, j))
                area = len(region)
                seen |= region
                if with_discount:
                    length = get_region_sides(region)
                else:
                    length = get_region_perimeter(region)
                ans += area * length
    return ans


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        grid = [[ch for ch in line.strip()] for line in f]
    print(get_fence_cost(grid))  # part 1
    print(get_fence_cost(grid, with_discount=True))  # part 2
