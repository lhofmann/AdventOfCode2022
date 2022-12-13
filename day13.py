from functools import cmp_to_key

DATA = open('day13.txt').read()
DIVIDERS = [[[2]], [[6]]]


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


def select(packets, divider):
    return sum(1 for packet in packets if cmp(packet, divider) < 0)


packets = [eval(line) for line in DATA.splitlines() if line] + DIVIDERS
result = (select(packets, DIVIDERS[0]) + 1) * \
         (select(packets, DIVIDERS[1]) + 1)

print(result)
assert result == 27690
