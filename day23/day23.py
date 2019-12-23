from intcode import Intcode
from collections import namedtuple


def parse_input(input):
    return [int(i) for i in input.split(',')]


def p1(program):
    computers = [Intcode(program) for _ in range(50)]
    packets = [[i] for i in range(50)]
    while True:
        if not any(p for p in packets):
            packets = [[-1] for _ in range(50)]
        outputs = []
        for i, c in enumerate(computers):
            if packets[i]:
                outputs.extend(c.run(packets[i]))
        packets = [[] for _ in range(50)]
        for i in range(0, len(outputs), 3):
            if outputs[i] == 255:
                return outputs[i + 2]
            packets[outputs[i]].extend([outputs[i + 1], outputs[i +2]])


def p2(program):
    computers = [Intcode(program) for _ in range(50)]
    packets = [[i] for i in range(50)]
    NAT = namedtuple("NAT", ["packet", "y_sent"])
    nat = NAT(packet=(float('inf'), float('inf')), y_sent=float('inf'))
    idle_count = 0
    while True:
        if not any(p for p in packets):
            idle_count += 1
            packets = [[-1] for _ in range(50)]
        else:
            idle_count = 0
        outputs = []
        if idle_count > 1:
            if nat.packet[1] == nat.y_sent:
                return nat.y_sent
            outputs.extend([0, nat.packet[0], nat.packet[1]])
            nat = NAT(packet=nat.packet, y_sent=nat.packet[1])
        for i, c in enumerate(computers):
            if packets[i]:
                outputs.extend(c.run(packets[i]))
        packets = [[] for _ in range(50)]
        for i in range(0, len(outputs), 3):
            if outputs[i] == 255:
                nat = NAT(packet=(outputs[i + 1], outputs[i +2]), y_sent=nat.y_sent)
            else:
                packets[outputs[i]].extend([outputs[i + 1], outputs[i +2]])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        input = parse_input(f.readline())
        print(f"Part 1: {p1(input)}")
        print(f"Part 2: {p2(input)}")
