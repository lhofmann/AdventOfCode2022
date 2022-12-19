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

cache = {}


def max_pressure(node, time, opened):
    if time <= 0 or len(opened) == len(nodes):
        return 0
    cache_key = (node, time, tuple(sorted(opened)))
    if cache_key in cache:
        return cache[cache_key]
    result = 0
    if flow[node] != 0 and node not in opened:
        opened_new = opened.copy()
        opened_new.add(node)
        result = (time - 1) * flow[node] + \
                 max_pressure(node, time - 1, opened_new)
    for neighbor in neighbors[node]:
        result = max(result, max_pressure(neighbor, time - 1, opened))
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
