#!/usr/bin/env python

from typing import NamedTuple
from collections import defaultdict
# from rich import print


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


tiles = defaultdict(int)

origin = Vector(0, 0)
delta_for = {
    'w': Vector(-2, 0),
    'e': Vector(2, 0),
    'nw': Vector(-1, -1),
    'ne': Vector(1, -1),
    'sw': Vector(-1, 1),
    'se': Vector(1, 1),
}


def neighbours_for(t):
    return [t + d for d in delta_for.values()]


for line in open('day24.txt').readlines():
    line = list(line.strip())
    tile = origin
    while line:
        char = line.pop(0)
        if char not in delta_for:
            char += line.pop(0)
        tile += delta_for[char]

    tiles[tile] = 1 - tiles[tile]

print("part1:", len([t for t in tiles.values() if t]))

# print(tiles.keys())

for m in range(100):
    check_tiles = []
    new_tiles = defaultdict(int)
    for t in tiles.keys():
        check_tiles.extend([t] + neighbours_for(t))
    for t in check_tiles:
        black_count = len([1 for n in neighbours_for(t) if tiles[n] == 1])
        if tiles[t] == 0 and black_count == 2:  # white
            new_tiles[t] = 1
        if tiles[t] == 1:
            if not (black_count == 0 or black_count > 2):
                new_tiles[t] = 1

    # print(sorted([t for t, v in tiles.items() if v == 1]))
    # print(sorted([t for t, v in new_tiles.items() if v == 1]))
    tiles = new_tiles

    # print("move:", m, len([t for t in tiles.values() if t]))


print("part2:", len([t for t in tiles.values() if t]))
