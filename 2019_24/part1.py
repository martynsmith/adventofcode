import fileinput
import re

initial_game = ""

for line in fileinput.input():
    initial_game += line.strip()

adjacent_for = {}

for index in range(25):
    x = index % 5
    y = index // 5
    a = []
    if x > 0:
        a.append(y * 5 + x - 1)
    if x < 4:
        a.append(y * 5 + x + 1)
    if y > 0:
        a.append((y - 1) * 5 + x)
    if y < 4:
        a.append((y + 1) * 5 + x)

    adjacent_for[index] = a


def step(game):
    new_game = ""
    for index, tile in enumerate(game):
        bugs = sum([1 for i in adjacent_for[index] if game[i] == '#'])
        if tile == '#' and bugs != 1:
            new_game += '.'
        elif tile == '.' and (bugs == 1 or bugs == 2):
            new_game += '#'
        else:
            new_game += tile

    return new_game


def print_game(game):
    print(re.sub(r'(.{5})', '\\1\n', game))


game = initial_game
seen = {game}

while True:
    game = step(game)
    if game in seen:
        print_game(game)
        break
    seen.add(game)

total = 0
for index, tile in enumerate(game):
    if tile == '#':
        total += pow(2, index)

print(total)
