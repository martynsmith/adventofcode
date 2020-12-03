import fileinput
from pprint import pprint
import itertools


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


# g = networkx.DiGraph()
# g.add_edge('a', 'b', command='north')
# g.add_edge('a', 'j', command='east')
# g.add_edge('a', 'p', command='south')
#
# pprint(networkx.shortest_path(g, 'a', 'b'))
# pprint(g.edges[('a', 'b')]['command'])
#
#
# raise SystemExit()

items = [
    'mug',
    'food ration',
    'mouse',
    'ornament',
    'candy cane',
    'coin',
    'mutex',
    'semiconductor',
]

commands = [
    'north', 'take mug', 'south',
    'north', 'north', 'take food ration', 'south', 'south',
    'south', 'east', 'take mouse', 'west', 'north',
    'east', 'take ornament', 'west',
    'east', 'east', 'take candy cane', 'west', 'west',
    'east', 'north', 'take coin', 'south', 'west',
    'east', 'north', 'east', 'take mutex', 'west', 'south', 'west',
    'north', 'east', 'north', 'east', 'take semiconductor', 'west', 'south', 'west', 'south',

    # move to staging area
    'south', 'east', 'south', 'west',
    'inv',
]
commands += [f'drop {i}' for i in items]
commands += ['inv']

if __name__ == '__main__':
    with open('input.txt') as fh:
        program_string = fh.readlines()[0]
    program = [int(x) for x in program_string.split(',')]

    e = Executor(program, [])

    e.run()
    print("".join(chr(n) for n in e.output))
    e.output = []

    # while True:
    #     command = input()
    #     e.input.extend(command)
    #     e.run()
    #     print("".join(chr(n) for n in e.output))
    #     e.output = []

    # exit()

    while commands:
        command = commands.pop(0)
        e.input.extend([ord(c) for c in command] + [10])
        print(command)
        e.run()
        print("".join(chr(n) for n in e.output))
        e.output = []

    print('---')
    for n in range(1, 9):
        for item_list in itertools.combinations(items, n):
            # grab items
            for item in item_list:
                e.input.extend([ord(c) for c in f'take {item}'] + [10])
                e.run()
                # print("".join(chr(n) for n in e.output))
                e.output = []

            e.input.extend([ord(c) for c in f'west'] + [10])
            e.run()
            out = "".join(chr(n) for n in e.output)
            if 'Alert' not in out:
                print('==============================')
                print(item_list)
                print(out)
                print('==============================')
                raise SystemExit()
            e.output = []

            # drop items
            for item in item_list:
                e.input.extend([ord(c) for c in f'drop {item}'] + [10])
                e.run()
                # print("".join(chr(n) for n in e.output))
                e.output = []
