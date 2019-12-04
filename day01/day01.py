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
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
