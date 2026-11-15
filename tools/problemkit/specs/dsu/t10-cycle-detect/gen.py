import random


def _fmt(pairs):
    return "".join("%d %d\n" % (u, v) for u, v in pairs)


def _tree_edges(rng, n):
    return [(rng.randint(1, i - 1), i) for i in range(2, n + 1)]


def _simple_edges(rng, n, m):
    seen = set()
    pairs = []
    while len(pairs) < m:
        u = rng.randint(1, n)
        v = rng.randint(1, n - 1)
        if v >= u:
            v += 1
        key = (u, v) if u < v else (v, u)
        if key in seen:
            continue
        seen.add(key)
        pairs.append((u, v))
    return pairs


def cases():
    rng = random.Random(20261115)
    out = []

    # 01 样例：1-2-3-4-1 形成一个长度 4 的环
    out.append({"id": "01", "input": "4 4\n" + _fmt([(1, 2), (2, 3), (3, 4), (4, 1)])})

    # 02 只有一个点，没有边
    out.append({"id": "02", "input": "1 0\n"})

    # 03 一条边
    out.append({"id": "03", "input": "2 1\n" + _fmt([(1, 2)])})

    # 04 一棵树，没有环
    out.append({"id": "04", "input": "6 5\n" + _fmt([(1, 2), (1, 3), (1, 4), (4, 5), (4, 6)])})

    # 05 三角形
    out.append({"id": "05", "input": "3 3\n" + _fmt([(1, 2), (2, 3), (1, 3)])})

    # 06 不连通：一个连通块是树，另一个连通块有环
    out.append({"id": "06", "input": "7 6\n" + _fmt([(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 5)])})

    # 07 随机树：2000 个点、1999 条边，没有环
    n = 2000
    out.append({"id": "07", "input": "%d %d\n" % (n, n - 1) + _fmt(_tree_edges(rng, n))})

    # 08 随机图：1000 个点、1500 条互不相同的边，必然有环
    n, m = 1000, 1500
    out.append({"id": "08", "input": "%d %d\n" % (n, m) + _fmt(_simple_edges(rng, n, m))})

    # 09 大数据：一条 200000 个点的链，没有环
    n = 200000
    out.append({"id": "09", "input": "%d %d\n" % (n, n - 1) + _fmt([(i, i + 1) for i in range(1, n)])})

    # 10 大数据：链再补一条 (1, 200000)，形成一个覆盖全图的大环
    out.append({"id": "10", "input": "%d %d\n" % (n, n) + _fmt([(i, i + 1) for i in range(1, n)] + [(1, n)])})

    # 11 大数据：200000 个点的随机树，没有环
    out.append({"id": "11", "input": "%d %d\n" % (n, n - 1) + _fmt(_tree_edges(rng, n))})

    return out
