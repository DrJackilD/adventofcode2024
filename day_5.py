from collections import defaultdict

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


def fix_page_ordering(row: list[str]) -> list[str]:
    n = len(row)
    if n == 1:
        return row

    # sort
    if n == 2:
        if row[0] in RULES[row[1]]:
            return [row[1], row[0]]
        return row

    pages1, pages2 = (
        fix_page_ordering(row[: (n // 2)]),
        fix_page_ordering(row[n // 2 :]),
    )
    fixed = []

    # merge
    i = j = 0
    n, m = len(pages1), len(pages2)
    while i < n and j < m:
        if pages1[i] in RULES[pages2[j]]:
            fixed.append(pages2[j])
            j += 1
        elif pages2[j] in RULES[pages1[i]]:
            fixed.append(pages1[i])
            i += 1
        else:
            fixed.append(pages1[i])
            fixed.append(pages2[j])
            i += 1
            j += 1

    if i < n:
        fixed.extend(pages1[i:])
    if j < m:
        fixed.extend(pages2[j:])
    return fixed


def middles_of_fixed_rows(rows: list[list[str]]) -> int:
    ans = 0
    for row in rows:
        if not is_valid_order(row):
            fixed = fix_page_ordering(row)
            ans += int(fixed[len(fixed) // 2])
    return ans


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        for line in f:
            if not line.strip():
                break
            before, after = line.strip().split("|")
            RULES[before].add(after)
        rows = [row.strip().split(",") for row in f.readlines()]
        # print(middles_of_valid_rows(rows))  # part 1
        print(middles_of_fixed_rows(rows))  # part 2
