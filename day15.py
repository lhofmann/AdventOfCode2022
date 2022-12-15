import re

DATA = open('day15.txt').read()

sensors = []
for line in DATA.splitlines():
    m = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
    sensors.append(tuple(map(int, m.groups())))


def get_intervals(y):
    intervals = []
    for sx, sy, bx, by in sensors:
        r = abs(sx - bx) + abs(sy - by)
        l = r - abs(sy - y)
        if l < 0:
            continue
        intervals.append((sx - l, sx + l))
    intervals.sort()
    return intervals


def part1(y):
    result = 0
    intervals = get_intervals(y)
    ca, cb = intervals.pop(0)
    for a, b in intervals:
        if a > cb:
            result += cb - ca
            ca, cb = a, b
        else:
            cb = max(cb, b)
    result += cb - ca
    return result


def part2(area):
    for y in range(area + 1):
        intervals = get_intervals(y) + [(area, float('+inf'))]
        cb = 0
        for a, b in intervals:
            if a > cb:
                return (cb + 1) * 4000000 + y
            else:
                cb = max(cb, b)


result = part1(2000000)
print(result)
assert result == 4424278

result = part2(4000000)
print(result)
assert result == 10382630753392