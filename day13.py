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


def quickselect(packets, divider):
    pivot = packets[-1]
    left = [packet for packet in packets if cmp(packet, pivot) < 0]
    c = cmp(divider, pivot)
    if c == 0:
        return len(left)
    elif c < 0:
        return quickselect(left, divider)
    right = [packet for packet in packets if cmp(packet, pivot) > 0]
    return len(left) + quickselect(right, divider)


packets = [eval(line) for line in DATA.splitlines() if line] + DIVIDERS
result = (quickselect(packets, DIVIDERS[0]) + 1) * \
         (quickselect(packets, DIVIDERS[1]) + 1)

print(result)
assert result == 27690
