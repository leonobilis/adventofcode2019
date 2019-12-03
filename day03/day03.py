def parse_input(input):
    wire1_paths = [(i[0], int(i[1:])) for i in input[0].split(',')]
    wire2_paths = [(i[0], int(i[1:])) for i in input[1].split(',')]
    return wire1_paths, wire2_paths


def points(paths):
    points_gen = {
        'U': lambda p, v: ({(p[0], i) for i in range(p[1] + 1, p[1] + 1 + v)}, (p[0], p[1] + v)),
        'D': lambda p, v: ({(p[0], i) for i in range(p[1] - 1, p[1] - 1 - v, -1)}, (p[0], p[1] - v)),
        'R': lambda p, v: ({(i, p[1]) for i in range(p[0] + 1, p[0] + 1 + v)}, (p[0] + v, p[1])),
        'L': lambda p, v: ({(i, p[1]) for i in range(p[0] - 1, p[0] - 1 - v, -1)}, (p[0] - v, p[1]))
    }
    pos = (0, 0)
    points_set = set()
    for direction, length in paths:
        new_points, pos = points_gen[direction](pos, length)
        points_set.update(new_points)
    return points_set


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def p1(wire1_paths, wire2_paths):
    wire1, wire2 = points(wire1_paths), points(wire2_paths)
    return min(map(lambda x: dist((0, 0), x), wire1.intersection(wire2)))


def points_dist(paths):
    points_gen = {
        'U': lambda p, v, vtotal: ({(p[0], p[1] + i): vtotal + i for i in range(1, v + 1)}, (p[0], p[1] + v), vtotal + v),
        'D': lambda p, v, vtotal: ({(p[0], p[1] - i): vtotal + i for i in range(1, v + 1)}, (p[0], p[1] - v), vtotal + v),
        'R': lambda p, v, vtotal: ({(p[0] + i, p[1]): vtotal + i for i in range(1, v + 1)}, (p[0] + v, p[1]), vtotal + v),
        'L': lambda p, v, vtotal: ({(p[0] - i, p[1]): vtotal + i for i in range(1, v + 1)}, (p[0] - v, p[1]), vtotal + v)
    }
    pos = (0, 0)
    total_dist = 0
    points_map = {}
    for direction, length in paths:
        new_points, pos, total_dist = points_gen[direction](pos, length, total_dist)
        points_map.update(new_points)
    return points_map


def p2(wire1_paths, wire2_paths):
    wire1, wire2 = points_dist(wire1_paths), points_dist(wire2_paths)
    return min([v + wire2[k] for k, v in wire1.items() if k in wire2])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print("Part 1: {}".format(p1(*inp)))
        print("Part 2: {}".format(p2(*inp)))
