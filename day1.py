from heapq import heappush, heappop

DATA = open('day1.txt').read()

current = 0
result = 0
H = []

def insert(n):
    global result
    result = max(result, n)
    heappush(H, n)
    if len(H) > 3:
        heappop(H)

for line in DATA.splitlines():
    if not line:
        insert(current)
        current = 0
    else:
        current += int(line)
insert(current)

print(result)
assert result == 70374
print(sum(H))
assert sum(H) == 204610
