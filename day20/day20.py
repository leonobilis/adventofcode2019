from itertools import product
import networkx as nx


def gen_tunnels(input):
    tunnels = nx.Graph()
    teleports = {}
    for x, y in product(range(len(input[0]) - 1), range(len(input) - 1)):
        val = input[y][x]
        if val != '#' and val != ' ':
            if 'A' <= val <= 'Z':
                t = None
                if 'A' <= input[y+1][x] <= 'Z':
                    t = f"{val}{input[y+1][x]}"
                    node = (x, y+2) if y+2 < len(input) and input[y+2][x] == '.' else (x, y-1)
                    tunnels.add_node(node, teleport=t)
                elif 'A' <= input[y][x+1] <= 'Z':
                    t = f"{val}{input[y][x+1]}"
                    node = (x+2, y) if x+2 < len(input[0]) and input[y][x+2] == '.' else (x-1, y)
                    tunnels.add_node(node, teleport=t)
                if t in teleports:
                    tunnels.add_edge(node, teleports[t])
                elif t:
                    teleports[t] = node
            if y > 0 and input[y-1][x] != '#' and input[y-1][x] != ' ':
                tunnels.add_edge((x, y), (x,y-1))
            if x > 0 and input[y][x-1] != '#' and input[y][x-1] != ' ':
                tunnels.add_edge((x, y), (x-1,y))
    return tunnels, teleports["AA"], teleports["ZZ"]


def p1(inp):
    tunnels, start, end = gen_tunnels(inp)
    return len(nx.shortest_path(tunnels, start, end)) - 1


def gen_tunnels2(input):
    tunnels = nx.Graph()
    inside_teleports = {}
    outside_teleports = {}
    for x, y in product(range(len(input[0]) - 1), range(len(input) - 1)):
        val = input[y][x]
        if val != '#' and val != ' ' and val != '\n':
            if 'A' <= val <= 'Z':
                t = None
                if 'A' <= input[y+1][x] <= 'Z':
                    t = f"{val}{input[y+1][x]}"
                    node = (x, y+2) if y+2 < len(input) and input[y+2][x] == '.' else (x, y-1)
                    #tunnels.add_node(node, teleport=t)
                elif 'A' <= input[y][x+1] <= 'Z':
                    t = f"{val}{input[y][x+1]}"
                    node = (x+2, y) if x+2 < len(input[0]) and input[y][x+2] == '.' else (x-1, y)
                    #tunnels.add_node(node, teleport=t)
                if t and (y==0 or y==len(input)-2 or x==0 or x==len(input[0])-3):
                    outside_teleports[t] = node
                elif t:
                    inside_teleports[t] = node
            if y > 0 and input[y-1][x] == '.':
                tunnels.add_edge((x, y, 0), (x,y-1, 0))
            if x > 0 and input[y][x-1] == '.':
                tunnels.add_edge((x, y, 0), (x-1,y, 0))
    
    for level in range(1, len(outside_teleports)):
        for n1, n2 in [(a, b) for a, b in tunnels.edges]:
            tunnels.add_edge((n1[0], n1[1], level), (n2[0], n2[1], level))
    for level in range(len(outside_teleports)):
        for key, val in inside_teleports.items():
            tunnels.add_edge((val[0], val[1], level), (outside_teleports[key][0], outside_teleports[key][1], level+1))
    return tunnels, outside_teleports["AA"] + (0,), outside_teleports["ZZ"] + (0,)


def p2(inp):
    tunnels, start, end = gen_tunnels2(inp)
    return len(nx.shortest_path(tunnels, start, end)) - 1


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = f.readlines()
        print(f"Part 1: {p1(inp.copy())}")
        print(f"Part 2: {p2(inp.copy())}")
