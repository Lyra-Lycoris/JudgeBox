import random

SEED = 20261114


def add(out, n, h):
    out.append({"id": "%02d" % (len(out) + 1),
                "input": "%d\n%s\n" % (n, " ".join(map(str, h)))})


def cases():
    rng = random.Random(SEED)
    out = [
        {"id": "01", "input": "6\n2 1 5 6 2 3\n"},
        {"id": "02", "input": "5\n7 7 7 7 7\n"},
    ]
    add(out, 1, [5])
    add(out, 1, [0])
    add(out, 5, [1, 2, 3, 4, 5])
    add(out, 5, [5, 4, 3, 2, 1])
    add(out, 7, [3, 0, 3, 0, 3, 0, 3])
    add(out, 1000, [rng.randint(0, 10 ** 9) for _ in range(1000)])
    add(out, 200000, [rng.randint(0, 10 ** 9) for _ in range(200000)])
    add(out, 200000, [(i + 1) * 5000 for i in range(200000)])
    add(out, 200000, [10 ** 9] * 200000)
    return out
