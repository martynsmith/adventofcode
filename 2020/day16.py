#!/usr/bin/env python

import re
from functools import reduce

data = open('day16.txt').read()

# data = """
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# """

fields = {}
your_ticket = None
nearby_tickets = []

# print(data)
# print('---')


def generate_check(min1, max1, min2, max2):
    return lambda x: min1 <= x <= max1 or min2 <= x <= max2


for row in data.split('\n'):
    if not row:
        continue

    match = re.search(r'^(.*?): (\d+)-(\d+) or (\d+)-(\d+)', row)
    if match:
        min1, max1, min2, max2 = [int(x) for x in match.groups()[1:]]
        fields[match.group(1)] = generate_check(min1, max1, min2, max2)

    if ':' in row:
        continue

    if not your_ticket:
        your_ticket = [int(x) for x in row.split(',')]
        continue

    nearby_tickets.append([int(x) for x in row.split(',')])

errors = []
valid_tickets = []
for ticket in nearby_tickets:
    valid_ticket = True
    for field in ticket:
        match = False
        for check in fields.values():
            if check(field):
                match = True
        if not match:
            errors.append(field)
            valid_ticket = False
    if valid_ticket:
        valid_tickets.append(ticket)

print("part1:", sum(errors))

field_names = [set(fields.keys()) for x in range(len(your_ticket))]

for ticket in valid_tickets:
    for index, value in enumerate(ticket):
        for field_name, field_check in fields.items():
            if not field_check(value):
                field_names[index].discard(field_name)

while len(set([len(x) for x in field_names])) > 1:
    for fn in field_names:
        if len(fn) == 1:
            field_name = list(fn)[0]
            for sfn in field_names:
                if fn is not sfn:
                    sfn.discard(field_name)

field_names = [list(fn)[0] for fn in field_names]
your_ticket = dict(zip(field_names, your_ticket))

part2 = reduce(lambda x, y: x * y, [v for k, v in your_ticket.items() if k.startswith('departure')])

print("part2:", part2)
