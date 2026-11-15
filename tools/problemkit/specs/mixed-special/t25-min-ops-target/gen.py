import random


def line(values):
    return " ".join(str(x) for x in values)


def cases():
    rng = random.Random(20261118)
    out = []

    def add(a, b):
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d\n%s\n%s\n" % (len(a), line(a), line(b))})

    add([1, 2, 3], [3, 2, 1])
    add([-1000000000], [1000000000])
    add([5], [5])
    add([1, 1, 1, 1], [1, 1, 1, 1])
    add([0, 0, 0, 0], [1, 2, 3, 4])
    add([0] * 10, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1])

    n = 2000
    add([rng.randint(-1000000000, 1000000000) for _ in range(n)],
        [rng.randint(-1000000000, 1000000000) for _ in range(n)])
    add([rng.randint(-1000, 1000) for _ in range(n)],
        [rng.randint(-1000, 1000) for _ in range(n)])

    n = 200000
    add([0] * n, [1000000000 if i % 2 == 0 else -1000000000 for i in range(n)])
    add([rng.randint(-1000, 1000) for _ in range(n)],
        [rng.randint(-1000, 1000) for _ in range(n)])
    add(list(range(n)), list(range(n, 2 * n)))
    m2 = 160000
    add([-1000000000] * m2, [1000000000] * m2)
    return out
