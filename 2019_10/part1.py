import fileinput
import math
from pprint import pprint

grid = {}

y = 0
for line in fileinput.input():
    x = 0
    for char in line.strip():
        if char == '#':
            grid[(x, y)] = 1
        x += 1
    y += 1

max = 0
location = None

for x, y in grid:
    asteroids = {}

    for vx, vy in grid:
        if vx == x and vy == y:
            continue
        ax = abs(vx - x)
        ay = abs(vy - y)
        angle = math.atan2(vx - x, vy - y)
        d = math.sqrt(ax**2 + ay**2)
        if angle in asteroids:
            continue
        asteroids[angle] = ((vx, vy), (x, y), angle)

    if len(asteroids) > max:
        max = len(asteroids)
        location = (x, y)

print(max)
print(location)
# 295 is too low
