import re

DATA = open('day5.txt').read()

def run(pick_multiple = False):
    stacks = []

    for line in DATA.splitlines():
        if not line:
            break
        if '[' not in line:
            continue
        for i in range(1, len(line), 4):
            c = line[i]
            if not c.isalpha():
                continue
            stack = (i - 1) // 4
            while len(stacks) < stack + 1:
                stacks.append([])
            stacks[stack].insert(0, c)

    for line in DATA.splitlines():    
        groups = re.match(r'^move (\d+) from (\d+) to (\d+)$', line)
        if not groups:
            continue
        n = int(groups.group(1))
        source = int(groups.group(2)) - 1
        dest = int(groups.group(3)) - 1
        if pick_multiple:
            stacks[dest] += stacks[source][-n:]
            stacks[source] = stacks[source][:-n]
        else:
            for _ in range(n):
                stacks[dest].append(stacks[source].pop())

    result = ''.join(s[-1] for s in stacks)
    return result

result = run()
print(result)
assert result == 'VPCDMSLWJ'

result = run(True)
print(result)
assert result == 'TPWCGNCCG'