from functools import cmp_to_key

DATA = open('day13.txt').read()
DIVIDER = [[[2]], [[6]]]


def cmp_int(a, b):
    return (a > b) - (a < b)


def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return cmp_int(a, b)
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            if (c := cmp(a[i], b[i])) != 0:
                return c
        return cmp_int(len(a), len(b))
    elif not isinstance(a, list):
        return cmp([a], b)
    elif not isinstance(b, list):
        return cmp(a, [b])


result = sum(i + 1
             for i, (a, b) in enumerate(map(eval, block.splitlines())
                                        for block in DATA.split('\n\n'))
             if cmp(a, b) < 0)

print(result)
assert result == 5529

packets = [eval(line) for line in DATA.splitlines() if line] + DIVIDER
packets.sort(key=cmp_to_key(cmp))
result = (packets.index(DIVIDER[0]) + 1) * (packets.index(DIVIDER[1]) + 1)

print(result)
assert result == 27690
