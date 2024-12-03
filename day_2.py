INPUT_FILE = "input_2.txt"
SKIPS_ALLOWED = 1


def is_safe_increasing(nums: list[int], skips: int = 0) -> bool:
    for i in range(1, len(nums)):
        diff = nums[i] - nums[i - 1]
        if diff < 1 or diff > 3:
            if skips < SKIPS_ALLOWED:
                return is_safe_increasing(
                    nums[:i] + nums[i + 1 :], skips + 1
                ) or is_safe_increasing(nums[: i - 1] + nums[i:], skips + 1)
            return False
    return True


def is_safe_decreasing(nums: list[int], skips: int = 0) -> bool:
    for i in range(1, len(nums)):
        diff = nums[i - 1] - nums[i]
        if diff < 1 or diff > 3:
            if skips < SKIPS_ALLOWED:
                return is_safe_decreasing(
                    nums[:i] + nums[i + 1 :], skips + 1
                ) or is_safe_decreasing(nums[: i - 1] + nums[i:], skips + 1)
            return False
    return True


def num_of_safe_levels() -> int:
    safe_reports = 0
    with open(INPUT_FILE) as f:
        for line in f:
            nums = [int(num) for num in line.split()]
            if not nums:
                break

            safe_reports += is_safe_increasing(nums) or is_safe_decreasing(nums)
    return safe_reports


if __name__ == "__main__":
    print(num_of_safe_levels())
