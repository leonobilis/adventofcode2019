def parse_input(input):
    return [int(i) for i in input.split(',')]


def run(program):
    opcode = {
        1: lambda a, b: a + b,
        2: lambda a, b: a * b
    }
    pos = 0
    while program[pos] != 99:
        program[program[pos + 3]] = opcode[program[pos]](program[program[pos + 1]], program[program[pos + 2]])
        pos += 4


def p1(input):
    program = input.copy()
    program[1] = 12
    program[2] = 2
    run(program)
    return program[0]


def p2(input):
    i = 0
    program = [0]
    while program[0] != 19690720:
        noun = int (i / 100)
        verb = i % 100
        program = input.copy()
        program[1] = noun
        program[2] = verb
        run(program)
        i += 1
    return 100 * noun + verb


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print("Part 1: {}".format(p1(inp)))
        print("Part 2: {}".format(p2(inp)))
