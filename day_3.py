INPUT_FILE = "input_3.txt"


def parse_muls(line: str, initial_state: int) -> tuple[int, int]:
    # 0 -> parse for "mul" token,
    # 1 -> parse for first integer
    # 2 -> parse for second integer and closing ")"
    # 3 -> execute state
    # 4 -> don't() instruction enabled, skip everyting until do() found
    res = 0
    state = initial_state

    curr = []
    nums = []
    for i in range(3, len(line)):
        match state:
            case 0:
                curr = []
                nums = []
                if line[i - 3 : i + 1] == "mul(":
                    state = 1
                    continue
                if i >= 6:
                    if line[i - 6 : i + 1] == "don't()":
                        state = 4
            case 1:
                if line[i] == ",":
                    if not curr:
                        state = 0
                        continue
                    nums.append(int("".join(curr)))
                    curr = []
                    state = 2
                    continue
                if not line[i].isnumeric():
                    state = 0
                    continue
                curr.append(line[i])
            case 2:
                if line[i] == ")":
                    if not curr:
                        state = 0
                        continue
                    nums.append(int("".join(curr)))
                    state = 3
                    continue
                if not line[i].isnumeric():
                    state = 0
                    continue
                curr.append(line[i])
            case 3:
                if len(nums) != 2:
                    state = 0
                    continue
                res += nums[0] * nums[1]
                state = 0
            case 4:
                if line[i - 3 : i + 1] == "do()":
                    state = 0
    return res, state


def sum_of_muls() -> int:
    ans = 0
    state = 0
    with open(INPUT_FILE) as f:
        for line in f:
            res, state = parse_muls(line, state)
            ans += res
    return ans


if __name__ == "__main__":
    print(sum_of_muls())
