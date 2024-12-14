import re
from functools import reduce
from typing import NamedTuple

INPUT_FILE = "input_14.txt"
ROBOT_PARSER = re.compile(
    r"p=(?P<px>-?\d+),(?P<py>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)"
)


class XYPair(NamedTuple):
    x: int
    y: int


class Robot(NamedTuple):
    position: XYPair
    velocity: XYPair


def easter_egg_after(size: tuple[int, int], robots: list[Robot]) -> int:
    width, height = size
    n = len(robots)
    for second in range(1, size[0] * size[1] + 1):
        robots = [
            Robot(
                position=XYPair(
                    (r.position.x + r.velocity.x) % width,
                    (r.position.y + r.velocity.y) % height,
                ),
                velocity=r.velocity,
            )
            for r in robots
        ]
        if len(set(r.position for r in robots)) == n:
            return second
    # unreachable with correct input
    return -1


def safety_factor(
    size: tuple[int, int], robots: list[Robot], iterations: int = 100
) -> int:
    positions: list[XYPair] = []
    for robot in robots:
        pos = (
            (robot.position.x + robot.velocity.x * iterations) % size[0],
            (robot.position.y + robot.velocity.y * iterations) % size[1],
        )
        positions.append(XYPair(*pos))
    middle_width = size[0] // 2
    middle_height = size[1] // 2

    quadrants = [0] * 4

    for x, y in positions:
        if x < middle_width and y < middle_height:
            quadrants[0] += 1
        elif x > middle_width and y < middle_height:
            quadrants[1] += 1
        elif x < middle_width and y > middle_height:
            quadrants[2] += 1
        elif x > middle_width and y > middle_height:
            quadrants[3] += 1
    return reduce(lambda x, y: (x if x > 0 else 1) * (y if y > 0 else 1), quadrants)


if __name__ == "__main__":
    robots: list[Robot] = []
    tiles_size = (101, 103)
    with open(INPUT_FILE) as f:
        for line in f:
            if match := ROBOT_PARSER.match(line.strip()):
                pos = (int(match.group("px")), int(match.group("py")))
                vel = (int(match.group("vx")), int(match.group("vy")))
                robots.append(Robot(XYPair(*pos), XYPair(*vel)))
    print(safety_factor(tiles_size, robots))  # part 1
    print(easter_egg_after(tiles_size, robots))  # part 2
