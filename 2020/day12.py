#!/usr/bin/env python

from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __repr__(self):
        if self.x < 0:
            x = f"west {-self.x}"
        else:
            x = f"east {self.x}"
        if self.y <= 0:
            y = f"north {-self.y}"
        else:
            y = f"south {self.y}"
        return f"Vector({x}, {y})"


data = [x.strip() for x in open('day12.txt').readlines()]

direction = Vector(1, 0)
position = Vector(0, 0)


def turn_right(direction):
    return Vector(-direction.y, direction.x)


def turn_left(direction):
    return Vector(direction.y, -direction.x)


for line in data:
    action = line[0]
    value = int(line[1:].strip())

    if action == 'N':
        position += Vector(0, -value)
    elif action == 'S':
        position += Vector(0, value)
    elif action == 'E':
        position += Vector(value, 0)
    elif action == 'W':
        position += Vector(-value, 0)
    elif action == 'L':
        for c in range(value // 90):
            direction = turn_left(direction)
    elif action == 'R':
        for c in range(value // 90):
            direction = turn_right(direction)
    elif action == 'F':
        position += direction * value
    else:
        raise ValueError(f"can't handle action {action}")

print(f"part1: {abs(position.x) + abs(position.y)}")

# Part 2
waypoint_offset = Vector(10, -1)
position = Vector(0, 0)

for line in data:
    action = line[0]
    value = int(line[1:].strip())

    if action == 'N':
        waypoint_offset += Vector(0, -value)
    elif action == 'S':
        waypoint_offset += Vector(0, value)
    elif action == 'E':
        waypoint_offset += Vector(value, 0)
    elif action == 'W':
        waypoint_offset += Vector(-value, 0)
    elif action == 'L':
        for c in range(value // 90):
            waypoint_offset = turn_left(waypoint_offset)
    elif action == 'R':
        for c in range(value // 90):
            waypoint_offset = turn_right(waypoint_offset)
    elif action == 'F':
        position += waypoint_offset * value
    else:
        raise ValueError(f"can't handle action {action}")

print(f"part2: {abs(position.x) + abs(position.y)}")
