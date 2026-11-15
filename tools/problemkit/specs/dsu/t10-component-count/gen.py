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
    rng = random.Random(20261114)
    out = []

    # 01 样例：{1,2,3}、{4}、{5}
    out.append({"id": "01", "input": "5 2\n" + _fmt([(1, 2), (2, 3)])})

    # 02 只有一个点，没有边
    out.append({"id": "02", "input": "1 0\n"})

    # 03 完全没有边：n 个孤立点
    out.append({"id": "03", "input": "5 0\n"})

    # 04 一条链，整张图连通
    out.append({"id": "04", "input": "6 5\n" + _fmt([(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])})

    # 05 大量重边，只有两个连通块
    out.append({"id": "05", "input": "4 6\n" + _fmt([(1, 2)] * 4 + [(3, 4)] * 2)})

    # 06 随机中等：1000 个点、800 条边
    n, m = 1000, 800
    out.append({"id": "06", "input": "%d %d\n" % (n, m) + _fmt([_rand_edge(rng, n) for _ in range(m)])})

    # 07 随机中等偏大：20000 个点、30000 条边
    n, m = 20000, 30000
    out.append({"id": "07", "input": "%d %d\n" % (n, m) + _fmt([_rand_edge(rng, n) for _ in range(m)])})

    # 08 大数据：200000 个点、200000 条随机边
    n, m = 200000, 200000
    out.append({"id": "08", "input": "%d %d\n" % (n, m) + _fmt([_rand_edge(rng, n) for _ in range(m)])})

    # 09 大数据边界：200000 个点、没有边，答案是 200000
    out.append({"id": "09", "input": "200000 0\n"})

    # 10 大数据：一条 200000 个点的链，答案是 1
    n = 200000
    out.append({"id": "10", "input": "%d %d\n" % (n, n - 1) + _fmt([(i, i + 1) for i in range(1, n)])})

    # 11 大数据：100 条互不相连的链，每条 2000 个点，答案是 100
    pairs = []
    for block in range(100):
        base = block * 2000 + 1
        for j in range(1999):
            pairs.append((base + j, base + j + 1))
    out.append({"id": "11", "input": "%d %d\n" % (200000, len(pairs)) + _fmt(pairs)})

    return out
