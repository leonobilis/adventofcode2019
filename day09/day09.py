def parse_input(input):
    return [int(i) for i in input.split(',')]


def run(prog, input, pos=0):
    output = []
    rb = [0]

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
    return output, pos

def p1(input):
    program = input.copy()
    program.extend([0]*100)
    return run(program, input=[1])[0][0]


def p2(input):
    program = input.copy()
    program.extend([0]*150)
    return run(program, input=[2])[0][0]


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp)}")