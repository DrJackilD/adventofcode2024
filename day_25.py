INPUT_FILE = "input_25.txt"

WIDTH = 5
HEIGHT = 7


def is_fit(key: list[int], lock: list[int]) -> bool:
    for col in range(WIDTH):
        if key[col] + lock[col] > HEIGHT:
            return False
    return True


def get_unique_pairs(locks: list[list[int]], keys: list[list[int]]) -> int:
    unique_pairs = set()
    for lock in locks:
        for i, key in enumerate(keys):
            if is_fit(key, lock):
                unique_pairs.add((tuple(key), tuple(lock)))
    return len(unique_pairs)


def main():
    with open(INPUT_FILE, "r") as f:
        locks = []
        keys = []
        curr = []
        for line in f:
            line = line.strip()
            if not line:
                item = []
                for col in zip(*curr):
                    item.append(col.count("#"))
                if curr[0][0] == "#":
                    locks.append(item)
                else:
                    keys.append(item)
                curr = []
            else:
                curr.append(list(line))
        if curr:
            item = []
            for col in zip(*curr):
                item.append(col.count("#"))
            if curr[0][0] == "#":
                locks.append(item)
            else:
                keys.append(item)

    print(get_unique_pairs(locks, keys))  # part 1


if __name__ == "__main__":
    main()
