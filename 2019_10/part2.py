import fileinput
import math
from pprint import pprint

grid = {}

station = (17, 23)
sx = station[0]
sy = station[1]

y = 0
for line in fileinput.input():
    x = 0
    for char in line.strip():
        if char == '#':
            grid[(x, y)] = 1
        x += 1
    y += 1


asteroids = {}

for vx, vy in grid:
    if vx == sx and vy == sy:
        continue
    ax = abs(vx - sx)
    ay = abs(vy - sy)
    angle = math.atan2(vx - sx, vy - sy)
    d = math.sqrt(ax**2 + ay**2)
    if angle not in asteroids:
        asteroids[angle] = []

    asteroids[angle].append((d, vx, vy))

count = 0
while len(asteroids):
    for angle in reversed(sorted(asteroids.keys())):
        if not asteroids[angle]:
            continue
        _, x, y = asteroids[angle].pop(0)
        count += 1
        print((count, x, y))
        if not asteroids[angle]:
            del asteroids[angle]
