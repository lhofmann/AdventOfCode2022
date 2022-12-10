DATA = open('day10.txt').read()
ROWS, COLS = 6, 40


def run():
    t, x, result = 0, 1, 0
    screen = [['.'] * COLS for _ in range(ROWS)]

    def tick():
        nonlocal t, result
        t += 1
        if (t - 20) % 40 == 0:
            result += t * x
        r = (t - 1) // COLS
        c = (t - 1) % COLS
        if abs(c - x) <= 1:
            screen[r][c] = '#'

    for line in DATA.splitlines():
        tick()
        if line.split()[0] == 'addx':
            tick()
            x += int(line.split()[1])

    return result, screen


result, screen = run()
print(result)
print('\n'.join(''.join(row) for row in screen))
assert result == 12520
