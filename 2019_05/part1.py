import fileinput


def execute_program(program, input):
    pointer = 0

    def get_param(number, modes):
        if modes[-number] == '0':
            return program[program[pointer + number]]
        elif modes[-number] == '1':
            return program[pointer + number]
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

    def set_param(number, modes, value):
        if modes[-number] == '0':
            program[program[pointer + number]] = value
        else:
            raise NotImplementedError(f"Unknown mode: {modes[-number]}")

    while True:
        # print(program)
        operation = int(str(program[pointer])[-2:], 10)
        modes = f"{int(str(program[pointer])[:-2] or '0', 10):05d}"

        if operation == 1:
            set_param(3, modes, get_param(1, modes) + get_param(2, modes))
            pointer += 4
        elif operation == 2:
            set_param(3, modes, get_param(1, modes) * get_param(2, modes))
            pointer += 4
        elif operation == 3:
            value = input.pop(0)
            print(f"input: {value}")
            set_param(1, modes, value)
            pointer += 2
        elif operation == 4:
            print(f"output: {get_param(1, modes)}")
            pointer += 2
        elif operation == 5:
            if get_param(1, modes) != 0:
                pointer = get_param(2, modes)
            else:
                pointer += 3
        elif operation == 6:
            if get_param(1, modes) == 0:
                pointer = get_param(2, modes)
            else:
                pointer += 3
        elif operation == 7:
            if get_param(1, modes) < get_param(2, modes):
                set_param(3, modes, 1)
            else:
                set_param(3, modes, 0)
            pointer += 4
        elif operation == 8:
            if get_param(1, modes) == get_param(2, modes):
                set_param(3, modes, 1)
            else:
                set_param(3, modes, 0)
            pointer += 4
        elif operation == 99:
            # print(program)
            return
        else:
            raise NotImplementedError(f"Invalid operation {operation}")


if __name__ == '__main__':
    program_string = list(fileinput.input())[0].strip()
    program = [int(x) for x in program_string.split(',')]
    execute_program(program, [1])
    print('---')
    program = [int(x) for x in program_string.split(',')]
    execute_program(program, [5])

    # for program_string in [
    #     # "3,9,8,9,10,9,4,9,99,-1,8",
    #     # "3,9,7,9,10,9,4,9,99,-1,8",
    #     # "3,3,1108,-1,8,3,4,3,99",
    #     # "3,3,1107,-1,8,3,4,3,99",
    #     # "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",
    #     "3,3,1105,-1,9,1101,0,0,12,4,12,99,1",
    # ]:
    #     program = [int(x) for x in program_string.split(',')]
    #     execute_program(program, [0])
    #     program = [int(x) for x in program_string.split(',')]
    #     execute_program(program, [1])
    #     program = [int(x) for x in program_string.split(',')]
    #     execute_program(program, [2])
    #     print('=======')
    #
