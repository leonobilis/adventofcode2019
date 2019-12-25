from intcode import Intcode


def parse_input(inp):
    return [int(i) for i in inp.split(',')]


def p1(program):
    commands = "east\ntake antenna\nwest\nnorth\ntake weather machine\nnorth\neast\ntake spool of cat6\neast\nsouth\ntake mug\nnorth\nwest\nsouth\nsouth\neast\n"
    return "".join([chr(o) for o in Intcode(program).run([ord(c) for c in commands])]).splitlines()[-1]


def p1manual(program):
    computer = Intcode(program)
    print("".join([chr(o) for o in computer.run()]))
    while computer.is_running():
        print("".join([chr(o) for o in computer.run([ord(i) for i in input()] + [10])]))
    return 0


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        # p1manual(inp)
        print(f"Part 1: {p1(inp)}")
        
