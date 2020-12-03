import fileinput
import re
from pprint import pprint


class Board:
    tiles = None
    sub_board = None  # type: Board
    super_board = None  # type: Board
    new_tiles = None

    def __init__(self):
        self.tiles = {}
        for x in range(5):
            for y in range(5):
                if x == 2 and y == 2:
                    self.tiles[(x, y)] = '?'
                else:
                    self.tiles[(x, y)] = '.'

    def get_bug_count(self):
        return sum([1 for t in self.tiles.values() if t == '#'])

    def is_bug(self, x, y) -> int:
        if (x, y) in self.tiles and self.tiles[(x, y)] == '#':
            return 1
        return 0

    def bug_count_for_tile(self, x, y) -> int:
        bug_count = 0
        if self.sub_board:
            if x == 2 and y == 1:
                bug_count += sum([self.sub_board.is_bug(sx, 0) for sx in range(5)])
            if x == 1 and y == 2:
                bug_count += sum([self.sub_board.is_bug(0, sy) for sy in range(5)])
            if x == 3 and y == 2:
                bug_count += sum([self.sub_board.is_bug(4, sy) for sy in range(5)])
            if x == 2 and y == 3:
                bug_count += sum([self.sub_board.is_bug(sx, 4) for sx in range(5)])
        if self.super_board:
            if x == 0:
                bug_count += self.super_board.is_bug(1, 2)
            if x == 4:
                bug_count += self.super_board.is_bug(3, 2)
            if y == 0:
                bug_count += self.super_board.is_bug(2, 1)
            if y == 4:
                bug_count += self.super_board.is_bug(2, 3)

        bug_count += self.is_bug(x - 1, y)
        bug_count += self.is_bug(x + 1, y)
        bug_count += self.is_bug(x, y - 1)
        bug_count += self.is_bug(x, y + 1)
        return bug_count

    def calculate_step(self):
        self.new_tiles = {}
        for x in range(5):
            for y in range(5):
                existing_tile = self.tiles[(x, y)]
                if existing_tile == '?':
                    self.new_tiles[(x, y)] = existing_tile
                    continue
                bug_count = self.bug_count_for_tile(x, y)
                if existing_tile == '#' and bug_count != 1:
                    self.new_tiles[(x, y)] = '.'
                elif existing_tile == '.' and (bug_count == 1 or bug_count == 2):
                    self.new_tiles[(x, y)] = '#'
                else:
                    self.new_tiles[(x, y)] = existing_tile

    def take_step(self):
        self.tiles = self.new_tiles


game = ""

for line in fileinput.input():
    game += line.strip()

initial_board = Board()

for index in range(25):
    x = index % 5
    y = index // 5
    if x == 2 and y == 2:
        initial_board.tiles[(x, y)] = '?'
    else:
        initial_board.tiles[(x, y)] = game[index]

boards = [initial_board]

for i in range(100):
    boards.append(Board())
    boards[-2].sub_board = boards[-1]
    boards[-1].super_board = boards[-2]

boards.append(Board())
boards[0].super_board = boards[-1]
boards[-1].sub_board = boards[0]

for i in range(100):
    boards.append(Board())
    boards[-2].super_board = boards[-1]
    boards[-1].sub_board = boards[-2]

pprint(f"initial bug count: {sum([b.get_bug_count() for b in boards])}")
for _ in range(200):
    for board in boards:
        board.calculate_step()
    for board in boards:
        board.take_step()
pprint(f"final bug count: {','.join([str(b.get_bug_count()) for b in boards])}")
pprint(f"final bug count: {sum([b.get_bug_count() for b in boards])}")
