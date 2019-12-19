from enum import IntEnum
from random import randint
from intcode import Intcode
import networkx as nx


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
    computer = Intcode(program)
    area = nx.Graph()
    walls = set()
    pos = (0,0)
    i = 0
    add = 0
    while i < 50000:
        move = decision(pos, area, walls)
        output = computer.run(input=[move])
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
