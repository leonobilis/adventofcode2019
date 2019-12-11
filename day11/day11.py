from collections import namedtuple
from enum import Enum


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


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


turn_left = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP
}


turn_right = {
    Direction.UP: Direction.RIGHT,
    Direction.LEFT: Direction.UP,
    Direction.DOWN: Direction.LEFT,
    Direction.RIGHT: Direction.DOWN
}


go = {
    Direction.UP: lambda x, y: (x, y+1),
    Direction.LEFT: lambda x, y: (x-1, y),
    Direction.DOWN: lambda x, y: (x, y-1),
    Direction.RIGHT: lambda x, y: (x+1, y)
}


def paint(program, panels={}):
    Robot = namedtuple('Robot', ['dir', 'pos'])
    robot = Robot(dir=Direction.UP, pos=(0, 0))
    program = program.copy()
    program.extend([0]*500)
    pointer = 0
    rb = 0
    while program[pointer] != 99:
        output, pointer, rb = run(program, input=[panels.get(robot.pos, 0)], pos=pointer, rb_val=rb)
        panels[robot.pos] = output[0]
        new_dir = turn_right[robot.dir] if output[1] else turn_left[robot.dir]
        robot = Robot(dir=new_dir, pos=go[new_dir](*robot.pos))
    return panels


def p1(input):
    return len(paint(input))


def p2(input):
    painted_panels = paint(input, panels={(0,0): 1})
    maxX = max(painted_panels.keys(), key=lambda x: x[0])[0]
    minX = min(painted_panels.keys(), key=lambda x: x[0])[0]
    maxY = max(painted_panels.keys(), key=lambda x: x[1])[1]
    minY = min(painted_panels.keys(), key=lambda x: x[1])[1]
    image = [[painted_panels.get((x, y), 0) for x in range(minX, maxX+1)] for y in range(minY, maxY+1)]
    return image


def image_print(image):
    for line in reversed(image):
        print("".join(['#' if i else ' ' for i in line]))


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print("Part 2:")
        image_print(p2(inp))
