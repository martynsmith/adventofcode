import typing
import fileinput
import networkx
import re
from pprint import pprint


class Vector(typing.NamedTuple):
    x: int
    y: int
    z: int

    def above(self):
        return Vector(self.x, self.y - 1, self.z)

    def below(self):
        return Vector(self.x, self.y + 1, self.z)

    def left_of(self):
        return Vector(self.x - 1, self.y, self.z)

    def right_of(self):
        return Vector(self.x + 1, self.y, self.z)

    def at_depth(self, depth):
        return Vector(self.x, self.y, depth)


points = {}

y = 0
for line in fileinput.input():
    x = 0
    for char in line.rstrip():
        points[Vector(x, y, 1)] = char
        x += 1
    y += 1
    x = 0
    print(line.rstrip())

max_x = max([p.x for p in points.keys()]) - 2
max_y = max([p.y for p in points.keys()]) - 2


def label_for(point: Vector):
    if re.match(r'\w', points.get(point.above(), '#')):
        return points[point.above().above()] + points[point.above()]
    if re.match(r'\w', points.get(point.below(), '#')):
        return points[point.below()] + points[point.below().below()]
    if re.match(r'\w', points.get(point.left_of(), '#')):
        return points[point.left_of().left_of()] + points[point.left_of()]
    if re.match(r'\w', points.get(point.right_of(), '#')):
        return points[point.right_of()] + points[point.right_of().right_of()]


g = networkx.Graph()
portals = {}

for point, char in sorted(points.items()):  # type: Vector, str
    if char != '.':
        continue
    for d in range(50):
        pd = point.at_depth(d)
        if points.get(point.left_of(), '#') == '.':
            g.add_edge(pd, pd.left_of())
        if points.get(point.above(), '#') == '.':
            g.add_edge(pd, pd.above())

    p_label = label_for(point)
    if p_label:
        portals.setdefault(p_label, [])
        portals[p_label].append(point)

for label, p in portals.items():
    if len(p) == 1:
        continue
    if len(p) != 2:
        raise Exception("nope")
    p_outside, p_inside = p  # type: Vector, Vector
    if p_inside.x in [2, max_x] or p_inside.y in [2, max_y]:
        p_outside, p_inside = p_inside, p_outside

    for d in range(50):
        g.add_edge(
            p_outside.at_depth(d + 1),
            p_inside.at_depth(d),
        )

print(networkx.shortest_path_length(
    g,
    portals['AA'][0],
    portals['ZZ'][0],
))
