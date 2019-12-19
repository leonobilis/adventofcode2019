from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(input):
    return Intcode(input).run(input=[1])[0]


def p2(input):
    return Intcode(input).run(input=[2])[0]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
