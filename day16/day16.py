from functools import reduce
from itertools import cycle


def parse_input(input):
    return [int(i) for i in input]


def get_digit(number):
    return abs(number) % 10 if number//10 else number


def p1(input):
    patterns = [reduce(lambda a, b: a + b, [[d]*i for d in [0, 1, 0, -1]]) for i in range(1, len(input) + 1)]
    digits = input.copy()
    for phase in range(100):
        new_digits = []
        for i in range(len(digits)):
            pattern = cycle(patterns[i])
            next(pattern)
            new_digits.append(get_digit(reduce(lambda a, b: a + b, [d*next(pattern) for d in digits])))
        digits = new_digits
    return "".join([str(d) for d in digits[:8]])


def p2(input):
    offset = int("".join([str(d) for d in input[:7]]))
    digits = (input*10000)[offset:]
    for phase in range(100):
        _sum = reduce(lambda a, b: a + b, [d for d in digits])
        new_digits = [get_digit(_sum)]
        for i in digits[:-1]:
            _sum -= i
            new_digits.append(get_digit(_sum))
        digits = new_digits
    return "".join([str(d) for d in digits[:8]])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
