import random


def _input(n, edges):
    parts = ["%d %d\n" % (n, len(edges))]
    for a, b in edges:
        parts.append("%d %d\n" % (a, b))
    return "".join(parts)


def _tree(rng, k, off):
    """在编号 off+1 .. off+k 上生成一棵随机树。"""
    edges = []
    for i in range(2, k + 1):
        p = rng.randint(1, i - 1)
        edges.append((p + off, i + off))
    return edges


def _extra_edge(rng, k, off, edges):
    """在 off+1 .. off+k 中挑一条还没出现的边，让连通块变成基环树。"""
    used = set()
    for a, b in edges:
        used.add((a, b) if a < b else (b, a))
    while True:
        a = rng.randint(1, k)
        b = rng.randint(1, k)
        if a == b:
            continue
        key = (a + off, b + off) if a < b else (b + off, a + off)
        if key in used:
            continue
        return (a + off, b + off)


def cases():
    rng = random.Random(20261123)
    out = []

    def add(n, edges):
        out.append({"id": "%02d" % (len(out) + 1), "input": _input(n, edges)})

    # 01 样例：三角形挂一条尾巴（基环树）
    add(4, [(1, 2), (2, 3), (3, 1), (3, 4)])

    # 02 边界：一个点、没有边
    add(1, [])

    # 03 边界：两个点、一条边
    add(2, [(1, 2)])

    # 04 一棵随机树
    add(6, _tree(rng, 6, 0))

    # 05 基环树：三角形加上挂在同一个点上的四片叶子
    add(7, [(1, 2), (2, 3), (3, 1), (1, 4), (1, 5), (1, 6), (1, 7)])

    # 06 无解：两个环连在一起，5 个点 6 条边
    add(5, [(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)])

    # 07 森林：树 + 基环树 + 孤立点
    edges = _tree(rng, 5, 0) + _tree(rng, 4, 5)
    edges.append(_extra_edge(rng, 4, 5, edges))
    add(11, edges)

    # 08 大数据：n = 200000 的随机树（m = n - 1）
    add(200000, _tree(rng, 200000, 0))

    # 09 大数据：n = 200000 的基环树（m = n）
    big = _tree(rng, 200000, 0)
    big.append(_extra_edge(rng, 200000, 0, big))
    add(200000, big)

    # 10 大数据：1000 个点数为 200 的连通块，一半树一半基环树
    edges = []
    for c in range(1000):
        off = c * 200
        edges += _tree(rng, 200, off)
        if c % 2 == 1:
            edges.append(_extra_edge(rng, 200, off, edges))
    add(200000, edges)

    # 11 大数据无解：199999 个点的树再多加两条边
    edges = _tree(rng, 199999, 0)
    edges.append(_extra_edge(rng, 199999, 0, edges))
    edges.append(_extra_edge(rng, 199999, 0, edges))
    add(200000, edges)

    # 12 中等规模无解：一个连通块里有两个环，另一个连通块是合法的树
    edges = _tree(rng, 30000, 0)
    edges.append(_extra_edge(rng, 30000, 0, edges))
    edges.append(_extra_edge(rng, 30000, 0, edges))
    edges += _tree(rng, 20000, 30000)
    add(50000, edges)

    return out
