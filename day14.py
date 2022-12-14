DATA = open('day14.txt').read()

AIR, ROCK, SAND = 0, 1, 2

grid = [[AIR] * 1000 for _ in range(1000)]
y_max = 0
for path in ([tuple(map(int, coord.split(','))) for coord in line.split(' -> ')]
             for line in DATA.splitlines()):
    for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
        y_max = max(y_max, y0, y1)
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        if x0 == x1:
            for y in range(y0, y1 + 1):
                grid[y][x0] = ROCK
        if y0 == y1:
            for x in range(x0, x1 + 1):
                grid[y0][x] = ROCK


def insert(x, y, abyss):
    if y == y_max + 1:
        if not abyss:
            grid[y][x] = SAND
        return False
    if grid[y + 1][x] == AIR:
        return insert(x, y + 1, abyss)
    elif grid[y + 1][x - 1] == AIR:
        return insert(x - 1, y + 1, abyss)
    elif grid[y + 1][x + 1] == AIR:
        return insert(x + 1, y + 1, abyss)
    grid[y][x] = SAND
    return True


def part1():
    result = 0
    while insert(500, 0, True):
        result += 1
    return result


def part2():
    result = 0
    while grid[0][500] == AIR:
        insert(500, 0, False)
        result += 1
    return result


grid_input = [row[:] for row in grid]
result = part1()
print(result)
assert result == 838

grid = grid_input
result = part2()
print(result)
assert result == 27539
