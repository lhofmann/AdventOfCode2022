from dataclasses import dataclass, field
import re

DATA = open('day11.txt').read()


def make_op(op, t):
    def accessor(x):
        return x if t == 'old' else int(t)
    if op == '+':
        return lambda x: x + accessor(x)
    else:
        return lambda x: x * accessor(x)


@dataclass
class Monkey:
    items: list = None
    op: callable = None
    div: int = None
    next: dict = field(default_factory=dict)
    inspected: int = 0


def parse():
    monkeys = []
    current = None
    for line in DATA.splitlines():
        if m := re.match(r'Monkey (\d+):', line):
            current = Monkey()
            monkeys.append(current)
        elif m := re.match(r'  Starting items: ((\d+(, )?)+)', line):
            current.items = [int(s) for s in m.group(1).split(', ')]
        elif m := re.match(r'  Operation: new = old (\+|\*) (\d+|old)', line):
            current.op = make_op(m.group(1), m.group(2))
        elif m := re.match(r'  Test: divisible by (\d+)', line):
            current.div = int(m.group(1))
        elif m := re.match(r'    If (\w+): throw to monkey (\d+)', line):
            current.next[m.group(1) == 'true'] = int(m.group(2))
    return monkeys


def run(steps=20, divisor=3):
    monkeys = parse()
    mod = 1
    for monkey in monkeys:
        mod *= monkey.div
    for _ in range(steps):
        for monkey in monkeys:
            for item in monkey.items:
                item = (monkey.op(item) // divisor) % mod
                monkeys[monkey.next[item % monkey.div == 0]].items.append(item)
            monkey.inspected += len(monkey.items)
            monkey.items = []
    monkeys.sort(key=lambda m: m.inspected)
    result = monkeys[-1].inspected * monkeys[-2].inspected
    return result


result = run()
print(result)
assert result == 67830

result = run(10000, 1)
print(result)
assert result == 15305381442
