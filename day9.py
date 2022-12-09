DATA = open('day9.txt').read()


def run(l=2):
    rope = [[0, 0] for _ in range(l)]
    visited = set([tuple(rope[-1])])

    for direction, n in (line.split() for line in DATA.splitlines()):
        vx, vy = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0),
                  'R': (1, 0)}[direction]
        for _ in range(int(n)):
            rope[0][0] += vx
            rope[0][1] += vy

            for p, q in zip(rope[:-1], rope[1:]):
                dx, dy = p[0] - q[0], p[1] - q[1]
                if abs(dx) <= 1 and abs(dy) <= 1:
                    continue
                q[0] += max(-1, min(1, dx))
                q[1] += max(-1, min(1, dy))

            visited.add(tuple(rope[-1]))
    return len(visited)


result = run()
print(result)
assert result == 6311

result = run(10)
print(result)
assert result == 2482
