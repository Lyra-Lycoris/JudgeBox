import random


def _edges(edges):
    return "".join("%d %d\n" % (u, v) for u, v in edges)


def _case(n, edges):
    return "%d %d\n%s" % (n, len(edges), _edges(edges))


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "5 3\n1 2\n2 3\n4 5\n"},
        {"id": "02", "input": "1 0\n"},
        {"id": "03", "input": "1 1\n1 1\n"},
        {"id": "04", "input": "5 0\n"},
        {"id": "05", "input": "4 3\n1 2\n1 2\n1 2\n"},
    ]

    def add(text):
        out.append({"id": "%02d" % (len(out) + 1), "input": text})

    add(_case(1000, [(i, i + 1) for i in range(1, 1000)]))

    add(_case(10, [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                   (7, 8), (8, 9), (9, 7)]))

    n = 200000
    edges = [(i, i + 1) for i in range(1, n)]
    add(_case(n, edges))

    edges = []
    for _ in range(200000):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        edges.append((u, v))
    add(_case(n, edges))

    add(_case(n, []))

    edges = [(2 * i - 1, 2 * i) for i in range(1, 1001)]
    add(_case(2000, edges))
    return out
