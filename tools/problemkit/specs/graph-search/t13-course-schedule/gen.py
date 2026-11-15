import random


def _case(n, edges):
    body = "".join("%d %d\n" % (u, v) for u, v in edges)
    return "%d %d\n%s" % (n, len(edges), body)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4 3\n1 2\n1 3\n3 4\n"},
        {"id": "02", "input": "3 3\n1 2\n2 3\n3 1\n"},
        {"id": "03", "input": "1 0\n"},
        {"id": "04", "input": "1 1\n1 1\n"},
        {"id": "05", "input": "2 2\n1 2\n1 2\n"},
    ]

    def add(text):
        out.append({"id": "%02d" % (len(out) + 1), "input": text})

    add(_case(6, [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6)]))

    n = 200000
    add(_case(n, [(i, i + 1) for i in range(1, n)]))

    edges = [(i, i + 1) for i in range(1, n)]
    edges.append((n, 1))
    add(_case(n, edges))

    edges = []
    for _ in range(200000):
        u = rng.randint(1, n - 1)
        v = rng.randint(u + 1, n)
        edges.append((u, v))
    add(_case(n, edges))

    add(_case(5, []))
    add(_case(3, [(1, 2), (2, 1)]))
    add(_case(2000, [(i, i + 1) for i in range(1, 1000)]))
    return out
