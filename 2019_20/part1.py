import typing
import fileinput
import networkx
import re
from pprint import pprint


class Vector(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(type(other))
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(type(other))
        return Vector(self.x - other.x, self.y - other.y)

    def above(self):
        return Vector(self.x, self.y - 1)

    def below(self):
        return Vector(self.x, self.y + 1)

    def left_of(self):
        return Vector(self.x - 1, self.y)

    def right_of(self):
        return Vector(self.x + 1, self.y)


points = {}

y = 0
for line in fileinput.input():
    x = 0
    for char in line.rstrip():
        points[Vector(x, y)] = char
        x += 1
    y += 1
    x = 0
    print(line.rstrip())

g = networkx.Graph()


def label_for(point: Vector):
    if re.match(r'\w', points.get(point.above(), '#')):
        return points[point.above().above()] + points[point.above()]
    if re.match(r'\w', points.get(point.below(), '#')):
        return points[point.below()] + points[point.below().below()]
    if re.match(r'\w', points.get(point.left_of(), '#')):
        return points[point.left_of().left_of()] + points[point.left_of()]
    if re.match(r'\w', points.get(point.right_of(), '#')):
        return points[point.right_of()] + points[point.right_of().right_of()]


portals = {}

for point, char in sorted(points.items()):  # type: Vector, str
    if char != '.':
        continue
    if points.get(point.left_of(), '#') == '.':
        g.add_edge(point, point.left_of())
    if points.get(point.above(), '#') == '.':
        g.add_edge(point, point.above())

    p_label = label_for(point)
    if p_label:
        portals.setdefault(p_label, [])
        portals[p_label].append(point)

for p in portals.values():
    if len(p) == 1:
        continue
    g.add_edge(*p)

print(networkx.shortest_path_length(
    g,
    portals['AA'][0],
    portals['ZZ'][0],
))
