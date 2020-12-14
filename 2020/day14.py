#!/usr/bin/env python

from rich import print
from itertools import zip_longest, combinations
import re

data = [x.strip() for x in open('day14.txt').readlines()]

# data = """
# mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# """.strip().split('\n')

# part 1

mem = {}

for line in data:
    match = re.search(r'mask = (\S+)', line)
    if match:
        mask = list(reversed(match.group(1)))
        continue

    match = re.search(r'mem\[(\d+)\] = (\d+)', line)
    addr, value = match.groups()
    binary_value = list(reversed(str(bin(int(value)))[2:]))
    masked_value = int(
        "".join(reversed([x if y == 'X' else y for x, y in zip_longest(binary_value, mask, fillvalue="0")])), 2)
    mem[addr] = masked_value

print("part1:", sum(mem.values()))

# part 1

# data = """
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# """.strip().split('\n')

mem = {}

for line in data:
    match = re.search(r'mask = (\S+)', line)
    if match:
        mask = list(reversed(match.group(1)))
        continue

    match = re.search(r'mem\[(\d+)\] = (\d+)', line)
    addr, value = match.groups()
    addr = int(addr)
    value = int(value)

    floaters = []

    for power, mask_value in enumerate(mask):
        if mask_value == "1":
            addr |= 2 ** power
        if mask_value == 'X':
            floaters.append(power)

    addrs = []

    mutated_addr = addr
    for power in floaters:
        mutated_addr &= (2**37-1) - 2**power
    addrs.append(mutated_addr)

    for x in range(len(floaters)):
        for c in combinations(floaters,  x + 1):
            mutated_addr = addr
            for power in floaters:
                if power in c:
                    mutated_addr |= 2**power
                else:
                    mutated_addr &= (2**37-1) - 2**power
            addrs.append(mutated_addr)

    for addr in addrs:
        mem[addr] = value

print("part2:", sum(mem.values()))
