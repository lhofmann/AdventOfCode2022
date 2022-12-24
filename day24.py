from collections import defaultdict
from heapq import heappush, heappop

DATA = open('day24.txt').read()
grid = DATA.splitlines()
rows, cols = len(grid), len(grid[0])

source = (0, next(i for i, c in enumerate(grid[0]) if c == '.'))
dest = (rows - 1, next(i for i, c in enumerate(grid[-1]) if c == '.'))
blizzards = {(i, j): [c] for i, row in enumerate(grid)
             for j, c in enumerate(row) if c in '><^v'}
states = {0: blizzards}


def next_state(state):
    blizzards = defaultdict(list)
    for (bi, bj), directions in state.items():
        for direction in directions:
            ni = bi + {'^': -1, 'v': 1, '<': 0, '>': 0}[direction]
            nj = bj + {'^': 0, 'v': 0, '<': -1, '>': 1}[direction]
            ni = 1 + (ni - 1) % (rows - 2)
            nj = 1 + (nj - 1) % (cols - 2)
            blizzards[(ni, nj)].append(direction)
    return blizzards


def run(time, source, dest):
    H = [(0, time) + source]
    visited = set()
    while H:
        _, time, i, j = heappop(H)
        if (time, i, j) in visited:
            continue
        if (i, j) == dest:
            return time
        visited.add((time, i, j))
        if time + 1 not in states:
            states[time + 1] = next_state(states[time])

        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1), (i, j)):
            if ni < 0 or nj < 0 or ni >= rows or nj >= cols or grid[ni][nj] == '#':
                continue
            if (ni, nj) in states[time + 1]:
                continue
            priority = time + 1 + abs(dest[0] - ni) + abs(dest[1] - nj)
            heappush(H, (priority, time + 1, ni, nj))


print(result := run(0, source, dest))
assert result == 240

result2 = run(result, dest, source)
result3 = run(result2, source, dest)
print(result3)
assert result3 == 717
