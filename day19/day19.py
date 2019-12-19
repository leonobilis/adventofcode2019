from itertools import product
from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    out = [Intcode(program).run(input=[x,y]) for y in range(50) for x in range(50)]
    return sum([o[0] for o in out])


def get_last_x(y, program):
    x =  y - ((y-4)//7 + (y+6)//7) - 1
    while get_intcode(x, y, program):
        x += 1
    return x - 1


def get_intcode(x, y, program):
    out = Intcode(program).run(input=[x,y])
    return out[0]


def check100(y, program):
    x = get_last_x(y, program)
    return get_intcode(x - 99, y + 99, program) and not get_intcode(x - 100, y + 99, program)


def p2(program):
    y = 1000
    while True:
        if check100(y, program):
            return 10000*(get_last_x(y, program) - 99) + y
        y+=1


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
