from itertools import cycle

DATA = open('day17.txt').read().strip()
SHAPES = '''
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''
SHAPES = tuple(map(str.splitlines, SHAPES.strip().split('\n\n')))
COLUMNS = 7


def can_place(grid, shape, x, y):
    if y < 0:
        return False
    for j, row in enumerate(reversed(shape)):
        for i, c in enumerate(row):
            if c == '#' and (x + i < 0 or x + i >=
                             COLUMNS or grid[y + j][x + i]):
                return False
    return True


def place(grid, shape, x, y):
    result = 0
    for j, row in enumerate(reversed(shape)):
        for i, c in enumerate(row):
            if c == '#':
                result = max(result, y + j)
                grid[y + j][x + i] = True
    return result


def run(blocks=2022):
    grid = [[False] * COLUMNS for _ in range(1000)]
    height = 0
    y_offset = 0
    i = 0
    j = 0
    block = 0
    cache = {}

    while block < blocks:
        x = 2
        y = height + 3 - y_offset
        shape = SHAPES[j]
        j = (j + 1) % len(SHAPES)
        while True:
            inp = DATA[i]
            i = (i + 1) % len(DATA)
            x_next = x + (1 if inp == '>' else -1)
            if can_place(grid, shape, x_next, y):
                x = x_next

            y_next = y - 1
            if not can_place(grid, shape, x, y_next):
                max_y = place(grid, shape, x, y)
                height = max(height, y_offset + max_y + 1)
                break
            y = y_next

        for y_full in reversed(range(y, y + 4)):
            if all(grid[y_full]):
                y_offset += y_full + 1
                grid = grid[y_full + 1:]
                grid += [[False] * COLUMNS for _ in range(y_full + 1)]
                break

        cache_key = (i, j,
                     tuple(tuple(row) for row in grid[:height - y_offset]))
        if cache_key in cache:
            prev_height, prev_block = cache[cache_key]
            dh = height - prev_height
            ds = block - prev_block
            skip = (blocks - block) // ds

            height += skip * dh
            y_offset += skip * dh
            block += skip * ds
        else:
            cache[cache_key] = (height, block)

        block += 1
    return height


result = run(2022)
print(result)
assert result == 3193

result = run(1000000000000)
print(result)
assert result == 1577650429835
