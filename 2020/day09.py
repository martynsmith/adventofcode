#!/usr/bin/env python

import itertools

data = open('day09.txt').readlines()

preamble_length = 25

buf = []

for line in data:
    n = int(line.strip())
    if len(buf) < preamble_length:
        buf.append(n)
        continue

    if not any(
            (x, y) for x, y in itertools.combinations(buf, 2) if x + y == n and x != y
    ):
        part1 = n
        break

    buf.append(n)
    buf.pop(0)

print(f"part1: {part1}")

buf = []
for line in data:
    n = int(line.strip())
    buf.append(n)

    while sum(buf) > part1:
        buf.pop(0)

    if len(buf) >= 2 and sum(buf) == part1:
        break

print(f"part2: {min(buf) + max(buf)}")
