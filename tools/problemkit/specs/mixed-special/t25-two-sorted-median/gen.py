import random


def line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261117)
    out = []

    def add(a, b):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n%d\n%s\n" % (len(a), line(a), len(b), line(b))})

    add([1, 3], [2])
    add([5], [5])
    add([1], [1000000000])
    add([-1000000000], [-1000000000])
    add([1, 2, 3], [4, 5, 6])
    add([7, 7, 7, 7, 7], [7, 7, 7, 7, 7])
    add(list(range(1, 1001, 2)), list(range(2, 1002, 2)))
    add([-1000000000, -999999999], [-1000000000])

    n = 200000
    add(sorted(rng.randint(-1000, 1000) for _ in range(n)),
        sorted(rng.randint(-1000, 1000) for _ in range(n)))
    add([0] * n, [0] * n)
    m2 = 160000
    add([-1000000000] * m2, [1000000000] * m2)
    add(list(range(-100000, 100000)), list(range(-100000, 100000)))
    return out
