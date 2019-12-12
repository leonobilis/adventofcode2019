import re
from collections import namedtuple
from math import gcd
from functools import reduce


#Point = namedtuple('Point', ['x', 'y', 'z'])
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
    for _ in range(1000):
        [apply_gravity(i, j) for j in moons for i in moons if i != j]
        [apply_velocity(moon) for moon in moons]
    return sum([potential_energy(m) * kinetic_energy(m) for m in moons])


def lcm(vals):
    return reduce(lambda a,b: a*b // gcd(a,b), vals)


def p2(moons):
    return 0
    i = 0
    cyclex = 0
    cycley = 0
    cyclez = 0
    #first_match = {}
    # [apply_gravity(i, j) for j in moons for i in moons if i != j]
    # [apply_velocity(moon) for moon in moons]
    #initial_pos = [m.pos.copy() for m in moons]
    # second_vel = [m.vel.copy() for m in moons]
    while not (cyclex and cycley and cyclez):
        #initial_pos = [m.pos.copy() for m in moons]
        [apply_gravity(i, j) for j in moons for i in moons if i != j]
        [apply_velocity(moon) for moon in moons]
        i += 1
        x, y, z = [[m.vel[i] for m in moons] for i in range(3)]
        cyclex = i if not any(x) else 0
        cycley = i if not any(y) else 0
        cyclez = i if not any(z) else 0
    return lcm([cyclex, cycley, cyclez])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp.copy())}")
        print(f"Part 2: {p2(inp.copy())}")
