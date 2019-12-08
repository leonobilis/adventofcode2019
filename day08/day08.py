from numpy import array, zeros
from itertools import product, dropwhile


WIDTH = 25
HEIGHT = 6
AREA = WIDTH*HEIGHT


def parse_input(input):
    return [int(i) for i in input]


def p1(input):
    layers = [input[i:i+AREA] for i in range(0, len(input), AREA)]
    min0layer = layers[0]
    for layer in layers[1:]: 
        min0layer = layer if layer.count(0) < min0layer.count(0) else min0layer
    return min0layer.count(1) * min0layer.count(2)


def p2(input):
    layers = array(input)
    layers.shape  = (len(input)//AREA, HEIGHT, WIDTH)
    image = zeros((HEIGHT, WIDTH), dtype=int)
    for h, w in product(range(HEIGHT), range(WIDTH)):
        image[h, w] = next(dropwhile(lambda x: x[h, w] == 2, layers))[h, w]
    return image


def image_print(image):
    for line in image:
        print("".join(['#' if i else ' ' for i in line]))


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = parse_input(f.readline())
        print(f"Part 1: {p1(inp)}")
        print("Part 2:")
        image_print(p2(inp))
