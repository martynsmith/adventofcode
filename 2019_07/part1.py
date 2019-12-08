import fileinput
import itertools


class Executor:
    program = None
    halted = False
    input = None
    output = None
    pointer = 0

    def __init__(self, program, input=None):
        self.program = program.copy()
        if input:
            self.input = input
        else:
            self.input = []

        self.output = []

    def get_param(self, number, modes):
        if modes[-number] == '0':
            return self.program[self.program[self.pointer + number]]
        elif modes[-number] == '1':
            return self.program[self.pointer + number]
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

    def set_param(self, number, modes, value):
        if modes[-number] == '0':
            self.program[self.program[self.pointer + number]] = value
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

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
            elif operation == 99:
                self.halted = True
                return
            else:
                raise NotImplementedError(f"Invalid operation {operation}")


if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    # program_string = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    program = [int(x) for x in program_string.split(',')]

    max = 0
    max5 = 0
    max_phases = ()

    for phases in itertools.permutations(range(5, 10)):
        out = 0
        out5 = 0
        executors = [Executor(program, [phase]) for phase in phases]
        while True:
            halted = False
            for executor in executors:
                executor.input.append(out)
                executor.run()
                out = executor.output.pop(0)
                if executor == executors[-1]:
                    out5 = out
                if executor.halted:
                    halted = True
            if halted:
                break

        if out > max:
            max = out
            max_phases = phases
            max5 = out5

print(max)
print(max5)
print(max_phases)

