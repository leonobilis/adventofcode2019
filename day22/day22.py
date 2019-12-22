def deal_into_new_stack(deck):
    return list(reversed(deck))


def cut_factory(N):
    def cut(deck):
        return deck[N:] + deck[:N]
    return cut


def deal_with_increment_factory(N):
    def deal_with_increment(deck):
        new_deck = {}
        i = 0
        for i, d in enumerate(deck):
            new_deck[i*N%len(deck)] = d
        return [new_deck[i] for i in sorted(new_deck)]
    return deal_with_increment


def get_technique(input):
    i = input.strip().split(' ')
    if i[-2] == "new":
        return deal_into_new_stack
    elif i[-2] == "cut":
        return cut_factory(int(i[-1]))
    else:
        return deal_with_increment_factory(int(i[-1]))


def p1(input):
    deck = list(range(10007))
    for i in input:
        deck = get_technique(i)(deck)
    return deck.index(2019)


def modular_inverse(x, dec_len):
    return pow(x, dec_len-2, dec_len)


def p2(input):
    deck_len = 119315717514047
    repeat = 101741582076661
    offset = 0
    mul = 1
    for i in input:
        j = i.strip().split(' ')
        if j[-2] == "new":
            mul *= (-1) % deck_len
            offset = (offset + mul) % deck_len
        elif j[-2] == "cut":
            offset = (offset + mul * int(j[-1])) % deck_len
        else:
            mul *= modular_inverse(int(j[-1]), deck_len) % deck_len

    increment = pow(mul, repeat, deck_len)
    offset = offset * (1 - increment) * modular_inverse((1 - mul) % deck_len, deck_len) % deck_len
    return (offset + 2020 * increment) % deck_len


if __name__ == "__main__":
    with open('input.txt', "r") as f:
        inp = f.readlines()
        print(f"Part 1: {p1(inp.copy())}")
        print(f"Part 2: {p2(inp.copy())}")
