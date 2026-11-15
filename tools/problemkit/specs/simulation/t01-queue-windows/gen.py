import random


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "3 1\n0 2 5\n4 4 4\n"},
        {"id": "02", "input": "1 1\n7\n3\n"},
        {"id": "03", "input": "3 5\n0 1 2\n10 10 10\n"},
        {"id": "04", "input": "4 2\n0 0 5 5\n0 0 0 0\n"},
        {"id": "05", "input": "5 1\n0 0 0 0 0\n1 1 1 1 1\n"},
        {"id": "06", "input": "6 3\n0 0 0 0 0 0\n5 5 5 5 5 5\n"},
        {"id": "07", "input": "2 1\n0 0\n1000000000 1000000000\n"},
    ]

    def add(n, k, max_serve):
        arrive = sorted(rng.randint(0, 10 ** 9) for _ in range(n))
        serve = [rng.randint(0, max_serve) for _ in range(n)]
        out.append({"id": "%02d" % (len(out) + 1),
                    "input": "%d %d\n%s\n%s\n" % (n, k, " ".join(map(str, arrive)),
                                                   " ".join(map(str, serve)))})

    add(1000, 7, 10 ** 9)
    add(200000, 1, 1000)
    add(200000, 1000, 10 ** 9)
    add(200000, 200000, 10 ** 9)
    add(200000, 3, 1000000)
    return out
