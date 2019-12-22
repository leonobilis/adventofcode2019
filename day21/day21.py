from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    inp = [ord(i) for i in "NOT A T\nOR C T\nAND A T\nNOT T T\nAND D T\nNOT T T\nNOT T J\nWALK\n"]
    return Intcode(program).run(inp)[-1]


def p2(program):
    inp = [ord(i) for i in "NOT E T\nNOT T T\nOR H T\nAND D T\nNOT T J\nNOT J J\nNOT C T\nNOT T T\nAND B T\nNOT T T\nAND T J\nNOT A T\nOR T J\nRUN\n"]
    return Intcode(program).run(inp)[-1]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        input = parse_input(f.readline())
        print(f"Part 1: {p1(input)}")
        print(f"Part 2: {p2(input)}")
