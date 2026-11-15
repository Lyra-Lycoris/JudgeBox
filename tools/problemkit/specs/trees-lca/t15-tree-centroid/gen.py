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


def double_star(n):
    # 两个中心 1、2，其余节点平均挂在两边：恰好有两个重心。
    edges = [(1, 2)]
    for v in range(3, n + 1):
        edges.append((1 if v % 2 == 0 else 2, v))
    return edges


def cases():
    rng = random.Random(20261116)
    out = []
    out.append({"id": "01", "input": pack(6, path_edges(6))})
    out.append({"id": "02", "input": pack(1, [])})
    out.append({"id": "03", "input": pack(2, [(1, 2)])})
    out.append({"id": "04", "input": pack(7, star_edges(7))})
    out.append({"id": "05", "input": pack(7, path_edges(7))})
    out.append({"id": "06", "input": pack(6, double_star(6))})
    out.append({"id": "07", "input": pack(100, random_tree(rng, 100))})
    out.append({"id": "08", "input": pack(5000, random_tree(rng, 5000))})
    out.append({"id": "09", "input": pack(200000, path_edges(200000))})
    out.append({"id": "10", "input": pack(200000, star_edges(200000))})
    out.append({"id": "11", "input": pack(200000, random_tree(rng, 200000))})
    return out
