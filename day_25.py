from itertools import product

INPUT_FILE = "input_25.txt"

WIDTH = 5
HEIGHT = 7


def is_fit(lock: list[int], key: list[int]) -> bool:
    for col in range(WIDTH):
        if key[col] + lock[col] > HEIGHT:
            return False
    return True


def main():
    with open(INPUT_FILE, "r") as f:
        locks = []
        keys = []

        for block in f.read().split("\n\n"):
            block = [line.strip() for line in block.splitlines()]
            item = []
            for col in zip(*block):
                item.append(col.count("#"))
            if block[0][0] == "#":
                locks.append(item)
            else:
                keys.append(item)

    print(sum(is_fit(*comb) for comb in product(locks, keys)))  # part 1


if __name__ == "__main__":
    main()
