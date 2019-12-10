from itertools import groupby, product
from math import atan2

def parse_input(input):
    return {(x, y) for y in range(len(input)) for x in range(len(input[y]) - 1) if input[y][x] == '#'}
    #return [[j=='#' for j in i.strip()] for i in input]


def p1(asteroids):
    a = [list(groupby(sorted([atan2(a2[1]-a1[1], a2[0]-a1[0]) for a2 in asteroids if a1 != a2]))) for a1 in asteroids]
    return max([len(x) for x in a])


def p2(input):
    return 0


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
