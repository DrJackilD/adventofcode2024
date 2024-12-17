"""
I didn't solve part 2 by myself, I've got the clue from the subreddit.
"""

from collections import deque
from typing import Deque

INPUT_FILE = "input_17.txt"


class Computer:
    def __init__(self, program: list[int], A: int, B: int, C: int):
        self.program = program
        self.A = A
        self.B = B
        self.C = C
        self.instruction_pointer = 0
        self.output = []

    def _combo_op(self, operand: int) -> int:
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case _:
                raise ValueError(f"invalid operand: {operand}")

    def _adv(self, operand: int):
        res = self.A // (2**operand)
        self.A = res
        self.instruction_pointer += 2

    def _bxl(self, operand: int):
        self.B ^= operand
        self.instruction_pointer += 2

    def _bst(self, operand: int):
        self.B = operand % 8
        self.instruction_pointer += 2

    def _jnz(self, operand: int):
        if self.A != 0:
            self.instruction_pointer = operand
        else:
            self.instruction_pointer += 2

    def _bxc(self, operand: int):
        self.B ^= self.C
        self.instruction_pointer += 2

    def _out(self, operand: int):
        self.output.append(operand % 8)
        self.instruction_pointer += 2

    def _bdv(self, operand: int):
        res = self.A // (2**operand)
        self.B = res
        self.instruction_pointer += 2

    def _cdv(self, operand: int):
        res = self.A // (2**operand)
        self.C = res
        self.instruction_pointer += 2

    def execute_instruction(self, opcode: int, operand: int):
        match opcode:
            case 0:
                return self._adv(self._combo_op(operand))
            case 1:
                return self._bxl(operand)
            case 2:
                return self._bst(self._combo_op(operand))
            case 3:
                return self._jnz(operand)
            case 4:
                return self._bxc(operand)
            case 5:
                return self._out(self._combo_op(operand))
            case 6:
                return self._bdv(self._combo_op(operand))
            case 7:
                return self._cdv(self._combo_op(operand))
            case _:
                raise ValueError(f"invalid opcode: {opcode}")

    def run(self) -> str:
        while self.instruction_pointer < len(self.program):
            opcode, operand = (
                self.program[self.instruction_pointer],
                self.program[self.instruction_pointer + 1],
            )
            self.execute_instruction(opcode, operand)
        return ",".join(map(str, self.output))


def solve_program(program: list[int]) -> int:
    q: Deque[tuple[int, int]] = deque([(len(program) - 1, 0)])
    while q:
        offset, value = q.popleft()
        for curr in range(8):
            next_val = (value << 3) + curr
            computer = Computer(program, next_val, 0, 0)
            computer.run()
            if computer.output == program[offset:]:
                if offset == 0:
                    return next_val
                q.append((offset - 1, next_val))
    return -1


if __name__ == "__main__":
    A = B = C = 0
    program = []
    with open(INPUT_FILE, "r") as f:
        for line in f:
            if line.startswith("Register A"):
                A = int(line.strip().split(": ")[-1])
            elif line.startswith("Register B"):
                B = int(line.strip().split(": ")[-1])
            elif line.startswith("Register C"):
                C = int(line.strip().split(": ")[-1])
            elif line.startswith("Program"):
                program = [int(ch) for ch in line.strip().split(": ")[-1].split(",")]
    computer = Computer(program, A, B, C)
    print(computer.run())  # part 1
    print(solve_program(program))  # part 2
