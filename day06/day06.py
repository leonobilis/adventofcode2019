from collections import defaultdict


def parse_input(input):
    orbits = defaultdict(list)
    for i in input:
        k, v = i.strip().split(")")
        orbits[k].append(v)
    return orbits


def traverse(orbits, elem):
    return len(orbits[elem]) + sum([traverse(orbits, i) for i in orbits[elem]])


def p1(orbits):
    return sum([traverse(orbits, o) for o in list(orbits)])


def traverse2(orbits, elem, catch):
    if elem not in orbits:
        return []
    if catch in orbits[elem]:
        return [elem]
    a = [o2 for o2 in [traverse2(orbits, o, catch) for o in orbits[elem]] if o2]
    return [elem] + a[0] if a else []


def p2(orbits):
    you = set(traverse2(orbits, 'COM', 'YOU'))
    san = set(traverse2(orbits, 'COM', 'SAN'))
    return len(you - san) + len(san - you)


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")
