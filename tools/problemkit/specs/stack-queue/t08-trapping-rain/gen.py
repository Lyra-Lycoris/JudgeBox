import random

SEED = 20261114
LIMIT = 10 ** 9


def add(out, n, h):
    out.append({"id": "%02d" % (len(out) + 1),
                "input": "%d\n%s\n" % (n, " ".join(map(str, h)))})


def cases():
    rng = random.Random(SEED)
    out = [
        {"id": "01", "input": "12\n0 1 0 2 1 0 1 3 2 1 2 1\n"},
        {"id": "02", "input": "6\n4 2 0 3 2 5\n"},
    ]
    add(out, 1, [5])
    add(out, 1, [0])
    add(out, 2, [3, 1])
    add(out, 6, [3, 3, 3, 3, 3, 3])
    add(out, 5, [5, 0, 0, 0, 5])
    add(out, 8, [0] * 8)
    add(out, 9, [LIMIT, 0, 0, 0, 0, 0, 0, 0, LIMIT])
    add(out, 1000, [rng.randint(0, LIMIT) for _ in range(1000)])
    add(out, 200000, [rng.randint(0, LIMIT) for _ in range(200000)])
    add(out, 200000, [abs(i - 100000) * 5000 for i in range(200000)])
    add(out, 200000, [i * 5000 for i in range(200000)])
    add(out, 200000, [LIMIT] * 200000)
    return out
