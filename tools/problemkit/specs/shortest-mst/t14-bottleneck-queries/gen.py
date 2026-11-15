import random


def pack(n, edges, queries):
    lines = ["%d %d %d" % (n, len(edges), len(queries))]
    lines.extend("%d %d %d" % e for e in edges)
    lines.extend("%d %d" % p for p in queries)
    return "\n".join(lines) + "\n"


def random_connected(rng, n, extra, wmax):
    edges = [(rng.randint(1, i - 1), i, rng.randint(1, wmax)) for i in range(2, n + 1)]
    for _ in range(extra):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        edges.append((u, v, rng.randint(1, wmax)))
    return edges


def random_queries(rng, n, q):
    return [(rng.randint(1, n), rng.randint(1, n)) for _ in range(q)]


def cases():
    rng = random.Random(20261121)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(
        4,
        [(1, 2, 5), (2, 3, 4), (3, 4, 6), (1, 3, 10), (2, 4, 2)],
        [(1, 4), (1, 3), (3, 4)])})

    # 02 只有一条边
    out.append({"id": "02", "input": pack(2, [(1, 2, 7)], [(1, 2)])})

    # 03 两点之间的重边，瓶颈取较小者
    out.append({"id": "03", "input": pack(2, [(1, 2, 9), (1, 2, 3)], [(1, 2), (2, 1)])})

    # 04 1000 点的树
    n = 1000
    edges = [(rng.randint(1, i - 1), i, rng.randint(1, 10 ** 9)) for i in range(2, n + 1)]
    out.append({"id": "04", "input": pack(n, edges, random_queries(rng, n, 1000))})

    # 05 菊花图，所有询问都要经过中心
    n = 50000
    edges = [(1, i, rng.randint(1, 10 ** 9)) for i in range(2, n + 1)]
    out.append({"id": "05", "input": pack(n, edges, random_queries(rng, n, 50000))})

    # 06 链：树很深，必须用倍增
    n = 50000
    edges = [(i, i + 1, rng.randint(1, 10 ** 9)) for i in range(1, n)]
    out.append({"id": "06", "input": pack(n, edges, random_queries(rng, n, 50000))})

    # 07 随机大图
    n = 50000
    out.append({"id": "07", "input": pack(n, random_connected(rng, n, 50001, 10 ** 9),
                                         random_queries(rng, n, 50000))})

    # 08 所有边权相同
    n = 50000
    edges = random_connected(rng, n, 50001, 1)
    out.append({"id": "08", "input": pack(n, edges, random_queries(rng, n, 50000))})

    # 09 询问两端相同，答案为 0
    n = 2000
    edges = random_connected(rng, n, 1000, 10 ** 6)
    out.append({"id": "09", "input": pack(n, edges, [(7, 7), (n, n), (1, 1), (500, 500)])})

    # 10 所有边权都是 10^9
    n = 50000
    edges = [(i, i + 1, 10 ** 9) for i in range(1, n)]
    edges += [(rng.randint(1, n), rng.randint(1, n), 10 ** 9) for _ in range(50001)]
    out.append({"id": "10", "input": pack(n, edges, random_queries(rng, n, 50000))})

    return out
