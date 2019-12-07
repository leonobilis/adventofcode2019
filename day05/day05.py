def parse_input(input):
    return [int(i) for i in input.split(',')]


def run(prog, input):
    output = []
    
    def add(a, b, c, pos):
        prog[c] = a + b
        return pos + 4

    def mul(a, b, c, pos):
        prog[c] = a * b
        return pos + 4

    def inp(a, pos):
        prog[a] = input
        return pos + 2

    def out(a, pos):
        output.append(a)
        return pos + 2

    def jump_true(a, b, pos):
        return b if a else pos + 3

    def jump_false(a, b, pos):
        return b if not a else pos + 3

    def less_than(a, b, c, pos):
        prog[c] = 1 if a < b else 0
        return pos + 4

    def equals(a, b, c, pos):
        prog[c] = 1 if a == b else 0
        return pos + 4

    opcode = {
        1: lambda a, b, c, pos: add(prog[a], prog[b], c, pos),
        101: lambda a, b, c, pos: add(a, prog[b], c, pos),
        1001: lambda a, b, c, pos: add(prog[a], b, c, pos),
        1101: lambda a, b, c, pos: add(a, b, c, pos),
        2: lambda a, b, c, pos: mul(prog[a], prog[b], c, pos),
        102: lambda a, b, c, pos: mul(a, prog[b], c, pos),
        1002: lambda a, b, c, pos: mul(prog[a], b, c, pos),
        1102: lambda a, b, c, pos: mul(a, b, c, pos),
        3: lambda a, _b, _c, pos: inp(a, pos),
        4: lambda a, _b, _c, pos: out(prog[a], pos),
        104: lambda a, _b, _c, pos: out(a, pos),
        5: lambda a, b, _c, pos: jump_true(prog[a], prog[b], pos),
        105: lambda a, b, _c, pos: jump_true(a, prog[b], pos),
        1005: lambda a, b, _c, pos: jump_true(prog[a], b, pos),
        1105: lambda a, b, _c, pos: jump_true(a, b, pos),
        6: lambda a, b, _c, pos: jump_false(prog[a], prog[b], pos),
        106: lambda a, b, _c, pos: jump_false(a, prog[b], pos),
        1006: lambda a, b, _c, pos: jump_false(prog[a], b, pos),
        1106: lambda a, b, _c, pos: jump_false(a, b, pos),
        7: lambda a, b, c, pos: less_than(prog[a], prog[b], c, pos),
        107: lambda a, b, c, pos: less_than(a, prog[b], c, pos),
        1007: lambda a, b, c, pos: less_than(prog[a], b, c, pos),
        1107: lambda a, b, c, pos: less_than(a, b, c, pos),
        8: lambda a, b, c, pos: equals(prog[a], prog[b], c, pos),
        108: lambda a, b, c, pos: equals(a, prog[b], c, pos),
        1008: lambda a, b, c, pos: equals(prog[a], b, c, pos),
        1108: lambda a, b, c, pos: equals(a, b, c, pos),
    }
    pos = 0
    while prog[pos] != 99:
        pos = opcode[prog[pos]](prog[pos + 1], prog[pos + 2], prog[pos + 3], pos)
    return output


def p1(program):
    return run(program.copy(), input=1)[-1]


def p2(program):
    return run(program.copy(), input=5)[0]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        input = parse_input(f.readline())
        print(f"Part 1: {p1(input)}")
        print(f"Part 2: {p2(input)}")
