from collections import namedtuple
from enum import Enum
from intcode import Intcode


def parse_input(input):
    return [int(i) for i in input.split(',')]


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
    computer = Intcode(program)
    computer.run()
    while computer.is_running():
        output = computer.run(input=[panels.get(robot.pos, 0)])
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
