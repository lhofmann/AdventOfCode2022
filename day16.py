from collections import defaultdict
from itertools import chain, combinations
import re

DATA = open('day16.txt').read()

nodes, flow, neighbors = [], {}, {}
for line in DATA.splitlines():
    m = re.match(
        r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)',
        line)
    node = m.group(1)
    nodes.append(node)
    flow[node] = int(m.group(2))
    neighbors[node] = m.group(3).split(', ')

weighted_neighbors = defaultdict(list)
for initial in nodes:
    S = [(initial, 0)]
    visited = set()
    while S:
        node, weight = S.pop(0)
        if node in visited:
            continue
        visited.add(node)
        if node != initial:
            weighted_neighbors[initial].append((node, weight))
        for neighbor in neighbors[node]:
            S.append((neighbor, weight + 1))

cache = {}


def max_pressure(node, time, opened):
    if time <= 0 or len(opened) == len(nodes):
        return 0
    cache_key = (node, time, tuple(sorted(opened)))
    if cache_key in cache:
        return cache[cache_key]
    result = 0
    for neighbor, cost in weighted_neighbors[node]:
        if neighbor in opened or flow[neighbor] == 0 or cost + 1 > time:
            continue
        opened_new = opened.copy()
        opened_new.add(neighbor)
        result_new = (time - cost - 1) * flow[neighbor] + \
                     max_pressure(neighbor, time - cost - 1, opened_new)
        result = max(result, result_new)
    cache[cache_key] = result
    return result


result = max_pressure('AA', 30, set())
print(result)
assert result == 1617


def part2(time):
    result = 0
    keys = [node for node in nodes if flow[node] > 0]
    for mask in chain.from_iterable(combinations(keys, r)
                                    for r in range(1, len(keys))):
        mask = set(mask)
        inverted_mask = set(k for k in keys if k not in mask)
        if len(mask) > len(inverted_mask):
            continue
        pressure = max_pressure('AA', time, mask) + \
                   max_pressure('AA', time, inverted_mask)
        result = max(result, pressure)
    return result


result = part2(26)
print(result)
assert result == 2171
