import random


def pack(n, edges):
    body = "".join("%d %d\n" % (u, v) for u, v in edges)
    return "%d\n%s" % (n, body)


def path_edges(n):
    return [(i, i + 1) for i in range(1, n)]


def star_edges(n):
    return [(1, i) for i in range(2, n + 1)]


def random_tree(rng, n):
    return [(rng.randint(1, i - 1), i) for i in range(2, n + 1)]


def caterpillar(rng, n):
    # 一条主干，每个主干点再挂 0~3 个叶子，用来制造较深的直径。
    spine = max(2, n // 4)
    edges = [(i, i + 1) for i in range(1, spine)]
    nxt = spine + 1
    while nxt <= n:
        edges.append((rng.randint(1, spine), nxt))
        nxt += 1
    return edges


def cases():
    rng = random.Random(20261114)
    out = []
    out.append({"id": "01", "input": pack(6, [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6)])})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [(1, 2)])})
    out.append({"id": "04", "input": pack(10, path_edges(10))})
    out.append({"id": "05", "input": pack(8, star_edges(8))})
    out.append({"id": "06", "input": pack(9, caterpillar(rng, 9))})
    out.append({"id": "07", "input": pack(50, random_tree(rng, 50))})
    out.append({"id": "08", "input": pack(5000, random_tree(rng, 5000))})
    out.append({"id": "09", "input": pack(200000, path_edges(200000))})
    out.append({"id": "10", "input": pack(200000, random_tree(rng, 200000))})
    out.append({"id": "11", "input": pack(200000, star_edges(200000))})
    return out
