from collections import defaultdict

DATA = open('day7.txt').read()


class Node:
    def __init__(self):
        self.parent = None
        self.childs = defaultdict(Node)
        self.file_size = 0


root = Node()
node = None
i = 0
lines = DATA.splitlines()
while i < len(lines):
    cmd = lines[i].split()
    assert cmd[0] == '$'
    if cmd[1] == 'ls':
        node.file_size = 0
        i += 1
        while i < len(lines) and not lines[i].startswith('$'):
            size, name = lines[i].split()
            if size != 'dir':
                node.file_size += int(size)
            i += 1
    elif cmd[1] == 'cd':
        if cmd[2] == '/':
            node = root
        elif cmd[2] == '..':
            node = node.parent
        else:
            prev = node
            node = node.childs[cmd[2]]
            node.parent = prev
        i += 1


MAX_SIZE = 100000


def part1(node):
    size = node.file_size
    result = 0
    for child in node.childs.values():
        child_size, child_result = part1(child)
        size += child_size
        result += child_result
    if size <= MAX_SIZE:
        result += size
    return size, result


total, result = part1(root)
print(result)
assert result == 1086293

TOTAL_SIZE = 70000000
REQUIRED_SIZE = 30000000
min_size = REQUIRED_SIZE - TOTAL_SIZE + total


def part2(node):
    size = node.file_size
    result = float('inf')
    for child in node.childs.values():
        child_size, child_result = part2(child)
        size += child_size
        result = min(result, child_result)
    if size >= min_size:
        result = min(result, size)
    return size, result


result = part2(root)[1]
print(result)
assert result == 366028
