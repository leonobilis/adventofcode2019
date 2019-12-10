from itertools import groupby, cycle, islice
from math import atan2, pi


def parse_input(input):
    return [(x, y) for y in range(len(input)) for x in range(len(input[y]) - 1) if input[y][x] == '#']


def best_asteroid(asteroids):
    a = [(a1, len(list(groupby(sorted([atan2(a2[1]-a1[1], a2[0]-a1[0]) for a2 in asteroids if a1 != a2]))))) for a1 in asteroids]
    return max(a, key=lambda x: x[1])


def p1(asteroids):
    return best_asteroid(asteroids)[1]


def phase90(fun):
    def phase90wrapper(y, x):
        return fun(y, x) + 3*pi/2 if x < 0 and y < 0 else fun(y, x) - pi/2
    return phase90wrapper


@phase90
def angle(y, x):
    return atan2(y, x)


def norm(a1, a2):
    return a2[1]-a1[1], a2[0]-a1[0]


def gen_asteroids(asteroids_groups):
    for group in cycle(asteroids_groups):
        if group: yield group.pop()[0]


def p2(asteroids):
    monitor = best_asteroid(asteroids)[0]
    dist = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
    others = [sorted(v, key=lambda x: dist(monitor, x[0]), reverse=True) for _, v in groupby(sorted([(a, angle(*norm(monitor, a))) for a in asteroids if monitor != a], key=lambda x: x[1]), key=lambda x: x[1])]
    a200 = list(islice(gen_asteroids(others), 200)).pop()
    return 100*a200[0] + a200[1]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
