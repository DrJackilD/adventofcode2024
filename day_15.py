# TODO: I have no idea why it's not working with the full input
# for the second part. The test input for part 2 works just fine.
# Fix it later.

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


def move_big_crate(grid: Grid, x: int, y: int, dir: str) -> None:
    dx, dy = DIR[dir]

    # for convenience we always work with the left part of the double crate
    if grid[x][y] == DOUBLE_CRATE_RIGHT:
        y -= 1

    new_x, new_y = x + dx, y + dy

    if grid[new_x][new_y] == WALL or grid[new_x][new_y + 1] == WALL:
        return

    grid[x][y] = EMPTY
    grid[x][y + 1] = EMPTY

    if grid[new_x][new_y] in [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]:
        move_big_crate(grid, new_x, new_y, dir)
    if grid[new_x][new_y + 1] == DOUBLE_CRATE_LEFT:
        move_big_crate(grid, new_x, new_y + 1, dir)

    if grid[new_x][new_y] != EMPTY or grid[new_x][new_y + 1] != EMPTY:
        # can't move
        grid[x][y] = DOUBLE_CRATE_LEFT
        grid[x][y + 1] = DOUBLE_CRATE_RIGHT
        return

    grid[new_x][new_y] = DOUBLE_CRATE_LEFT
    grid[new_x][new_y + 1] = DOUBLE_CRATE_RIGHT
    return


def move_v2(grid: Grid, x: int, y: int, dir: str) -> XYPair:
    dx, dy = DIR[dir]
    grid[x][y] = EMPTY
    new_x, new_y = x + dx, y + dy

    if grid[new_x][new_y] == WALL:
        return (x, y)

    if grid[new_x][new_y] in [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]:
        move_big_crate(grid, new_x, new_y, dir)

    if grid[new_x][new_y] == EMPTY:
        grid[new_x][new_y] = ROBOT
        grid[x][y] = EMPTY
        return (new_x, new_y)

    # can't move
    grid[x][y] = ROBOT
    return (x, y)


def move(grid: Grid, x: int, y: int, dir: str) -> XYPair:
    dx, dy = DIR[dir]
    new_x, new_y = x + dx, y + dy
    if grid[new_x][new_y] == WALL:
        return (x, y)

    if grid[new_x][new_y] == CRATE:
        move(grid, new_x, new_y, dir)

    if grid[new_x][new_y] == EMPTY:
        grid[new_x][new_y] = grid[x][y]
        grid[x][y] = EMPTY
        return (new_x, new_y)
    return (x, y)


def gps_total(grid: Grid) -> int:
    ans = 0
    for i in range(len(grid)):
        for j, cell in enumerate(grid[i]):
            if cell in {CRATE, DOUBLE_CRATE_LEFT}:
                ans += 100 * i + j
    return ans


def prepare_v2_map(grid: Grid) -> Grid:
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == CRATE:
                new_row.extend([DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT])
            elif cell == WALL:
                new_row.extend([WALL, WALL])
            elif cell == ROBOT:
                new_row.extend([ROBOT, EMPTY])
            elif cell == EMPTY:
                new_row.extend([EMPTY, EMPTY])
            else:
                raise ValueError(f"unknown cell: {cell}")
        new_grid.append(new_row)
    return new_grid


def enrich(cell: str) -> list[str]:
    if cell == CRATE:
        return [DOUBLE_CRATE_LEFT, DOUBLE_CRATE_RIGHT]
    if cell == WALL:
        return [WALL, WALL]
    if cell == ROBOT:
        return [ROBOT, EMPTY]
    return [cell, cell]


def run_robot(grid: Grid, start: XYPair, commands: list[str], v2: bool = False):
    for row in grid:
        print("".join(row))
    while commands:
        cmd = commands.pop()
        if not v2:
            start = move(grid, start[0], start[1], cmd)
        else:
            start = move_v2(grid, start[0], start[1], cmd)
    for row in grid:
        print("".join(row))
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

    grid = [list(chain(*[enrich(cell) for cell in row])) for row in grid]
    for i, row in enumerate(grid):
        if ROBOT in row:
            start_pos = (i, row.index(ROBOT))
    print(run_robot(grid, start_pos, commands, v2=True))  # part 2
