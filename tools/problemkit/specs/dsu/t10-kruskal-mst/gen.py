import random


def _fmt(edges):
    return "".join("%d %d %d\n" % (u, v, w) for u, v, w in edges)


def _rand_edge(rng, n):
    u = rng.randint(1, n)
    v = rng.randint(1, n - 1)
    if v >= u:
        v += 1
    return (u, v)


def _connected(rng, n, m, low, high):
    edges = []
    for i in range(2, min(n, m + 1) + 1):
        u, v = _rand_edge(rng, i)
        edges.append((u, i, rng.randint(low, high)))
    while len(edges) < m:
        u, v = _rand_edge(rng, n)
        edges.append((u, v, rng.randint(low, high)))
    return edges


def cases():
    rng = random.Random(20261119)
    out = []

    # 01 样例：选 (1,2,1)、(2,3,2)、(3,4,3)，总权重 6
    out.append({"id": "01", "input": "4 5\n" + _fmt([(1, 2, 1), (2, 3, 2), (3, 4, 3), (1, 4, 5), (1, 3, 4)])})

    # 02 只有一个点：空生成树，权重 0
    out.append({"id": "02", "input": "1 0\n"})

    # 03 图不连通：点 4 是孤立的
    out.append({"id": "03", "input": "4 3\n" + _fmt([(1, 2, 5), (2, 3, 5), (1, 3, 9)])})

    # 04 负权：最小生成树取两条负权边，总权重 -15
    out.append({"id": "04", "input": "3 3\n" + _fmt([(1, 2, -5), (2, 3, -4), (1, 3, -10)])})

    # 05 全是相同权重：5 个点的完全图，任何生成树权重都是 4 * 7 = 28
    n = 5
    pairs = [(u, v, 7) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    out.append({"id": "05", "input": "%d %d\n" % (n, len(pairs)) + _fmt(pairs)})

    # 06 60 个点的完全图，随机权重
    n = 60
    pairs = [(u, v, rng.randint(-1000, 1000)) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    out.append({"id": "06", "input": "%d %d\n" % (n, len(pairs)) + _fmt(pairs)})

    # 07 随机中等：2000 个点、5000 条边，保证连通
    n, m = 2000, 5000
    out.append({"id": "07", "input": "%d %d\n" % (n, m) + _fmt(_connected(rng, n, m, 1, 10 ** 9))})

    # 08 大数据：120000 个点、120000 条边，保证连通
    n, m = 120000, 120000
    out.append({"id": "08", "input": "%d %d\n" % (n, m) + _fmt(_connected(rng, n, m, 1, 10 ** 9))})

    # 09 大数据：200000 个点的链，边权全是 1，答案是 199999
    n = 200000
    out.append({"id": "09", "input": "%d %d\n" % (n, n - 1) + _fmt([(i, i + 1, 1) for i in range(1, n)])})

    # 10 大数据：链上每条边的权重都是极值 -10^9
    n2 = 140000
    out.append({"id": "10", "input": "%d %d\n" % (n2, n2 - 1)
                + _fmt([(i, i + 1, -10 ** 9) for i in range(1, n2)])})

    # 11 大数据：图不连通，边只落在前 100000 个点上
    n, m = 200000, 100000
    edges = _connected(rng, 100000, m, 1, 10 ** 9)
    out.append({"id": "11", "input": "%d %d\n" % (n, m) + _fmt(edges)})

    return out
