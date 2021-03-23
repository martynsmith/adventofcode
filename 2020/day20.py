#!/usr/bin/env python

from rich import print
from collections import defaultdict
import re

raw_tiles = open('day20.txt').read().strip().split('\n\n')

tiles = {}
edges = {}

for raw_tile in raw_tiles:
    match = re.search(r'^Tile (\d+):', raw_tile)
    tile_id = int(match.group(1))
    tile = tiles[tile_id] = {}
    for y, row in enumerate(raw_tile.split('\n')[1:]):
        for x, cell in enumerate(row):
            tile[(x, y)] = cell

    for edge in [
        "".join(tile[(x, 0)] for x in range(10)),
        "".join(tile[(x, 9)] for x in range(10)),
        "".join(tile[(0, y)] for y in range(10)),
        "".join(tile[(9, y)] for y in range(10)),
    ]:
        edges.setdefault(edge, [])
        edges[edge].append(tile_id)
        reversed_edge = "".join(reversed(edge))
        edges.setdefault(reversed_edge, [])
        edges[reversed_edge].append(tile_id)

neighbour_count = defaultdict(int)

for edge, tile_ids in edges.items():
    assert len(tile_ids) in [1, 2], tile_ids
    if len(tile_ids) == 2:
        for tile_id in tile_ids:
            neighbour_count[tile_id] += 1

part1 = 1
for tile_id, count in neighbour_count.items():
    if count == 4:
        part1 *= tile_id

print("part1:", part1)
