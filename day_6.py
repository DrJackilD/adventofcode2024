INPUT_FILE = "input_6.txt"
OBSTACLE = "#"

DIRECTIONS = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}


def visited_positions(
    grid: list[list[str]], start: tuple[int, int]
) -> set[tuple[int, int]]:
    n, m = len(grid), len(grid[0])
    dir = 0
    x, y = start
    visited = {start}

    def valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m

    while valid(x, y):
        to_x, to_y = DIRECTIONS[dir]
        nx, ny = x + to_x, y + to_y
        if not valid(nx, ny):
            break
        if grid[nx][ny] == OBSTACLE:
            dir = (dir + 1) % 4
        else:
            x, y = nx, ny
            if (x, y) not in visited:
                visited.add((x, y))
    return visited


def is_loop(grid: list[list[str]], start: tuple[int, int]) -> bool:
    n, m = len(grid), len(grid[0])
    dir = 0
    x, y = start
    visited = {(x, y, dir)}

    def valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m

    while valid(x, y):
        to_x, to_y = DIRECTIONS[dir]
        nx, ny = x + to_x, y + to_y
        if not valid(nx, ny):
            break
        if grid[nx][ny] == OBSTACLE:
            dir = (dir + 1) % 4
        else:
            x, y = nx, ny
            if (x, y, dir) in visited:
                return True
            visited.add((x, y, dir))
    return False


def possible_loops(
    grid: list[list[str]], positions: set[tuple[int, int]], start: tuple[int, int]
):
    positions = positions ^ {start}
    loops = 0
    for x, y in positions:
        grid[x][y] = "#"
        if is_loop(grid, start):
            loops += 1
        grid[x][y] = "."
    return loops


if __name__ == "__main__":
    grid = []
    start = (0, 0)
    with open(INPUT_FILE) as f:
        for line in f:
            guard_pos = line.find("^")
            row = list(line.strip())
            grid.append(row)
            if guard_pos != -1:
                start = (len(grid) - 1, guard_pos)
    visited = visited_positions(grid, start)
    print(len(visited))  # part 1
    print(possible_loops(grid, visited, start))  # part 2
