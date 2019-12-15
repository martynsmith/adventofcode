import typing
import fileinput
from pprint import pprint
import networkx


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

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

VECTORS = {
    NORTH: Vector(0, -1),
    SOUTH: Vector(0, 1),
    WEST: Vector(-1, 0),
    EAST: Vector(1, 0),
}
for k, v in list(VECTORS.items()):
    VECTORS[v] = k

WALL = 0
EMPTY = 1
OXYGEN = 2

chamber = {}
current_position = Vector(0, 0)
chamber[current_position] = 'X'
uncharted_points = {
    current_position: [NORTH, SOUTH, WEST, EAST]
}
inverse_direction = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST,
}


def render_chamber(chamber):
    min_x = min([x for x, _ in chamber.keys()])
    max_x = max([x for x, _ in chamber.keys()])
    min_y = min([y for _, y in chamber.keys()])
    max_y = max([y for _, y in chamber.keys()])

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(chamber.get(Vector(x, y), '?'), end="")
        print()
    print()


graph = networkx.Graph()

oxygen_position = None

if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    program = [int(x) for x in program_string.split(',')]

    executor = Executor(program, [])
    while uncharted_points:
        if current_position not in uncharted_points:
            length, target_position = sorted([
                (networkx.shortest_path_length(graph, current_position, p), p)
                for p in uncharted_points.keys()
            ])[0]
            # print(f"moving from {current_position} => {target_position}")
            for target_position in networkx.shortest_path(graph, current_position, target_position)[1:]:
                executor.input.append(VECTORS[target_position - current_position])
                executor.run()
                executor.output.pop(0)
                current_position = target_position

        direction = uncharted_points[current_position].pop(0)
        executor.input.append(direction)
        if len(uncharted_points[current_position]) == 0:
            del uncharted_points[current_position]
        executor.run()
        response = executor.output.pop(0)

        if response == WALL:
            chamber[current_position + VECTORS[direction]] = '#'
        elif response == EMPTY:
            graph.add_edge(current_position, current_position + VECTORS[direction])
            current_position += VECTORS[direction]
            chamber[current_position] = ' '
            uncharted_points[current_position] = [NORTH, SOUTH, WEST, EAST]
            uncharted_points[current_position].remove(inverse_direction[direction])
        elif response == OXYGEN:
            graph.add_edge(current_position, current_position + VECTORS[direction])
            current_position += VECTORS[direction]
            chamber[current_position] = 'O'
            oxygen_position = current_position
            uncharted_points[current_position] = [NORTH, SOUTH, WEST, EAST]
            uncharted_points[current_position].remove(inverse_direction[direction])
        else:
            raise NotImplementedError("nope")

    render_chamber(chamber)

    print(networkx.shortest_path_length(graph, Vector(0, 0), oxygen_position))

    oxygenated_positions = {oxygen_position}
    unoxygenated_positions = set([p for p, c in chamber.items() if c == ' '])

    minutes = 0
    while unoxygenated_positions:
        minutes += 1
        for p in list(oxygenated_positions):
            for t in networkx.all_neighbors(graph, p):
                if t in unoxygenated_positions:
                    chamber[t] = 'O'
                    oxygenated_positions.add(t)
                    unoxygenated_positions.remove(t)

        render_chamber(chamber)

    print(minutes)
