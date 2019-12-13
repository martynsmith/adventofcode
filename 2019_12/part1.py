import typing
from dataclasses import dataclass
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

    def add_x(self, delta):
        return Vector(self.x + delta, self.y, self.z)

    def add_y(self, delta):
        return Vector(self.x, self.y + delta, self.z)

    def add_z(self, delta):
        return Vector(self.x, self.y, self.z + delta)

@dataclass
class Moon:
    position: Vector
    velocity: Vector = Vector(0, 0, 0)

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
# moons = [
#     Moon(Vector(x=-1, y=0, z=2)),
#     Moon(Vector(x=2, y=-10, z=-7)),
#     Moon(Vector(x=4, y=-8, z=8)),
#     Moon(Vector(x=3, y=5, z=-1)),
# ]
# pprint(moons)

for _ in range(1000):
    # apply gravity
    for m1, m2 in combinations(moons, 2):  # type: Moon, Moon
        if m1.position.x < m2.position.x:
            m1.velocity = m1.velocity.add_x(1)
            m2.velocity = m2.velocity.add_x(-1)
        elif m1.position.x > m2.position.x:
            m1.velocity = m1.velocity.add_x(-1)
            m2.velocity = m2.velocity.add_x(1)
        if m1.position.y < m2.position.y:
            m1.velocity = m1.velocity.add_y(1)
            m2.velocity = m2.velocity.add_y(-1)
        elif m1.position.y > m2.position.y:
            m1.velocity = m1.velocity.add_y(-1)
            m2.velocity = m2.velocity.add_y(1)
        if m1.position.z < m2.position.z:
            m1.velocity = m1.velocity.add_z(1)
            m2.velocity = m2.velocity.add_z(-1)
        elif m1.position.z > m2.position.z:
            m1.velocity = m1.velocity.add_z(-1)
            m2.velocity = m2.velocity.add_z(1)

    # move moons
    for moon in moons:
        moon.position += moon.velocity

total_energy = 0
for moon in moons:
    total_energy += moon.get_kinetic_energy() * moon.get_potential_energy()

print(total_energy)

