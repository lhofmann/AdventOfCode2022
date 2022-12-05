import re

DATA = open('day5.txt').read()


def run(pick_multiple=False):
    stacks = []
    STACK_EXPR = r'(   |\[(\w)\]) ?'

    for line in DATA.splitlines():
        if not re.match(f'^({STACK_EXPR})+$', line):
            break
        groups = re.findall(STACK_EXPR, line)
        while len(stacks) < len(groups):
            stacks.append([])
        for stack, (_, c) in zip(stacks, groups):
            if c:
                stack.insert(0, c)

    for line in DATA.splitlines():
        m = re.match(r'^move (\d+) from (\d+) to (\d+)$', line)
        if not m:
            continue
        n, source, dest = map(int, m.groups())
        source, dest = source - 1, dest - 1
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
