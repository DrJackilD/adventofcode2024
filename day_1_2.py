from collections import Counter

INPUT_FILE = "input_1.txt"


def get_similatiry_sum():
    first, second = Counter(), Counter()
    with open(INPUT_FILE) as f:
        for line in f.readlines():
            a, b = line.split()
            first[int(a)] += 1
            second[int(b)] += 1

    total_score = 0
    for a in first:
        sim_score = a * second[a]
        total_score += first[a] * sim_score
    return total_score


if __name__ == "__main__":
    print(get_similatiry_sum())
