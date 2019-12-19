from itertools import takewhile
from enum import IntEnum
from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    out = Intcode(program).run(input=[])
    grid = ''.join([chr(o) for o in out]).strip().split('\n')

    #print("\n".join(grid))
    
    return sum([x*y for y in range(1, len(grid) - 1) for x in range(1,len(grid[0]) - 1) if grid[y][x]=='#' and all([grid[y+d[1]][x+d[0]]=='#' for d in [(0,1), (1,0), (0,-1), (-1,0)]])])


class Dir(IntEnum):
    north = 1
    south = 2
    west = 3
    east = 4


def get_vacuum_robot(grid):
    for y, line in enumerate(grid):
        for c, _dir in [('^', Dir.north), ('v', Dir.south), ('<', Dir.west), ('>', Dir.east)]:
            x = line.find(c)
            if x >= 0:
                return (x, y), _dir


def safeget(x, y, grid):
    return grid[y][x] if 0 <= y < len(grid) and 0 <= x < len(grid[y]) else ''


rotate = {
    Dir.north: lambda pos, grid: ('R', Dir.east) if safeget(pos[0]+1, pos[1], grid) == "#" else (('L', Dir.west) if safeget(pos[0]-1, pos[1], grid) == "#" else (None, None)),
    Dir.south: lambda pos, grid: ('R', Dir.west) if safeget(pos[0]-1, pos[1], grid) == "#" else (('L', Dir.east) if safeget(pos[0]+1, pos[1], grid) == "#" else (None, None)),
    Dir.west: lambda pos, grid: ('R', Dir.north) if safeget(pos[0], pos[1]-1, grid) == "#" else (('L', Dir.south) if safeget(pos[0], pos[1]+1, grid) == "#" else (None, None)),
    Dir.east: lambda pos, grid: ('R', Dir.south) if safeget(pos[0], pos[1]+1, grid) == "#" else (('L', Dir.north) if safeget(pos[0], pos[1]-1, grid) == "#" else (None, None))
}


steps_gen = {
    Dir.north: lambda pos, _, grid_t: reversed(grid_t[pos[0]][:pos[1]]),
    Dir.south: lambda pos, _, grid_t: grid_t[pos[0]][pos[1]+1:],
    Dir.west: lambda pos, grid, _: reversed(grid[pos[1]][:pos[0]]),
    Dir.east: lambda pos, grid, _: grid[pos[1]][pos[0]+1:]
}


update_pos = {
    Dir.north: lambda pos, steps: (pos[0], pos[1] - steps),
    Dir.south: lambda pos, steps: (pos[0], pos[1] + steps),
    Dir.west: lambda pos, steps: (pos[0] - steps, pos[1]),
    Dir.east: lambda pos, steps: (pos[0] + steps, pos[1])
}

def p2(program):
    program[0] = 2
    computer = Intcode(program)
    out = computer.run(input=[])
    grid = ''.join([chr(o) for o in out[:-7]]).strip().split('\n')
    grid_t = [i for i in zip(*grid)]

    #print("\n".join(grid))
    #print()
    #print("\n".join(["".join(g) for g in grid_t]))

    vrpos, vrdir = get_vacuum_robot(grid)
    path = []
    rot, vrdir = rotate[vrdir](vrpos, grid)
    while rot:
        path.append(rot)
        steps = len(list(takewhile(lambda x: x == '#', steps_gen[vrdir](vrpos, grid, grid_t))))
        path.append(str(steps))
        vrpos = update_pos[vrdir](vrpos, steps)
        rot, vrdir = rotate[vrdir](vrpos, grid)

    print(",".join(path))
    inp=[ord(i) for i in ("A,A,B,C,B,C,B,C,B,A\nL,10,L,8,R,8,L,8,R,6\nR,6,R,8,R,8\nR,6,R,6,L,8,L,10\ny\n")]
    out  = computer.run(input=inp)
    return out[-1]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
