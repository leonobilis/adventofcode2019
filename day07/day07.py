from itertools import permutations
from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    def to_thrusters(phases):
        signal = 0
        for phase in phases:
            signal = Intcode(program).run(input=[phase, signal]).pop()
        return signal
    return max([to_thrusters(phases) for phases in permutations(range(5), 5)])


def p2(program):
    def to_thrusters(phases):
        amplifiers = [Intcode(program) for _ in range(5)]
        [amplifiers[i].run(input=[phase]) for i, phase in enumerate(phases)]
        signal = 0
        while amplifiers[-1].is_running():
            for amp in amplifiers:
                signal = amp.run(input=[signal]).pop()
        return signal
    return max([to_thrusters(phases) for phases in permutations(range(5, 10), 5)])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        input = parse_input(f.readline())
        print(f"Part 1: {p1(input)}")
        print(f"Part 2: {p2(input)}")
