import typing
import fileinput
import networkx


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


G = networkx.Graph()
y = 0
for line in fileinput.input():
    x = 0
    for c in line.strip():
        position = Vector(x, y)
        G.add_node(position, type=c)
        x += 1
    y += 1

a = list(G.nodes(data=True))[0]

print([p for p, d in G.nodes(data=True) if d['type'] == '@'])
