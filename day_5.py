from collections import defaultdict
from functools import cmp_to_key

INPUT_FILE = "input_5.txt"
RULES = defaultdict(set)


def is_valid_order(arr: list[str]) -> bool:
    printed = set()

    for page in arr:
        if RULES[page] & printed:
            return False
        printed.add(page)
    return True


def middles_of_valid_rows(rows: list[list[str]]) -> int:
    ans = 0
    for row in rows:
        if is_valid_order(row):
            ans += int(row[len(row) // 2])
    return ans


def page_order_cmp(x: int, y: int) -> int:
    if y in RULES[x]:
        return -1
    elif x in RULES[y]:
        return 1
    return 0


def middles_of_fixed_rows(rows: list[list[str]]) -> int:
    ans = 0
    for row in rows:
        if not is_valid_order(row):
            row.sort(key=cmp_to_key(page_order_cmp))  # type: ignore
            ans += int(row[len(row) // 2])
    return ans


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        for line in f:
            if not line.strip():
                break
            after, before = line.strip().split("|")
            RULES[after].add(before)
        rows = [row.strip().split(",") for row in f.readlines()]
        # print(middles_of_valid_rows(rows))  # part 1
        print(middles_of_fixed_rows(rows))  # part 2
