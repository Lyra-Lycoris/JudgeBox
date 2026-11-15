import random

SEED = 20261114


def add(out, n, k, a):
    out.append({"id": "%02d" % (len(out) + 1),
                "input": "%d %d\n%s\n" % (n, k, " ".join(map(str, a)))})


def cases():
    rng = random.Random(SEED)
    out = [
        {"id": "01", "input": "8 3\n1 3 -1 -3 5 3 6 7\n"},
        {"id": "02", "input": "5 1\n-4 -2 -7 0 -1\n"},
    ]
    add(out, 1, 1, [-5])
    add(out, 5, 5, [1, 2, 3, 4, 5])
    add(out, 6, 3, [4] * 6)
    add(out, 7, 4, [9, -9, 8, -8, 7, -7, 6])
    add(out, 6, 2, [10 ** 9, -10 ** 9, 0, 10 ** 9, -10 ** 9, 0])
    add(out, 1000, 37, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(1000)])
    add(out, 200000, 100, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    add(out, 200000, 200000, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    add(out, 200000, 1, [rng.randint(-10 ** 9, 10 ** 9) for _ in range(200000)])
    add(out, 200000, 3, [10 ** 9 - i * 5000 for i in range(200000)])
    return out
