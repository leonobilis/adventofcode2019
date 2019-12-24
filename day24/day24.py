def parse_input(input):
    return [i.strip() for i in input]


def count_bug_adjacent(x, y, grid):
    return sum([grid[y+ydiff][x+xdiff] == '#' for xdiff, ydiff in ((0,1), (1,0), (0, -1), (-1, 0)) if 0 <= x+xdiff < len(grid[0]) and 0 <= y+ydiff < len(grid)])


def p1(input):
    grid = tuple(input)
    seen = set()
    while grid not in seen:
        seen.add(grid)
        new_grid = []
        adjacent = [[count_bug_adjacent(x, y, grid) for x, xval in enumerate(yval)] for y, yval in enumerate(grid)]
        for g, a in zip(grid, adjacent):
            new_line = ""
            for i in range(len(g)):
                if g[i] == '#' and a[i] != 1:
                    new_line += '.'
                elif g[i] == '.' and  1 <= a[i] <= 2:
                    new_line += '#'
                else:
                    new_line += g[i]
            new_grid.append(new_line)
        grid = tuple(new_grid)
    return sum([2**(y*len(grid[0])+x) for y, line in enumerate(grid) for x, g in enumerate(line) if g == '#'])


def count_bug_adjacent2(x, y, grid, level, grids):
    if grid[y][x] == '?':
        return 0
    bugs = 0
    for xdiff, ydiff in ((0,1), (1,0), (0, -1), (-1, 0)):
        if 0 > x + xdiff or x + xdiff > 4 or 0 > y + ydiff or y + ydiff > 4:
            bugs += int(grids[level-1][2+ydiff][2+xdiff] == '#') if level > 0 else 0
        elif x == 2 and y+ydiff == 2:
            bugs += grids[level+1][0 if ydiff+1 else -1].count('#') if level + 1 < len(grids) else 0
        elif y == 2 and x+xdiff == 2:
            bugs += [i[0 if xdiff+1 else -1] for i in grids[level+1]].count('#') if level + 1 < len(grids) else 0
        else:
            bugs += int(grid[y+ydiff][x+xdiff] == '#')
    return bugs
         

def p2(input, iter):
    depth = iter + 2
    initial_grid = input.copy()
    initial_grid[2] = initial_grid[2][:2] + '?' + initial_grid[2][3:]
    empty_grid = ['..?..' if i==2 else '.....' for i in range(5)]
    grids = [initial_grid if i==depth//2 else empty_grid.copy() for i in range(depth)]
    for _ in range(iter):
        new_grids = []
        for level, grid in enumerate(grids):
            new_grid = []
            adjacent = [[count_bug_adjacent2(x, y, grid, level, grids) for x, xval in enumerate(yval)] for y, yval in enumerate(grid)]
            for g, a in zip(grid, adjacent):
                new_line = ""
                for i in range(len(g)):
                    if g[i] == '#' and a[i] != 1:
                        new_line += '.'
                    elif g[i] == '.' and  1 <= a[i] <= 2:
                        new_line += '#'
                    else:
                        new_line += g[i]
                new_grid.append(new_line)
            new_grids.append(new_grid)
        grids = new_grids
    return sum([g.count('#') for grid in grids for g in grid])


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readlines())
        print(f"Part 1: {p1(inp)}")
        print(f"Part 2: {p2(inp, 200)}")
