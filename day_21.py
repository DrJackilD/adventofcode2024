from functools import cache

INPUT_FILE = "input_21.txt"

NUMPAD_TO_COORDINATES = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "X": (3, 0),
    "0": (3, 1),
    "A": (3, 2),
}

KEYPAD_TO_COORDINATES = {
    "X": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}


def get_all_possible(from_: str, to: str) -> list[str]:
    if any(key.isnumeric() for key in (from_, to)):
        x, y = NUMPAD_TO_COORDINATES[from_]
        ex, ey = NUMPAD_TO_COORDINATES[to]
        no_go = NUMPAD_TO_COORDINATES["X"]
    else:
        x, y = KEYPAD_TO_COORDINATES[from_]
        ex, ey = KEYPAD_TO_COORDINATES[to]
        no_go = KEYPAD_TO_COORDINATES["X"]

    horizontal = "<" if y > ey else ">"
    vertical = "^" if x > ex else "v"

    h_moves = horizontal * abs(y - ey)
    v_moves = vertical * abs(x - ex)

    paths = []
    if (x, ey) != no_go:
        paths.append(h_moves + v_moves + "A")
    if (ex, y) != no_go:
        paths.append(v_moves + h_moves + "A")
    return paths


@cache
def get_sequence_len(seq: str, depth: int) -> int:
    seq = "A" + seq  # add "A" to the beginning of the sequence because robo-hand is always starts at "A"

    ans = 0
    for from_, to in zip(seq, seq[1:]):
        paths = get_all_possible(from_, to)
        if depth == 0:
            ans += min(len(path) for path in paths)
        else:
            ans += min(get_sequence_len(path, depth - 1) for path in paths)
    return ans


def apply_codes(sequences: list[str], number_of_keypads: int) -> int:
    ans = 0
    for seq in sequences:
        ans += get_sequence_len(seq, number_of_keypads) * int(seq[:-1])

    return ans


if __name__ == "__main__":
    with open(INPUT_FILE, "r") as f:
        codes = [line.strip() for line in f.readlines()]
    print(apply_codes(codes, 2))  # part 1
    print(apply_codes(codes, 25))  # part 2
