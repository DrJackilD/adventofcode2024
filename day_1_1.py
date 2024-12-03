from heapq import *

INPUT_FILE = "input_1.txt"


def get_distance_sum():
    first, second = [], []
    with open(INPUT_FILE) as f:
        for line in f.readlines():
            a, b = line.split()
            heappush(first, int(a))
            heappush(second, int(b))

    ans = 0
    while first and second:
        a, b = heappop(first), heappop(second)
        ans += abs(a-b)
    return ans


if __name__ == "__main__":
    print(get_distance_sum())
