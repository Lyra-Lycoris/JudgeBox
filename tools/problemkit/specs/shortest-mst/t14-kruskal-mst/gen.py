import random


def pack(n, edges):
    lines = ["%d %d" % (n, len(edges))]
    lines.extend("%d %d %d" % e for e in edges)
    return "\n".join(lines) + "\n"


def cases():
    rng = random.Random(20261117)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(4, [(1, 2, 1), (1, 3, 4), (2, 3, 2), (2, 4, 5), (3, 4, 3)])})

    # 02 边界：只有一个点，没有边
    out.append({"id": "02", "input": pack(1, [])})

    # 03 两个点一条零权边
    out.append({"id": "03", "input": pack(2, [(1, 2, 0)])})

    # 04 小完全图，大量等权边，考察并列最优
    out.append({"id": "04", "input": pack(4, [
        (1, 2, 2), (1, 3, 2), (1, 4, 2), (2, 3, 2), (2, 4, 2), (3, 4, 2)])})

    # 05 1000 点随机连通图：先连成随机树，再补随机边
    n = 1000
    edges = [(rng.randint(1, i - 1), i, rng.randint(-10 ** 9, 10 ** 9)) for i in range(2, n + 1)]
    while len(edges) < 5000:
        edges.append((rng.randint(1, n), rng.randint(1, n), rng.randint(-10 ** 9, 10 ** 9)))
    out.append({"id": "05", "input": pack(n, edges)})

    # 06 200000 点的链，再加一条权重很大的额外边
    n = 200000
    edges = [(i, i + 1, rng.randint(0, 9)) for i in range(1, n)]
    edges.append((1, n, 10 ** 9))
    out.append({"id": "06", "input": pack(n, edges)})

    # 07 200000 点的树，所有边权相同
    n = 200000
    edges = [(rng.randint(1, i - 1), i, 7) for i in range(2, n + 1)]
    out.append({"id": "07", "input": pack(n, edges)})

    # 08 500 点稠密图，100000 条边
    n = 500
    edges = [(rng.randint(1, i - 1), i, rng.randint(-1000, 1000)) for i in range(2, n + 1)]
    while len(edges) < 100000:
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u != v:
            edges.append((u, v, rng.randint(-1000, 1000)))
    out.append({"id": "08", "input": pack(n, edges)})

    # 09 100000 点随机连通图，边权有正有负
    n = 100000
    edges = [(i, i + 1, rng.randint(-10 ** 6, 10 ** 6)) for i in range(1, n)]
    while len(edges) < 150000:
        edges.append((rng.randint(1, n), rng.randint(1, n), rng.randint(-10 ** 6, 10 ** 6)))
    out.append({"id": "09", "input": pack(n, edges)})

    # 10 链，每条边都是最大权 10^9
    n = 60000
    edges = [(i, i + 1, 10 ** 9) for i in range(1, n)]
    out.append({"id": "10", "input": pack(n, edges)})

    return out
