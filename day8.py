from bisect import bisect
DATA = open('day8.txt').read()

grid = [list(map(int, line)) for line in DATA.splitlines()]
rows, cols = len(grid), len(grid[0])
visible = [[False] * cols for _ in range(rows)]
score = [[1] * cols for _ in range(rows)]


def run(row, col, dr, dc):
    num_visible = 0
    current_max = float('-inf')
    S = [(float('+inf'), row, col)]

    while row >= 0 and col >= 0 and row < rows and col < cols:
        if grid[row][col] > current_max and not visible[row][col]:
            num_visible += 1
            visible[row][col] = True
        current_max = max(current_max, grid[row][col])

        i = bisect(S, (grid[row][col],))
        score[row][col] *= abs(row - S[i][1]) + abs(col - S[i][2])
        while grid[row][col] >= S[0][0]:
            S.pop(0)
        S.insert(0, (grid[row][col], row, col))

        row += dr
        col += dc
    return num_visible


result = 0
for row in range(rows):
    result += run(row, 0, 0, 1)
    result += run(row, cols - 1, 0, -1)
for col in range(cols):
    result += run(0, col, 1, 0)
    result += run(rows - 1, col, -1, 0)

print(result)
assert result == 1681

result = max(max(S) for S in score)
print(result)
assert result == 201684
