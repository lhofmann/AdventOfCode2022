from collections import defaultdict

DATA = open('day6.txt').read()


def run(n=4):
    counts = defaultdict(int)
    num_unique = 0
    for i, c in enumerate(DATA):
        if counts[c] == 1:
            num_unique -= 1
        elif counts[c] == 0:
            num_unique += 1
        counts[c] += 1
        if i >= n:
            d = DATA[i - n]
            if counts[d] == 1:
                num_unique -= 1
            elif counts[d] == 2:
                num_unique += 1
            counts[d] -= 1
        if num_unique == n:
            return i + 1


result = run(4)
print(result)
assert result == 1361

result = run(14)
print(result)
assert result == 3263
