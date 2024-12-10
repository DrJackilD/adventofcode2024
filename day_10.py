INPUT_FILE = "input_10.txt"
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def trailhead_score(
    grid: list[list[int]], start: tuple[int, int], all_routes: bool = False
) -> int:
    n, m = len(grid), len(grid[0])

    seen = {start}

    def dfs(x: int, y: int):
        if grid[x][y] == 9:
            return 1

        reached = 0
        for to_x, to_y in DIRECTIONS:
            nx, ny = x + to_x, y + to_y
            if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in seen:
                if grid[nx][ny] - grid[x][y] == 1:
                    seen.add((nx, ny))
                    reached += dfs(nx, ny)
                    if all_routes:
                        seen.remove((nx, ny))
        return reached

    score = dfs(*start)
    return score


def trailheads_sum(grid: list[list[int]], all_routes: bool = False) -> int:
    n, m = len(grid), len(grid[0])
    total_score = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                total_score += trailhead_score(grid, (i, j), all_routes)
    return total_score


if __name__ == "__main__":
    grid = []
    with open(INPUT_FILE) as f:
        for line in f:
            grid.append([int(ch) for ch in line.strip()])
    print(trailheads_sum(grid))  # part 1
    print(trailheads_sum(grid, all_routes=True))  # part 2
