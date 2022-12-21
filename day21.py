from collections import defaultdict
import math

DATA = open('day21.txt').read()
FLOAT_DIV = False
OPS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if FLOAT_DIV else a // b,
}

nodes, dependencies = {}, defaultdict(list)
for label, value in (line.split(': ') for line in DATA.splitlines()):
    tokens = value.split()
    if len(tokens) == 1:
        nodes[label] = (int(tokens[0]),)
    else:
        nodes[label] = (tokens[0], tokens[2], OPS[tokens[1]])
        dependencies[label] = [tokens[0], tokens[2]]
neighbors = defaultdict(list)
for node in nodes.keys():
    for dependency in dependencies[node]:
        neighbors[dependency].append(node)


def evaluate(initial=None):
    values = {}
    if initial is not None:
        values['humn'] = initial
    indegrees = {node: len(dependencies[node]) for node in nodes.keys()}
    S = [node for node in nodes.keys() if indegrees[node] == 0]
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
                indegrees[neighbor] -= 1
                if indegrees[neighbor] == 0:
                    T.append(neighbor)
        S = T
    return values['root']


print(result := evaluate())
assert result == 353837700405464


nodes['root'] = nodes['root'][:2] + (OPS['-'],)

FLOAT_DIV = True
result = 42
h = 1
f = evaluate(result)
while abs(f) >= 0.1:
    df = (evaluate(result + h) - evaluate(result - h)) / (2 * h)
    result = result - f / df
    f = evaluate(result)
result = math.floor(result)
if evaluate(result) != 0:
    result += 1

print(result)
assert result == 3678125408017
