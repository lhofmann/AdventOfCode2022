DATA = open('day18.txt').read()

cubes = set(tuple(map(int, line.split(','))) for line in DATA.splitlines())

result = 0
for x, y, z in cubes:
    for nx, ny, nz in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                       (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
        if (nx, ny, nz) not in cubes:
            result += 1

print(result)
assert result == 4456


min_x, max_x = min(x for x, _, _ in cubes) - 1, max(x for x, _, _ in cubes) + 1
min_y, max_y = min(y for _, y, _ in cubes) - 1, max(y for _, y, _ in cubes) + 1
min_z, max_z = min(z for _, _, z in cubes) - 1, max(z for _, _, z in cubes) + 1

S = [(min_x, min_y, min_z)]
visited = set()
result = 0
while S:
    x, y, z = S.pop(0)
    if (x, y, z) in visited:
        continue
    visited.add((x, y, z))
    for nx, ny, nz in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z),
                       (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
        if nx < min_x or ny < min_y or nz < min_z or \
           nx > max_x or ny > max_y or nz > max_z:
            continue
        if (nx, ny, nz) in cubes:
            result += 1
        else:
            S.append((nx, ny, nz))


print(result)
assert result == 2510
