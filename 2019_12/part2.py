import typing
from itertools import combinations
from pprint import pprint


class Vector(typing.NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(type(other))
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)


class Moon:
    position: Vector
    velocity: Vector = Vector(0, 0, 0)

    def __init__(self, position):
        self.position = position

    def get_kinetic_energy(self):
        return abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)

    def get_potential_energy(self):
        return abs(self.position.x) + abs(self.position.y) + abs(self.position.z)


moons = [
    Moon(Vector(x=4, y=1, z=1)),
    Moon(Vector(x=11, y=-18, z=-1)),
    Moon(Vector(x=-2, y=-10, z=-4)),
    Moon(Vector(x=-7, y=-2, z=14)),
]
moons = [
    Moon(Vector(x=0, y=0, z=1)),
    Moon(Vector(x=0, y=0, z=-1)),
    Moon(Vector(x=0, y=0, z=-4)),
    Moon(Vector(x=0, y=0, z=14)),
]

# moons = [
#     Moon(Vector(x=-1, y=0, z=2)),
#     Moon(Vector(x=2, y=-10, z=-7)),
#     Moon(Vector(x=4, y=-8, z=8)),
#     Moon(Vector(x=3, y=5, z=-1)),
# ]

seen_positions = set()


def moon_hash():
    return tuple([(m.position, m.velocity) for m in moons]).__hash__()


seen_positions.add(moon_hash())

from time import time

rx = 268296
ry = 84032
rz = 231614

x = rx
y = ry
z = rz

while True:
    if x == y and y == z:
        print(x)
        break

    # print((x, y, z))

    if x == min(x, y, z):
        x += rx
    elif y == min(x, y, z):
        y += ry
    elif z == min(x, y, z):
        z += rz


raise SystemExit()


i = 0
t = time()
while True:
    i += 1
    if i % 100000 == 0:
        new_t = time()
        print(f"{100000 / (new_t - t):0.0f} steps per second")
        t = new_t
    # apply gravity
    for m1, m2 in combinations(moons, 2):  # type: Moon, Moon
        m1dx = 0
        m1dy = 0
        m1dz = 0
        m2dx = 0
        m2dy = 0
        m2dz = 0

        if m1.position.x < m2.position.x:
            m1dx = 1
            m2dx = -1
        elif m1.position.x > m2.position.x:
            m1dx = -1
            m2dx = 1
        if m1.position.y < m2.position.y:
            m1dy = 1
            m2dy = -1
        elif m1.position.y > m2.position.y:
            m1dy = -1
            m2dy = 1
        if m1.position.z < m2.position.z:
            m1dz = 1
            m2dz = -1
        elif m1.position.z > m2.position.z:
            m1dz = -1
            m2dz = 1

        m1.velocity = Vector(
            m1.velocity.x + m1dx,
            m1.velocity.y + m1dy,
            m1.velocity.z + m1dz,
        )
        m2.velocity = Vector(
            m2.velocity.x + m2dx,
            m2.velocity.y + m2dy,
            m2.velocity.z + m2dz,
        )

    # move moons
    for moon in moons:
        moon.position += moon.velocity

    if moon_hash() in seen_positions:
        break

    seen_positions.add(moon_hash())

print(i)

