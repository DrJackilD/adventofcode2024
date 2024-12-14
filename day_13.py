"""
Huge thanks to https://winslowjosiah.com/blog/2024/12/13/advent-of-code-2024-day-13/
for helping me to figure out the math behind the solution
"""

import re
from itertools import batched
from typing import TypeAlias, cast

INPUT_FILE = "input_13.txt"

XY_PATTERN = re.compile(r"(\d+).+?(\d+)")

A_COST = 3
B_COST = 1

XYPair: TypeAlias = tuple[int, int]
Machine: TypeAlias = tuple[XYPair, XYPair, XYPair]


def solve_machine(machine: Machine, prize_offset: int = 0) -> tuple[int, int] | None:
    (ax, ay), (bx, by), (px, py) = machine
    if prize_offset:
        px += prize_offset
        py += prize_offset

    a_presses, remainder = divmod(px * by - py * bx, ax * by - ay * bx)
    # remainder means prize is not achievable
    if remainder:
        return None

    b_presses, remainder = divmod(px - ax * a_presses, bx)
    # remainder means prize is not achievable
    if remainder:
        return None
    return (a_presses, b_presses)


def tokens_spent(machines: list[Machine], prize_offset: int = 0) -> int:
    tokens = 0
    for machine in machines:
        match solve_machine(machine, prize_offset):
            case None:
                continue
            case (a_presses, b_presses):
                tokens += a_presses * A_COST + b_presses * B_COST
    return tokens


if __name__ == "__main__":
    machines: list[Machine] = []

    with open(INPUT_FILE) as f:
        for machine_input in batched((line.strip() for line in f if line.strip()), 3):
            machine = []
            for setting in machine_input:
                param = [int(match) for match in XY_PATTERN.findall(setting)[0]]
                machine.append(param)
            machines.append(cast(Machine, machine))
    print(tokens_spent(machines))  # part 1
    print(tokens_spent(machines, prize_offset=10_000_000_000_000))  # part 2
