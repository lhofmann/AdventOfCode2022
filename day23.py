from collections import defaultdict

DATA = open('day23.txt').read()
ELVES = {(i, j) for i, row in enumerate(DATA.splitlines())
         for j, c in enumerate(row) if c == '#'}


def move(elves, step):
    moves = []
    want_move = defaultdict(int)
    for i, j in elves:
        NE = (i - 1, j + 1)
        N = (i - 1, j)
        NW = (i - 1, j - 1)
        W = (i, j - 1)
        SW = (i + 1, j - 1)
        S = (i + 1, j)
        SE = (i + 1, j + 1)
        E = (i, j + 1)

        ni, nj = i, j
        if elves & {NE, N, NW, W, SW, S, SE, E}:
            for k in range(4):
                k = (k + step) % 4
                if k == 0 and not (elves & {N, NE, NW}):
                    ni -= 1
                    break
                if k == 1 and not (elves & {S, SE, SW}):
                    ni += 1
                    break
                if k == 2 and not (elves & {W, NW, SW}):
                    nj -= 1
                    break
                if k == 3 and not (elves & {E, NE, SE}):
                    nj += 1
                    break

        moves.append(((i, j), (ni, nj)))
        want_move[(ni, nj)] += 1

    elves_next = set()
    did_move = False
    for (i, j), (ni, nj) in moves:
        if want_move[(ni, nj)] == 1:
            elves_next.add((ni, nj))
            did_move = did_move or (i, j) != (ni, nj)
        else:
            elves_next.add((i, j))
    return elves_next, did_move


def part1():
    elves = ELVES.copy()
    for step in range(10):
        elves, _ = move(elves, step)
    min_i, max_i = min(i for i, _ in elves), max(i for i, _ in elves)
    min_j, max_j = min(j for _, j in elves), max(j for _, j in elves)
    return (max_i - min_i + 1) * (max_j - min_j + 1) - len(elves)


print(result := part1())
assert result == 3931


def part2():
    elves = ELVES.copy()
    step, did_move = 0, True
    while did_move:
        elves, did_move = move(elves, step)
        step += 1
    return step


print(result := part2())
assert result == 944
