from itertools import permutations

def parse_input(input):
    return [int(i) for i in input.split(',')]


def run(prog, input, pos=0):
    output = []
    
    def add(a, b, c, pos):
        prog[c] = a + b
        return pos + 4

    def mul(a, b, c, pos):
        prog[c] = a * b
        return pos + 4

    def inp(a, pos):
        prog[a] = input.pop()
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
    while prog[pos] != 99 and not (prog[pos] == 3 and not input):
        pos = opcode[prog[pos]](prog[pos + 1], prog[pos + 2], prog[pos + 3], pos)
    return output, pos


def p1(program):
    def to_thrusters(phases):
        signal = 0
        for phase in phases:
            signal = run(program.copy(), input=[signal, phase])[0].pop()
        return signal
    return max([to_thrusters(phases) for phases in permutations(range(5), 5)])


def p2(program):
    program.extend([99, 99])
    def to_thrusters(phases):
        amplifiers = [program.copy() for _ in range(5)]
        amplifiers = [list(i) for i in zip(amplifiers, [run(amplifiers[i], input=[phase])[1] for i, phase in enumerate(phases)])]
        signal = 0
        while amplifiers[-1][0][amplifiers[-1][1]] != 99:
            for amp in amplifiers:
                s, amp[1] = run(amp[0], input=[signal], pos=amp[1])
                signal = s.pop()
        return signal
    return max([to_thrusters(phases) for phases in permutations(range(5, 10), 5)])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        input = parse_input(f.readline())
        print(f"Part 1: {p1(input)}")
        print(f"Part 2: {p2(input)}")
