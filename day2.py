DATA = open('day2.txt').read()

score = 0
score2 = 0

for a, b in (line.split() for line in DATA.splitlines()):
    a, b = 'ABC'.index(a), 'XYZ'.index(b)
    score += [1, 2, 3][b] + (a == b) * 3 + ((b - a) % 3 == 1) * 6
    score2 += (b == 0) * ([3, 1, 2][a] + 0) + \
              (b == 1) * ([1, 2, 3][a] + 3) + \
              (b == 2) * ([2, 3, 1][a] + 6)

print(score)
assert score == 14531
print(score2)
assert score2 == 11258
