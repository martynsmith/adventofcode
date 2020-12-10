#!/usr/bin/env python

from collections import defaultdict

data = [int(x) for x in open('day10.txt').readlines()]

# data = [
#     16
#     , 10
#     , 15
#     , 5
#     , 1
#     , 11
#     , 7
#     , 19
#     , 6
#     , 12
#     , 4
# ]

j = 0

counts = defaultdict(int)

for n in sorted(data):
    counts[n - j] += 1
    j = n

counts[3] += 1

print(f"part1: {counts[1] * counts[3]}")


def count_possibilities_from(x):
    count = 0
    for n in range(x - 3, x):
        if n in data:
            count += count_possibilities_from(n)
        elif n == 0:
            return 1

    return count


print(f"part2: {count_possibilities_from(max(data))}")
