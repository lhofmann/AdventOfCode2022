DATA = open('day25.txt').read()


def from_snafu(s):
    result = 0
    for c in s:
        result = 5 * result + {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}[c]
    return result


def to_snafu(n):
    result = []
    while n:
        m = n % 5
        n = n // 5
        if m > 2:
            m = m - 5
            n += 1
        result.append(m)

    if not result:
        result = [0]
    return ''.join({2: '2', 1: '1', 0: '0', -1: '-', -2: '='}[n] for n in reversed(result))


result = to_snafu(sum(from_snafu(n) for n in DATA.splitlines()))
print(result)
assert result == '2-2--02=1---1200=0-1'
