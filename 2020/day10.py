#!/usr/bin/env python

from collections import defaultdict

data = [int(x) for x in open('day10.txt').readlines()]

j = 0

counts = defaultdict(int)

for n in sorted(data):
    counts[n - j] += 1
    j = n

counts[3] += 1

print(f"part1: {counts[1] * counts[3]}")

combinations_for = {0: 1}

for n in sorted(data):
    combinations_for.setdefault(n, 0)
    if n - 1 in combinations_for:
        combinations_for[n] += combinations_for[n - 1]
    if n - 2 in combinations_for:
        combinations_for[n] += combinations_for[n - 2]
    if n - 3 in combinations_for:
        combinations_for[n] += combinations_for[n - 3]

    counts[n - j] += 1
    j = n

print(f"part2: {combinations_for[max(data)]}")
