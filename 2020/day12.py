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

    def turn_right(self):
        return Vector(-self.y, self.x)

    def turn_left(self):
        return Vector(self.y, -self.x)

    def move(self, action, value):
        assert action in ('N', 'S', 'E', 'W')
        if action == 'N':
            return self + Vector(0, -value)
        if action == 'S':
            return self + Vector(0, value)
        if action == 'E':
            return self + Vector(value, 0)
        if action == 'W':
            return self + Vector(-value, 0)

    def rotate(self, action, value):
        assert action in ('L', 'R')
        direction = self
        for c in range(value // 90):
            if action == 'L':
                direction = direction.turn_left()
            if action == 'R':
                direction = direction.turn_right()
        return direction


actions = [(x[0], int(x[1:].strip())) for x in open('day12.txt').readlines()]

# part 1

direction = Vector(1, 0)
position = Vector(0, 0)

for action, value in actions:
    if action in ('N', 'S', 'E', 'W'):
        position = position.move(action, value)
    if action in ('L', 'R'):
        direction = direction.rotate(action, value)
    if action == 'F':
        position += direction * value

print(f"part1: {abs(position.x) + abs(position.y)}")

# part 2

direction = Vector(10, -1)
position = Vector(0, 0)

for action, value in actions:
    if action in ('N', 'S', 'E', 'W'):
        direction = direction.move(action, value)
    if action in ('L', 'R'):
        direction = direction.rotate(action, value)
    if action == 'F':
        position += direction * value

print(f"part2: {abs(position.x) + abs(position.y)}")
