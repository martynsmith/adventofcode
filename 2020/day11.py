#!/usr/bin/env python

from collections import defaultdict

data = [x.strip() for x in open('day11.txt').readlines()]

cells = {}

for y, row in enumerate(data):
    for x, cell in enumerate(row):
        cells[(x, y)] = cell

delta = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

change_count = 0
for (x, y), cell in cells.items():
    if cell == '.':
        continue
    hash_count = 0
    for dx, dy in delta:
        if cells.get((x + dx, y + dy), '?') == '#':
            hash_count += 1

    if cell == 'L' and hash_count == 0:
        cells[(x, y)] = '#'
        change_count += 1

    print(cell, hash_count)

    # print(x, y, '=>', dx, dy, cells.get((x + dx, y + dy), '?'))

print(f"change_count: {change_count}")
