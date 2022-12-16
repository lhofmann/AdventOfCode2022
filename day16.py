from dataclasses import dataclass
import re

DATA = open('day16.txt').read()


@dataclass
class Node:
    flow: int
    neighbors: list


nodes = {}
for line in DATA.splitlines():
    m = re.match(
        r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)',
        line)
    nodes[m.group(1)] = Node(int(m.group(2)), m.group(3).split(', '))


cache = {}


def max_pressure(node, time, opened):
    if time <= 0 or len(opened) == len(nodes):
        return 0
    cache_key = (node, time, tuple(sorted(opened)))
    if cache_key in cache:
        return cache[cache_key]
    result = 0
    if nodes[node].flow != 0 and node not in opened:
        opened_new = opened.copy()
        opened_new.add(node)
        result = (time - 1) * nodes[node].flow + \
            max_pressure(node, time - 1, opened_new)
    for neighbor in nodes[node].neighbors:
        result = max(result, max_pressure(neighbor, time - 1, opened))
    cache[cache_key] = result
    return result


result = max_pressure('AA', 30, set())
print(result)
assert result == 1617


cache = {}


def max_pressure2(node1, node2, time, opened):
    if time <= 0 or len(opened) == len(nodes):
        return 0
    cache_key = (node1, node2, time, tuple(sorted(opened)))
    cache_key_sym = (node2, node1, time, tuple(sorted(opened)))
    if cache_key in cache:
        return cache[cache_key]
    if cache_key_sym in cache:
        return cache[cache_key_sym]

    result = 0

    for neighbor1 in [node1] + nodes[node1].neighbors:
        if neighbor1 == node1 and (nodes[node1].flow == 0 or node1 in opened):
            continue

        for neighbor2 in [node2] + nodes[node2].neighbors:
            result_inner = 0
            opened_new = opened.copy()
            if neighbor1 == node1:
                opened_new.add(node1)
                result_inner += (time - 1) * nodes[node1].flow

            if neighbor2 == node2:
                if nodes[node2].flow == 0 or node2 in opened_new:
                    continue
                opened_new.add(node2)
                result_inner += (time - 1) * nodes[node2].flow

            result_inner += max_pressure2(neighbor1,
                                          neighbor2, time - 1, opened_new)
            result = max(result, result_inner)

    cache[cache_key] = cache[cache_key_sym] = result
    return result


result = max_pressure2('AA', 'AA', 26, set())
print(result)
assert result == 2171
