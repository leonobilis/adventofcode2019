import re
from collections import namedtuple
from math import gcd
from functools import reduce


Moon = namedtuple('Moon', ['pos', 'vel'])


def parse_input(input):
    def get_xyz(line):
        s = re.search(r"<x=([-\d]+), y=([-\d]+), z=([-\d]+)>", line)
        return [int(s.group(1)), int(s.group(2)), int(s.group(3))]
    return [Moon(pos=get_xyz(i), vel=[0, 0, 0]) for i in input]


def apply_gravity(moon, other):
    moon.vel[0] = moon.vel[0] - 1 if moon.pos[0] > other.pos[0] else moon.vel[0] + int(moon.pos[0] < other.pos[0])
    moon.vel[1] = moon.vel[1] - 1 if moon.pos[1] > other.pos[1] else moon.vel[1] + int(moon.pos[1] < other.pos[1])
    moon.vel[2] = moon.vel[2] - 1 if moon.pos[2] > other.pos[2] else moon.vel[2] + int(moon.pos[2] < other.pos[2])


def apply_velocity(moon):
    moon.pos[0] += moon.vel[0]
    moon.pos[1] += moon.vel[1]
    moon.pos[2] += moon.vel[2]


def potential_energy(moon):
    return abs(moon.pos[0]) + abs(moon.pos[1]) + abs(moon.pos[2])


def kinetic_energy(moon):
    return abs(moon.vel[0]) + abs(moon.vel[1]) + abs(moon.vel[2])


def p1(moons):
    moons = [Moon(pos=m.pos.copy(), vel=m.vel.copy()) for m in moons]
    for _ in range(1000):
        [apply_gravity(i, j) for j in moons for i in moons if i != j]
        [apply_velocity(moon) for moon in moons]
    return sum([potential_energy(m) * kinetic_energy(m) for m in moons])


def lcm(vals):
    return reduce(lambda a,b: a*b // gcd(a,b), vals)


def p2(moons):
    i = 0
    cycle = {}
    initial = [[m.pos[j] for m in moons] for j in range(3)]
    while len(cycle) != 3:
        [apply_gravity(i, j) for j in moons for i in moons if i != j]
        [apply_velocity(moon) for moon in moons]
        i += 1
        for j in range(3):
            if j not in cycle and not any([m.vel[j] for m in moons]) and [m.pos[j] for m in moons] == initial[j]:
                cycle[j] = i
    result = lcm(cycle.values())
    return result


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
