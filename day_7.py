from operator import add, mul

INPUT_FILE = "input_7.txt"

OPS = {
    "+": add,
    "*": mul,
    "||": lambda x, y: int(f"{x}{y}"),
}


def is_valid_combination(nums: list[int], target: int, ops: list[str]) -> bool:
    stack = [nums[0]]
    for num in nums[1:]:
        next_stack = []
        while stack:
            curr = stack.pop()
            for op in ops:
                fun = OPS[op]
                next_stack.append(fun(curr, num))
        stack = next_stack
    return target in stack


def valid_combinations_sum(
    combinations: list[tuple[list[int], int]], ops: list[str]
) -> int:
    ans = 0
    for nums, target in combinations:
        if is_valid_combination(nums, target, ops):
            ans += target
    return ans


if __name__ == "__main__":
    combinations = []
    with open(INPUT_FILE) as f:
        for line in f:
            target, nums = line.strip().split(": ")
            target = int(target)
            nums = [int(num) for num in nums.split(" ")]
            combinations.append([nums, target])

    print(valid_combinations_sum(combinations, ops=["+", "*"]))  # part 1
    print(valid_combinations_sum(combinations, ops=["+", "*", "||"]))  # part 2
