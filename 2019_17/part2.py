import typing
import fileinput
import re


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

    def turn_right(self):
        return Vector(self.y, -self.x)

    def turn_left(self):
        return Vector(-self.y, self.x)


if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    program = [int(x) for x in program_string.split(',')]
    program[0] = 2

    executor = Executor(program, [])
    executor.run()

    print("".join([chr(x) for x in executor.output]))

    scaffold = {}
    x = 0
    y = 39
    initial_position = None
    for c in executor.output:
        # 35 = scaffold
        # 46 = space
        # 10 = newline
        if c == 10:
            y -= 1
            x = 0
            continue
        if chr(c) in ['<', '>', '^', 'V']:
            if initial_position:
                raise Exception("nope")
            initial_position = Vector(x, y)
        scaffold[Vector(x, y)] = c
        x += 1

    position = initial_position
    direction = Vector(0, 1)
    commands = []

    while scaffold.get(position + direction.turn_left(), 46) == 35 or scaffold.get(position + direction.turn_right(),
                                                                                   46) == 35:
        if scaffold.get(position + direction.turn_left(), 46) == 35:
            direction = direction.turn_left()
            commands.append('L')
        else:
            direction = direction.turn_right()
            commands.append('R')

        while scaffold.get(position + direction, 46) == 35:
            position += direction
            if not isinstance(commands[-1], int):
                commands.append(0)
            commands[-1] += 1

    command_string = ",".join([str(c) for c in commands])

    def find_substrings(L):
        best_quality = 0
        result = ''
        for i in range(1, len(L) + 1):
            matches = re.findall(L[0:i], L)
            if len(matches[0]) > 20:
                continue
            quality = len(matches) * len(matches[0])
            if quality > best_quality:
                result = matches[0]
                best_quality = quality
        return result

    part1 = 'R,8,L,10,R,8'
    part2 = 'R,12,R,8,L,8,L,12'
    part3 = 'L,12,L,10,L,8'
    groups = 'A,B,A,C,A,B,C,C,A,B'

    print(f"cmd  : {command_string}")
    # part1 = find_substrings(command_string)
    # print(f"part1: {part1}")
    command_string = re.sub(part1, "." * len(part1), command_string)
    print(f"cmd  : {command_string}")
    # part2 = find_substrings(command_string.strip())
    # print(f"part2: {part2}")
    command_string = re.sub(part2, "." * len(part2), command_string)
    print(f"cmd  : {command_string}")
    # part3 = find_substrings(command_string.strip())
    # print(f"part3: {part3}")
    command_string = re.sub(part3, "." * len(part3), command_string)
    print(f"cmd  : {command_string}")

    executor.output = []
    executor.input.extend([ord(c) for c in groups] + [10])
    executor.input.extend([ord(c) for c in part1] + [10])
    executor.input.extend([ord(c) for c in part2] + [10])
    executor.input.extend([ord(c) for c in part3] + [10])
    executor.input.extend([ord(c) for c in "n"] + [10])
    executor.run()

    print("".join([chr(x) for x in executor.output]))
