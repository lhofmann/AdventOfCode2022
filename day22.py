DATA = open('day22.txt').read()
GRID, MOVES = DATA.split('\n\n')
REGION_SIZE = 50

grid = GRID.splitlines()
rows = len(grid)
cols = max(len(row) for row in grid)
grid = [row + ' ' * (cols - len(row)) for row in grid]


def moves():
    current = 0
    for c in MOVES.strip():
        if c in 'RL':
            if current != 0:
                yield current
                current = 0
            yield {'R': 1j, 'L': -1j}[c]
        else:
            current = 10 * current + int(c)
    if current != 0:
        yield current


def wrap_around(x, y, orientation):
    nx, ny = x, y
    while nx >= 0 and ny >= 0 and nx < cols and ny < rows and grid[ny][nx] != ' ':
        nx -= int(orientation.real)
        ny -= int(orientation.imag)
    nx, ny = nx + int(orientation.real), ny + int(orientation.imag)
    return nx, ny, orientation


def run(wrap):
    y = 0
    x = next(x for x, g in enumerate(grid[y]) if g == '.')
    orientation = 1 + 0j

    for move in moves():
        if isinstance(move, complex):
            orientation *= move
            continue
        for _ in range(move):
            nx, ny = x + int(orientation.real), y + int(orientation.imag)
            norientation = orientation
            if nx < 0 or ny < 0 or nx >= cols or ny >= rows or grid[ny][nx] == ' ':
                nx, ny, norientation = wrap(x, y, orientation)
            if grid[ny][nx] == '.':
                x, y, orientation = nx, ny, norientation

    return 1000 * (1 + y) + 4 * (1 + x) + \
        {1: 0, 1j: 1, -1: 2, -1j: 3}[orientation]


print(result := run(wrap_around))
assert result == 75254


def permute(p, q):
    return tuple(p[i] for i in q)


# Orientation of cube <-> permutation of its faces.
BOTTOM, BACK, TOP, FRONT, LEFT, RIGHT = range(6)
# Generators of the symmetry group.
IDENTITY = (BOTTOM, BACK, TOP, FRONT, LEFT, RIGHT)
ROLL_UP = (BACK, TOP, FRONT, BOTTOM, LEFT, RIGHT)
ROLL_DOWN = (FRONT, BOTTOM, BACK, TOP, LEFT, RIGHT)
ROLL_LEFT = (LEFT, BACK, RIGHT, FRONT, TOP, BOTTOM)
ROLL_RIGHT = (RIGHT, BACK, LEFT, FRONT, BOTTOM, TOP)
# Check group invariants.
assert (permute(permute(IDENTITY, ROLL_UP), ROLL_DOWN) == IDENTITY)
assert (permute(permute(IDENTITY, ROLL_DOWN), ROLL_UP) == IDENTITY)
assert (permute(permute(IDENTITY, ROLL_LEFT), ROLL_RIGHT) == IDENTITY)
assert (permute(permute(IDENTITY, ROLL_RIGHT), ROLL_LEFT) == IDENTITY)
for p in (ROLL_UP, ROLL_DOWN, ROLL_LEFT, ROLL_RIGHT, IDENTITY):
    q = IDENTITY
    for _ in range(4):
        q = permute(q, p)
    assert q == IDENTITY


regions = [[grid[i * REGION_SIZE][j * REGION_SIZE] != ' '
            for j in range(cols // REGION_SIZE)]
           for i in range(rows // REGION_SIZE)]

# Roll cube across regions and assign bottom face to each region.
j = 0
i = next(i for i, r in enumerate(regions[j]) if r)
faces = {}  # Maps a face of the cube to a region.
cube = {}  # Maps a region to an orientation.
S = [(i, j, IDENTITY)]
while S:
    i, j, p = S.pop(0)
    if (i, j) in cube:
        continue
    faces[p[0]] = (i, j)
    cube[(i, j)] = p
    for ni, nj, q in ((i, j - 1, ROLL_UP), (i, j + 1, ROLL_DOWN),
                      (i + 1, j, ROLL_RIGHT), (i - 1, j, ROLL_LEFT)):
        if ni < 0 or nj < 0 or ni >= len(regions[0]) or \
           nj >= len(regions) or not regions[nj][ni]:
            continue
        S.append((ni, nj, permute(p, q)))
assert len(faces) == 6

# Each region is assigned a unique face of the cube and a permutation p.
# Transitions across edges correspond to maps between permutations.
#
# E.g., moving from p(Btm) = q(L) downwards to p(F) = q(Btm):
# Orientation of the edge crossed is represented by p(L), p(R) (left to right)
# and changes to q(L), q(R) (top to bottom).
#
#  p  +---+             q  +---+
#     |Bck|                | L |
# +---+---+---+        +---+---+---+
# | L |Btm| R | ---->  |Btm| F | * |
# +---+---+---+        +---+---+---+
#     | F |                | R |
#     +---+                +---+
#


def wrap_cube(x, y, orientation):
    i, j = x // REGION_SIZE, y // REGION_SIZE
    p = cube[(i, j)]
    edge, source, dest = {
        -1j: (BACK, LEFT, RIGHT),
        1j: (FRONT, LEFT, RIGHT),
        1: (RIGHT, BACK, FRONT),
        -1: (LEFT, BACK, FRONT),
    }[orientation]

    ni, nj = faces[p[edge]]
    q = cube[(ni, nj)]

    if orientation.imag != 0:
        coord = x % REGION_SIZE
    else:
        coord = y % REGION_SIZE

    if q.index(p[source]) in [LEFT, RIGHT]:
        ny = REGION_SIZE * nj
        if q.index(p[0]) == FRONT:
            ny += REGION_SIZE - 1
            norientation = -1j
        else:
            assert q.index(p[0]) == BACK
            norientation = 1j
        if q.index(p[dest]) != RIGHT:
            nx = REGION_SIZE * (ni + 1) - 1 - coord
        else:
            nx = REGION_SIZE * ni + coord
    else:
        assert q.index(p[source]) in [BACK, FRONT]
        nx = REGION_SIZE * ni
        if q.index(p[0]) == RIGHT:
            nx += REGION_SIZE - 1
            norientation = -1
        else:
            assert q.index(p[0]) == LEFT
            norientation = 1
        if q.index(p[dest]) != FRONT:
            ny = REGION_SIZE * (nj + 1) - 1 - coord
        else:
            ny = REGION_SIZE * nj + coord

    return nx, ny, norientation


print(result := run(wrap_cube))
assert result == 108311
