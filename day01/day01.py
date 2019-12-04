def fuel(mass):
    return mass//3 - 2


def total_fuel(mass):
    result = 0
    r = fuel(mass)
    while r > 0:
        result += r
        r = fuel(r)
    return result


def p1(input):
    return sum([fuel(int(i)) for i in input])


def p2(input):
    return sum([total_fuel(int(i)) for i in input])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = f.readlines()
        print("Part 1: {}".format(p1(inp)))
        print("Part 2: {}".format(p2(inp)))
