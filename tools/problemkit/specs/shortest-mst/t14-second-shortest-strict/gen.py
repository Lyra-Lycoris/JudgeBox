import random


def pack(n, edges):
    lines = ["%d %d" % (n, len(edges))]
    lines.extend("%d %d %d" % e for e in edges)
    return "\n".join(lines) + "\n"


def random_connected(rng, n, extra, wmax):
    edges = [(rng.randint(1, i - 1), i, rng.randint(1, wmax)) for i in range(2, n + 1)]
    for _ in range(extra):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        edges.append((u, v, rng.randint(1, wmax)))
    return edges


def cases():
    rng = random.Random(20261119)
    out = []

    # 01 样例
    out.append({"id": "01", "input": pack(4, [(1, 2, 1), (2, 4, 3), (1, 3, 2), (3, 4, 4)])})

    # 02 只有一条边：次短路必须来回走一遍
    out.append({"id": "02", "input": pack(2, [(1, 2, 5)])})

    # 03 两点之间的两条重边
    out.append({"id": "03", "input": pack(2, [(1, 2, 1), (1, 2, 3)])})

    # 04 三点链，次短路要在中间来回
    out.append({"id": "04", "input": pack(3, [(1, 2, 1), (2, 3, 1)])})

    # 05 终点不可达
    out.append({"id": "05", "input": pack(5, [(1, 2, 4), (2, 3, 4), (4, 5, 4)])})

    # 06 随机中等图
    out.append({"id": "06", "input": pack(1000, random_connected(rng, 1000, 4000, 10 ** 9))})

    # 07 随机大图
    out.append({"id": "07", "input": pack(20000, random_connected(rng, 20000, 80000, 10 ** 9))})

    # 08 所有边权都为 1 的大图
    n = 20000
    edges = [(rng.randint(1, i - 1), i, 1) for i in range(2, n + 1)]
    while len(edges) < 100000:
        edges.append((rng.randint(1, n), rng.randint(1, n), 1))
    out.append({"id": "08", "input": pack(n, edges)})

    # 09 三角形，两条路等长时严格次短路要更大
    out.append({"id": "09", "input": pack(3, [(1, 2, 2), (2, 3, 2), (1, 3, 4)])})

    # 10 长链，边权都是 10^9
    out.append({"id": "10", "input": pack(4, [(1, 2, 10 ** 9), (2, 3, 10 ** 9), (3, 4, 10 ** 9)])})

    return out
