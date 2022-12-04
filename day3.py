DATA = open('day3.txt').read()


def priority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    return ord(c) - ord('A') + 27


result = 0
for items in DATA.splitlines():
    n = len(items) // 2
    both = set(items[:n]) & set(items[n:])
    result += sum(priority(c) for c in both)

print(result)
assert result == 7824

result = 0
lines = DATA.splitlines()
for i in range(0, len(lines), 3):
    badge = set(lines[i + 0]) & set(lines[i + 1]) & set(lines[i + 2])
    result += priority(badge.pop())

print(result)
assert result == 2798
