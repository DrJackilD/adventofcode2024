from functools import cache

INPUT_FILE = "input_11.txt"
MAGIC = 2024


@cache
def evolve_num(num: int, evolutions: int) -> int:
    if evolutions == 0:
        return 1

    if num == 0:
        return evolve_num(1, evolutions - 1)

    if len(str(num)) % 2 == 0:
        temp = str(num)
        temp_l = len(temp)
        return evolve_num(int(temp[: temp_l // 2]), evolutions - 1) + evolve_num(
            int(temp[temp_l // 2 :]), evolutions - 1
        )

    return evolve_num(num * MAGIC, evolutions - 1)


def evolve(nums: list[int], evolutions: int) -> int:
    ans = 0
    for num in nums:
        ans += evolve_num(num, evolutions)
    return ans


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        nums = [int(i) for i in f.readline().strip().split()]
    print(evolve(nums, 25))  # part 1
    print(evolve(nums, 75))  # part 2
