#!/usr/bin/env python

import re
from functools import reduce

data = [l.strip() for l in open('day03.txt').readlines()]

def tree_count(dx, dy):
    x = 0
    y = 0
    tree_count = 0

    while y < len(data):
        row = data[y]
        if row[x] == '#':
            tree_count += 1
        x += dx
        y += dy
        x %= len(row)

    return tree_count

def part1():
    print(f"part1: {tree_count(3, 1)}")

def part2():
    tree_counts = [
        tree_count(1, 1),
        tree_count(3, 1),
        tree_count(5, 1),
        tree_count(7, 1),
        tree_count(1, 2),
    ]

    print("part2:", reduce(lambda a, b: a * b, tree_counts, 1))

part1()
part2()
