from functools import cache

INPUT_FILE = "input_19.txt"


def number_of_variants(combination: str, towels: list[str]) -> int:
    n = len(combination)

    @cache
    def dp(i: int):
        if i == n:
            return 1

        ans = 0
        for towel in towels:
            if combination[i:].startswith(towel):
                ans += dp(i + len(towel))
        return ans

    ans = dp(0)
    return ans


def number_of_combinations(combinations: list[str], towels: list[str]) -> int:
    ans = 0

    for combination in combinations:
        ans += number_of_variants(combination, towels)

    return ans


def number_of_possible_designs(combinations: list[str], towels: list[str]) -> int:
    ans = 0

    for combination in combinations:
        if number_of_variants(combination, towels) > 0:
            ans += 1

    return ans


if __name__ == "__main__":
    towels = []
    combinations = []
    with open(INPUT_FILE) as f:
        towels = f.readline().strip().split(", ")
        next(f)  # skip the blank line
        for line in f:
            combinations.append(line.strip())

    print(number_of_possible_designs(combinations, towels))  # part 1
    print(number_of_combinations(combinations, towels))  # part 2
