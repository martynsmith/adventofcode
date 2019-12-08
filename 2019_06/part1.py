import fileinput
from collections import defaultdict

orbits = {}

# data = [
#     'COM)B',
#     'B)C',
#     'C)D',
#     'D)E',
#     'E)F',
#     'B)G',
#     'G)H',
#     'D)I',
#     'E)J',
#     'J)K',
#     'K)L',
# ]

for line in fileinput.input():
    hub, sat = line.strip().split(')')
    orbits[sat] = hub

direct = 0
indirect = 0


def count_orbits(sat):
    if sat not in orbits:
        return 0
    return 1 + count_orbits(orbits[sat])


for sat, orbiting in list(orbits.items()):
    direct += 1
    indirect += count_orbits(orbiting)

from pprint import pprint
pprint(orbits)

print('---')
print(direct)
print(indirect)
print(direct + indirect)
