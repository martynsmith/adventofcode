#!/usr/bin/env python

from itertools import product
from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def neighbours(self):
        neighbour_deltas = [Vector(*v) for v in product([-1, 1, 0], repeat=3) if v != Vector(0, 0, 0)]

        return [self + d for d in neighbour_deltas]


data = [l.strip() for l in open('day17.txt').readlines()]

# data = [l.strip() for l in """
# .#.
# ..#
# ###
# """.strip().split('\n')]


def print_grid(grid):
    min_x = min([v.x for v in grid.keys()])
    max_x = max([v.x for v in grid.keys()])
    min_y = min([v.y for v in grid.keys()])
    max_y = max([v.y for v in grid.keys()])
    min_z = min([v.z for v in grid.keys()])
    max_z = max([v.z for v in grid.keys()])
    # print((min_x, max_x), (min_y, max_y))

    for z in range(min_z, max_z + 1):
        print(f"z={z}")
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print(grid.get(Vector(x, y, z), '.'), end="")
            print()
        print()

    print('---------------')


def step(grid):
    new_grid = {}

    processed = set()
    neighbours = set()

    for v, c in grid.items():
        processed.add(v)
        neighbours.update(v.neighbours())
        active_neighbour_count = [grid.get(dv, '.') for dv in v.neighbours()].count('#')
        if c == '#' and active_neighbour_count in [2, 3]:
            new_grid[v] = '#'
        elif c == '.' and active_neighbour_count == 3:
            new_grid[v] = '#'

    for v in neighbours.difference(processed):
        active_neighbour_count = [grid.get(dv, '.') for dv in v.neighbours()].count('#')
        if active_neighbour_count == 3:
            new_grid[v] = '#'

    return new_grid


initial_grid = {}
for y, row in enumerate(data):
    for x, cell in enumerate(row):
        initial_grid[Vector(x, y, 0)] = cell

grid = initial_grid

for s in range(6):
    grid = step(grid)

print("part1:", len([x for x in grid.values() if x == '#']))
