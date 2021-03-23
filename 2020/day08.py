#!/usr/bin/env python

from rich import print

data = open('day08.txt').readlines()
operations = [l.strip().split(' ') for l in data]


def run():
    ptr = 0
    acc = 0
    seen_ptr = set()

    while ptr not in seen_ptr and ptr < len(operations):
        seen_ptr.add(ptr)
        operation = operations[ptr][0]
        argument = int(operations[ptr][1])

        if operation == 'acc':
            acc += argument
            ptr += 1
        elif operation == 'jmp':
            ptr += argument
        elif operation == 'nop':
            ptr += 1
        else:
            raise ValueError(f"invalid {operation=}")

    return ptr, acc


print(f"part1: {run()[1]}")

for index, (operation, argument) in list(enumerate(operations)):
    if operation == 'acc':
        continue
    if operation == 'jmp':
        operations[index][0] = 'nop'
    elif operation == 'nop':
        operations[index][0] = 'jmp'

    ptr, acc = run()
    if len(operations) == ptr:
        print(f"part2: {acc}")

    if operation == 'jmp':
        operations[index][0] = 'jmp'
    elif operation == 'nop':
        operations[index][0] = 'nop'
