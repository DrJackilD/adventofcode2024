from itertools import chain
from typing import TypeAlias

INPUT_FILE = "input_15.txt"

WALL = "#"
CRATE = "O"
DOUBLE_CRATE_LEFT = "["
DOUBLE_CRATE_RIGHT = "]"
ROBOT = "@"
EMPTY = "."

DIR = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

Grid: TypeAlias = list[list[str]]
XYPair: TypeAlias = tuple[int, int]


def enlarge(cell: str) -> list[str]:
    if cell == CRATE:
        return [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]
    if cell == WALL:
        return [WALL, WALL]
    if cell == ROBOT:
        return [ROBOT, EMPTY]
    return [cell, cell]


def can_move_big_crate(grid: Grid, x: int, y: int, dir: str) -> bool:
    dx, dy = DIR[dir]

    # for convenience we always point to the left part of the double crate
    if grid[x][y] == DOUBLE_CRATE_RIGHT:
        y -= 1

    new_x, new_y = x + dx, y + dy

    if grid[new_x][new_y] == WALL or grid[new_x][new_y + 1] == WALL:
        return False

    grid[x][y] = EMPTY
    grid[x][y + 1] = EMPTY

    can_move = True
    if grid[new_x][new_y] in [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]:
        if not can_move_big_crate(grid, new_x, new_y, dir):
            can_move = False
    if grid[new_x][new_y + 1] == DOUBLE_CRATE_LEFT:
        if not can_move_big_crate(grid, new_x, new_y + 1, dir):
            can_move = False

    grid[x][y] = DOUBLE_CRATE_LEFT
    grid[x][y + 1] = DOUBLE_CRATE_RIGHT

    return can_move


def move_big_crate(grid: Grid, x: int, y: int, dir: str):
    dx, dy = DIR[dir]

    # for convenience we always point to the left part of the double crate
    if grid[x][y] == DOUBLE_CRATE_RIGHT:
        y -= 1

    new_x, new_y = x + dx, y + dy

    grid[x][y] = EMPTY
    grid[x][y + 1] = EMPTY

    if grid[new_x][new_y] in [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]:
        move_big_crate(grid, new_x, new_y, dir)
    if grid[new_x][new_y + 1] == DOUBLE_CRATE_LEFT:
        move_big_crate(grid, new_x, new_y + 1, dir)

    grid[new_x][new_y] = DOUBLE_CRATE_LEFT
    grid[new_x][new_y + 1] = DOUBLE_CRATE_RIGHT


def move(grid: Grid, x: int, y: int, dir: str) -> XYPair:
    dx, dy = DIR[dir]
    new_x, new_y = x + dx, y + dy

    if grid[new_x][new_y] == WALL:
        return x, y

    if grid[new_x][new_y] == CRATE:
        move(grid, new_x, new_y, dir)
    elif grid[new_x][new_y] in [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]:
        if not can_move_big_crate(grid, new_x, new_y, dir):
            return x, y
        else:
            move_big_crate(grid, new_x, new_y, dir)

    if grid[new_x][new_y] == EMPTY:
        grid[new_x][new_y] = grid[x][y]
        grid[x][y] = EMPTY
        return new_x, new_y
    return x, y


def gps_total(grid: Grid) -> int:
    ans = 0
    for i in range(len(grid)):
        for j, cell in enumerate(grid[i]):
            if cell in {CRATE, DOUBLE_CRATE_LEFT}:
                ans += 100 * i + j
    return ans


def run_robot(grid: Grid, start: XYPair, commands: list[str]):
    while commands:
        cmd = commands.pop()
        start = move(grid, start[0], start[1], cmd)
    return gps_total(grid)


if __name__ == "__main__":
    grid = []
    commands = []
    start_pos = (0, 0)
    with open(INPUT_FILE) as f:
        row = 0
        for line in f:
            if line.startswith("#"):
                grid.append(list(line.strip()))
                robot_pos = line.strip().find(ROBOT)
                if robot_pos != -1:
                    start_pos = (row, robot_pos)
                row += 1
            elif line:
                commands.extend(list(line.strip()))
    commands.reverse()  # make it a stack

    print(run_robot([row[:] for row in grid], start_pos, commands[:]))  # part 1

    grid = [list(chain(*[enlarge(cell) for cell in row])) for row in grid]
    for i, row in enumerate(grid):
        if ROBOT in row:
            start_pos = (i, row.index(ROBOT))
    print(run_robot(grid, start_pos, commands))  # part 2
