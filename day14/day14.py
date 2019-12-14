import re
from collections import namedtuple, defaultdict
from math import ceil


Chemical = namedtuple("Chemical", ["name", "number"])


def parse_input(inp):
    regexp = re.compile(r"(?:(\d+ [\w, ]+)+) => (\d+ [\w]+)")
    
    def get_chemical(exp):
        exp = exp.split(' ')
        return Chemical(name=exp[1], number=int(exp[0]))

    return {j[1].split(' ')[1]: (int(j[1].split(' ')[0]), [get_chemical(c) for c in j[0].split(', ')]) for j in [regexp.search(i).groups() for i in inp]}


def num_ore(chemical, number, reactions, reserve):
    rnum = reserve.get(chemical, 0)
    if rnum >= number:
        reserve[chemical] -= number
        return 0
    elif rnum:
        reserve[chemical] = 0
        number -= rnum
    if chemical == "ORE":
        return number
    num_possible, reaction = reactions[chemical]
    num_prod = ceil(number/num_possible)
    if num_prod*num_possible > number:
        reserve[chemical] = num_prod*num_possible - number
    return sum(num_ore(i.name, num_prod*i.number, reactions, reserve) for i in reaction)


def p1(reactions):
    return num_ore("FUEL", 1, reactions, defaultdict(int))


def p2(reactions):
    reserve = defaultdict(int)
    opf = num_ore("FUEL", 1, reactions, defaultdict(int))
    ore_cargo = 1000000000000
    total_fuel = 0
    fuel = ore_cargo//opf
    while fuel:
        total_fuel += fuel
        ore_cargo -= num_ore("FUEL", fuel, reactions, reserve)
        fuel = ore_cargo//opf
    return total_fuel


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
