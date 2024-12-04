INPUT_FILE = "input_4.txt"

WORD = set("MAS")


def find_all_xmas(grid: list[list[str]]) -> int:
    n, m = len(grid), len(grid[0])

    def valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m

    def find_xmas(x: int, y: int) -> bool:
        """
        x, y is a position in a grid
        """
        words = [
            {grid[x - 1][y - 1], grid[x][y], grid[x + 1][y + 1]},
            {grid[x + 1][y - 1], grid[x][y], grid[x - 1][y + 1]},
        ]
        return all(w == WORD for w in words)

    ans = 0
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if grid[i][j] == "A":
                ans += find_xmas(i, j)
    return ans


if __name__ == "__main__":
    grid = []
    with open(INPUT_FILE) as f:
        for line in f:
            grid.append(list(line.strip()))
    print(find_all_xmas(grid))
