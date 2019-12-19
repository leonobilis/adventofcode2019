from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    output = Intcode(program).run(input=[])
    return len([o for o in output[2::3] if o == 2])


def p2(program):
    program[0] = 2
    computer = Intcode(program)
    output = computer.run(input=[])
    ball = output[[i for i, o in enumerate(output[2::3]) if o == 4][0]*3]
    paddle = output[[i for i, o in enumerate(output[2::3]) if o == 3][0]*3]
    while computer.is_running():
        move = -1 if ball < paddle else (1 if ball > paddle else 0)
        output = computer.run(input=[move])
        ball = output[-3]
        paddle += move
    return output[-1]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
