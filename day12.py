from heapq import heapify, heappop, heappush

DATA = open('day12.txt').read()

start_a = []

for i, row in enumerate(DATA.splitlines()):
    if 'S' in row:
        start = (i, row.index('S'))
    if 'E' in row:
        dest = (i, row.index('E'))
    start_a += [(i, j) for j, c in enumerate(row) if c == 'a']

grid = [[ord(c) - ord('a') if c not in 'SE' else [0, 25]['SE'.index(c)]
         for c in row] for row in DATA.splitlines()]
rows = len(grid)
cols = len(grid[0])


def heuristic(i, j):
    return abs(i - dest[0]) + abs(j - dest[1])


def run(initial):
    S = [(heuristic(i, j), (i, j), 0) for i, j in initial]
    heapify(S)
    visited = set()
    while S:
        _, (i, j), cost = heappop(S)
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if (i, j) == dest:
            return cost
        for ni, nj in ((i + 1, j + 0), (i - 1, j + 0),
                       (i + 0, j + 1), (i + 0, j - 1)):
            if ni < 0 or nj < 0 or ni >= rows or nj >= cols:
                continue
            if grid[ni][nj] - grid[i][j] > 1:
                continue
            priority = heuristic(ni, nj) + cost + 1
            heappush(S, (priority, (ni, nj), cost + 1))


result = run([start])
print(result)
assert result == 352

result = run(start_a)
print(result)
assert result == 345
