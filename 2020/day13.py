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

timestamp, timestamp_delta = busses.pop(0)

while busses:
    offset, bus = busses.pop(0)

    while (timestamp + offset) % bus:
        timestamp += timestamp_delta

    ts1 = timestamp
    timestamp += timestamp_delta
    while (timestamp + offset) % bus:
        timestamp += timestamp_delta

    timestamp_delta = timestamp - ts1
    timestamp = ts1

print(f"part2: {timestamp}")
