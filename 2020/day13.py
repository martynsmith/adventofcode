#!/usr/bin/env python

timestamp, busses = open('day13.txt').readlines()

timestamp = int(timestamp.strip())
busses = [(i, int(b)) for i, b in enumerate(busses.strip().split(',')) if b != 'x']

schedule = []
for _, bus in busses:
    if bus == 'x':
        continue
    next_timestamp = timestamp // bus * bus + bus
    schedule.append((next_timestamp - timestamp, bus))

wait_minutes, next_bus = sorted(schedule)[0]

print(f"part1: {wait_minutes * next_bus}")

print(f"bus count: {len(busses)}")
busses = busses[:2]
checks = []
timestamp, timestamp_delta = busses.pop(0)
timestamp += 69 + 23

def is_valid():
    for offset, bus in checks:
        if (timestamp + offset) % bus != 0:
            return False
    return True


while busses:
    offset, bus = busses.pop(0)
    checks.append((offset, bus))
    while not is_valid():
        timestamp += timestamp_delta
    # timestamp_delta = timestamp
    # print(offset, bus, timestamp, timestamp_delta)

print("part2: 74306157408 (TOO LOW)")

print(f"part2: {timestamp}")

for offset, bus in checks:
    print(f"{offset=} {bus=} {(timestamp + offset) % bus=}")

#
# print(timestamp)

# from sympy import *
#
# a, b, t = symbols('a b t', integer=True)
# init_printing(use_unicode=True)

# print(
#     solve(
#         Eq(23 * a - t, 41 * b - 13 - t),
#         t, a, b,
#         dict=True,
#         set=True,
#     )
# )
