import typing
import fileinput
import re


class Vector(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(type(other))
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError(type(other))
        return Vector(self.x * other, self.y * other)


def process_line(line):
    instructions = re.split(r',', line)
    grid = {}
    base = Vector(0, 0)
    step = 0

    for instruction in instructions:
        direction = instruction[0]
        distance = int(instruction[1:])
        if direction == 'U':
            delta = Vector(0, -1)
        elif direction == 'D':
            delta = Vector(0, +1)
        elif direction == 'L':
            delta = Vector(-1, 0)
        elif direction == 'R':
            delta = Vector(+1, 0)
        else:
            raise NotImplementedError("nope")

        for i in range(1, distance + 1):
            step += 1
            grid[base + delta * i] = step

        base = base + delta * distance

    return grid


def process(line1, line2):
    grid1 = process_line(line1)
    grid2 = process_line(line2)
    intersections = []
    for point in grid1.keys():
        if point not in grid2.keys():
            continue
        intersections.append((grid1[point] + grid2[point], point))
    print(sorted(intersections)[0])

process(
    'R75,D30,R83,U83,L12,D49,R71,U7,L72',
    'U62,R66,U55,R34,D71,R55,D58,R83',
)
process(
    'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
    'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
)

line1, line2 = fileinput.input()
process(
    line1.strip(),
    line2.strip(),
)


