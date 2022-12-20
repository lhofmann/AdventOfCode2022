DATA = open('day20.txt').read()


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = self.next = None


def insert(node, neighbor, insert_after=True):
    if insert_after:
        left, right = neighbor, neighbor.next
    else:
        left, right = neighbor.prev, neighbor
    left.next = node
    right.prev = node
    node.next = right
    node.prev = left


def delete(node):
    left, right = node.prev, node.next
    left.next = right
    right.prev = left


def parse():
    nodes = []
    head = Node(None)
    head.prev = head.next = head
    for n in map(int, DATA.splitlines()):
        node = Node(n)
        nodes.append(node)
        insert(node, head, False)
    delete(head)
    return nodes


def mix(nodes):
    for node in nodes:
        n = node.value % (len(nodes) - 1)
        neighbor = node
        for _ in range(abs(n)):
            neighbor = neighbor.next if n > 0 else neighbor.prev
        if node == neighbor:
            continue
        delete(node)
        insert(node, neighbor, True)


def get_result(nodes):
    result = 0
    node = next(node for node in nodes if node.value == 0)
    for i in range(3001):
        if i % 1000 == 0:
            result += node.value
        node = node.next
    return result


nodes = parse()
mix(nodes)
result = get_result(nodes)
print(result)
assert result == 19070


nodes = parse()
for node in nodes:
    node.value *= 811589153
for _ in range(10):
    mix(nodes)
result = get_result(nodes)
print(result)
assert result == 14773357352059
