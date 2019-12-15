from enum import IntEnum
from random import randint
import networkx as nx


def run(prog, input, pos=0, rb_val=0):
    output = []
    rb = [rb_val]

    def get_modes(opcode):
        return (opcode%1000//100, opcode%10000//1000, opcode%100000//10000)

    modes_values = {
        0: lambda x: prog[x],
        1: lambda x: x,
        2: lambda x: prog[x + rb[0]],
    }

    def value(a, mode):
        return modes_values[mode](a)

    def add(a, b, c, modes, pos):
        mod_a, mod_b, mod_c = modes
        if mod_c == 2:
            prog[c + rb[0]] = value(a, mod_a) + value(b, mod_b)
        else:
            prog[c] = value(a, mod_a) + value(b, mod_b)
        return pos + 4

    def mul(a, b, c, modes, pos):
        mod_a, mod_b, mod_c = modes
        if mod_c == 2:
            prog[c + rb[0]] = value(a, mod_a) * value(b, mod_b)
        else:
            prog[c] = value(a, mod_a) * value(b, mod_b)
        return pos + 4

    def inp(a, modes, pos):
        if modes[0] == 2:
            prog[a + rb[0]] = input.pop()
        else:
            prog[a] = input.pop()
        return pos + 2

    def out(a, modes, pos):
        output.append(value(a, modes[0]))
        return pos + 2

    def jump_true(a, b, modes, pos):
        mod_a, mod_b, _ = modes
        return value(b, mod_b) if value(a, mod_a) else pos + 3

    def jump_false(a, b, modes, pos):
        mod_a, mod_b, _ = modes
        return value(b, mod_b) if not value(a, mod_a) else pos + 3

    def less_than(a, b, c, modes, pos):
        mod_a, mod_b, mod_c = modes
        if mod_c == 2:
            prog[c + rb[0]] = 1 if value(a, mod_a) < value(b, mod_b) else 0
        else:
            prog[c] = 1 if value(a, mod_a) < value(b, mod_b) else 0
        return pos + 4

    def equals(a, b, c, modes, pos):
        mod_a, mod_b, mod_c = modes
        if mod_c == 2:
            prog[c + rb[0]] = 1 if value(a, mod_a) == value(b, mod_b) else 0
        else:
            prog[c] = 1 if value(a, mod_a) == value(b, mod_b) else 0
        return pos + 4

    def adjust_rb(a, modes, pos):
        rb[0] += value(a, modes[0])
        return pos + 2

    instructions = {
        1: add,
        2: mul,
        3: lambda a, _b, _c, modes, pos: inp(a, modes, pos),
        4: lambda a, _b, _c, modes, pos: out(a, modes, pos),
        5: lambda a, b, _c, modes, pos: jump_true(a, b, modes, pos),
        6: lambda a, b, _c, modes, pos: jump_false(a, b, modes, pos),
        7: less_than,
        8: equals,
        9: lambda a, _b, _c, modes, pos: adjust_rb(a, modes, pos)
    }

    opcode = lambda o: o%100
    while opcode(prog[pos])!= 99 and not (opcode(prog[pos]) == 3 and not input):
        pos = instructions[opcode(prog[pos])](prog[pos + 1], prog[pos + 2], prog[pos + 3], get_modes(prog[pos]), pos)
    return output, pos, rb[0]


class Dir(IntEnum):
    north = 1
    south = 2
    west = 3
    east = 4


go = {
    Dir.north: lambda x, y: (x, y+1),
    Dir.south: lambda x, y: (x, y-1),
    Dir.west: lambda x, y: (x-1, y),
    Dir.east: lambda x, y: (x+1, y)
}


def decision(pos, area, walls):
    for i in [Dir.south, Dir.east, Dir.north, Dir.west]:
        if not go[i](*pos) in walls and not go[i](*pos) in area:
            return i
    i = randint(1, 4)
    while go[i](*pos) in walls:
        i = randint(1, 4)
    return i

def parse_input(input):
    program = [int(i) for i in input.split(',')]
    area = nx.Graph()
    walls = set()
    pos = (0,0)
    pointer = 0
    rb = 0
    i = 0
    add = 0
    while i < 50000:
        move = decision(pos, area, walls)
        output, pointer, rb = run(program, input=[move], pos=pointer, rb_val=rb)
        newpos = go[move](*pos)
        if output[0]:
            if output[0] == 2:
                os = newpos
                add = 1
            area.add_edge(pos, newpos)
            pos = newpos
        else:
            walls.add(newpos)
        i += add
    return area, os


def p1(area, os):
    path = nx.bidirectional_shortest_path(area, (0,0), os)
    return len(path) - 1


def p2(area, os):
    neighbors = area.neighbors(os)
    i = 0
    while len(area):
        new_neighbors = [n for n1 in neighbors for n in area.neighbors(n1) if n != n1]
        area.remove_nodes_from(neighbors)
        neighbors = new_neighbors
        i += 1
    return i


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(*inp)}")
        print(f"Part 2: {p2(*inp)}")
