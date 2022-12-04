DATA = open('day4.txt').read()

result = 0
result2 = 0
for (a, b), (c, d) in (map(lambda s: map(int, s.split('-')), line.split(','))
                       for line in DATA.splitlines()):
    if a >= c:
        a, b, c, d = c, d, a, b
    result += b >= d or (c == a and d >= b)
    result2 += b >= c

print(result)
assert result == 431
print(result2)
assert result2 == 823
