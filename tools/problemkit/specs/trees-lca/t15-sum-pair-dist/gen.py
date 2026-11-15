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


def broom(n):
    # 一根短主干，末端挂一大团叶子，答案结构比较“不均匀”。
    spine = max(2, n // 10)
    edges = [(i, i + 1) for i in range(1, spine)]
    for v in range(spine + 1, n + 1):
        edges.append((spine, v))
    return edges


def cases():
    rng = random.Random(20261119)
    out = []
    out.append({"id": "01", "input": pack(3, [(1, 2), (2, 3)])})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [(1, 2)])})
    out.append({"id": "04", "input": pack(10, path_edges(10))})
    out.append({"id": "05", "input": pack(5, star_edges(5))})
    out.append({"id": "06", "input": pack(12, broom(12))})
    out.append({"id": "07", "input": pack(100, random_tree(rng, 100))})
    out.append({"id": "08", "input": pack(5000, random_tree(rng, 5000))})
    out.append({"id": "09", "input": pack(200000, path_edges(200000))})
    out.append({"id": "10", "input": pack(200000, star_edges(200000))})
    out.append({"id": "11", "input": pack(200000, random_tree(rng, 200000))})
    return out
