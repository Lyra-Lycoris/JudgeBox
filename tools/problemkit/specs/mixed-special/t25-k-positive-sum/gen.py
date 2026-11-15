import random


def cases():
    rng = random.Random(20261116)
    pairs = [
        (10, 3),
        (1, 1),
        (5, 5),
        (200000, 1),
        (200000, 200000),
        (1000000000, 1),
        (1000000000, 200000),
        (100, 7),
        (999999999, 199999),
        (3, 2),
        (1000000000, 2),
    ]
    out = [{"id": "01", "input": "%d %d\n" % (10, 3)}]
    for i, (s, k) in enumerate(pairs[1:], start=2):
        out.append({"id": "%02d" % i, "input": "%d %d\n" % (s, k)})
    s = rng.randint(200000, 1000000000)
    k = rng.randint(1, 200000)
    out.append({"id": "%02d" % (len(out) + 1), "input": "%d %d\n" % (s, k)})
    return out
