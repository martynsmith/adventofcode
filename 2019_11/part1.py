import typing
import fileinput
import itertools
from collections import defaultdict


class Executor:
    program = None
    halted = False
    input = None
    output = None
    pointer = 0
    relative_base = 0

    def __init__(self, program, input=None):
        self.program = program.copy()
        if input:
            self.input = input
        else:
            self.input = []

        self.output = []

    def assert_min_program_length(self, index):
        while len(self.program) <= index:
            self.program.append(0)

    def get_param(self, number, modes):
        if modes[-number] == '0':  # position mode
            self.assert_min_program_length(self.pointer + number)
            index = self.program[self.pointer + number]
        elif modes[-number] == '1':  # immediate mode
            index = self.pointer + number
        elif modes[-number] == '2':  # relative mode
            self.assert_min_program_length(self.pointer + number)
            index = self.program[self.pointer + number] + self.relative_base
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

        self.assert_min_program_length(index)
        return self.program[index]

    def set_param(self, number, modes, value):
        self.pointer + number

        if modes[-number] == '0':  # position mode
            self.assert_min_program_length(self.pointer + number)
            index = self.program[self.pointer + number]
        elif modes[-number] == '2':  # relative mode
            self.assert_min_program_length(self.pointer + number)
            index = self.program[self.pointer + number] + self.relative_base
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

        self.assert_min_program_length(index)
        self.program[index] = value

    def run(self):
        while True:
            operation = int(str(self.program[self.pointer])[-2:], 10)
            modes = f"{int(str(self.program[self.pointer])[:-2] or '0', 10):05d}"

            if operation == 1:
                self.set_param(3, modes, self.get_param(1, modes) + self.get_param(2, modes))
                self.pointer += 4
            elif operation == 2:
                self.set_param(3, modes, self.get_param(1, modes) * self.get_param(2, modes))
                self.pointer += 4
            elif operation == 3:
                if not self.input:
                    return
                value = self.input.pop(0)
                self.set_param(1, modes, value)
                self.pointer += 2
            elif operation == 4:
                self.output.append(self.get_param(1, modes))
                self.pointer += 2
            elif operation == 5:
                if self.get_param(1, modes) != 0:
                    self.pointer = self.get_param(2, modes)
                else:
                    self.pointer += 3
            elif operation == 6:
                if self.get_param(1, modes) == 0:
                    self.pointer = self.get_param(2, modes)
                else:
                    self.pointer += 3
            elif operation == 7:
                if self.get_param(1, modes) < self.get_param(2, modes):
                    self.set_param(3, modes, 1)
                else:
                    self.set_param(3, modes, 0)
                self.pointer += 4
            elif operation == 8:
                if self.get_param(1, modes) == self.get_param(2, modes):
                    self.set_param(3, modes, 1)
                else:
                    self.set_param(3, modes, 0)
                self.pointer += 4
            elif operation == 9:
                self.relative_base += self.get_param(1, modes)
                self.pointer += 2
            elif operation == 99:
                self.halted = True
                return
            else:
                raise NotImplementedError(f"Invalid operation {operation}")


class Vector(typing.NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplementedError(type(other))
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError(type(other))
        return Vector(self.x * other, self.y * other)


if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    program = [int(x) for x in program_string.split(',')]

    ship = defaultdict(int)
    robot = Executor(program, [])
    position = Vector(0, 0)
    direction = Vector(0, -1)
    ship[position] = 1  # for part 2
    while not robot.halted:
        robot.input.append(ship[position])
        robot.run()
        ship[position] = robot.output.pop(0)
        turn = robot.output.pop(0)
        if turn == 0:
            if direction.x == 0:
                direction = Vector(direction.y, 0)
            else:
                direction = Vector(0, -direction.x)
        elif turn == 1:
            if direction.x == 0:
                direction = Vector(-direction.y, 0)
            else:
                direction = Vector(0, direction.x)
        else:
            raise NotImplementedError(f"Invalid turn: {turn}")
        position += direction

    # part 1
    print(len(ship))

    # part2
    min_x = min([v.x for v in ship.keys()])
    max_x = max([v.x for v in ship.keys()])
    min_y = min([v.y for v in ship.keys()])
    max_y = max([v.y for v in ship.keys()])

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if ship[Vector(x, y)]:
                print(u"\u2588\u2588", end="")
            else:
                print(u"  ", end="")

        print()
