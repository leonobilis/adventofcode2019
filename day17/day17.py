from itertools import takewhile
from enum import IntEnum


def parse_input(input):
    return [int(i) for i in input.split(',')]


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


def p1(program):
    return 0
    program = program.copy()
    program.extend([0]*5000)
    out, *_ = run(program, input=[])
    grid = ''.join([chr(o) for o in out]).strip().split('\n')

    print("\n".join(grid))
    
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
    program1 = program.copy()
    #program[0] = 2
    program1.extend([0]*5000)
    out, *_ = run(program1, input=[])
    grid = ''.join([chr(o) for o in out]).strip().split('\n')
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

    #print(",".join(path))

    program2 = program.copy()
    program2[0] = 2
    program2.extend([0]*5000)
    inp=[ord(i) for i in reversed("A,A,B,C,B,C,B,C,B,A\nL,10,L,8,R,8,L,8,R,6\nR,6,R,8,R,8\nR,6,R,6,L,8,L,10\ny\n")]
    print(inp)
    out, *_ = run(program2, input=inp)
    return out[-1]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
