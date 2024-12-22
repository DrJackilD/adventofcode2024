from collections import defaultdict

INPUT_FILE = "input_22.txt"


def next_secret(secret: int) -> int:
    secret ^= secret * 64
    secret = secret % 16777216

    secret ^= secret // 32
    secret = secret % 16777216

    secret ^= secret * 2048
    secret = secret % 16777216
    return secret


def get_n_secret(nums: list[int], n: int) -> list[int]:
    for _ in range(n):
        nums = [next_secret(num) for num in nums]
    return nums


def get_price_changes(num: int, n: int) -> list[tuple[int, int]]:
    changes = []
    curr = num
    for _ in range(n):
        nsecret = next_secret(curr)
        changes.append((nsecret % 10 - curr % 10, nsecret % 10))
        curr = nsecret
    return changes


def get_max_income(nums: list[int], n: int) -> int:
    seqs = defaultdict(int)
    for num in nums:
        changes = get_price_changes(num, n)
        seen = set()
        for start in range(len(changes) - 3):
            seq = tuple([ch[0] for ch in changes[start:start + 4]])
            if seq in seen:
                continue

            seen.add(seq)
            seqs[seq] += changes[start + 3][1]
    return max(seqs.values())


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        data = [int(line.strip()) for line in f]
    print(sum(get_n_secret(data, 2000)))  # part 1
    print(get_max_income(data, 2000))  # part 2
