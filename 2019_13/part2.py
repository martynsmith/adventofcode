import typing
import fileinput
import itertools
from collections import defaultdict
from enum import Enum


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


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

char_for = {
    EMPTY: ' ',
    WALL: u'\u2588',
    BLOCK: u'\u25a1',
    PADDLE: 'X',
    BALL: u'\u2b24',
}


if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    program = [int(x) for x in program_string.split(',')]
    program[0] = 2

    score = 0
    frame_count = 0
    points = {}

    max_x = 34
    max_y = 22

    paddle_x = 0
    ball_x = 0

    def print_frame():
        print(f"Score: {score}      Frame: {frame_count}")
        for y in range(max_y, -1, -1):
            for x in range(0, max_x + 1):
                t = points.get((x, y), EMPTY)
                print(char_for[t], end='')
            print()
        print()


    executor = Executor(program, [])
    executor.run()

    while executor.output:
        while executor.output:
            x = executor.output.pop(0)
            y = executor.output.pop(0)
            t = executor.output.pop(0)
            if x == -1:
                score = t
                continue
            points[(x, y)] = t
            if t == PADDLE:
                paddle_x = x
            if t == BALL:
                ball_x = x

        print_frame()
        frame_count += 1

        if executor.halted:
            break

        if paddle_x < ball_x:
            executor.input.append(1)
        elif paddle_x > ball_x:
            executor.input.append(-1)
        else:
            executor.input.append(0)


        executor.run()
