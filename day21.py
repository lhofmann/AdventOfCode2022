from collections import defaultdict

DATA = open('day21.txt').read()
OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}

nodes, indegrees, dependencies = {}, defaultdict(int), defaultdict(list)
for label, value in (line.split(': ') for line in DATA.splitlines()):
    tokens = value.split()
    if len(tokens) == 1:
        nodes[label] = (int(tokens[0]),)
    else:
        nodes[label] = (tokens[0], tokens[2], OPS[tokens[1]])
        dependencies[label] = [tokens[0], tokens[2]]
        indegrees[label] = 2
neighbors = defaultdict(list)
for node in nodes.keys():
    for dependency in dependencies[node]:
        neighbors[dependency].append(node)


def evaluate(initial=None):
    values = {}
    if initial is not None:
        values['humn'] = initial
    indegrees_ = indegrees.copy()
    S = [node for node in nodes.keys() if indegrees_[node] == 0]
    while S:
        T = []
        for node in S:
            if node not in values:
                if len(nodes[node]) == 1:
                    values[node] = nodes[node][0]
                else:
                    a, b, op = nodes[node]
                    values[node] = op(values[a], values[b])
            for neighbor in neighbors[node]:
                indegrees_[neighbor] -= 1
                if indegrees_[neighbor] == 0:
                    T.append(neighbor)
        S = T
    return values['root']


print(result := evaluate())
assert result == 353837700405464


nodes['root'] = nodes['root'][:2] + (OPS['-'],)

a, b = 0, 10
fa, fb = evaluate(a), evaluate(b)
while fa * fb > 0:
    b *= 10
    fb = evaluate(b)
while a < b:
    m = a + (b - a) // 2
    fm = evaluate(m)
    if fa * fm <= 0:
        b = m - 1
        fb = evaluate(b)
    else:
        a = m + 1
        fa = evaluate(a)

print(result := a)
assert result == 3678125408017
