import random


def _case(n, edges):
    body = "".join("%d %d\n" % (u, v) for u, v in edges)
    return "%d %d\n%s" % (n, len(edges), body)


def cases():
    rng = random.Random(20261114)
    out = [
        {"id": "01", "input": "4 4\n1 2\n2 3\n3 4\n4 1\n"},
        {"id": "02", "input": "3 3\n1 2\n2 3\n3 1\n"},
        {"id": "03", "input": "1 0\n"},
        {"id": "04", "input": "1 1\n1 1\n"},
        {"id": "05", "input": "5 0\n"},
    ]

    def add(text):
        out.append({"id": "%02d" % (len(out) + 1), "input": text})

    # 一个偶环加一个三角形：不是二分图
    add(_case(9, [(1, 2), (2, 3), (3, 4), (4, 1), (5, 6), (6, 7), (7, 5)]))

    # 1000 个点的偶环
    add(_case(1000, [(i, i + 1) for i in range(1, 1000)] + [(1000, 1)]))

    # 1000 个点的树：一定是二分图
    add(_case(1000, [(i, rng.randint(1, i - 1)) for i in range(2, 1001)]))

    n = 200000
    add(_case(n, [(i, i + 1) for i in range(1, n)]))

    edges = []
    half = n // 2
    for _ in range(200000):
        u = rng.randint(1, half)
        v = rng.randint(half + 1, n)
        edges.append((u, v))
    add(_case(n, edges))

    edges = []
    for _ in range(200000):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        edges.append((u, v))
    add(_case(n, edges))
    return out
