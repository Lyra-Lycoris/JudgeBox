import random


def _fmt(pairs):
    return "".join("%d %d\n" % (u, v) for u, v in pairs)


def _rand_edge(rng, n):
    u = rng.randint(1, n)
    v = rng.randint(1, n - 1)
    if v >= u:
        v += 1
    return (u, v)


def cases():
    rng = random.Random(20261118)
    out = []

    # 01 样例：4 个点全连通，保留 3 条边即可，最多删 2 条
    out.append({"id": "01", "input": "4 5\n" + _fmt([(1, 2), (2, 3), (3, 1), (1, 2), (3, 4)])})

    # 02 只有一个点，没有边
    out.append({"id": "02", "input": "1 0\n"})

    # 03 一棵树：任何一条边都不能删
    out.append({"id": "03", "input": "6 5\n" + _fmt([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])})

    # 04 完全没有边
    out.append({"id": "04", "input": "5 0\n"})

    # 05 不连通 + 重边：只有 (1,2) 这条边是多余的
    out.append({"id": "05", "input": "6 3\n" + _fmt([(1, 2), (1, 2), (3, 4)])})

    # 06 100 个点的完全图：4950 条边，只需保留 99 条
    n = 100
    pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    out.append({"id": "06", "input": "%d %d\n" % (n, len(pairs)) + _fmt(pairs)})

    # 07 随机中等：2000 个点、5000 条边
    n, m = 2000, 5000
    out.append({"id": "07", "input": "%d %d\n" % (n, m) + _fmt([_rand_edge(rng, n) for _ in range(m)])})

    # 08 大数据：200000 个点连成一条链，答案是 0
    n = 200000
    out.append({"id": "08", "input": "%d %d\n" % (n, n - 1) + _fmt([(i, i + 1) for i in range(1, n)])})

    # 09 大数据：200000 个点、200000 条随机边
    n, m = 200000, 200000
    out.append({"id": "09", "input": "%d %d\n" % (n, m) + _fmt([_rand_edge(rng, n) for _ in range(m)])})

    # 10 大数据边界：200000 个点、没有边
    out.append({"id": "10", "input": "200000 0\n"})

    # 11 大数据：100 条互不相连的链，每条 2000 个点，另外再加 100 条边
    pairs = []
    for block in range(100):
        base = block * 2000 + 1
        for j in range(1999):
            pairs.append((base + j, base + j + 1))
    for block in range(100):
        base = block * 2000 + 1
        pairs.append((base, base + 1))
    out.append({"id": "11", "input": "%d %d\n" % (200000, len(pairs)) + _fmt(pairs)})

    return out
