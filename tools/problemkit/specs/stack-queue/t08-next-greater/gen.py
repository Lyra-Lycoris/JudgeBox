import random

SEED = 20261114


def add(out, n, a):
    out.append({"id": "%02d" % (len(out) + 1),
                "input": "%d\n%s\n" % (n, " ".join(map(str, a)))})


def cases():
    rng = random.Random(SEED)
    out = [
        {"id": "01", "input": "5\n2 1 3 5 4\n"},
        {"id": "02", "input": "4\n4 4 3 5\n"},
    ]
    add(out, 1, [7])
    add(out, 6, [4] * 6)
    add(out, 5, [5, 4, 3, 2, 1])
    add(out, 5, [1, 2, 3, 4, 5])
    add(out, 4, [-5, -1, -3, -2])
    add(out, 8, [10 ** 9, -10 ** 9, 10 ** 9, -10 ** 9, 0, 0, -1, 10 ** 9])
    add(out, 1000, [rng.randint(-100, 100) for _ in range(1000)])
    add(out, 200000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    add(out, 200000, [i * 5000 - 10 ** 9 for i in range(200000)])
    add(out, 200000, [7] * 200000)
    return out
