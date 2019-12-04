from itertools import groupby

def criteria(password):
    return any([password[i] == password[i + 1] for i in range(len(password) - 1)]) \
            and all([password[i] <= password[i + 1] for i in range(len(password) - 1)])


def p1(start, end):
    return len([i for i in range(start, end + 1) if criteria(str(i))])


def criteria2(password):
    return any([len(list(i)) == 2 for _, i in groupby(password)]) \
            and all([password[i] <= password[i + 1] for i in range(len(password) - 1)])


def p2(start, end):
    return len([i for i in range(start, end + 1) if criteria2(str(i))])


if __name__ == "__main__":
    _range = (123257, 647015)
    print("Part 1: {}".format(p1(*_range)))
    print("Part 2: {}".format(p2(*_range)))
