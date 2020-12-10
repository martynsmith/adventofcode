#!/usr/bin/env python

import re

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

data = open('day05.txt').readlines()

seat_ids = []

for line in data:
    line = line.strip()
    row = int(line[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(line[7:].replace('L', '0').replace('R', '1'), 2)
    seat_id = row * 8 + col
    seat_ids.append(seat_id)

print(f"part1: {max(seat_ids)}")

seat_ids = sorted(seat_ids)

last_id = None
for si in seat_ids:
    if last_id and last_id != si - 1:
        print(f"part2: {si-1}")
    last_id = si
