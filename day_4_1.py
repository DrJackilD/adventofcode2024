INPUT_FILE = "input_4.txt"

WORD = list("XMAS")
WL = 4

DIRS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


def find_all_xmas(grid: list[list[str]]) -> int:
    n, m = len(grid), len(grid[0])

    def valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m

    def find_xmas(x: int, y: int, i: int, dir: tuple[int, int]) -> int:
        """
        x, y is a position in a grid
        i is the pointer to the character in the XMAS word
        """
        if i == WL - 1:
            return 1

        i += 1
        ans = 0
        to_x, to_y = dir
        nx, ny = x + to_x, y + to_y
        if valid(nx, ny) and grid[nx][ny] == WORD[i]:
            if find_xmas(nx, ny, i, dir):
                ans += 1
        return ans

    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "X":
                for dir in DIRS:
                    ans += find_xmas(i, j, 0, dir)
    return ans


if __name__ == "__main__":
    grid = []
    with open(INPUT_FILE) as f:
        for line in f:
            grid.append(list(line.strip()))
    print(find_all_xmas(grid))
