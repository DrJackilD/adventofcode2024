INPUT_FILE = "input_9.txt"


def get_segments(memory: list[int]) -> list[str]:
    """returns the segments map"""
    segments = []
    id_seq = 0
    for i, val in enumerate(memory):
        fill = str(id_seq) if i % 2 == 0 else "_"
        if i % 2 == 0:
            id_seq += 1
        for _ in range(val):
            segments.append(fill)
    return segments


def calculate_checksum(segments: list[str]) -> int:
    checksum = 0
    for i, file_id in enumerate(segments):
        if file_id == "_":
            continue
        checksum += i * int(segments[i])
    return checksum


def compact(memory: list[int]) -> int:
    segments = get_segments(memory)
    n = len(segments)

    left, right = 0, n - 1
    while left < right:
        while segments[left] != "_":
            left += 1
        while segments[right] == "_":
            right -= 1
        if left >= right:
            break
        segments[left], segments[right] = segments[right], "_"
        left += 1
        right -= 1
    return calculate_checksum(segments)


def defragment(memory: list[int]) -> int:
    segments = get_segments(memory)
    segment_ids = [0]
    for i in range(len(memory)):
        segment_ids.append(segment_ids[-1] + memory[i])

    for i in range(len(memory) - 1, -1, -1):
        if i % 2 != 0:
            continue

        free_mem_ix = None
        for j in range(1, i, 2):
            if memory[j] >= memory[i]:
                free_mem_ix = j
                break
        if not free_mem_ix:
            continue

        file_id = i // 2
        free_ix = segment_ids[free_mem_ix]
        file_ix = segment_ids[i]
        for _ in range(memory[i]):
            segments[free_ix] = str(file_id)
            segments[file_ix] = "_"
            file_ix += 1
            free_ix += 1
        segment_ids[free_mem_ix] += memory[i]
        memory[free_mem_ix] = memory[free_mem_ix] - memory[i]
        memory[i] = 0
    return calculate_checksum(segments)


if __name__ == "__main__":
    memory = []
    with open(INPUT_FILE) as f:
        line = f.readline()
        memory = [int(i) for i in line.strip()]
    print(compact(memory))  # part 1
    print(defragment(memory))  # part 2
