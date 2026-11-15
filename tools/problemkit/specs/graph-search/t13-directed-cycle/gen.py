import random


def _case(n, edges):
    body = "".join("%d %d\n" % (u, v) for u, v in edges)
    return "%d %d\n%s" % (n, len(edges), body)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "6 5\n1 2\n2 3\n3 1\n4 5\n5 6\n"},
        {"id": "02", "input": "2 1\n1 1\n"},
        {"id": "03", "input": "1 0\n"},
        {"id": "04", "input": "1 1\n1 1\n"},
        {"id": "05", "input": "5 4\n1 2\n2 3\n3 4\n4 5\n"},
    ]

    def add(text):
        out.append({"id": "%02d" % (len(out) + 1), "input": text})

    # 两个共享顶点的有向环：1->2->3->1 与 3->4->5->3
    add(_case(5, [(1, 2), (2, 3), (3, 1), (3, 4), (4, 5), (5, 3)]))

    # 环路带一条弦：1->2->3->1 且 1->3
    add(_case(3, [(1, 2), (2, 3), (3, 1), (1, 3)]))

    n = 200000
    edges = [(i, i + 1) for i in range(1, n)]
    edges.append((n, 1))
    add(_case(n, edges))

    add(_case(n, [(i, i + 1) for i in range(1, n)]))

    edges = []
    for i in range(1, n + 1, 2):
        edges.append((i, i + 1))
        edges.append((i + 1, i))
    add(_case(n, edges))

    edges = []
    for _ in range(3000):
        u = rng.randint(1, 2000)
        v = rng.randint(1, 2000)
        edges.append((u, v))
    add(_case(2000, edges))

    edges = []
    for _ in range(2000):
        u = rng.randint(1, 1999)
        v = rng.randint(u + 1, 2000)
        edges.append((u, v))
    add(_case(2000, edges))
    return out
